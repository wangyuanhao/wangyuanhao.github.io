---
title: "Proof Roadmap of Convergence Analysis of Prox-SVRG"
date: 2026-10-01
permalink: /blog/Proof-Roadmap-ProxSVRG/
excerpt: "Proof roadmap of theorectial analysis of Prox-SVRG, a stochastic first-order optimization method for solving composite objectives"
tags: [Stochastic Optimization, Proof Roadmap]
lang: en
published: true
---

This blog presents the proof roadmap of theorectial analysis of Prox-SVRG (Xiao & Zhang, 2014), a stochastic first-order optimization method for solving composite objectives.

## 1. Statement and goal

The theorem aims to prove a geometric convergence rate for Prox-SVRG.

The assumptions are:

- $P(x) = F(x) + R(x)$.
- $F(x)$ is $\mu_F$-strongly convex and $R(x)$ is $\mu_R$-strongly convex. Hence $P(x)$ is $\mu$-strongly convex, where $\mu = \mu_F + \mu_R$.
- $F(x)$ is $L$-smooth.
- $F(x) = \frac{1}{n}\sum\limits_{i=1}^{n} f_i(x)$, where each $f_i(x)$ is convex and $L_i$-smooth.

The desired conclusion is that there exists $0 < \rho < 1$ such that

$$
\mathbb{E}\left[P(\tilde{x}_s) - P(x_*)\right]
\leq
\rho^s \left[P(\tilde{x}_0) - P(x_*)\right].
$$

## 2. Main difficulty

A direct proof is difficult because the proximal update is driven by a stochastic gradient estimator $v_k$ rather than the full gradient $\nabla F(x_{k-1})$. Therefore, the corresponding proximal gradient mapping is random and cannot be controlled in the same way as in the deterministic proximal gradient method.

More precisely, by defining

$$
g_k := \frac{1}{\eta}(x_{k-1} - x_k),
$$

we have

$$
\|x_k - x_*\|^2
=
\|x_{k-1} - x_*\|^2
-
2\eta g_k^T(x_{k-1} - x_*)
+
\eta^2 \|g_k\|^2.
$$

Hence the problematic term is

$$
-2\eta g_k^T(x_{k-1} - x_*)
+
\eta^2 \|g_k\|^2.
$$

Another difficulty comes from the gradient estimation error

$$
\Delta_k := v_k - \nabla F(x_{k-1}).
$$

Although

$$
\mathbb{E}_k[\Delta_k] = 0,
$$

the point $x_k$ depends on $v_k$, and hence depends on $\Delta_k$. Therefore, we cannot directly use
$\mathbb{E}_k[\Delta_k] = 0$ to eliminate the term

$$
-\Delta_k^T(x_k - x_*).
$$

## 3. Key idea

The proof overcomes these difficulties by converting the stochastic proximal update into a controllable one-step recursion.

The central auxiliary objects are

$$
g_k := \frac{1}{\eta}(x_{k-1} - x_k),
\qquad
\Delta_k := v_k - \nabla F(x_{k-1}),
$$

and the full-gradient proximal point

$$
\bar{x}_k
:=
\operatorname{prox}_{\eta R}
\left(
x_{k-1} - \eta \nabla F(x_{k-1})
\right).
$$

Lemma 3.7 is used to control the stochastic proximal gradient mapping term. The auxiliary point $\bar{x}_k$ is introduced to decouple the dependence between $\Delta_k$ and $x_k$. Specifically,

$$
-\Delta_k^T(x_k - x_*)
=
-\Delta_k^T(\bar{x}_k - x_*)
-
\Delta_k^T(x_k - \bar{x}_k).
$$

Since $\bar{x}_k$ is independent of the current random sample conditioned on the past information, we have

$$
\mathbb{E}_k\left[\Delta_k^T(\bar{x}_k - x_*)\right] = 0.
$$

The remaining term

$$
-\Delta_k^T(x_k - \bar{x}_k)
$$

can then be controlled by the variance of the gradient estimator.

## 4. Structure of the proof and role of each lemma

* Step 1: Start from the squared-distance recursion
$$
\|x_k - x_*\|^2
=
\|x_{k-1} - x_*\|^2
-
2\eta g_k^T(x_{k-1} - x_*)
+
\eta^2 \|g_k\|^2.
$$

* Step 2: Use Lemma 3.7 to control the proximal gradient mapping term

$$
-2\eta g_k^T(x_{k-1} - x_*)
+
\eta^2 \|g_k\|^2.
$$

This step transforms the stochastic proximal update into an inequality involving objective gaps and the gradient estimation error.

* Step 3: Identify the stochastic error term

$$
-\Delta_k^T(x_k - x_*),
$$

which cannot be directly removed by taking conditional expectation because $x_k$ depends on the same randomness as $\Delta_k$.

* Step 4: Introduce the full-gradient proximal point

$$
\bar{x}_k
=
\operatorname{prox}_{\eta R}
\left(
x_{k-1} - \eta \nabla F(x_{k-1})
\right)
$$

and decompose

$$
-\Delta_k^T(x_k - x_*)
=
-\Delta_k^T(\bar{x}_k - x_*)
-
\Delta_k^T(x_k - \bar{x}_k).
$$

The first term vanishes after taking conditional expectation, while the second term is bounded by the variance of $v_k$.

* Step 5: Bound $-\Delta_k^T(x_k - \bar{x}_k)$ by Cauchy–Schwarz inequality and non-expansiveness property of proximal mapping

$$
\begin{aligned}
-\Delta_k^T(x_k - \bar{x}_k) &\leq \|\Delta_{k}\|\|x_k - \bar{x}_k\| \\
& \leq \|\Delta_{k}\|\|\operatorname{prox}_{\eta R}(x_{k-1} - \eta v_{k}) - \operatorname{prox}_{\eta R}(x_{k-1} - \eta \nabla F(x_{k-1}))\| \\
& \leq \|\Delta_{k}\|\| x_{k-1} - \eta v_{k} - (x_{k-1} - \eta \nabla F(x_{k-1}))\| \\
& = \eta \|\Delta_{k}\|^{2}.
\end{aligned}
$$

* Step 6: Use Corollary 3.5, which follows from Lemma 3.4, to control the variance term

$$
\mathbb{E}\|\Delta_k\|^{2} = \mathbb{E}\left\|v_k - \nabla F(x_{k-1})\right\|^2.
$$

This is where the variance-reduction structure of SVRG enters the proof.

* Step 7: Combine the above estimates to obtain a one-step recursive inequality for

$$
\mathbb{E}\left[\|x_k - x_*\|^2\right]
\quad \text{and} \quad
\mathbb{E}\left[P(x_k) - P(x_*)\right].
$$

* Step 8: Sum the one-step inequality over the inner loop $k = 1,\dots,m$. The summation produces a telescoping effect for the squared-distance terms and gives a bound for the average or selected inner iterate in terms of the snapshot point $\tilde{x}_{s-1}$.

* Step 9: Use the snapshot update rule and the strong convexity of $P$ to convert the inner-loop bound into a stage-wise contraction

$$
\mathbb{E}\left[P(\tilde{x}_s) - P(x_*)\right]
\leq
\rho
\mathbb{E}\left[P(\tilde{x}_{s-1}) - P(x_*)\right],
\qquad 0 < \rho < 1.
$$

* Step 10: Iterate the stage-wise contraction over $s$ outer loops to obtain

$$
\mathbb{E}\left[P(\tilde{x}_s) - P(x_*)\right]
\leq
\rho^s
\left[
P(\tilde{x}_0) - P(x_*)
\right].
$$

## 5. Dependency graph

$$
\begin{array}{c}
\text{Theorem 3.1: geometric convergence of Prox-SVRG}
\\
\uparrow
\\
\text{stage-wise contraction}
\\
\uparrow
\\
\text{telescoping the one-step recursion over the inner loop}
\\
\uparrow
\\
\begin{array}{cc}
\text{Lemma 3.7} & \text{Corollary 3.5}
\\
& \uparrow
\\
& \text{Lemma 3.4}
\end{array}
\end{array}
$$

## 6. Final assembly

By Lemma 3.7, the proximal gradient mapping term in the squared-distance recursion can be upper bounded by objective gaps and stochastic error terms. By introducing $\bar{x}_k$, the dependence between $\Delta_k$ and $x_k$ is decoupled, which allows the zero-mean property $\mathbb{E}_k[\Delta_k] = 0$ to be used. The remaining stochastic error is controlled by the variance bound in Corollary 3.5.

Combining these estimates gives a one-step recursion. Summing this recursion over the inner loop yields a telescoping inequality. Finally, the strong convexity of $P$ and the snapshot update rule convert this inequality into a contraction from one outer loop to the next. Iterating the contraction gives the desired geometric convergence rate.

## 7. Key takeaway

The proof is essentially based on the following mechanism:

$$
\begin{aligned}
&\text{stochastic proximal update}
\\
&\quad \Longrightarrow \text{one-step descent recursion}
\\
&\quad \Longrightarrow \text{variance control}
\\
&\quad \Longrightarrow \text{inner-loop telescoping}
\\
&\quad \Longrightarrow \text{outer-loop geometric contraction}.
\end{aligned}
$$

In words, the proof transforms the stochastic proximal step into a controllable one-step descent inequality, absorbs the gradient-estimation error through the variance-reduction estimate, and then telescopes the resulting recursion to obtain a stage-wise contraction.

## Reference

Xiao, L., & Zhang, T. (2014). A proximal stochastic gradient method with progressive variance reduction. *SIAM Journal on Optimization*, *24*(4), 2057-2075.
