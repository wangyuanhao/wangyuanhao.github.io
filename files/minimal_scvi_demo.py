"""A minimal scVI demo with 100 genes and a 10-dimensional latent space.

Run `python minimal_scvi_demo.py`. Pass `--show` to open the figure as well.
"""

import argparse
import math
from pathlib import Path

import matplotlib.pyplot as plt
import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.data import DataLoader, TensorDataset


# ── Dataset: synthetic counts with three cell states in ten dimensions ──

def sample_zinb(mu, theta, zi_logits):
    """Draw counts via Gamma–Poisson sampling and a separate zero-inflation mask."""
    intensity = torch.distributions.Gamma(theta, rate=theta / mu).sample()
    counts = torch.poisson(intensity)
    zero_mask = torch.bernoulli(zi_logits.sigmoid()).bool()
    return counts.masked_fill(zero_mask, 0)


def make_data(n_cells=1000, n_genes=100, n_latent=10):
    state = torch.arange(n_cells) % 3
    angles = 2 * math.pi * torch.arange(3) / 3
    centers = 2.3 * torch.stack((angles.cos(), angles.sin()), dim=-1)
    z_true = 0.5 * torch.randn(n_cells, n_latent)
    z_true[:, :2] += centers[state]

    gene_loadings = torch.randn(n_latent, n_genes) / math.sqrt(n_latent)
    gene_baseline = 0.45 * torch.randn(n_genes)
    rho = (z_true @ gene_loadings + gene_baseline).softmax(dim=-1)
    log_library = math.log(2000) + 0.35 * torch.randn(n_cells, 1)
    theta = torch.linspace(8., 16., n_genes)
    zi_logits = torch.full_like(rho, -3.)
    counts = sample_zinb(log_library.exp() * rho, theta, zi_logits)
    return counts, state  # State labels are only used for plotting.


# ── Model ──

class Encoder(nn.Module):
    """Return a diagonal Gaussian's mean and log variance."""

    def __init__(self, n_genes, n_latent, hidden=32):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(n_genes, hidden), nn.Tanh())
        self.mean = nn.Linear(hidden, n_latent)
        self.logvar = nn.Linear(hidden, n_latent)

    def forward(self, x):
        h = self.net(x.log1p())
        return self.mean(h), self.logvar(h)


class Decoder(nn.Module):
    """Return the NB mean, gene-specific inverse dispersion and ZI logits."""

    def __init__(self, n_latent, n_genes, hidden=32):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(n_latent, hidden), nn.Tanh())
        self.scale = nn.Linear(hidden, n_genes)
        self.zero_logits = nn.Linear(hidden, n_genes)
        self.log_theta = nn.Parameter(torch.full((n_genes,), math.log(8)))
        nn.init.constant_(self.zero_logits.bias, -3.)

    def forward(self, z, log_library):
        h = self.net(z)
        rho = self.scale(h).softmax(dim=-1)  # (batch, genes), rows sum to 1
        mu = log_library.exp() * rho        # L × rho, the NB mean
        return mu, self.log_theta.exp(), self.zero_logits(h)


def zinb_log_prob(x, mu, theta, zi_logits):
    """Per-entry log p(x | z, log L), with w, y and the zero mask marginalized."""
    # $\Delta = \log(\mu) - \log(\theta) = \log(\frac{\mu}{\theta})$ 
    log_mu_over_theta = mu.log() - theta.log()
   
   # \log nb(x_{g}=0|z, L) = \log \left(\frac{\theta}{\theta + \mu}\right)^{\theta} 
    # = -\theta \log(1 + \frac{\mu}{\theta}) = -\theta \log(1 + e^{\Delta}) = -\theta \text{softplus}(\Delta)
    nb_zero = -theta * F.softplus(log_mu_over_theta)
    
    # \log nb(x_{g}|z, L) = -\theta \log(1 + e^{\Delta}) + x_{g} \log(\frac{\mu}{\theta}) 
    #                      + \log \Gamma(x_{g} + \theta) - \log \Gamma(\theta) - \log \Gamma(x_{g} + 1)
    nb_log_prob = (
        nb_zero - x * F.softplus(-log_mu_over_theta)
        + torch.lgamma(x + theta) - torch.lgamma(theta) - torch.lgamma(x + 1)
    )
    # $log (1 - \pi) = log (1 - sigmoid(zi_logits)) = log (sigmoid(-zi_logits))$
    log_keep = F.logsigmoid(-zi_logits)
    
    # $log p(x_{g}=0 | z, log L) = \log \left\[\pi + (1 - \pi)\left(\frac{\theta}{\theta + \mu}\right)^{\theta}\right]$
    #                            = \log \left\[\exp(logsigmoid(zi_logits)) + \exp(log_keep + nb_zero)\right]$
    log_zero = torch.logaddexp(F.logsigmoid(zi_logits), log_keep + nb_zero)
    return torch.where(x == 0, log_zero, log_keep + nb_log_prob)


def reparameterize(mean, logvar):
    return mean + (0.5 * logvar).exp() * torch.randn_like(mean)


def elbo(x, z_encoder, library_encoder, decoder, prior_mean, prior_var):
    """One draw of (z, log L) per cell, with both KL terms in closed form."""
    z_mean, z_logvar = z_encoder(x)                       # (batch, latent)
    library_mean, library_logvar = library_encoder(x)   # (batch, 1), log L
    z = reparameterize(z_mean, z_logvar)
    log_library = reparameterize(library_mean, library_logvar)
    mu, theta, zi_logits = decoder(z, log_library)

    recon = zinb_log_prob(x, mu, theta, zi_logits).sum(dim=-1).mean()
    kl_z = 0.5 * (z_mean.square() + z_logvar.exp() - 1 - z_logvar).sum(dim=-1).mean()
    kl_library = 0.5 * (
        prior_var.log() - library_logvar
        + (library_logvar.exp() + (library_mean - prior_mean).square()) / prior_var
        - 1
    ).mean()
    return recon - kl_z - kl_library, recon, kl_z, kl_library


# ── Visualization: training, count space and latent space ──

def fit_pca(data):
    """Fit two principal axes and return their explained variance fractions."""
    center = data.mean(dim=0)
    _, singular_values, axes = torch.linalg.svd(data - center, full_matrices=False)
    explained = singular_values[:2].square() / singular_values.square().sum()
    return center, axes[:2].T, explained


def plot_demo(history, counts, state, z_mean, generated):
    fig, axes = plt.subplots(1, 4, figsize=(14, 3.8), layout="constrained")
    epochs = range(len(history["elbo"]))
    ax = axes[0]
    ax.plot(epochs, history["elbo"], color="#245b91", lw=2, label="ELBO")
    ax.plot(epochs, history["recon"], color="#b74b39", ls="--", label="Log likelihood")
    ax.plot(epochs, history["neg_kl"], color="#896608", ls=":", label="−Total KL")
    ax.legend(frameon=False, fontsize=9)
    ax.set(title="Training objective", xlabel="Epoch", ylabel="Per-cell value")

    # Put observed and generated log-counts on the same axes for comparison.
    log_counts = counts.log1p()
    count_center, count_axes, count_variance = fit_pca(log_counts)
    observed_xy = (log_counts - count_center) @ count_axes
    generated_xy = (generated.log1p() - count_center) @ count_axes
    axes[2].sharex(axes[1])
    axes[2].sharey(axes[1])
    axes[2].scatter(*generated_xy.T, color="#596979", s=12, alpha=0.45, linewidths=0)
    for ax, title in zip(axes[1:3], ("Observed counts", "Counts sampled from prior")):
        ax.set(title=title, xlabel=f"Count PC 1 ({count_variance[0]:.0%})",
               ylabel=f"Count PC 2 ({count_variance[1]:.0%})")

    # Each cell is represented by its full posterior mean vector E[z | x].
    z_center, z_axes, z_variance = fit_pca(z_mean)
    latent_xy = (z_mean - z_center) @ z_axes
    for i, color in enumerate(("#0072b2", "#d55e00", "#009e73")):
        mask = state == i
        for ax, xy in ((axes[1], observed_xy), (axes[3], latent_xy)):
            ax.scatter(*xy[mask].T, color=color, s=12, alpha=0.6,
                       linewidths=0, label=f"State {i + 1}")
    axes[3].set(title=f"Latent posterior means ({z_mean.shape[1]}D)",
                xlabel=f"Latent PC 1 ({z_variance[0]:.0%})",
                ylabel=f"Latent PC 2 ({z_variance[1]:.0%})")
    axes[3].legend(frameon=False, fontsize=9, markerscale=1.4)
    return fig


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--show", action="store_true")
    args = parser.parse_args()
    if args.epochs < 1:
        parser.error("--epochs must be positive")

    
    torch.manual_seed(305)
    torch.set_num_threads(1)  # Small CPU batches benefit from low thread overhead.
    n_genes, n_latent = 100, 10
    counts, state = make_data(n_genes=n_genes, n_latent=n_latent)
    z_encoder = Encoder(n_genes, n_latent)
    library_encoder = Encoder(n_genes, 1)
    decoder = Decoder(n_latent, n_genes)

    # Empirical prior of log L, fitted using the observed total count per cell.
    log_totals = counts.sum(dim=-1).clamp_min(1).log()
    prior_mean = log_totals.mean()
    prior_var = log_totals.var(unbiased=False).clamp_min(1e-4)
    with torch.no_grad():
        library_encoder.mean.bias.copy_(prior_mean.expand_as(library_encoder.mean.bias))
        library_encoder.logvar.bias.copy_(prior_var.log().expand_as(library_encoder.logvar.bias))

    params = list(z_encoder.parameters()) + list(library_encoder.parameters()) + list(decoder.parameters())
    optimizer = torch.optim.Adam(params, lr=1e-3)
    loader = DataLoader(TensorDataset(counts), batch_size=128, shuffle=True)
    history = {"elbo": [], "recon": [], "neg_kl": []}

    for epoch in range(args.epochs + 1):
        if epoch > 0:
            for (x_batch,) in loader:
                optimizer.zero_grad()
                bound, _, _, _ = elbo(x_batch, z_encoder, library_encoder,
                                      decoder, prior_mean, prior_var)
                (-bound).backward()
                optimizer.step()

        # Record the objective on the full synthetic data, including epoch zero.
        with torch.no_grad():
            bound, recon, kl_z, kl_library = elbo(counts, z_encoder, library_encoder,
                                                 decoder, prior_mean, prior_var)
        history["elbo"].append(bound.item())
        history["recon"].append(recon.item())
        history["neg_kl"].append(-(kl_z + kl_library).item())
        if epoch == 0 or epoch % 20 == 0 or epoch == args.epochs:
            print(f"Epoch {epoch:3d}  ELBO={bound:.2f}  log p(x|z,L)={recon:.2f}  "
                  f"KL_z={kl_z:.2f}  KL_logL={kl_library:.2f}")

    with torch.no_grad():
        z_mean, _ = z_encoder(counts)
        log_library_mean, _ = library_encoder(counts)
        # Plug posterior means into the decoder for a simple point reconstruction.
        mu, _, zi_logits = decoder(z_mean, log_library_mean)
        reconstructed = (1 - zi_logits.sigmoid()) * mu
        z_prior = torch.randn(500, n_latent)
        log_library_prior = prior_mean + prior_var.sqrt() * torch.randn(500, 1)
        generated = sample_zinb(*decoder(z_prior, log_library_prior))

    print(f"Counts: {tuple(counts.shape)}  Posterior means: {tuple(z_mean.shape)}")
    print("First cell, first six observed counts:", counts[0, :6].int().tolist())
    print("First cell, first six fitted means:", [round(value, 1) for value in reconstructed[0, :6].tolist()])
    fig = plot_demo(history, counts, state, z_mean, generated)
    figure_path = Path(__file__).resolve().parent / "output" / "minimal_scvi_demo.png"
    figure_path.parent.mkdir(exist_ok=True)
    fig.savefig(figure_path, dpi=180)
    print(f"Figure saved to {figure_path}")
    if args.show:
        plt.show()
    plt.close(fig)


if __name__ == "__main__":
    main()
