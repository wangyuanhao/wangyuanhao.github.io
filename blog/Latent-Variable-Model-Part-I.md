---
title: "Generative Models-Part I: Probabilistic PCA and VAE"
date: 2026-11-21
permalink: /blog/Latent-Variable-Model-Part-I/
excerpt: "This blog presents descriptions and minimal implementation demos for probabilistic principal analysis and variational autoencoders."
tags: [Machine Learning]
lang: en
published: true
---

## Vanilla Latent Variable Model and Evidence Lower Bound

Suppose an observable random variable $$x$$ is generated from the process:

$$
\begin{aligned}
z &\sim& p(z) \\
x\vert z &\sim& p(x|z)
\end{aligned}
$$

where the random variable $$z$$ is unobserved and is called a latent variable. 

Traditionally, we try to maximize the likelihood of samples of $$x$$ to infer the unknown parameters governing the distribution $$p(x)$$. However, we cannot explicitly write the likelihood of samples of $$x$$ if 

$$
p(x) = \int_{z} p(x\vert z)p(z)\mathtt{d}z = \mathbb{E}_{p(z)}\left[p(x\vert z)\right]
$$

causes difficulties in computing the expectation $$\mathbb{E}_{p(z)}\left[p(x\vert z)\right]$$, we can instead maximize the surrogate of the likelihood by variational inference.

Speficially, let $$q(z)$$ be a surrogate distribution of $$p(z)$$ (Note that $$q(z)$$ can be **<mark>ANY FORM</mark>** of distribution of $$z$$),  we can write 

$$
\begin{aligned}
\log p(x) & = \int_{z}q(z) \log p(x)\mathtt{d}z \\
					& =  \int_{z} q(z) \log \left(p(x \vert z)\frac{q(z)}{p(z\vert{x})}\frac{p(z)}{q(z)}\right)\mathtt{d}z \\
					&	= \int_{z}q(z)\log p(x \vert z)\mathtt{d}z - \int_{z} q(z)\log \frac{p(z \vert x)}{q(z)}\mathtt{d}z + \int_{z}q(z)\log \frac{p(z)}{q(z)}\mathtt{d}z \\
					& = \underbrace{\mathbb{E}_{q(z)}\left[\log p(x\vert z)\right] - D_{\mathtt{KL}}(q(z)\vert\vert p(z))}_{\text{Evidence Lower Bound (ELBO)}} + D_{\mathtt{KL}}(q(z) \vert \vert p(z \vert x)).
\end{aligned}
$$

By the non-negative property of KL-divergence $$D_{\mathtt{KL}}$$, we have

$$
\log p(x) \geq \mathbb{E}_{q(z)}\left[\log p(x\vert z)\right] - D_{\mathtt{KL}}(q(z)\vert\vert p(z))
$$

The equality holds if $$q(z) = p(z \vert x)$$.

Hence, we can maximaize the ELBO instead, if the surrogate expectation $$\mathbb{E}_{q(z)}\left[\log p(x\vert z)\right]$$ and the KL-divergence $$D_{\mathtt{KL}}(q(z)\vert\vert p(z))$$ are known, to approximate the maximization of the log-likelihood $$\log p(x)$$.

##### Two equivalent versions of EBLO

$$
\mathcal{L}_{\mathtt{ELBO}} = \mathbb{E}_{q(z)}\left[\log p(x\vert z)\right] - D_{\mathtt{KL}}(q(z)\vert\vert p(z))
\tag{ELBO-v1}
\label{elbov1}
$$

$$
\mathcal{L}_{\mathtt{ELBO}} = \mathbb{E}_{q(z)}\left[\log p(x, z)\right] + H(q)
\tag{ELBO-v2}
\label{elbov2}
$$

where $$H(q) = -\int_{z} q(z) \log q(z) \mathtt{d}z$$.

$\eqref{elbov1}$ is generally used in variational autoencoder (described later).

##  Probabilistic Principal Component Analysis (Bishop, Chapter 12.2)

Now we consider the generative process as

$$
\begin{aligned}
z &\sim& p(z) &= \mathcal{N}(0, \boldsymbol{I}_{D}) \\
x \vert z &\sim& p(x\vert z) &= \mathcal{N}(Wz+\mu, \sigma^{2}\boldsymbol{I}_{d})
\end{aligned}
$$

where $$z \in \mathbb{R}^{D}$$ and $$x \in \mathbb{R}^{d}$$ almost surely. Such generative process is called probabilistic principal component analysis (PPCA).

#### Maximization of Likelihood 

By the additivity of Gaussian variables, the distribution of $$x$$ is

$$
\begin{aligned}
p(x)& = \int_{z} p(x \vert z)p(z) \mathtt{d}z \\
		& = \mathcal{N}(\mu, WW^{T}+\sigma^{2}I_{d}).
\end{aligned}
$$

Hence, we can estimate the unknown parameters $$\mu$$, $$W$$, and $\sigma^{2}$ by maximization of the likelihood of samples of $$x$$. 

We can also write down the posterior distribution $$p(z \vert x)$$ as 

$$
p(z \vert x) = \mathcal{N}(M^{-1}W^{T}(x - \mu), \sigma^{2}M^{-1}),
$$

where $$M = W^{T}W+\sigma^{2}I_{D}$$

#### Maximization of ELBO by Expectation-Maximization (EM) Algorithm

Alternatively, we can estimate the unknown parameters $$\mu$$, $$W$$, and $\sigma^{2}$  by optimizing $$\eqref{elbov2}$$. We have

$$
\log p(x \vert \mu, \sigma^{2}, W) \geq \mathbb{E}_{q(z)}\left[\log p(x, z\vert \mu, \sigma^{2}, W)\right] + H(q),
$$

and the ELBO is maximized by the EM algorithm.

In E-step, we take 

$$
q(z) = p_{t}(z\vert x)=\mathcal{N}(M^{-1}_{t}W^{T}_{t}(x - \mu_{t}), \sigma^{2}_{t}M^{-1}_{t}),
$$

where $$W_{t}$$, $$\mu_{t}$$, and $$\sigma^{2}_{t}$$ are parameters estimated at the $$t$$-th iteration.

In M-step, given $$q(z) = p_{t}(z\vert x)$$, $$H(q)$$ is a constant w.r.t. the unknown parameters $$\mu$$, $$W$$, and $$\sigma^{2}$$ . Thereforem maximizing the ELBO is equivalent to maximizing the expectation of complete log likelihood, i.e., 

$$
(\mu_{t+1}, \sigma^{2}_{t+1}, W_{t+1}) = \mathop{\arg\max}\limits_{\mu, \sigma^{2}, W}~~\mathbb{E}_{p_{t}(z \vert x)}\left[\log p(x, z\vert \mu, \sigma^{2}, W)\right].
$$

The complete log likelihood 

$$
\begin{aligned}
\log p(x, z \vert \mu, \sigma^{2}, W) &= \log (p(x \vert z)p(z)) \\
&=\log p(x \vert z) + \log p(z) \\
&= -\left(\frac{d}{2}\log 2\pi \sigma^{2} + \frac{1}{2\sigma^{2}}\|x -\mu\|^{2} + \frac{1}{2\sigma^{2}}z^{T}W^{T}Wz - \frac{1}{\sigma^{2}}z^{T}W^{T}(x -\mu)\right) \\
  & - \left(\frac{D}{2}\log2\pi + \frac{1}{2}z^{T}z\right ) \\
&= -\left(\frac{d}{2}\log 2\pi \sigma^{2} + \frac{1}{2\sigma^{2}}\|x -\mu\|^{2} + \frac{1}{2\sigma^{2}}\mathtt{Tr}(W^{T}Wzz^{T}) - \frac{1}{\sigma^{2}}z^{T}W^{T}(x -\mu)\right) \\
  & - \left(\frac{D}{2}\log2\pi + \frac{1}{2}\mathtt{Tr}(zz^{T})\right ) 
\end{aligned}
$$

Taking expecation w.r.t. $z$ on distirbution $$p_{t}(z \vert x)$$ gives

$$
\mathbb{E}[z] = M^{-1}_{t}W^{T}_{t}(x - \mu_{t})
$$

and 

$$
\mathbb{E}[zz^{T}] = \sigma^{2}_{t}M_{t}^{-1} + \mathbb{E}[z]\mathbb{E}[z]^{T}
$$

by the fact that $$\mathtt{cov}(z) = \mathbb{E}[zz^{T}] - \mathbb{E}[z]\mathbb{E}[z]^{T}$$. We have omitted the subscript $$p_{t}(z \vert x)$$ for the expectation for brevity.

Hence

$$
\begin{aligned}
\mathbb{E}[\log p(x, z \vert \mu, \sigma^{2}, W)] &= -\left(\frac{d}{2}\log (2\pi \sigma^{2}) + \frac{1}{2\sigma^{2}}\|x -\mu\|^{2} + \frac{1}{2\sigma^{2}}\mathtt{Tr}(W^{T}W\mathbb{E}[zz^{T}]) - \frac{1}{\sigma^{2}}\mathbb{E}[z]^{T}W^{T}(x -\mu)\right) \\
  & - \left(\frac{D}{2}\log(2\pi) + \frac{1}{2}\mathtt{Tr}(\mathbb{E}[zz^{T}])\right ) 
 \\
 &= -\left(\frac{d}{2}\log (2\pi \sigma^{2}) + \frac{1}{2\sigma^{2}}\|x -\mu\|^{2} + \frac{1}{2\sigma^{2}}\mathtt{Tr}(W^{T}WC_{t}) - \frac{1}{\sigma^{2}}h_{t}^{T}W^{T}(x -\mu)\right) \\
  & - \left(\frac{D}{2}\log(2\pi) + \frac{1}{2}\mathtt{Tr}(C_{t})\right )
\end{aligned}
$$

where 

$$
C_{t} = \mathbb{E}[zz^{T}] = \sigma^{2}_{t}M_{t}^{-1} + \mathbb{E}[z]\mathbb{E}[z]^{T} =  \sigma^{2}_{t}M_{t}^{-1} + M^{-1}_{t}W^{T}_{t}(x - \mu_{t})(M^{-1}_{t}W^{T}_{t}(x - \mu_{t}))^{T}
$$

and

$$
h_{t} = \mathbb{E}[z]= M^{-1}_{t}W^{T}_{t}(x - \mu_{t})
$$

Take derivatives of $$\mathbb{E}[\log p(x, z \vert \mu, \sigma^{2}, W)]$$ w.r.t. $$\mu$$, $$W$$, and $$\sigma^{2}$$  and  let them be zero. We have

$$
\frac{\partial \mathbb{E}[\log p(x, z \vert \mu, \sigma^{2}, W)]}{\partial \mu} = \frac{1}{\sigma^{2}}(x -\mu) - \frac{1}{\sigma^{2}}Wh_{t} =0
$$

$$
\frac{\partial \mathbb{E}[\log p(x, z \vert \mu, \sigma^{2}, W)]}{\partial W} = -\frac{1}{\sigma^{2}}WC_{t} + \frac{1}{\sigma^{2}}(x - \mu)h_{t}^{T}=0
$$

Therefore, $$W_{t+1}$$ and $$\mu_{t+1}$$ can be found by solving the linear system

$$
\left(\begin{aligned}
W \quad \mu
\end{aligned}\right)\left(\begin{aligned}h_{t} \quad C_{t} \\ 1 \quad h_{t}^{T}\end{aligned}\right) = \left(\begin{aligned}x \quad  xh_{t}^{T}\end{aligned}\right)
$$

Let $$W = W_{t+1}$$ and $$\mu=\mu_{t+1}$$. 

$$
\begin{aligned}
\frac{\partial \mathbb{E}[\log p(x, z \vert \mu_{t+1}, \sigma^{2}, W_{t+1})]}{\partial \sigma^{2}}  =& -\frac{d}{2}\frac{1}{\sigma^{2}} + \frac{1}{2}\|x -\mu_{t+1}\|^{2}\left(\frac{1}{\sigma^{2}}\right)^{2} \\ &+ \frac{1}{2}\mathtt{Tr}(W_{t+1}^{T}W_{t+1}C_{t})\left(\frac{1}{\sigma^{2}}\right)^{2} \\
&- h_{t}^{T}W_{t+1}^{T}(x - \mu_{t+1})\left(\frac{1}{\sigma^{2}}\right)^{2} = 0
\end{aligned}
$$

we have 

$$
\sigma_{t+1}^{2} = \frac{1}{d}\left\{\|x - \mu_{t+1}\|^{2} -2h_{t}^{T}W_{t+1}^{T}(x-\mu_{t+1}) + \mathtt{Tr}\left(W_{t+1}^{T}W_{t+1}C_{t}\right)\right\}
$$

In summary, the EM algorithm for solving PPCA estimation follows steps:

* Let 
  
  $$
  q(z) = p_{t}(z\vert x)=\mathcal{N}(M^{-1}_{t}W^{T}_{t}(x - \mu_{t}), \sigma^{2}_{t}M^{-1}_{t})
  $$

* Solve the linear system 

$$
\left(\begin{aligned}
W \quad \mu
\end{aligned}\right)\left(\begin{aligned}h_{t} \quad C_{t} \\ 1 \quad h_{t}^{T}\end{aligned}\right) = \left(\begin{aligned}x \quad  xh_{t}^{T}\end{aligned}\right)
$$

for $$\mu_{t+1}$$ and $$W_{t+1}$$, and update $$\sigma_{t+1}^{2}$$ by

$$
\sigma_{t+1}^{2} = \frac{1}{d}\left\{\|x - \mu_{t+1}\|^{2} -2h_{t}^{T}W_{t+1}^{T}(x-\mu_{t+1}) + \mathtt{Tr}\left(W_{t+1}^{T}W_{t+1}C_{t}\right)\right\}
$$

The update rule can be simplified by the fact that the maximum likelihood estimation of $$\mu$$ using $$\mathbb{E}_{p(z \vert x)}[\log p(x, z\vert \mu, W, \sigma^{2})]$$ is $$x$$. Hence, we have

$$
\begin{aligned}
\mu_{t} &= x \\
W_{t+1} &= (x - \mu_{t})h^{T}_{t}C_{t}^{-1} \\
\sigma_{t+1}^{2} &= \frac{1}{d}\left\{\|x - \mu_{t}\|^{2} -2h_{t}^{T}W_{t+1}^{T}(x-\mu_{t}) + \mathtt{Tr}\left(W_{t+1}^{T}W_{t+1}C_{t}\right)\right\}
\end{aligned}
$$

#### Generalization of Multiple Samples

Note that in the above description, we only use one sample of $$x$$ as an example. Now, we generalize it to multiple iid. samples $$X = \{x_{1}, x_{2}, \dots, x_{N}\}$$ generated from $$p(x)$$ .

The log likelihood of $$X$$ is

$$
\sum\limits_{i=1}^{N}\log p(x_{i} \vert \mu, \sigma^{2}, W).
$$

And the ELBO becomes

$$
\sum\limits_{i=1}^{N} \left\{\mathbb{E}_{q(z_{i})}\left[\log p(x_{i}, z_{i}\vert \mu, \sigma^{2}, W)\right] + H(q(z_{i}))\right\}
$$

In the EM algorithm, we take $$\mu_{t}$$ as the maximization of log likelihood estimation $$\bar{x} = \frac{1}{N}\sum\limits_{i=1}^{N}x_{i}$$ and

$$
q(z_{i}) = p_{t}(z_{i} \vert x_{i}) = \mathcal{N}(M_{t}^{-1}W_{t}^{T}(x_{i} - \bar{x}), \sigma^{2}_{t}M^{-1}_{t}), \quad \forall i=1, 2, \dots, N.
$$

We solve for $$W_{t+1}$$ and $$\sigma^{2}_{t+1}$$ by 

$$
\max\limits_{W, \sigma^{2}} \sum\limits_{i=1}^{N}\mathbb{E}_{q(z_{i})}[\log p(x_{i}, z_{i}\vert \mu_{t}, \sigma^{2}, W)],
$$

We have

$$
\begin{aligned}
\sum\limits_{i=1}^{N}\mathbb{E}_{q(z_{i})}[\log p(x_{i}, z_{i}\vert \mu_{t}, \sigma^{2}, W)]&=
-\sum\limits_{i=1}^{N}\left(\frac{d}{2}\log (2\pi \sigma^{2}) + \frac{1}{2\sigma^{2}}\|x_{i} -\bar{x}\|^{2} + \frac{1}{2\sigma^{2}}\mathtt{Tr}(W^{T}WC_{t}^{(i)}) - \frac{1}{\sigma^{2}}\left(h^{(i)}_{t}\right)^{T}W^{T}(x_{i} -\bar{x})\right) \\
  & - \sum\limits_{i=1}^{N}\left(\frac{D}{2}\log(2\pi) + \frac{1}{2}\mathtt{Tr}(C_{t}^{(i)})\right )
\end{aligned}
$$

where

$$
C_{t}^{(i)} = \mathbb{E}[z_{i}z_{i}^{T}] = \sigma^{2}_{t}M_{t}^{-1} + \mathbb{E}[z_{i}]\mathbb{E}[z_{i}]^{T} =  \sigma^{2}_{t}M_{t}^{-1} + M^{-1}_{t}W^{T}_{t}(x_{i} - \bar{x})(M^{-1}_{t}W^{T}_{t}(x_{i} - \bar{x}))^{T}
$$

$$
h_{t}^{(i)} = \mathbb{E}[z_{i}] =M^{-1}_{t}W^{T}_{t}(x_{i} - \bar{x})
$$

for $$i=1,2, \dots, N$$.

Therefore, the update rule for the M-step becomes

$$
\begin{aligned}
\mu_{t+1} & = \mu_{t} = \bar{x} \\
W_{t+1}   & =  \left(\sum\limits_{i=1}^{N}\left(x_{i} - \bar{x}\right)(h_{t}^{(i)})^{T}\right)\left(\sum\limits_{i=1}^{N}C_{t}^{(i)}\right)^{-1} \\
\sigma^{2}_{t+1} & = \frac{1}{dN}\sum\limits_{i=1}^{N}\left\{\|x_{i} - \bar{x}\|^{2} -2\left(h_{t}^{(i)}\right)^{T}W_{t+1}^{T}(x_{i}-\bar{x}) + \mathtt{Tr}\left(W_{t+1}^{T}W_{t+1}C_{t}^{(i)}\right)\right\}
\end{aligned}
$$

#### Implemetation Demo of PPCA
```python
import torch

# ── Dataset: 2D observations with a noisy 1D linear structure ───────────────
torch.manual_seed(305)
torch.set_default_dtype(torch.float64)

N, H, D = 1000, 1, 2
z_true = torch.randn(N, H)
mu_true = torch.tensor([1.0, -0.5])
W_true = torch.tensor([[1.5], [0.8]])
sigma_true = 0.3                  # noise standard deviation

X = mu_true + z_true @ W_true.T + sigma_true * torch.randn(N, D)


# ── Model: exact Gaussian posterior ──────────────────────────────────────
def posterior(x, mu, W, sigma2):
    """Return per-observation posterior means and a shared covariance."""
    I = torch.eye(W.shape[1], dtype=W.dtype, device=W.device)
    M = W.T @ W + sigma2 * I
    h = torch.linalg.solve(M, ((x - mu) @ W).T).T  # (N, H)
    Sigma = sigma2 * torch.linalg.solve(M, I)      # (H, H)
    return h, Sigma


# ── Training: full-data EM ───────────────────────────────────────────────
mu = X.mean(dim=0)
Xc = X - mu
W = 0.1 * torch.randn(D, H)
sigma2 = torch.tensor(1.0)       # variance, not standard deviation
num_iters = 200
history = {'elbo': []}

for step in range(num_iters):
    # E-step: moments under the old parameters
    h, Sigma = posterior(X, mu, W, sigma2)
    sum_C = h.T @ h + N * Sigma             # sum_i E[z_i z_i^T]
    Sxz = Xc.T @ h                          # sum_i (x_i-mu) h_i^T

    # M-step: keep h and Sigma fixed
    W = torch.linalg.solve(sum_C, Sxz.T).T
    residual = Xc - h @ W.T
    sigma2 = (residual.square().sum()
              + N * torch.trace(W.T @ W @ Sigma)) / (N * D)

    # Exact-posterior ELBO = marginal log likelihood, averaged over data
    cov_x = W @ W.T + sigma2 * torch.eye(D)
    dist = torch.distributions.MultivariateNormal(
        mu, covariance_matrix=cov_x
    )
    lb = dist.log_prob(X).mean().item()
    history['elbo'].append(lb)

    if (step + 1) % 20 == 0:
        print(f'Iteration {step + 1:03d}  ELBO={lb:.4f}  '
              f'sigma2={sigma2.item():.4f}')

print(f'Final mu: {mu.tolist()}')
print(f'Final W: {W.tolist()}')
print(f'Final noise variance: {sigma2.item():.4f} '
      f'(true: {sigma_true**2:.4f})')
```

```
# ── Visualisation ──────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 4, figsize=(16, 4))

# Panel 1: training curve
axes[0].plot(range(1, num_iters + 1), history['elbo'],
             lw=2, color='steelblue')
axes[0].set_xlabel('EM iteration')
axes[0].set_ylabel('Mean log likelihood / exact ELBO')
axes[0].set_title('Training objective')

# Panel 2: observed data, coloured by the true latent variable
axes[1].scatter(X[:, 0].numpy(), X[:, 1].numpy(),
                c=c_true, cmap='coolwarm', s=8, alpha=0.7)
axes[1].set_title('Observed data (true latent colour)')

# Panel 3: recompute posterior means using the final parameters
h, _ = posterior(X, mu, W, sigma2)
sc = axes[2].scatter(X[:, 0].numpy(), X[:, 1].numpy(),
                     c=h[:, 0].numpy(), cmap='coolwarm', s=8, alpha=0.7)
fig.colorbar(sc, ax=axes[2], label=r'$\mathbb{E}[z\mid x]$')
axes[2].set_title('Posterior mean encoding')

# Panel 4: sample both the latent variable and observation noise
z_prior = torch.randn(500, H)
x_gen = mu + z_prior @ W.T + sigma2.sqrt() * torch.randn(500, D)
axes[3].scatter(x_gen[:, 0].numpy(), x_gen[:, 1].numpy(),
                c=z_prior[:, 0].numpy(), cmap='coolwarm', s=8, alpha=0.7)
axes[3].set_title('Samples from fitted PPCA')

for ax in axes[1:]:
    ax.set_xlabel('$x_1$')
    ax.set_ylabel('$x_2$')
    ax.set_aspect('equal', adjustable='box')

plt.tight_layout()
plt.show()
```

## Variational AutoEncoder (VAE, Kingma et al., 2013)

Classical evidence lower bound (ELBO) of the log likelihood of observation $$x_{n}$$ can be written as

$$
L_{n}(\eta_{n}, \theta) = \mathbb{E}_{q(z_{n}\vert\eta_{n}, x_{n})}[\log p(x_{n}\vert z_{n},\theta)] - \mathtt{KL}(q(z_{n}\vert\eta_{n}, x_{n})\vert\vert p(z_{n}))
$$

In VAE, the core techinque is to use neural networks to parameterize the moments that determine the distributions $$q(z_{n} \vert \eta_{n})$$ and $$p(x_{n}\vert \theta)$$.

The Gaussian VAE assumes that 

$$
\begin{aligned}
p(z_{n}) & = \mathcal{N}(0, I) \\
p(x_{n}\vert z_{n}, \theta) & = \mathcal{N}(g_{\theta}(z_{n}), I) \\
q(z_{n}\vert x_{n}, \eta_{n}) & = \mathcal{N}(\mu_{\phi}(x_{n}), \mathtt{diag}(\sigma^{2}_{\phi}(x_{n}))
\end{aligned}
$$

where 

$$
f_{\phi}(x_{n}) = \left(\begin{aligned} ~~\mu_{\phi}(x_{n})~~\\ \log \sigma_{\phi}(x_{n})^{2} \end{aligned}\right)
$$

By these assumption, the ELBO can be expliclty computed by

$$
\begin{aligned}
L_{n}(\eta_{n}, \theta) = & \mathbb{E}_{q(z_{n}\vert x_{n}, \eta_{n})}\left[-\frac{1}{2}\|x_{n} - g_{\theta}(z_{n})\|^{2}\right]  \\
& - \mathtt{KL}(q(z_{n}\vert\eta_{n}, x_{n})\vert\vert p(z_{n})) + \mathtt{const}.
\end{aligned}
\label{gaussian-elbo}
\tag{Gaussian-ELBO}
$$

For similicity, we denote $$\mu_{\phi}(x_{n})$$ as $$\mu_{n}$$ and $$\sigma_{\phi}^{2}(x_{n})$$ as $$\sigma_{n}^{2}$$, the KL divergence has closed form as

$$
\mathtt{KL}(\mathcal{N}(\mu_{n},\mathtt{diag}(\sigma_{n}^{2}))\vert\vert\mathcal{N}(0, I)) = \frac{1}{2}\sum\limits_{k}\left(\mu_{n,k}^{2} + \sigma_{n,k}^{2} - 1 -\log \sigma_{n,k}^{2}\right)
$$

There is an obstacle to optimize Eq. $$\eqref{gaussian-elbo}$$ by backward propogation as we should sample $$z_{n}$$ from $$q(z_{n}\vert x_{n}, \eta_{n})$$ to computed the reconstruction error $$\|x_{n}-g_{\theta}(z_{n})\|^{2}$$.

To solve the problem, VAE introduces a reparameterization trick for $$z_{n}$$ as

$$
z_{n} = \mu_{\phi}(x_{n}) + \epsilon \odot \sigma_{\phi}(x_{m}) \quad \text{where} \quad \epsilon \sim \mathcal{N}(0, \epsilon).
\label{reparameterization}
\tag{Reparameterization}
$$

Therefore, the first term in Eq. $$\eqref{gaussian-elbo}$$ is expressed as

$$
\mathbb{E}_{\epsilon}\left[-\frac{1}{2}\|x_{n} - g_{\theta}(z_{n})\|^{2}\right]
$$

where $$z_{n}$$ is dertermined by $$\eqref{reparameterization}$$.

Putting together, we have the loss function of VAE as 

$$
\begin{aligned}
L_{n}(\phi, \theta) = & \mathbb{E}_{\epsilon}\left[-\frac{1}{2}\|x_{n} - g_{\theta}(z_{n})\|^{2}\right]  \\
& - \mathtt{KL}(\mathcal{N}(\mu_{\phi}(x_{n}),\mathtt{diag}(\sigma_{\phi}(x_{n})^{2}))\vert\vert\mathcal{N}(0, I))
\end{aligned}
$$

where 

$$
f_{\phi}(x_{n}) = \left(\begin{aligned} ~~\mu_{\phi}(x_{n})~~\\ \log \sigma_{\phi}(x_{n})^{2} \end{aligned}\right).
$$

The relationship between the log-likelihood of $$x_{n}$$ and its ELBO is expressed as

$$
\log p(x_{n} \vert \theta) = L_{n}(\eta_{n}, \theta) + \mathtt{KL}(q(z_{n}\vert x_{n}, \eta_{n})\vert\vert p(z_{n}\vert x_{n}, \theta)).
\label{log-likelihood}
\tag{Log-Likelihood}
$$

In $$\eqref{log-likelihood}$$ , $$q(z_{n} \vert x_{n}, \eta_{n})$$ can be any form for any data point $$x_{n}$$. However, in vae, it is fixed as $$\mathcal{N}(\mu_{\phi}(x_{n}), \sigma^{2}_{\phi}(x_{n}))$$, which induces gap between the best possible $$q(z_{n}\vert x_{n},\eta_{n})$$ that achives 

$$
\min \mathtt{KL}(q(z_{n}\vert x_{n}, \eta_{n})\vert\vert p(z_{n}\vert x_{n}, \theta)).
$$

Let $$q^{*}$$ be the best possible substitutional distribution. The gap

$$
\mathtt{KL}(q^{*}\vert\vert p(z_{n}\vert x_{n}, \theta)) - \mathtt{KL}(\mathcal{N}(\mu_{\phi}(x_{n}), \sigma^{2}_{\phi}(x_{n})) \vert\vert p(z_{n}\vert x_{n}, \theta))
$$

is call the **<mark>amortization gap</mark>**.

For similicity, we deonte $$q(z_{n} \vert x_{n}, \eta_{n}):=\mathcal{N}(\mu_{\phi}(x_{n}), \sigma^{2}_{\phi}(x_{n}))$$ as $$q_{\phi}$$. The inference gap of VAE can be decomposed as 

$$
\begin{aligned}
\log p(x_{n}\vert \theta) - L(\eta_{n}, \theta) = &\underbrace{\mathtt{KL}(q^{*}\vert\vert p(z_{n}\vert x_{n},\theta))}_{\text{Approximation error}} \\
& + \underbrace{\mathtt{KL}(q_{\phi}\vert\vert p(z_{n}\vert x_{n}, \theta)) - \mathtt{KL}(q^{*}\vert\vert p(z_{n}\vert x_{n},\theta))}_{\text{Amortization gap}}
\end{aligned}
$$

A demo of VAE implemetation is provide as follows (see Scott Linderman).

```python
import torch
import torch.nn as nn
import matplotlib.pyplot as plt

# ── Dataset: 2D observations on a noisy 1D manifold (sine curve) ─────────────
torch.manual_seed(305)
N = 1000
t_true = torch.linspace(-3, 3, N) + 0.05 * torch.randn(N)  # latent "phase"
X = torch.stack([t_true + 0.15 * torch.randn(N),
                 torch.sin(t_true) + 0.15 * torch.randn(N)], dim=1)   # (N, 2)
# Colour points by their true phase for later visualisation
c_true = t_true.numpy()


# ── Model ─────────────────────────────────────────────────────────────────────
class Encoder(nn.Module):
    """Maps x ∈ R^D to (μ_z, log σ_z) ∈ R^H × R^H."""
    def __init__(self, D, H, hidden=32):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(D, hidden), nn.Tanh(),
            nn.Linear(hidden, hidden), nn.Tanh(),
        )
        self.mu_head    = nn.Linear(hidden, H)
        self.logσ_head  = nn.Linear(hidden, H)

    def forward(self, x):
        h = self.net(x)
        return self.mu_head(h), self.logσ_head(h)


class Decoder(nn.Module):
    """Maps z ∈ R^H to μ_x ∈ R^D (Gaussian likelihood with unit variance)."""
    def __init__(self, H, D, hidden=32):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(H, hidden), nn.Tanh(),
            nn.Linear(hidden, hidden), nn.Tanh(),
            nn.Linear(hidden, D),
        )

    def forward(self, z):
        return self.net(z)


def elbo(x, encoder, decoder):
    """Single-sample reparameterised ELBO (per data point, mean over batch)."""
    μ_z, logσ_z = encoder(x)           # (B, H)
    σ_z  = logσ_z.exp()

    # Reparameterised sample
    ε    = torch.randn_like(μ_z)
    z    = μ_z + σ_z * ε               # (B, H)

    # Reconstruction: -0.5 ||x - g(z)||^2  (ignoring log 2π constant)
    x_hat    = decoder(z)               # (B, D)
    recon    = -0.5 * ((x - x_hat) ** 2).sum(dim=1).mean()

    # KL[ N(μ_z, diag(σ_z²)) || N(0, I) ]  closed form
    kl = 0.5 * (μ_z**2 + σ_z**2 - 1 - logσ_z * 2).sum(dim=1).mean()

    return recon - kl, recon.item(), kl.item()


# ── Training ──────────────────────────────────────────────────────────────────
H, D        = 1, 2          # 1-D latent space, 2-D observations
batch_size  = 128
num_epochs  = 300

encoder = Encoder(D, H, hidden=32)
decoder = Decoder(H, D, hidden=32)
opt     = torch.optim.Adam(list(encoder.parameters()) +
                           list(decoder.parameters()), lr=1e-3)

dataset = torch.utils.data.TensorDataset(X)
loader  = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)

history = {'elbo': [], 'recon': [], 'kl': []}

for epoch in range(num_epochs):
    for (xb,) in loader:
        lb, r, k = elbo(xb, encoder, decoder)
        (-lb).backward()
        opt.step(); opt.zero_grad()
        print(f'Epoch {epoch:03d}  ELBO={lb.item():.2f}  '
              f'(recon={r:.2f}, KL={k:.2f})', end='\r')
    # Track once per epoch on full data
    with torch.no_grad():
        lb_full, r_full, k_full = elbo(X, encoder, decoder)
    history['elbo'].append(lb_full)
    history['recon'].append(r_full)
    history['kl'].append(k_full)

print(f'Final ELBO: {history["elbo"][-1]:.2f}  '
      f'(recon={history["recon"][-1]:.2f}, KL={history["kl"][-1]:.2f})')
```

```python
fig, axes = plt.subplots(1, 4, figsize=(15, 4))

# ── Panel 1: Training curves ─────────────────────────────────────────────────
ax = axes[0]
ep = range(1, num_epochs + 1)
ax.plot(ep, history['elbo'],  lw=2, color='steelblue', label='ELBO')
ax.plot(ep, history['recon'], lw=1.5, ls='--', color='tomato',   label='Recon')
ax.plot(ep, [-k for k in history['kl']], lw=1.5, ls=':', color='goldenrod', label='−KL')
ax.set_xlabel('Epoch'); ax.set_ylabel('Value')
ax.set_title('Training objective'); ax.legend(fontsize=9)

# ── Panel 2: Original data ────────────────────────────────────────────────────
axes[1].scatter(X[:, 0].numpy(), X[:, 1].numpy(),
                c=c_true, cmap='coolwarm', s=8, alpha=0.7)
axes[1].set_title('Observed data $\mathbf{x}_n$')
axes[1].set_xlabel('$x_1$'); axes[1].set_ylabel('$x_2$')

# ── Panel 3: Latent encoding ──────────────────────────────────────────────────
with torch.no_grad():
    μ_enc, _ = encoder(X)              # (N, H=1)
z_vals = μ_enc[:, 0].numpy()
sc = axes[2].scatter(X[:, 0].numpy(), X[:, 1].numpy(),
                     c=z_vals, cmap='coolwarm', s=8, alpha=0.7)
plt.colorbar(sc, ax=axes[2], label='$\hat{z}_n$')
axes[2].set_title('Data coloured by encoder mean $\mu_\phi(x_n)$')
axes[2].set_xlabel('$x_1$'); axes[2].set_ylabel('$x_2$')

# ── Panel 4: Samples from prior ───────────────────────────────────────────────
with torch.no_grad():
    z_prior = torch.randn(500, H)
    x_gen   = decoder(z_prior)
axes[3].scatter(x_gen[:, 0].numpy(), x_gen[:, 1].numpy(),
                c=z_prior[:, 0].numpy(), cmap='coolwarm', s=12, alpha=0.7)
axes[3].set_title('Samples from prior $z \sim \mathcal{N}(0,I)$\ndecoded to $\hat{x} = g(z;\\theta)$')
axes[3].set_xlabel('$x_1$'); axes[3].set_ylabel('$x_2$')

plt.tight_layout()
plt.show()
```

## Single-Cell Variational Inference (Lopez et al., 2018)

#### Gamma, Poisson, and Negative Bionomial(NB) Distributions

Let $$w \sim \mathtt{Gamma}(\rho, \theta)$$, with the probabiltiy density function

$$
p(w\vert\rho, \theta) = \frac{(\theta/\rho)^{\theta}}{\Gamma(\theta)}w^{\theta-1}\exp\left(-\frac{\theta}{\rho}w\right), \quad w > 0.
$$

and $$Y \vert w \sim \mathtt{Poisson}(\ell w)$$, with the probability mass function

$$
P(Y=k\vert w; \ell)= \frac{(\ell w)^{k}e^{-\ell k}}{k!}.
$$

We get the marginal distribution of $$Y$$ by

$$
\begin{aligned}
P(Y=k) & = \int_{0}^{\infty} P(Y=k\vert w; \ell) p(w\vert\rho, \theta) \mathtt{d} w \\
& =  \frac{\Gamma(k+\theta)}{\Gamma(\theta)\Gamma(k+1)}\left(\frac{\theta}{\theta + \ell \rho}\right)^{\theta}\left(\frac{\ell \rho}{\theta + \ell \rho}\right)^{k}.
\end{aligned}
$$

Hence $$Y \sim \mathtt{NB}(\ell \rho, \theta)$$.

#### Generative Process

For the latent variables representation$$z \in \mathbb{R}^{D}$$ and library size $$\ell$$, we assume their priors as

$$
z \sim \mathcal{N}(0, \boldsymbol{I}_{D}) \quad \text{and} \quad \ell \sim \log \mathcal{N}(\hat{\mu}_{\ell}, \hat{\sigma}^{2}_{\ell})
$$

where $$\hat{\mu}_{\ell}$$ and $$\hat{\sigma}^{2}_{\ell}$$ are piror mean and variance of $$\ell$$ (<mark> usually esitimated from data </mark>). The generative process is:

$$
\begin{aligned}
\rho \quad & = f_{\phi}(z), \\
w \quad & \sim \mathtt{Gamma}(\rho, \theta), \\
y \quad & \sim \mathtt{Poisson}(\ell w), \\
h \quad & \sim \mathtt{Bernoulli}(f_{\psi}(z)), \\
x \quad & = (1 - h) \odot y.
\end{aligned}
$$

$$f_{\phi}$$ and $$f_{\psi}$$ are <mark>neural networks</mark> (**<mark>Decoders</mark>**)  that map the latent representation $$z$$ to $$\mathbb{R}^{d}$$. By the previous result the Gamma-Poisson subprocess is equivalent to

$$
y \sim \mathtt{NB}(\ell \rho, \theta).
$$

The invere dispersion parameter $$\theta \in \mathbb{R}^{d}_{+}$$  that governs the Gamma distribution is estimated via variational inference described next.

#### Inference Models

The posterior of the latent variables $$p(z, \ell \vert x)$$ is approximated by 

$$
q(z, \ell \vert x) = q_{\kappa}(z\vert x)q_{\xi}(\ell\vert x),
$$

$$
q_{\kappa}(z|x) = \mathcal{N}(\mu_{\kappa}(x), \sigma_{\kappa}^{2}(x))
$$

$$
q_{\xi}(\ell|x) = \log \mathcal{N}(\mu_{\xi}(x), \sigma^{2}_{\xi}(x))
$$

##### Reparameterization trick

$$
\begin{aligned}
z & = \mu_{\kappa}(x) + \sigma_{\kappa}(x) \odot \epsilon_{z}, \quad &\epsilon_{z} \sim \mathcal{N}(0, \boldsymbol{I}_{D})\\
\log(\ell) & = \mu_{\xi}(x) + \sigma_{\xi}(x) \cdot \epsilon_{\ell}, \quad &\epsilon_{\ell} \sim \mathcal{N}(0, 1)
\end{aligned}
$$

The moments $$\mu_{\cdot}(x)$$ and $$\sigma_{\cdot}^{2}(x)$$ are characterized by <mark>neural networks</mark> (**<mark>Encoder</mark>**) parameterized by $$\kappa$$ and $$\xi$$ for $$z$$ and $$\ell$$, respectively.

#### Evidence Lower Bound (ELBO)

The log-likelihood of observation $$x$$ is lower bounded by 

$$
\begin{aligned}
\log p(x) \geq & \mathbb{E}_{q(z, \ell \vert x)}[\log p(x\vert z, \ell)] - D_{\mathtt{KL}}(q_{\xi}(\ell \vert x)\vert\vert p(\ell))  \\
& - D_{\mathtt{KL}}(q_{\kappa}(z\vert x)\vert\vert p(z))
\end{aligned}
$$

##### Conditionally marginal likelihood 

Since

$$
p(x_{g}|h_{g}, y_{g}) = \boldsymbol{1}\{x_{g} = (1 - h_{g})y_{g}\}
$$

$$
p(h_{g}\vert z) =  \pi_{g}(z)^{h_{g}}(1 - \pi_{g}(z))^{1- h_{g}}
$$

$$
p(y_{g} \vert z, \ell;\theta) = \frac{\Gamma(y_{g}+\theta_{g})}{\Gamma(\theta_{g})\Gamma(y_{g}+1)}\left(\frac{\theta_{g}}{\theta_{g}+\ell \rho_{g}(z)}\right)^{\theta_{g}}\left(\frac{\ell \rho_{g}(z)}{\theta_{g} + \ell \rho_{g}(z)}\right)^{y_{g}}
$$

We have

$$
\begin{aligned}
p(x_{g}\vert z, \ell) = & \sum\limits_{y_{g} \in \mathbb{N}} p(x_{g}\vert h_{g}=0, y_{g})p(h_{g}=0 \vert z)p(y_{g}\vert z, \ell; \theta)  \\
 & + \sum\limits_{y_{g} \in \mathbb{N}} p(x_{g}\vert h_{g}=1, y_{g})p(h_{g}=1 \vert z)p(y_{g}\vert z, \ell; \theta)  \\
 = & (1 - \pi_{g}(z))\sum\limits_{y_{g} \in \mathbb{N}} p(x_{g}\vert h_{g}=0, y_{g}) p(y_{g}\vert z, \ell; \theta) \\
 & + \pi_{g}(z) \sum\limits_{y_{g} \in \mathbb{N}} p(x_{g}\vert h_{g}=1, y_{g})p(y_{g}\vert z, \ell; \theta) \\
 = & (1 - \pi_{g}(z)) p(y_{g}=x_{g}|z, \ell; \theta) + \\
 & + \pi_{g}(z) \boldsymbol{1}_{\{x_{g}=0\}}\sum\limits_{y_{g} \in \mathbb{N}}p(y_{g} \vert z, \ell;\theta)  \\
 =& (1 - \pi_{g}(z)) p(y_{g}=x_{g}|z, \ell; \theta) + \\
 & + \pi_{g}(z) \boldsymbol{1}_{\{x_{g}=0\}},
\end{aligned}
$$

which can be wirtten as

$$
\begin{aligned}
p(x_{g}\vert z, \ell;\theta) & = (1 - \pi_{g}(z)) \\
& \times \frac{\Gamma(x_{g}+\theta_{g})}{\Gamma(\theta_{g})\Gamma(x_{g}+1)}\left(\frac{\theta_{g}}{\theta_{g}+\ell \rho_{g}(z)}\right)^{\theta_{g}}\left(\frac{\ell \rho_{g}(z)}{\theta_{g} + \ell \rho_{g}(z)}\right)^{x_{g}} \\
& + \pi_{g}(z)\boldsymbol{1}_{\{x_{g}=0\}}
\end{aligned}
$$

Hence

$$
p(x\vert z, \ell) = \prod_{g=1}^{d}p(x_{g}\vert z, \ell;\theta)
$$

Note that

$$
\log p(x_{g}\vert z, \ell; \theta) =\left\{\begin{aligned}
&\log (1 - \pi_{g}(z)) + \log \mathtt{NB}(x_{g}; \ell\rho_{g}(z), \theta_{g}), \quad & x_{g} >0 \\
& \log \{(1-\pi_{g}(z))\log \mathtt{NB}(0; \ell\rho_{g}(z), \theta_{g})+ \pi_{g}(z)\}, \quad &x_{g}=0
\end{aligned}
\right.
$$

##### KL divergence between normal distributions

Let $$m_{z} = \mu_{\kappa}(x)$$, $$v_{z} = \sigma_{\kappa}^{2}(x)$$, we have

$$
D_{\mathtt{KL}}(q_{\kappa}(z\vert x)\vert\vert p(z)) = \frac{1}{2}\sum\limits_{j=1}^{D}\left\{m_{z, j}^{2} + v_{z, j} - 1  - \log v_{z,j}\right\}
$$

##### KL divergence between log-normal distributions

Let 

$$
m_{\ell} = \mu_{\xi}(x),\quad v_{\ell} = \sigma^{2}_{\xi}(x), \quad m_{0}=\hat{\mu}_{\ell}, \quad v_{0} = \hat{\sigma}^{2}_{\ell}.
$$

Denote $$r = \log \ell$$, then

$$
q_{r}(r \vert z) = \mathcal{N}(m_{\ell}, v_{\ell}) \quad \text{and} \quad p_{r}(r) = \mathcal{N}(m_{0}, v_{0})
$$

By changing variables, we get

$$
q_{\xi}(\ell \vert z) = \frac{q_{r}(\log \ell \vert z)}{\ell} \quad \text{and} \quad p(\ell) = \frac{p_{r}(\log \ell)}{\ell}.
$$

Hence, 

$$
\begin{aligned}
D_{\mathtt{KL}}(q_{\xi}(\ell \vert z) \vert \vert p(\ell)) & = D_{\mathtt{KL}}(\mathcal{N}(m_{\ell}, v_{\ell})\vert \vert \mathcal{N} (m_{0}, v_{0})) \\
& = \frac{1}{2}\left[\log \frac{v_{0}}{v_{\ell}} + \frac{v_{\ell}+ (m_{\ell} - m_{0})^{2}}{v_{0}} - 1\right]
\end{aligned}
$$

In summary, the loss of scVI can be written as

$$
\begin{aligned}
\mathcal{L}_{\mathtt{scVI}} = & \mathbb{E}_{q(z, \ell \vert x)}[\log p(x\vert z, \ell)]  \\ &- D_{\mathtt{KL}}(q_{\xi}(\ell \vert x)\vert\vert p(\ell))  
 - D_{\mathtt{KL}}(q_{\kappa}(z\vert x)\vert\vert p(z)) \\
 = & \mathbb{E}_{q(z, \ell \vert x)}\left[\sum\limits_{g=1}^{d}\log p(x_{g}\vert z, \ell; \theta)\right] \\ &- D_{\mathtt{KL}}(q_{\xi}(\ell \vert x)\vert\vert p(\ell))  
 - D_{\mathtt{KL}}(q_{\kappa}(z\vert x)\vert\vert p(z)) 
\end{aligned}
$$

Combing Monte Carlo sampling and reparameterization tricks, the estimated loss of scVI is

$$
\hat{\mathcal{L}}_{\mathtt{scVI}} = \frac{1}{S}\sum\limits_{s=1}^{S}\sum\limits_{g=1}^{d}\log p(x_{g}|z^{(s)}, \ell^{(s)}) - D_{\mathtt{KL}}(q_{\xi}(\ell \vert x)\vert\vert p(\ell))  
 - D_{\mathtt{KL}}(q_{\kappa}(z\vert x)\vert\vert p(z)),
$$

where 

$$
\begin{aligned}
z^{(s)} & = \mu_{\kappa}(x) + \sigma_{\kappa}(x) \odot \epsilon_{z}^{(s)}, \quad &\epsilon_{z}^{(s)} \sim \mathcal{N}(0, \boldsymbol{I}_{D})\\
\log(\ell^{(s)}) & = \mu_{\xi}(x) + \sigma_{\xi}(x) \cdot \epsilon^{(s)}_{\ell}, \quad &\epsilon^{(s)}_{\ell} \sim \mathcal{N}(0, 1)
\end{aligned}
$$

and $$S$$ is the number of rounds of sampling. Note that the estimated loss $$\hat{\mathcal{L}}_{\mathtt{scVI}}$$  is the actual loss for training to learn encoders $$\kappa$$ and $$\xi$$, decoders $$\phi$$ and  $$\psi$$, and parameter $$\theta$$.

#### Implemetation Demo of scVI

```python
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
    log_mu_over_theta = mu.log() - theta.log()
    nb_zero = -theta * F.softplus(log_mu_over_theta)
    nb_log_prob = (
        nb_zero - x * F.softplus(-log_mu_over_theta)
        + torch.lgamma(x + theta) - torch.lgamma(theta) - torch.lgamma(x + 1)
    )
    log_keep = F.logsigmoid(-zi_logits)
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
```
Refer to [`minimal_scvi_demo.py`](../files/minimal_scvi_demo.py) for the full implementation. 

## Posterior Collapse (Murphy, Chapter 21.4)

For variational autoencoder (VAE), the ELBO can be written as

$$
\mathcal{L}(\phi, \theta) = \mathbb{E}_{q_{\phi}(z\vert x)}[\log p_{\theta}(x \vert z)] - D_{\mathtt{KL}}(q_{\phi}(z\vert x)\vert\vert p(z)),
$$

where $$\theta$$ and $$\phi$$ are parameters for the decoder and the encoder respectively. 

If the decoder is higly expressive, i.e., there exists $$\theta^{*}$$ such that

$$
p_{\theta^{*}}(x \vert z) = p_{\mathcal{D}}(x),
$$

where $$p_{\mathcal{D}}(x)$$ is the empirical distribution of $$x$$. For the Bayes' rule, we get

$$
p_{\mathcal{D},\theta^{*}}(z \vert x) = \frac{p_{\theta^{*}}(x \vert z)p(z)}{p_{\mathcal{D}}(x)} = p(z),
$$

which implies that the latent variable $$z$$ is independent of $$x$$  and there exists $$\phi^{*}$$ such that

$$
q_{\phi^{*}}(z \vert x) = p(z).
$$

In such case, the posterior collapse happens: for every $$x$$, it yields the same estimated apporxiamte posterior.

<img src="../img/posterior_collapse.png" alt="posterior_collapse" style="zoom:50%;" />

It is shown that linear VAE may also has posterior collapse, so it is not merely caused by the powerful decoders (Lucas et al., 2019 & Bai et al., 2020).

#### Understanding Posterior Collapse by Mutual Information

Let $$X$$ and $$Z$$ be random variables with respective distrbutions $$p(x)$$ and $$p(z)$$, the mutual information between $$X$$ and $$Z$$ is defined as

$$
I(X; Z) = D_{\mathtt{KL}}(p(x, z) \vert \vert p(x)p(z)).
$$

The mutual information measure the independence between $$X$$ and $$Z$$. If $$I(X;Y)=0$$, then $$X$$ and $$Y$$ are independent.

Define 

$$
q_{\mathcal{D}, \phi}(x, z) = q_{\phi}(z \vert x) p_{\mathcal{D}}(x)
$$

the aggregated posterior 

$$
q_{\phi}(z) = \int_{x} q_{\phi}(z \vert x) p_{\mathcal{D}}(x) \mathtt{d} x.
$$

the expectation of ELBO w.r.t. $$p_{D}(x)$$ is

$$
\mathbb{E}_{p_{\mathcal{D}}(x)}[\mathbb{E}_{q_{\phi}(z \vert x)}[\log p_{\theta}(x \vert z)]] - \mathbb{E}_{p_{\mathcal{D}}(x)}[D_{\mathtt{KL}}(q_{\phi}(z \vert x)\vert\vert p(z))]
$$

where the second term can be rewritten as

$$
\begin{aligned}
\int_{x}p_{D}(x)\int_{z} q_{\phi}(z \vert x)\log \frac{q_{\phi}(z \vert x)}{p(z)} \mathtt{d}z \mathtt{d}x &= \int_{x}\int_{z} q_{\mathcal{D}, \phi}(x, z)\log \left(\frac{q_{\phi}(z \vert x)p_{\mathcal{D}}(x)}{q_{\phi}(z)p_{\mathcal{D}}(x)} \cdot \frac{q_{\phi}(z)}{p(z)} \right)\mathtt{d}z\mathtt{d}x \\
& = \int_{x}\int_{z} q_{\mathcal{D}, \phi}(x, z)\log \frac{q_{\mathcal{D}, \phi}(x, z)}{q_{\phi}(z)p_{\mathcal{D}(x)}} \mathtt{d}z\mathtt{d}x + \int_{z}q_{\phi}(z)\log\frac{q_{\phi}(z)}{p(z)}\mathtt{d}z \\
&= I(X; Z) + D_{\mathtt{KL}}(q_{\phi}(z)\vert \vert p(z)).
\end{aligned}
$$

Therefore, maximizing the ELBO simultaneously 

* maximizes the conditional likelihood;
* minimizes the mutual information between $$X$$ and $$Z$$;
* minimizes the KL-divergence between  the aggregated posterior $$q_{\phi}(z)$$ and the prior $$p(z)$$.

The secod goal may lead to the independence between latent variable $$z$$ and input $$x$$.

When posterior collapse happens, it may also achieve the optimal ELBO. To see this, we note that

$$
\mathbb{E}_{p_{\mathcal{D}}(x)}[\log p_{\theta}(x)] \geq \mathbb{E}_{p_{D}(x)}[\mathbb{E}_{q_{\phi}(z \vert x)}\log p_{\theta}(x \vert z)] - \mathbb{E}_{p_{\mathcal{D}}(x)}[D_{\mathtt{KL}}(q_{\phi}(z \vert x)\vert\vert p(z))] := \mathcal{E}(\theta, \phi).
$$

Suppose 

$$
p_{\theta^{*}}(x \vert z) = p_{\mathcal{D}}(x) \quad \text{and} \quad q_{\phi^{*}}(z \vert x) = p(z).
$$

we have

$$
\mathcal{E}(\theta^{*}, \phi^{*}) = \mathbb{E}_{p_{\mathcal{D}}(x)}[\log p_{D}(x)] = -H(X)
$$

and 

$$
\mathcal{E}(\theta, \phi) \leq \mathbb{E}_{p_{\mathcal{D}}(x)}[\log p_{\theta}(x)]  = -H(X) - D_{\mathtt{KL}}(p_{D} \vert \vert p_{\theta}(x)) \leq -H(X) = \mathcal{E}(\theta^{*}, \phi^{*})
$$

That is $$\theta^{*}$$ and $$\phi^{*}$$ that cause the posterior collapse yield the optimal ELBO.

There are several solutions  to address the posterior collapse, including

* KL annealing
* Lower bounding the rate
* Free bits
* Adding skip connections
* Alternative objectives (InfoVAE, $$\beta$$-VAE)

# Reference

1. Bishop, C. M. (2006). *Pattern Recognition and Machine Learning* . New York: springer.
2. Scott Linderman. [Varitional Autoencoders](https://slinderman.github.io/stats305c/vaes/). Stats 305C(2026). 
3. Kingma, D. P. (2013). Auto-encoding variational bayes. *arXiv preprint arXiv:1312.6114*.
4. Lopez, R., Regier, J., Cole, M. B., Jordan, M. I., & Yosef, N. (2018). Deep generative modeling for single-cell transcriptomics. *Nature methods*, *15*(12), 1053-1058.
5. Murphy, K. P. (2023). *Probabilistic machine learning: Advanced topics*. MIT press.
6. Lucas, J., Tucker, G., Grosse, R. B., & Norouzi, M. (2019). Don't blame the elbo! a linear vae perspective on posterior collapse. *Advances in neural information processing systems*, *32*.
7. Dai, B., Wang, Z., & Wipf, D. (2020, November). The usual suspects? Reassessing blame for VAE posterior collapse. In *International conference on machine learning* (pp. 2313-2322). PMLR.
