---
title: "文章标题"
date: 2026-09-30
excerpt: "用一两句话概括文章内容，显示在 Blog 列表中。"
tags: [机器学习, 研究笔记]
published: false
---

用一段话介绍问题背景，以及这篇文章想回答的问题。

## 背景

介绍背景、动机与必要的定义。

## 方法

行内公式：$y = f_{\theta}(x)$。

$$
\mathcal{L}(\theta) = \frac{1}{n}\sum_{i=1}^{n}\ell(f_{\theta}(x_i), y_i)
$$

### 实现

```python
def square(x):
    return x * x
```

<!-- 图片示例：将图片放在 blog/images/ 中，再取消下方注释。
<figure>
  <img src="{{ '/blog/images/example.png' | relative_url }}" alt="描述图片内容">
  <figcaption>图 1：图片说明与来源。</figcaption>
</figure>
-->

## 讨论

记录观察、局限和下一步计划。引用可以使用 Markdown 脚注。[^note]

## 参考资料

1. 作者，文章或论文标题，年份，链接。

[^note]: 在这里补充说明或文献来源。
