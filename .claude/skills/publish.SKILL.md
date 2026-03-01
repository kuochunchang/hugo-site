---
name: publish
description: 發布 Markdown 檔案到 Hugo 網站。使用方式：/publish <檔案路徑> [section]
arguments:
  - name: file_path
    description: 要發布的 Markdown 檔案路徑
    required: true
  - name: section
    description: Hugo section（預設 posts，可選 reports 或其他）
    required: false
---

# 發布 Markdown 到 Hugo 網站

## Step 1: 讀取檔案

1. 使用 Read 工具讀取指定的 Markdown 檔案。
2. 從第一個 `# ` 開頭的行提取標題，去掉 `# ` 前綴。
3. 如果檔案已有 Hugo frontmatter（以 `---` 開頭），保留原有 frontmatter 不重複添加。
4. 如果檔案開頭有日期行（如 `> 研究日期：2026-02-27`），提取日期作為 `date` 欄位。

## Step 2: 確認參數

使用 AskUserQuestion 確認：

1. **標題**：顯示自動提取的標題，可修改
2. **Section**：posts（預設）/ reports / 其他自訂 section
3. **標籤**：逗號分隔，可留空
4. **草稿**：是否為草稿（draft: true 不會公開）

## Step 3: 加上 frontmatter 並複製

如果檔案沒有 frontmatter：

1. **移除原始 `# 標題` 行**（避免 Hugo 渲染時標題重複）。
2. 如果標題下方有副標題或 meta 行（如 `> 研究日期：...`、`> 用途：...`），也一併移除（資訊已併入 frontmatter）。
3. 在開頭加上：

```yaml
---
title: "<標題>"
date: <提取的日期，或今天日期 YYYY-MM-DD>
draft: <true/false>
tags: [<標籤列表>]
description: "<從副標題或前幾行內容自動生成的摘要>"
---
```

將處理後的檔案寫入 Hugo 專案的 `content/<section>/` 目錄。

Hugo 專案路徑：`~/workspace/hugo-site`

## Step 4: Git push

```bash
cd ~/workspace/hugo-site
git add content/<section>/
git commit -m "publish: <標題>"
git push
```

告知使用者文章已發布，GitHub Actions 將自動建構部署。
