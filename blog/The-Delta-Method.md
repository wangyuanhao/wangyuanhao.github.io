---
title: "The Delta Method"
date: 2026-10-20
permalink: /blog/The-Delta-Method/
excerpt: "Introduction to the convergence of random variables, the delta method that shows convergence of random variables dervied from smooth functions of known random variables, and the stochastic small o and big O notations."
tags: [Theoretical Statistics]
lang: en
published: true
---

This blog presents the delta method that establishes convergence of random variables that are transformed from the other random variables with known convergence properties. For example, let $$X_{i} \overset{iid}{\sim} P$$, $$E(X) = \theta \neq 0$$, $$\mathtt{Cov}(X)= \Gamma$$, we know that

$$
\sqrt{n}\left(\frac{1}{n}\sum\limits_{i=1}^{n}X_{i}- \theta\right) \overset{d}{\rightarrow} \mathcal{N}(0, \Gamma).
$$

Can we say something about the random variable $$\sqrt{n}\left(\left\|\frac{1}{n}\sum\limits_{i=1}^{n}X_{i}\right\|^{2}- \|\theta\|^{2}\right)$$? We can get the answer by the delta method.

Before we dive into the delta method, we first introduce the convergence of random variables.

# Convergence of random variables  

Let $$\{X_{n}\}$$ be a sequence of random variables and $$X$$ be a random variable.

Defintion 1 (Convergence in probability) $$X_{n}$$ converges to a random variable *in probability*  or $$X_{n} \overset{p}{\rightarrow}X$$, if

$$
\lim\limits_{n \rightarrow \infty} P(|X_{n} -X|>\epsilon) = 0, \forall \epsilon>0.
$$

Definition 2 (Convergence in distribution) Denote $$F_{n}(t) = \mathbb{P}(X_{n}<t)$$ and $$F(t) = \mathbb{P}(X<t)$$. $$X_{n}$$ converges to a random variable $$X$$ *in distribution* or $$X_{n} \overset{d}{\rightarrow} X$$, if

$$
\lim\limits_{n \rightarrow \infty} F_{n}(t) = F(t),
$$

for every continuous point $$t$$ of $$F(t)$$.

Defintion 3 (Convergence in $$L_{2}$$) $$X_{n}$$ converges to $$X$$ in $$L_{2}$$ or $$X_{n} \overset{L_{2}}{\rightarrow} X$$, if

$$
\lim\limits_{n \rightarrow \infty} E(X_{n} - X)^{2} = 0.
$$

Definition 4 (Converges almost surely) $$X_{n}$$ converges *almost surely* to $$X$$ or $$X_{n} \overset{a.s.}{\rightarrow} X$$, if

$$
P(\lim\limits_{n \rightarrow \infty}X_{n} = X) = 1.
$$

> Lemma 1. $$X_{n} \overset{a.s.}{\rightarrow} X$$ if and only if for every $$\epsilon >0$$,
> 
> $$
> \lim\limits_{n \rightarrow \infty}P\{|X_{k} - X| < \epsilon, \text{for~all}~ k \geq n\} = 1.
> $$

**Proof of Lemma 1**

Let 

$$
A_{n, \epsilon} = \{|X_{k} - X |<\epsilon ~\text{for~all}~k\geq n\}.
$$

Then 

$$
\begin{aligned}
P(\lim\limits_{n \rightarrow \infty} X_{n} = X) & =P\{\forall \epsilon>0, \exists n \in \mathbb{N}_{+}, \text{when}~ k\geq n, ~\text{we have}~|X_{k} - X| < \epsilon\} \\
& = P\left(\cap_{\epsilon >0} \cup_{n \in \mathbb{N}_{+}}A_{n, \epsilon}\right).
\end{aligned}
$$

Hence $$X_{n} \overset{a.s.}{\rightarrow} X$$ is equivalent to

$$
P\left(\cap_{\epsilon >0} \cup_{n \in \mathbb{N}_{+}}A_{n, \epsilon}\right)=1.
$$

Note that the monotone descreasing of $$\cup_{n \in \mathbb{N}_{+}}A_{n, \epsilon}$$ w.r.t $$\epsilon$$,

$$
\cap_{\epsilon >0} \cup_{n \in \mathbb{N}_{+}}A_{n, \epsilon} = \lim\limits_{\epsilon \downarrow 0} \cup_{n \in \mathbb{N}_{+}} A_{n, \epsilon}.
$$

By the continuity of probability $$P$$, we have

$$
P(\lim\limits_{\epsilon \downarrow 0} \cup_{n \in \mathbb{N}_{+}} A_{n, \epsilon})= \lim\limits_{\epsilon \downarrow 0} P(\cup_{n \in \mathbb{N}_{+}}A_{n, \epsilon}) = 1,
$$

i.e., for every $$\epsilon >0$$,

$$
P(\cup_{n \in \mathbb{N}_{+}}A_{n, \epsilon})=1.
$$

Since $$A_{1, \epsilon} \subset A_{2,\epsilon} \subset \cdots \subset A_{n, \epsilon} \subset \cdots$$, we have $$\cup_{n \in \mathbb{N}_{+}} A_{n, \epsilon}= \lim\limits_{n \rightarrow \infty} A_{n, \epsilon}$$.

Therefore, we conclude that, for every $$\epsilon > 0$$,

$$
P(A_{n, \epsilon})=1 \quad \text{as} \quad n \rightarrow \infty.
$$

> Theorem 1 (Relationships among various modes of convergence) 
>
> * $$X_{n} \overset{a.s.}{\rightarrow} X \Longrightarrow X_{n} \overset{p}{\rightarrow} X$$.
> * $$X_{n} \overset{L_{2}}{\rightarrow} X \Longrightarrow X_{n} \overset{p}{\rightarrow} X$$.
> * $$ X_{n} \overset{p}{\rightarrow} X \Longrightarrow X_{n} \overset{d}{\rightarrow} X$$.

**Proof of Theorem 1**

(1) Using Lemma 1, $$X_{n} \overset{a.s.}{\rightarrow} X$$ is equivalent to

$$
\lim\limits_{n \rightarrow \infty} P(|X_{k} - X|<\epsilon~\text{for all}~k > n) = 1, \quad \forall \epsilon>0.
$$

As $$k > n$$ and $$n \rightarrow \infty$$, we have $$k \rightarrow \infty$$ and hence

$$
\lim\limits_{k \rightarrow \infty} P(|X_{k}- X|<\epsilon)=1, \quad \forall \epsilon>0.
$$

That is $$X_{n} \overset{p}{\rightarrow} X$$.

(2) Using Chebyshev's inequality, we have

$$
P(|X_{n} - X|>\epsilon) = P(|X_{n}-X|^{2}>\epsilon^{2}) \leq \frac{E(X_{n}-X)^{2}}{\epsilon^{2}}, \quad \forall \epsilon>0.
$$

Taking $$n \rightarrow \infty$$ in both sides and by the fact that $$X_{n} \overset{L_{2}}{\rightarrow} X $$, we have

$$
\lim\limits_{n \rightarrow \infty} P(|X_{n} - X|>\epsilon) = 0, \quad \epsilon >0.
$$

That is $$X_{n} \overset{p}{\rightarrow} X$$.

(3) Let $$\epsilon>0$$. If $$X_{n}\leq t_{0}$$, then either  $$X \leq t_{0} +\epsilon$$ or $$X>t_{0}+\epsilon$$, where in the latter case we have $$\lvert X_{n} - X\rvert  >\epsilon$$. Hence we have $$\{X_{n} \leq t_{0}\} \subset \{X \leq t_{0}+\epsilon\} \cup \{\lvert X_{n} - X\rvert >\epsilon\}$$ and

$$
F_{n}(t_{0}) \leq F(t_{0}+\epsilon) + P(|X_{n} - X|>\epsilon)
$$

holds.

Similarly, if $$X \leq t_{0} -\epsilon$$, then either $$X_{n} \leq t_{0}$$ or $$\lvert X_{n} - X\rvert  >\epsilon$$, and

$$
F(t_{0} - \epsilon) \leq F_{n}(t_{0}) + P(|X_{n} - X|>\epsilon)
$$

holds.

Since $$P(\lvert X_{n} - X\rvert >\epsilon) \rightarrow 0$$ as $$n \rightarrow \infty$$,

$$
F(t_{0} - \epsilon) \leq \mathop{\lim\inf}\limits_{n \rightarrow \infty} F_{n}(t_{0}) \leq \mathop{\lim\sup}\limits_{n \rightarrow \infty} F_{n}(t_{0}) \leq F(t_{0}+\epsilon), \quad \forall \epsilon > 0.
$$

Taking $$\epsilon \downarrow 0$$ and using the continuity of $$t_{0}$$ in $$F(t)$$, we have

$$
\lim\limits_{n \rightarrow \infty} F_{n}(t_{0}) = F(t_{0}).
$$

> Theorem 2 (Slutsky's Theorem)
>
> (1) If $$c$$ is constant, then
> 
> $$
> X_{n} \overset{d}{\rightarrow} c \Longleftrightarrow X_{n} \overset{p}{\rightarrow} c.
> $$
> 
> (2) If $$X_{n} \overset{d}{\rightarrow} X$$, $$d(X_{n}, Y_{n}) \overset{p}{\rightarrow} 0$$, then
> 
> $$
> Y_{n} \overset{d}{\rightarrow} X.
> $$
>
>  (3) If $$X_{n} \overset{d}{\rightarrow} X$$, $$Y_{n} \overset{p}{\rightarrow} c$$ ($$c$$ constant), then
> 
> $$
> \left(\begin{aligned}X_{n} \\ Y_{n}\end{aligned}\right) \overset{d}{\rightarrow}\left(\begin{aligned}  X & \\  c~ & \end{aligned}\right).
> $$

> Theorem 3 (Continuous mapping ) Let $$g: \mathbb{R}^{d} \rightarrow \mathbb{R}$$ be continuous at every point of a set $$C$$ such that $$P(X \in C) = 1$$.
>
> * If $$X_{n} \overset{d}{\rightarrow} X$$, then $$g(X_{n}) \overset{d}{\rightarrow} g(X)$$.
> * If $$X_{n} \overset{p}{\rightarrow} X$$, then $$g(X_{n}) \overset{p}{\rightarrow} g(X)$$.
> * If $$X_{n} \overset{a.s.}{\rightarrow} X$$, then $$g(X_{n}) \overset{a.s.}{\rightarrow} g(X)$$.

# The delta method

> Theorem 4 (First-order delta method). Let $$r_{n} \rightarrow \infty$$ and $$\phi: \mathbb{R}^{d} \rightarrow \mathbb{R}^{k}$$ be differentiable at $$\theta$$ and assume that $$r_{n}(T_{n} - \theta) \overset{d}{\rightarrow} T$$ for some random vector $$T$$. Then
>
> * $$r_{n}(\phi(T_{n}) - \phi(\theta))$$ converges in distribution to $$\phi'(\theta) T$$
> * $$r_{n}(\phi(T_{n}) - \phi(\theta)) - r_{n}\phi'(\theta)(T_{n} - \theta)$$ converges in probability $$0$$.

**Proof of Theorem 4**

For any $$t$$ in the neighborhood of $$\theta$$, we have

$$
\phi(t) = \phi(\theta) + \phi'(\theta)( t - \theta) + o(|| t- \theta\|).
$$

Let $$h = t - \theta$$. we have $$\lim\limits_{h \rightarrow 0} \frac{o(\|h\|)}{h} = 0$$.

Since $$r_{n}(T_{n} - \theta) \overset{d}{\rightarrow} T$$, $$r_{n}\|T_{n}-\theta\| = O_{p}(1)$$ and $$T_{n} - \theta = o_{p}(1)$$. By Lemma F, we have

$$
\phi(T_{n}) = \phi(\theta) + \phi'(\theta)(T_{n} - \theta) + o_{p}(\|T_{n}- \theta\|)
$$

Multiplying both sides by $$r_{n}$$ yields

$$
r_{n}(\phi(T_{n}) - \phi(\theta)) - r_{n}\phi'(\theta)(T_{n} - \theta) = r_{n}o_{p}(\|T_{n} - \theta\|).
$$

Note that

$$
r_{n}o_{p}(\|T_{n} - \theta\|) = o_{p}(r_{n}\|T_{n} - \theta\|) = o_{p}(O_p(1))=o_{p}(1).
$$

We have the second conclusion. 

Since $$r_{n}\phi'(\theta)(T_{n} - \theta) \overset{d}{\rightarrow} \phi'(\theta)T$$. Applying Slutsky's Theorem, we get the first conclusion.

> Theorem 5 (Second-order delta method) Let $$\phi: \mathbb{R}^{d} \rightarrow \mathbb{R} $$ be twice differentiable at $$\theta$$, and $$r_{n}(T_{n} - \theta) \overset{d}{\rightarrow} T$$ . If $$\nabla \phi(\theta) = 0$$, we have
> 
> $$
> r_{n}^{2}(\phi(T_{n}) - \phi(\theta)) \overset{d}{\rightarrow} \frac{1}{2}T^{T}\nabla^{2}\phi(\theta)T
> $$

**Proof of Theorem 5**

By the second-order Taylor expansion, for any $$t$$ in the neighbor of $$\theta$$, we have

$$
\begin{aligned}
\phi(t) & = \phi(\theta) + \nabla \phi(\theta)^{T}(t-\theta) + \frac{1}{2}(t - \theta)^{T}\nabla^{2}\phi(t-\theta) + o(\|t - \theta\|^{2}) \\
& = \phi(\theta) + \frac{1}{2}(t - \theta)^{T}\nabla^{2}\phi(\theta)(t-\theta) + o(\|t - \theta\|^{2})
\end{aligned}
$$

As $$r_{n}(T_{n} - \theta) \overset{d}{\rightarrow} T$$,  $$r_{n}(T_{n} - \theta)$$ is uniformly tight and $$T_{n} - \theta$$ converges to zero in probability. Hence by Lemma F, we have

$$
\phi(T_{n}) - \phi(\theta) - \frac{1}{2}(T_{n}- \theta)^{T}\nabla^{2}\phi(\theta)(T_{n} - \theta) = o_{p}(\|T_{n} - \theta\|^{2})
$$

Multiplying both sides by $$r_{n}^{2}$$,

$$
r_{n}^{2}(\phi(T_{n}) - \phi(\theta)) - \frac{1}{2}r_{n}(T_{n}- \theta)^{T}\nabla^{2}\phi(\theta)r_{n}(T_{n} - \theta) = r_{n}^{2}o_{p}(\|T_{n} - \theta\|^{2})
$$

Note that 

$$
r_{n}^{2}o_{p}(\|T_{n} - \theta\|^{2}) = o_{p}(r_{n}^{2}\|T_{n}- \theta\|^{2}) = o_{p}(O_{p}(1)) = o_{p}(1).
$$

And 

$$
\frac{1}{2}r_{n}(T_{n} - \theta)^{2}\nabla^{2}\phi(\theta)r_{n}(T_{n} - \theta) \overset{d}{\rightarrow} \frac{1}{2}T^{T}\nabla^{2}\phi(\theta)T.
$$

By the Slutsky's Theorem, we conclude that

$$
r_{n}^{2}(\phi(T_{n} - \phi(\theta)) \overset{d}{\rightarrow} \frac{1}{2}T^{T}\nabla^{2}\phi(\theta)T.
$$


# Appendix

#### Continuity of probability 

Definition A (Convergence of a sequence of sets).  

* A sequence of sets $$A_{1}$$, $$A_{2}$$, $$\cdots$$ is monote increasing if $$A_{1} \subset A_{2} \subset \cdots A_{n} \subset \cdots$$. The limit of such sequence is defined as

$$
\lim\limits_{n \rightarrow \infty} A_{n} = \mathop{\cup}\limits_{n \in \mathbb{N}_{+}} A_{n}.
$$

* A sequence of sets $$A_{1}$$, $$A_{2}$$, $$\cdots$$ is monote descreasing if $$A_{1} \supset A_{2} \cdots \supset A_{n} \supset\cdots$$.  The limit of such sequence is defined as

$$
\lim\limits_{n \rightarrow \infty} A_{n} = \mathop{\cap}\limits_{n \in \mathbb{N}_{+}}A_{n}
$$

Theorem B (Continuity of probability) If $$\lim\limits_{n \rightarrow \infty} A_{n} = A$$, then

$$
P(\lim\limits_{n \rightarrow \infty}A_{n}) = P(A).
$$

#### Stochastic $$o$$ and $$O$$ symbols

Definition C ($$o_{p}$$ notation) If $$X_{n} \overset{d}{\rightarrow} 0$$, then $$X_{n}=o_{p}(1)$$.

Definition D (Tighness) Any random variable $$X$$ is tight, if for every $$\epsilon>0$$, there exists a constant $$M$$ such that $$P(\lvert X\rvert >M)<\epsilon$$. A set of random variables $$\{X_{\alpha}: \alpha \in A\}$$ is called uniformly tight (or bounded in probability),  if for every $$\epsilon>0$$, there exists a constant $$M$$ such that

$$
\sup\limits_{\alpha \in A} P(|X_{\alpha}|>M)<\epsilon.
$$

Definition E ($$O_{p}$$ notation) If $$\{X_{n}: n\in\mathbb{N}_{+}\}$$ is bounded in probability, then $$X_{n} = O_{p}(1)$$.

Generally, for a give sequence of random variables $$R_{n}$$,

$$
X_{n} = o_{1}(R_{n}) \Longrightarrow X_{n} = Y_{n}R_{n} \quad \text{and} \quad Y_{n}=o_{p}(1)
$$

$$
Y_{n} = O_{p}(R_{n}) \Longrightarrow X_{n} = Y_{n}R_{n} \quad \text{and} \quad Y_{n}=O_{p}(1)
$$

Rules of caculus with $$o$$ and $$O$$ symbols:

$$
\begin{aligned}
o_{p}(1) + o_{p}(1) &= o_{p}(1) \\
o_{p}(1) + O_{p}(1) &= O_{p}(1) \\
O_{p}(1)o_{p}(1)		&= o_{p}(1) \\
(1+o_{p}(1))^{-1}   &= O_{p}(1) \\
o_{p}(R_{n})        &= R_{n}o_{p}(1) \\
O_{p}(R_{n})        &= R_{n}O_{p}(1) \\
o_{p}(O_{p}(1))     &= o_{p}(1)
\end{aligned}
$$

> Lemma F.  Let $$R$$ be a function defined on domain in $$\mathbb{R}$$ such that $$R(0)=0$$. Let $$X_{n}$$ be a sequence of random variables with values in the domain of $$R$$ that converges in probability to zero. Then, for every $$p>0$$,
>
> (i) if $$R(h)=o(\lvert h\rvert ^{p})$$ as $$ h \rightarrow 0$$, then $$R(X_{n}) = o_{p}(\lvert X_{n}\rvert ^{p})$$;
>
> (ii) if $$R(h)= O(\lvert h\rvert ^{p})$$ as $$h \rightarrow 0$$, then $$R(X_{n}) = O_{p}(\lvert X_{n}\rvert ^{p})$$.

**Proof of Lemma F** 

Define $$g(h) = \frac{R(h)}{\lvert h\rvert ^{p}}$$ for $$h\neq 0$$, and $$g(0) = 0$$.  By assumtion, $$g(h)$$ is continuous at $$0$$.

(i) By the Continuous Mapping Theorem, we have 

$$
g(X_{n}) \overset{p}{\rightarrow} g(0)=0,
$$

and $$R(X_{n}) = \lvert h\rvert ^{p}g(X_{n})$$. Therefore, $$R(X_{n}) = o_{p}(\lvert h\rvert ^{p})$$.

(ii) There exist $$M>0$$ and $$\delta >0$$, such that

$$
|g(h)|< M \quad \forall h \in U(0;h)
$$

Hence 

$$
P(|g(X_{n})|>M)\leq P(|X_{n}|>\delta)\rightarrow0 \quad \text{as} \quad n\rightarrow \infty.
$$

For any $$\epsilon>0$$, there exists $$N \in \mathbb{N}_{+}$$, such that

$$
P(|g(X_{n})| > M) < \frac{\epsilon}{2},
$$

for $$n>N$$.

For finite random variables $$g(X_{1}), \cdots, g(X_{N})$$, we can chosen $$C_{\epsilon}$$ such that

$$
P(|g(X_{n})|>C_{\epsilon}) < \frac{\epsilon}{2}, \quad \forall~ n \leq N.
$$

Denote $$M_{\epsilon} = \max\{C_{\epsilon}, M\}$$, we have

$$
\sup\limits_{n \in \mathbb{N}_{+}}P(|g(X_{n})|>M_{\epsilon}) < \frac{\epsilon}{2}<\epsilon.
$$

That is $$g(X_{n}) = O_{p}(1)$$.



# Reference

1. Ferguson, T.S. A Course in Large Sample Theory.
2. van der Vaart, A. Asymptotic Statistics.
3. Duchi, J. Lecture notes of Theorectial Statistics II (Stats 300B). 2021.