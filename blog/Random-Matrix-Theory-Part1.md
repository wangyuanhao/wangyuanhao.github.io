---
title: "An Introductory Random Matrix Theory Part I: Matrix Elementary Revisited"
date: 2026-10-03
permalink: /blog/Random-Matrix-Theory-Part1/
excerpt: "We revist elementary vector space and characterization of matrix"
tags: [High Dimensional Probability, Random Matrix Theory]
lang: en
published: true
---

# Vector Space

**<u>(Linear Dependence Lemma)</u>**  Suppose $$v_{1}, v_{2}, \dots, v_{m}$$ is a linearly dependent list in $$V$$. Then there exists $$k \in \{1, 2, \dots, m\}$$ such that

$$
 v_{k} \in \mathtt{span}\{v_{1}, v_{2}, \dots, v_{k-1}\}.
$$
Furthermore, if $$k$$ satisfies the condition above and the $$k^{\mathtt{th}}$$ term is removed from $$v_{1}, v_{2}, \dots, v_{m}$$, then the span of the remaining list equals to $$\mathtt{span}\{v_{1}, v_{2}, \dots, v_{m}\}$$.

---

**<u>Proof</u>** 

**(1)** Since $$v_{1}, v_{2}, \dots, v_{m}$$ are linearly dependent, there exists a list of $$a_{1}, a_{2}, \dots, a_{m} \in \mathbb{F}$$ and they are not all zero, such that
$$
a_{1}v_{1} + a_{2}v_{2} + \cdots + a_{m}v_{m} = 0
$$
Let $k$ be the largest index of  a non-zero $$a_{i}$$,  then we have $$a_{i}=0$$ for all $$k>i$$ and 
$$
v_{k} = -\frac{a_{1}}{a_{k}}v_{1} - \frac{a_{2}}{a_{k}}v_{2} -\cdots \frac{a_{k-1}}{a_{k}}v_{k-1},
$$
i.e.,  $$v_{k} \in \mathtt{span}\{v_{1}, v_{2}, \dots, v_{k-1}\}.$$

**(2)**  If $v_{k}$ is removed from the list, we have $$\mathtt{span}\{v_{1}, \dots, v_{k-1}, v_{k+1}, v_{m}\} \subset \mathtt{span}\{v_{1}, \dots, v_{m}\}$$. Let $$v \in \mathtt{span}\{v_{1}, \dots, v_{m}\}$$, there exists a list of $$\beta_{1}, \dots, \beta_{m}$$ such that
$$
\begin{aligned}
v & = \beta_{1}v_{1} + \cdots + \beta_{m}v_{m} \\
  & = \beta_{1}v_{1} + \cdots + \beta_{k-1}v_{k-1}+ \beta_{k}\left(-\frac{a_{1}}{a_{k}}v_{1} - \frac{a_{2}}{a_{k}}v_{2} -\cdots \frac{a_{k-1}}{a_{k}}v_{k-1}\right)+ \beta_{k+1}v_{k+1} +\cdots + \beta_{m}v_{m} \\
  & = \left(\beta_{1} -\frac{a_{1}}{a_{k}}\right)v_{1} + \cdots + \left(\beta_{k-1} -\frac{a_{k-1}}{a_{k}}\right)v_{k-1} + \beta_{k+1}v_{k+1} +\cdots + \beta_{m}v_{m}, 
\end{aligned}
$$
which implies $$v \in \mathtt{span}\{v_{1}, \dots, v_{k-1}, v_{k+1}, v_{m}\} \subset \mathtt{span}\{v_{1}, \dots, v_{m}\}$$.



 **(<u>Every Spanning List Contains a Biasis</u>)**  Every spanning list in a vector space can be reduced to a basis of the vector space.

---

**<u>Proof</u>**

Let $$V = \mathtt{span}\{v_{1}, v_{2}, \dots, v_{m}\}$$ and $$B:=\{v_{1}, v_{2}, \dots, v_{m}\}$$. 

If $$v_{1} = 0$$, remove $$v_{1}$$ from $$B$$, otherwise keep $$v_{1}$$ in $$B$$.

for $$k = 2,3, \dots, m$$, if $$v_{k} \in \mathtt{span}\{v_{1}, v_{2}, \cdots, v_{k-1}\}$$, remove $$v_{k}$$ from $$B$$, otherwise keep $$B$$ unchanged.

After the removing procedure, we obtain a list of vectors $$B$$ satisifed that
$$
v_{k_{i}} \notin \mathtt{span}\{v_{k_{1}}, v_{k_{2}}, \dots, v_{k_{i-1}}\}, \forall v_{k_{i}} \in B.
$$
By the Linear Dependence Lemma, the vectors in $$B$$ are linearly independent and these vectors span $$V$$. Hence we get a basis of $$V$$.

---



