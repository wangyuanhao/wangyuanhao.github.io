# Blog 写作指南

文章 Markdown 文件直接放在本目录。网站导航中的 **Blog** 指向 `/blog/`，列表自动按日期倒序排列，并按年份分组。文章页参考 Lil'Log 的单栏阅读排版，包含日期、阅读时间、可折叠目录、标题锚点、数学公式和代码高亮。

Blog 页面及文章页导航中的 **Archive** 指向 `/archives/`，按年份、月份倒序归档，并显示每组的文章数量。归档与 Blog 列表使用相同的文章来源，新增或修改文章后自动更新；`published: false` 的草稿不会出现。归档模板位于 `_pages/blog-archive.html`，博客导航在 `_data/navigation.yml` 的 `blog` 部分配置。

## 新建文章

1. 复制 `_template.md` 为 `my-first-post.md`（文件名不要以 `_` 开头）。
2. 修改文件顶部的 `title`、`date`、`excerpt` 和 `tags`。
3. 完成正文后，将 `published: false` 改为 `published: true`，或删除该行。
4. 提交并推送到 GitHub，等待现有 GitHub Pages 流程构建。

最小文章格式：

```yaml
---
title: "我的第一篇文章"
date: 2026-09-30
excerpt: "文章摘要。"
tags: [机器学习]
---
```

在这段 YAML 之后直接写 Markdown 正文。文件顶部必须保留两行 `---`；布局与目录功能由 `_config.yml` 自动配置，无需逐篇指定。

默认地址为 `/blog/my-first-post.html`。如需以 `/` 结尾的地址，在文章顶部添加 `permalink: /blog/my-first-post/`。每篇文章的 permalink 必须唯一，不要使用列表地址 `/blog/`。

## 可选字段

| 字段 | 用途 |
| --- | --- |
| `byline: "作者姓名"` | 覆盖默认作者 |
| `modified: 2026-10-01` | 显示更新日期 |
| `toc: false` | 隐藏目录 |
| `math: false` | 不加载数学公式脚本 |
| `lang: en` | 设置英文文章的页面语言 |
| `published: false` | 草稿，不生成公开文章页，也不进入列表 |

`date` 统一使用不带引号的 `YYYY-MM-DD`。当前网站启用了 `future: true`，未来日期不会自动隐藏文章；草稿请明确使用 `published: false`。

正文建议从 `##` 开始分节，`###` 表示子节；目录自动识别正文的一级至三级标题。目录和中英文阅读时间估算由浏览器生成，不影响正文的静态输出。数学公式由 MathJax 渲染，需要网络加载其 CDN 脚本。代码块在三个反引号后标注语言（如 `python`），即可启用语法高亮。

图片建议存放在 `blog/images/`，在 Markdown 中使用 `![说明]({{ '/blog/images/文件名.png' | relative_url }})`，这样也能兼容带站点子路径的部署。带图注的写法见 `_template.md`。

`welcome.md` 是可替换或删除的示例文章；`_template.md` 和本指南不会被发布为博客文章。原有 `_posts/` 下的主题示例不会混入新 Blog 列表。

## 本地预览

```sh
bundle install
bundle exec jekyll serve
```

打开 `http://localhost:4000/blog/`。修改 `_config.yml` 后需重启服务。
