---
title: "SAGA: Algorithm and Convergence Proof Roadmap"
date: 2026-10-01
permalink: /blog/Proof-Roadmap-SAGA/
excerpt: "Proof roadmap of theorectial analysis of SAGA, a stochastic first-order optimization method for solving composite objectives"
tags: [Stochastic Optimization, Proof Roadmap]
lang: en
published: true
---

# SAGA: Algorithm and Convergence Proof Roadmap

This blog presents the proof roadmap of theorectial analysis of SAGA (Defazio, Bach & Lacoste-Julien, 2014), a stochastic first-order optimization method for solving composite objectives.

##### SAGA update

Objective function


$$
\min_{x \in \mathbb{R}^{d}} F(x)
:= f(x) + h(x)
= \frac{1}{n}\sum_{i=1}^{n} f_i(x) + h(x).
$$

Update

$$
j \sim \operatorname{Unif}([n]).
$$

$$
\phi_i^{k+1} =
\begin{cases}
x^k, & i = j, \\
\phi_i^k, & i \neq j.
\end{cases}
$$

$$
w^{k+1}
= x^k - \gamma\left[
f'_j(\phi_j^{k+1}) - f'_j(\phi_j^k)
+ \frac{1}{n}\sum_{i=1}^{n} f'_i(\phi_i^k)
\right].
$$

$$
\begin{aligned}
x^{k+1}
&= \operatorname{prox}_{\gamma}^{h}(w^{k+1}) \\
&= \operatorname*{arg\,min}_{x \in \mathbb{R}^{d}}
\left\{
h(x) + \frac{1}{2\gamma}\|x - w^{k+1}\|^2
\right\}.
\end{aligned}
$$



## 1. Statement and goal

The theorem aims to prove a geometric convergence rate of the Lyapunov function $$T$$ of SAGA. The assumptions are

- $$F(x) = \frac{1}{n}\sum\limits_{i=1}^{n}f_{i}(x) + h(x)$$.
- Each $$f_{i}(x)$$ is $$\mu$$-strongly convex and $$L$$-smooth.
- $$h(x)$$ is convex but not necessarily differentiable.
- The proximal operator of $$h(x)$$ is easy to compute.

The desired conclusion is that there exists $$\kappa > 1$$ such that

$$
\mathbb{E}[T^{k+1}] \leq (1 - \frac{1}{\kappa})T^{k},
$$

where the Lyapunov function $$T$$ is defined as

$$
\begin{aligned}
T^k
&:= \frac{1}{n}\sum_{i=1}^{n} f_i(\phi_i^k) - f(x^*) \\
&\quad - \frac{1}{n}\sum_{i=1}^{n}
\left\langle f'_i(x^*), \phi_i^k - x^* \right\rangle
+ c\|x^k - x^*\|^{2}.
\end{aligned}
$$



## 2.  Main difficulty

A direct proof is difficult because SAGA uses a stochastic gradient estimate instead of the full gradient for the proximal update.

Another difficulty comes from that  SAGA  randomly  picks one of the previous computed gradient $$f'_{j}(\phi_{j}^{k})$$ to compute the stochastic gradient, which is different from the Prox-SVRG that uses a snapshot of the solution $$\tilde{x}^{s}$$ to do so.  Hence, we need to develop the upper bound for

$$
\frac{1}{n}\sum\limits_{i=1}^{n}\|f'_{i}(\phi_{i}^{k}) - f'_{i}(x^{*})\|^{2}
$$

rather than

$$
\frac{1}{n}\sum\limits_{i=1}^{n}\|f'_{i}(x^{k}) - f_{i}'(x^{*})\|^{2}.
$$

It leads to the non-negative term

$$
\frac{1}{n}\sum\limits_{i=1}^{n}f_{i}(\phi_{i}^{k}) - f(x^{*}) - \frac{1}{n}\sum\limits_{i=1}^{n}\langle f'_{i}(x^{*}), \phi_{i}^{k} - x^{*} \rangle
$$

that can not be canceled by a proper choice of parameters and should be absorbed in the Lyapunov function.



## 3. Key idea

Instead of following the proof in Prox-SVRG, the proof in SAGA bounds the optimal gap by $$\mathbb{E}[\|f'_{i}(\phi_{i}^{k}) - f'_{i}(x^{*})\|^{2}]$$ and
$$\mathbb{E}[\|f_{i}'(x^{k}) - f_{i}'(x^{*})\|^{2}]$$.

To this end, the non-expansiveness property of the proximal operator is employed to control the optimal gap at the very first step.

All the positive terms in the upper bound can be canceled out by choosing proper parameters or be absorbed in the Lyapunov function.

To enable the flexible choice of parameters, undetermined parameters are introduced to the inequality.



## 4. Structure of the proof and role of each lemma

* Step 1: Exploit the non-expansiveness property of proximal mapping to control the optimal gap $$c\|x^{k+1} - x^{*}\|^{2}$$ where $$c$$ is an introduced parameter to enable flexible choice of parameters.

* Step 2: Open the square of $$c\mathbb{E}\|x^{k} - x^{*} + w^{k+1} - x^{k} + \gamma f'(x^{*})\|^{2}$$ a result of Step 1. Control the inner product between $$f'(x^{k})$$ and $$x^{k} - x^{*}$$ by Lemma 1 that is concluded by the property of $$\mu$$-strong convexity and $$L$$-smoothness of $$f_{i}$$. Here the unbiased property of the stochastic gradient estimate is exploited.

* Step 3: Control the term $$c\mathbb{E}\|w^{k+1} - x^{k} + \gamma f'(x^{*})\|^{2}$$ by $$\mathbb{E}\|f'_{j}(\phi_{j}^{k}) - f_{j}'(x^{*})\|^{2}$$, $$\mathbb{E}\|f'_{j}(x^{k}) - f'_{j}(x^{*})\|^{2}$$, and $$\|f'(x^{k}) - f'(x^{*})\|^{2}$$ using Lemma 3. A free parameter $$\beta$$ is introduced as the role of $$c$$. The term $$\mathbb{E}\|f'_{j}(\phi_{j}^{k}) - f_{j}'(x^{*})\|^{2}$$ is bounded by Lemma 2.

* Step 4: The negative of the difference  $$-\|f'(x^{k}) - f'(x^{*})\|^{2}$$ is upper bounded by the difference of $$f(x^{k})$$ and its first-order Taylor approximation at $$x^{*}$$.

* Step 5: Putting all the upper bounds together and exploiting the results of $$\mathbb{E}[T^{k+1}]$$, we have

$$
\mathbb{E}[T^{k+1}]  \leq (1 - \gamma \mu) T^{k} + \mathtt{N},
$$

where the non-negative term  $$\frac{1}{n}\sum\limits_{i=1}^{n}f_{i}(\phi_{i}^{k}) - f(x^{*}) - \frac{1}{n}\sum\limits_{i=1}^{n}\langle f'_{i}(x^{*}), \phi_{i}^{k} - x^{*} \rangle$$ is absorbed in the Lyapunov function. The remained terms can be canceled or dropped out from the inequality by a proper choice of free parameters $$\gamma$$, $$c$$, and $$\beta$$.



## 5. Dependency graph

$$
\begin{array}{c}
\text{Theorem 1: A geometric rate of decay for the Lyapunov function in SAGA}
\\
\uparrow
\\
\text{Cancel or drop the terms that need not to be absorbed } \\
\text{by the Lyapunov function by properly choosing the free parameters.}
\\
\uparrow

\\
\begin{array}{cc}
\text{Lemma 1} & \text{Lemma 3}
\\
& \uparrow
\\
& \text{Lemma 2}
\end{array}
\end{array}
$$



## 6. Final assembly

The non-expansiveness property of the proximal mapping is exploited at the very first step. Then we expand the square of upper bound and apply Lemma 1 to control the negative inner product between $$f'(x^{k})$$ and $$x^{k} - x^{*}$$. We use Lemma 3 to control the resulting square term, which is further bounded by Lemma 1.

By absorbing the irreducible term into the Lyapunov function, we obtain the desired form of the conclusion, whereas the remained terms can be canceled or discarded by a proper choice of free parameters.



## 7. Key takeaway

The proof is essentially based on the following mechanism:

$$
\begin{aligned}
&\text{non-expansiveness property of proximal mapping}
\\
&\quad \Longrightarrow \text{variance control}
\\
&\quad \Longrightarrow \text{construction of the Lyapunov function}
\\
&\quad \Longrightarrow \text{a proper choice of free parameters to drop the reducible terms}.
\end{aligned}
$$

In words,  the proof controls the optimal gap by the non-expansiveness property of proximal mapping, and then constructs the upper bound of the expanding terms by the difference of gradients. The irreducible term is used to design the Lyapunov function, whereas the remaining terms are canceled or discarded through a proper choice of free parameters.



## Reference

Defazio, A., Bach, F., & Lacoste-Julien, S. (2014). SAGA: A fast incremental gradient method with support for non-strongly convex composite objectives. *Advances in neural information processing systems*, *27*.
