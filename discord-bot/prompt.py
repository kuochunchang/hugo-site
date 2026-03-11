from datetime import date

from tags import get_existing_tags


# ── 共用片段 ──────────────────────────────────────────────

_RESEARCH_STEPS = """\
### 第一步：深度研究

1. 使用 WebSearch 從至少 3-5 個不同角度搜尋最新資料
2. 使用 WebFetch 閱讀 5-10 個最重要的參考來源全文
3. 交叉驗證不同來源的資訊"""

_ARTICLE_STRUCTURE = """\
### 第二步：撰寫文章

寫一篇結構完整的繁體中文 Markdown 技術文章：

1. 用 `# ` 開頭寫標題
2. 第二行寫 `> 研究日期：{today}`
3. 包含以下結構：
   - 背景與概述
   - 核心內容（技術細節、架構分析等）
   - 比較分析（如適用）
   - 實際應用場景
   - 結論與展望
4. 深度要求：
   - 不要只是重述來源資料的內容，要加入基於來源事實的分析
   - 指出不同來源之間的矛盾或爭議
   - 用自己的框架重新組織資訊，不要沿用原始來源的章節順序和敘事結構
5. 引用參考來源（附上連結）
6. 技術名詞保留英文原文"""

_WRITING_STYLE_RULES = """\
**寫作風格要求（嚴格遵守）：**
- 標題要簡潔有力，禁止使用「深度研究」「深度探討」「深度解析」「全面解析」「完整指南」等空泛修飾
- 禁止使用破折號（——）作為句子開頭或強調手段
- 禁止使用 emoji 符號
- 禁止使用「值得注意的是」「總而言之」「不僅...更...」「從...到...」「至關重要」「不可或缺」「令人印象深刻」「令人震驚」「令業界震驚」「前所未有」「驚人的」「驚艷」等誇張或 AI 常見套話
- 不要在每段開頭用問句引導（如「那麼，XXX 到底是什麼？」）
- 語氣直接、平實，像資深工程師寫的技術筆記，不是行銷文案
- 用具體的技術細節和例子說明觀點，避免空泛的形容詞堆砌
- 段落之間自然銜接，不需要每段都有「總結性」開頭或結尾"""

def _hugo_publish_steps(today: str) -> str:
    tags = get_existing_tags()
    tag_list = ", ".join(tags)
    return f"""\
### 發布到 Hugo

1. 從標題產生一個英文 slug（用小寫和連字號，例如 `mcp-protocol-analysis-2026`）
2. 建立 Page Bundle 目錄：`content/posts/<slug>/`
3. 將文章存為 `content/posts/<slug>/index.md`，加上 Hugo front matter：

```yaml
---
title: "<標題>"
date: {today}
draft: false
tags: [<選擇 3-5 個標籤>]
summary: "<一句話摘要>"
---
```

**標籤規範：**
- 統一使用英文
- 優先從以下已有標籤中選擇：{tag_list}
- 只在已有標籤都無法描述文章內容時才新增標籤
- 新增標籤時，專有名詞保持原始大小寫（如 Claude Code），通用詞用 Title Case（如 Software Engineering）
- 不要使用過於籠統的標籤（如單獨用 "AI"）

注意：front matter 中不要包含原始的 `# 標題` 行和 `> 研究日期` 行。"""

_AUDIO_STEPS = """\
### 生成語音

1. 將文章分段（按 `## ` 二級標題切分）
2. 對每個段落，改寫為適合語音朗讀的自然口語文字：
   - 使用繁體中文
   - 語氣自然流暢，像在跟聽眾說話
   - 技術名詞保留原文但用口語解釋
   - 表格改為口語描述
   - 程式碼改為描述功能
   - 連結只保留描述文字
   - 不加入原文沒有的資訊
   - 不使用 Markdown 語法
3. 合併：
   - 直接從文章內容開始，不要加「以下是...的語音版本」之類的開場白
   - 段落間加空行
   - 結尾不要加「感謝收聽」之類的套話，自然結束即可
4. 存為 `content/posts/<slug>/audio.txt`
5. 用 edge-tts 生成音檔：
   ```bash
   edge-tts --voice "{voice}" --file "content/posts/<slug>/audio.txt" --write-media "/tmp/<slug>-raw.mp3"
   ```
6. 用 ffmpeg 壓縮：
   ```bash
   ffmpeg -y -i "/tmp/<slug>-raw.mp3" -ac 1 -ab 64k "content/posts/<slug>/audio.mp3"
   ```
7. 清理暫存檔：`rm -f /tmp/<slug>-raw.mp3`
8. 在 front matter `---` 結束後插入播放器：
   ```html
   <audio controls preload="none" style="width:100%; margin: 1rem 0;">
     <source src="audio.mp3" type="audio/mpeg">
     你的瀏覽器不支援音頻播放。
   </audio>
   ```"""

_GIT_PUSH_STEPS = """\
### Git Push

```bash
cd ~/workspace/hugo-site
git add content/posts/<slug>/
git commit -m "feat: add research article - <標題>"
git push
```"""

_RESULT_OUTPUT_STEPS = """\
### 輸出結果

在所有步驟完成後，最後一行輸出（Bot 會解析這一行）：

```
RESULT::TITLE=<文章標題>::SLUG=<slug>::STATUS=SUCCESS
```

如果任何步驟失敗，輸出：

```
RESULT::STATUS=FAILED::REASON=<失敗原因>
```"""


# ── Prompt builders ───────────────────────────────────────

def build_research_prompt(topic: str, voice: str) -> str:
    """完整的單進程研究 prompt（研究 → 寫文 → Hugo → 語音 → git push）。"""
    today = date.today().isoformat()
    return f"""你是一位專業的技術研究員和繁體中文技術寫作者。

## 任務

對以下主題進行深度研究，產出一篇完整的繁體中文技術文章，並生成語音版本。

### 研究主題
{topic}

## 執行步驟

{_RESEARCH_STEPS}

{_ARTICLE_STRUCTURE.format(today=today)}

{_WRITING_STYLE_RULES}

### 第三步：{_hugo_publish_steps(today).removeprefix("### ")}

### 第四步：{_AUDIO_STEPS.format(voice=voice).removeprefix("### ")}

### 第五步：{_GIT_PUSH_STEPS.removeprefix("### ")}

### 第六步：{_RESULT_OUTPUT_STEPS.removeprefix("### ")}
"""


def build_draft_prompt(topic: str, output_path: str) -> str:
    """草稿 prompt：只做研究 + 寫文，輸出到指定路徑。"""
    today = date.today().isoformat()
    return f"""你是一位專業的技術研究員和繁體中文技術寫作者。

## 任務

對以下主題進行深度研究，產出一篇完整的繁體中文 Markdown 技術文章草稿。

### 研究主題
{topic}

## 執行步驟

{_RESEARCH_STEPS}

{_ARTICLE_STRUCTURE.format(today=today)}

{_WRITING_STYLE_RULES}

### 第三步：儲存草稿

將完成的文章（含 `# 標題` 和 `> 研究日期：{today}` 開頭）存入以下路徑：

```
{output_path}
```

### 第四步：輸出結果

完成後，最後一行輸出：

```
RESULT::STATUS=SUCCESS
```

如果任何步驟失敗，輸出：

```
RESULT::STATUS=FAILED::REASON=<失敗原因>
```
"""


def build_final_prompt(topic: str, draft_paths: list[str]) -> str:
    """合併發布 prompt：合併/潤飾草稿 → Hugo 發布（不含語音和 git push）。"""
    today = date.today().isoformat()

    if len(draft_paths) == 2:
        merge_instructions = f"""## 任務

你有兩份獨立研究的草稿，主題是：{topic}

請合併這兩份草稿為一篇更完整、更有深度的繁體中文技術文章。

### 草稿路徑
- 草稿 A：`{draft_paths[0]}`
- 草稿 B：`{draft_paths[1]}`

### 合併策略

1. 先閱讀兩份草稿全文
2. 整合兩者的觀點、資料和參考來源，去除重複內容
3. 取各自的獨特見解和細節，組成更完整的文章
4. 保持統一的文章結構和行文風格
5. 確保引用來源不重複、不遺漏"""
    else:
        merge_instructions = f"""## 任務

你有一份研究草稿，主題是：{topic}

請潤飾這份草稿，使其更完整流暢。

### 草稿路徑
- 草稿：`{draft_paths[0]}`

### 潤飾策略

1. 閱讀草稿全文
2. 修正任何文字錯誤或不通順的地方
3. 確保結構完整、邏輯清晰"""

    return f"""你是一位專業的繁體中文技術寫作者。

{merge_instructions}

{_WRITING_STYLE_RULES}

## 發布步驟

### 第一步：{_hugo_publish_steps(today).removeprefix("### ")}

### 第二步：{_RESULT_OUTPUT_STEPS.removeprefix("### ")}
"""
