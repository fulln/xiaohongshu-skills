# Xiaohongshu Skills Consolidation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Consolidate the currently installed Xiaohongshu skills back into `/Users/fulln/opensource/xiaohongshu-skills`, align docs and behavior around copy-ready and long-article workflows, add style guidance at the right layer, and switch the repo to the user's personal public GitHub remote.

**Architecture:** Keep the existing 5-skill structure and current CLI architecture intact. Update the source repo to become the single truth by synchronizing root routing docs, per-skill boundaries, copy-ready guidance, and style/verification rules; only add code or tests where the source repo is materially behind the installed behavior.

**Tech Stack:** Markdown skill definitions, Python CLI (`scripts/cli.py`), pytest, git, GitHub remote configuration

---

## File Map

### Existing files to modify
- `SKILL.md` — top-level routing, global constraints, copy-ready/source-of-truth rules, Bridge explanation
- `README.md` — public-facing install/use docs, CLI surface, architecture overview, copy-ready guidance
- `CLAUDE.md` — maintainer guidance to prevent future drift
- `ARCHITECTURE.md` — align architecture docs with Bridge, multi-account, long-article, copy-ready workflows
- `skills/xhs-auth/SKILL.md` — merge installed multi-account and login rules
- `skills/xhs-publish/SKILL.md` — merge copy-ready publish flow, long-article flow, publish guardrails, style gate
- `skills/xhs-explore/SKILL.md` — align search/detail constraints and result handling
- `skills/xhs-interact/SKILL.md` — align confirmation/frequency/reply guidance
- `skills/xhs-content-ops/SKILL.md` — align orchestration flows, copy-ready publishing path, style-writing guidance
- `scripts/cli.py` — only if command surface differs from installed version

### Existing files that may need to be created or modified if source repo lacks installed capabilities
- `scripts/copy_ready_parser.py` — parser for `post-xx-copy-ready.md`
- `tests/test_copy_ready_parser.py` — parser tests
- `tests/test_cli_copy_ready_publish.py` — CLI parser/behavior tests for copy-ready commands

### Existing files to inspect during implementation
- `~/.claude/skills/xiaohongshu-skills/SKILL.md`
- `~/.claude/skills/xiaohongshu-skills/skills/xhs-auth/SKILL.md`
- `~/.claude/skills/xiaohongshu-skills/skills/xhs-publish/SKILL.md`
- `~/.claude/skills/xiaohongshu-skills/skills/xhs-explore/SKILL.md`
- `~/.claude/skills/xiaohongshu-skills/skills/xhs-interact/SKILL.md`
- `~/.claude/skills/xiaohongshu-skills/skills/xhs-content-ops/SKILL.md`
- `~/.claude/skills/xiaohongshu-skills/scripts/cli.py`
- `~/.claude/skills/xiaohongshu-skills/scripts/copy_ready_parser.py`
- `~/.claude/skills/xiaohongshu-skills/tests/test_copy_ready_parser.py`
- `docs/superpowers/specs/2026-04-10-xiaohongshu-skills-consolidation-design.md`

---

### Task 1: Diff installed and source skill surfaces

**Files:**
- Modify: `SKILL.md`
- Modify: `README.md`
- Modify: `skills/xhs-auth/SKILL.md`
- Modify: `skills/xhs-publish/SKILL.md`
- Modify: `skills/xhs-explore/SKILL.md`
- Modify: `skills/xhs-interact/SKILL.md`
- Modify: `skills/xhs-content-ops/SKILL.md`
- Modify: `scripts/cli.py`

- [ ] **Step 1: Capture the installed-vs-source command and rule differences**

Read and compare:

```text
Installed:
- ~/.claude/skills/xiaohongshu-skills/SKILL.md
- ~/.claude/skills/xiaohongshu-skills/skills/xhs-auth/SKILL.md
- ~/.claude/skills/xiaohongshu-skills/skills/xhs-publish/SKILL.md
- ~/.claude/skills/xiaohongshu-skills/skills/xhs-explore/SKILL.md
- ~/.claude/skills/xiaohongshu-skills/skills/xhs-interact/SKILL.md
- ~/.claude/skills/xiaohongshu-skills/skills/xhs-content-ops/SKILL.md
- ~/.claude/skills/xiaohongshu-skills/scripts/cli.py

Source repo:
- /Users/fulln/opensource/xiaohongshu-skills/SKILL.md
- /Users/fulln/opensource/xiaohongshu-skills/skills/xhs-auth/SKILL.md
- /Users/fulln/opensource/xiaohongshu-skills/skills/xhs-publish/SKILL.md
- /Users/fulln/opensource/xiaohongshu-skills/skills/xhs-explore/SKILL.md
- /Users/fulln/opensource/xiaohongshu-skills/skills/xhs-interact/SKILL.md
- /Users/fulln/opensource/xiaohongshu-skills/skills/xhs-content-ops/SKILL.md
- /Users/fulln/opensource/xiaohongshu-skills/scripts/cli.py
```

Produce a checklist in your scratchpad with at least these categories:
- command surface missing in source repo
- installed rules missing in source repo
- source-only rules that should be preserved
- docs that mention outdated behavior

- [ ] **Step 2: Verify whether copy-ready parser code exists in source repo**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
root = Path('/Users/fulln/opensource/xiaohongshu-skills')
for rel in [
    'scripts/copy_ready_parser.py',
    'tests/test_copy_ready_parser.py',
    'tests/test_cli_copy_ready_publish.py',
]:
    p = root / rel
    print(rel, 'EXISTS' if p.exists() else 'MISSING')
PY
```

Expected before implementation:
- likely at least one of these files is `MISSING`

- [ ] **Step 3: Verify current source CLI command surface before changing anything**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
import re
text = Path('/Users/fulln/opensource/xiaohongshu-skills/scripts/cli.py').read_text(encoding='utf-8')
for name in ['parse-copy-ready', 'fill-publish-copy-ready', 'publish-copy-ready', 'list-accounts', 'add-account', 'set-default-account']:
    print(name, 'YES' if name in text else 'NO')
PY
```

Expected:
- commands missing from source repo should print `NO`

- [ ] **Step 4: Commit nothing yet**

Do not edit files in this task. This task is complete only when the diff is understood well enough to implement without guessing.

---

### Task 2: Align the top-level repo docs and router

**Files:**
- Modify: `SKILL.md`
- Modify: `README.md`
- Modify: `CLAUDE.md`
- Modify: `ARCHITECTURE.md`

- [ ] **Step 1: Write a failing documentation checklist**

Create a local checklist in your scratchpad with these required outcomes:
- root router mentions copy-ready as source-of-truth for series publishing
- root router explains Bridge mode accurately
- README install/use docs match current local install model
- README examples include copy-ready publishing and local-image-only rule
- CLAUDE.md documents drift-prevention and source-repo-as-truth
- ARCHITECTURE.md mentions Bridge, long-article path, multi-account, and copy-ready path

This checklist is your doc “test”.

- [ ] **Step 2: Update `SKILL.md` minimally but completely**

Edit `SKILL.md` so it includes:

```markdown
- 对于已整理好的系列发帖资产，发布阶段应只接受单一 copy-ready Markdown 文件作为输入真源。
```

and route descriptions equivalent to:

```markdown
1. 认证相关 → xhs-auth
2. 内容发布 → xhs-publish
3. 搜索发现 → xhs-explore
4. 社交互动 → xhs-interact
5. 复合运营 → xhs-content-ops
```

Also ensure it explains Bridge-mode/local-browser execution in a short section.

- [ ] **Step 3: Update `README.md` to match real capabilities**

Add or update sections so README clearly documents:

```markdown
| **xhs-auth** | 认证管理 | 登录检查、扫码登录、多账号切换 |
| **xhs-publish** | 内容发布 | 图文 / 视频 / 长文发布、定时发布、分步预览 |
| **xhs-content-ops** | 复合运营 | 竞品分析、热点追踪、批量互动、内容创作 |
```

and include usage examples for:
- `fill-publish` → `click-publish`
- `save-draft`
- `long-article`
- `publish-copy-ready` or `fill-publish-copy-ready` if implemented in the repo

Also add a sentence equivalent to:

```markdown
> 图文发布只接受用户已准备好的本地图片绝对路径，不负责生成、提取或下载图片。
```

- [ ] **Step 4: Update `CLAUDE.md` for maintainers**

Add explicit maintainer rules covering:
- source repo is the single truth
- installed-skill-only hotfixes must be synced back immediately
- `xhs-content-ops` owns writing/orchestration guidance
- `xhs-publish` owns publish execution and pre-publish verification
- `copy-ready` is the final publish source for series assets

- [ ] **Step 5: Update `ARCHITECTURE.md` if current contents omit real workflows**

Ensure it documents:
- CLI → bridge_server → extension → browser → Xiaohongshu
- multi-account separation if present in source code/docs
- long-article branch and template selection flow
- copy-ready flow as a publishing path

- [ ] **Step 6: Verify the documentation checklist now passes**

Run:

```bash
grep -n "copy-ready\|Bridge\|长文\|多账号\|本地图片绝对路径" \
  /Users/fulln/opensource/xiaohongshu-skills/SKILL.md \
  /Users/fulln/opensource/xiaohongshu-skills/README.md \
  /Users/fulln/opensource/xiaohongshu-skills/CLAUDE.md \
  /Users/fulln/opensource/xiaohongshu-skills/ARCHITECTURE.md
```

Expected:
- hits in the appropriate files for all required concepts

- [ ] **Step 7: Commit doc/router alignment**

```bash
git -C /Users/fulln/opensource/xiaohongshu-skills add \
  SKILL.md README.md CLAUDE.md ARCHITECTURE.md
git -C /Users/fulln/opensource/xiaohongshu-skills commit -m "docs: align xiaohongshu skill docs with installed workflows"
```

---

### Task 3: Align per-skill boundaries and writing rules

**Files:**
- Modify: `skills/xhs-auth/SKILL.md`
- Modify: `skills/xhs-publish/SKILL.md`
- Modify: `skills/xhs-explore/SKILL.md`
- Modify: `skills/xhs-interact/SKILL.md`
- Modify: `skills/xhs-content-ops/SKILL.md`

- [ ] **Step 1: Write the failing rule checklist**

Before editing, create a checklist that each skill must satisfy:
- `xhs-auth` includes multi-account management if installed version has it
- `xhs-publish` includes copy-ready publishing and final-source rule
- `xhs-publish` includes save-draft requirement when user cancels
- `xhs-publish` includes a pre-publish style gate
- `xhs-content-ops` includes writing guidance for trustworthy/specific/human copy
- `xhs-explore` and `xhs-interact` use `feed_id` + `xsec_token` consistently

- [ ] **Step 2: Update `skills/xhs-auth/SKILL.md`**

Merge in the installed behavior for account management. Ensure the skill documents commands equivalent to:

```markdown
| `add-account --name` | 添加命名账号（自动分配端口） |
| `list-accounts` | 列出所有命名账号及端口 |
| `remove-account --name` | 删除命名账号 |
| `set-default-account --name` | 设置默认账号 |
```

Also add the account-selection pre-step for login-related operations.

- [ ] **Step 3: Update `skills/xhs-publish/SKILL.md`**

Add installed copy-ready workflow and explicit rule:

```markdown
- 对于已经整理成系列发布资产的内容，最终发布只接受 `post-xx-copy-ready.md`。
- final/xx-最终发帖版.md 不是最终发布真源，不能直接当作发布输入。
```

Also add the `parse-copy-ready`, `fill-publish-copy-ready`, `publish-copy-ready`, and `save-draft` command references if the CLI will support them after Task 4.

Add a pre-publish style gate section that checks:
- 标题是否只有概念没有判断
- 首段是否太泛
- 是否缺少具体对象/动作/场景
- 结尾是否模板化
- 首评是否自然承接

- [ ] **Step 4: Update `skills/xhs-content-ops/SKILL.md`**

Add writing rules for the new style guidance. Include bullets equivalent to:

```markdown
- 先判断，后展开
- 抽象观点必须落到真对象 / 真动作 / 真场景
- 可用第一人称状态变化，但不要写成日记流
- 避免官腔、课程腔、统一模板收尾
- 不照搬别人的黑话宇宙或命名体系
```

Also update the publishing path to use copy-ready when dealing with series assets.

- [ ] **Step 5: Update `xhs-explore` and `xhs-interact` only where source still lags installed guidance**

Preserve good source-only improvements (for example result-usage advice) while ensuring consistency with installed boundaries.

- [ ] **Step 6: Verify the rule checklist now passes**

Run:

```bash
grep -n "copy-ready\|save-draft\|多账号\|先判断\|真对象\|feed_id\|xsec_token" \
  /Users/fulln/opensource/xiaohongshu-skills/skills/xhs-auth/SKILL.md \
  /Users/fulln/opensource/xiaohongshu-skills/skills/xhs-publish/SKILL.md \
  /Users/fulln/opensource/xiaohongshu-skills/skills/xhs-explore/SKILL.md \
  /Users/fulln/opensource/xiaohongshu-skills/skills/xhs-interact/SKILL.md \
  /Users/fulln/opensource/xiaohongshu-skills/skills/xhs-content-ops/SKILL.md
```

Expected:
- all required keywords appear in the right files

- [ ] **Step 7: Commit per-skill alignment**

```bash
git -C /Users/fulln/opensource/xiaohongshu-skills add skills/xhs-auth/SKILL.md \
  skills/xhs-publish/SKILL.md \
  skills/xhs-explore/SKILL.md \
  skills/xhs-interact/SKILL.md \
  skills/xhs-content-ops/SKILL.md
git -C /Users/fulln/opensource/xiaohongshu-skills commit -m "docs: consolidate xiaohongshu skill boundaries and writing rules"
```

---

### Task 4: Bring source CLI and parser up to installed copy-ready behavior

**Files:**
- Create or Modify: `scripts/copy_ready_parser.py`
- Modify: `scripts/cli.py`
- Create: `tests/test_copy_ready_parser.py`
- Create: `tests/test_cli_copy_ready_publish.py`

- [ ] **Step 1: Write the failing parser test**

Create `tests/test_copy_ready_parser.py` with at least this coverage:

```python
from pathlib import Path
import pytest
from copy_ready_parser import load_copy_ready_payload

def test_load_copy_ready_payload_reads_required_sections(tmp_path: Path) -> None:
    path = tmp_path / "post-03-copy-ready.md"
    path.write_text(
        """# Post 03｜可直接复制发帖版

## 发帖标题

真正的 AI Coding 高手，最后都在搭运行壳

## 正文（可直接复制）

第一段。

第二段。

## 封面文案

高手不是会更多命令，而是在搭一套运行壳

## 标签

#AICoding #ClaudeCode #AI编程

## 首评（建议发布后立刻发）

你现在最缺的，是 skill、hooks，还是验证体系？
""",
        encoding="utf-8",
    )

    payload = load_copy_ready_payload(path)
    assert payload.title == "真正的 AI Coding 高手，最后都在搭运行壳"
    assert payload.tags == ["AICoding", "ClaudeCode", "AI编程"]
```

Also add tests for missing tags and non-copy-ready filenames.

- [ ] **Step 2: Run the parser test and verify it fails if the file is missing**

Run:

```bash
cd /Users/fulln/opensource/xiaohongshu-skills && uv run pytest tests/test_copy_ready_parser.py -q
```

Expected before implementation:
- FAIL with import/file-not-found errors if parser does not yet exist

- [ ] **Step 3: Implement `scripts/copy_ready_parser.py` minimally**

Use the installed implementation shape:

```python
_REQUIRED_SECTIONS = {
    "发帖标题": "title",
    "正文（可直接复制）": "content",
    "封面文案": "cover_text",
    "标签": "tags",
    "首评（建议发布后立刻发）": "first_comment",
}
```

and return a dataclass `CopyReadyPayload` with fields:
- `path`
- `title`
- `content`
- `cover_text`
- `tags`
- `first_comment`

Do not add speculative fields.

- [ ] **Step 4: Run the parser tests and verify they pass**

Run:

```bash
cd /Users/fulln/opensource/xiaohongshu-skills && uv run pytest tests/test_copy_ready_parser.py -q
```

Expected:
- PASS

- [ ] **Step 5: Write the failing CLI parser test**

Create `tests/test_cli_copy_ready_publish.py` with coverage for command registration like:

```python
from cli import build_parser

def test_copy_ready_commands_are_registered() -> None:
    parser = build_parser()
    args = parser.parse_args([
        "parse-copy-ready",
        "--copy-ready-file",
        "/tmp/post-03-copy-ready.md",
    ])
    assert args.command == "parse-copy-ready"
```

Also cover `fill-publish-copy-ready` and `publish-copy-ready` command parsing.

- [ ] **Step 6: Run the CLI parser test and verify it fails before command registration**

Run:

```bash
cd /Users/fulln/opensource/xiaohongshu-skills && uv run pytest tests/test_cli_copy_ready_publish.py -q
```

Expected before implementation:
- FAIL because commands are not registered

- [ ] **Step 7: Implement the minimal CLI support**

In `scripts/cli.py`:
- import the parser module
- add `cmd_parse_copy_ready`
- add `cmd_fill_publish_copy_ready`
- add `cmd_publish_copy_ready`
- register these subcommands
- preserve all existing source-repo behavior
- if installed version includes account commands missing in source repo, port those too, including parser registration

Keep the implementation thin: parse copy-ready → map to existing publish/fill-publish behavior.

- [ ] **Step 8: Run focused tests and verify they pass**

Run:

```bash
cd /Users/fulln/opensource/xiaohongshu-skills && uv run pytest tests/test_copy_ready_parser.py tests/test_cli_copy_ready_publish.py -q
```

Expected:
- PASS

- [ ] **Step 9: Run a broader regression pass for touched areas**

Run:

```bash
cd /Users/fulln/opensource/xiaohongshu-skills && uv run pytest -q
```

Expected:
- all tests pass, or if pre-existing failures exist, identify them explicitly before proceeding

- [ ] **Step 10: Commit CLI/parser alignment**

```bash
git -C /Users/fulln/opensource/xiaohongshu-skills add \
  scripts/cli.py \
  scripts/copy_ready_parser.py \
  tests/test_copy_ready_parser.py \
  tests/test_cli_copy_ready_publish.py
git -C /Users/fulln/opensource/xiaohongshu-skills commit -m "feat: add copy-ready publishing support"
```

---

### Task 5: Switch the repository to the user's public GitHub remote

**Files:**
- Modify: `.git/config` (via git remote commands)

- [ ] **Step 1: Inspect current remote before changing it**

Run:

```bash
git -C /Users/fulln/opensource/xiaohongshu-skills remote -v
```

Expected before change:
- `origin` points to `autoclaw-cc/xiaohongshu-skills.git`

- [ ] **Step 2: Confirm the exact target URL from the user or known repo configuration**

Use the exact personal public repo URL the user wants. Do not guess. If it has not yet been provided explicitly, stop and ask.

Expected:
- one exact `https://github.com/<user>/<repo>.git` URL

- [ ] **Step 3: Update `origin` to the user's personal public repo**

Run:

```bash
git -C /Users/fulln/opensource/xiaohongshu-skills remote set-url origin "https://github.com/<user>/<repo>.git"
```

- [ ] **Step 4: Verify the remote change**

Run:

```bash
git -C /Users/fulln/opensource/xiaohongshu-skills remote -v
```

Expected:
- `origin` fetch and push URLs both point to the user's personal repo

- [ ] **Step 5: Push the branch**

Run:

```bash
git -C /Users/fulln/opensource/xiaohongshu-skills push -u origin main
```

Expected:
- branch pushed successfully to the user's personal public repo

- [ ] **Step 6: Capture the resulting repo URL for reporting**

Report both:
- remote URL
- pushed branch name

---

### Task 6: Final verification and handoff

**Files:**
- Modify: none necessarily

- [ ] **Step 1: Verify the working tree is clean**

Run:

```bash
git -C /Users/fulln/opensource/xiaohongshu-skills status --short
```

Expected:
- no output

- [ ] **Step 2: Verify the latest commit sequence reflects the consolidation logically**

Run:

```bash
git -C /Users/fulln/opensource/xiaohongshu-skills log --oneline -5
```

Expected:
- recent commits clearly reflect docs alignment, per-skill consolidation, and copy-ready support (if implemented)

- [ ] **Step 3: Summarize the completed consolidation in concrete terms**

Your handoff summary must explicitly state:
- which files changed
- whether copy-ready CLI support was added or already existed
- whether style guidance now lives in `xhs-content-ops`
- whether publish verification/style gate now lives in `xhs-publish`
- what the new `origin` URL is

- [ ] **Step 4: Do not claim success without evidence**

Before calling the work complete, ensure you have actual outputs for:
- docs grep verification
- focused pytest verification
- full pytest verification or explicit explanation of any pre-existing failures
- `git remote -v`
- `git status --short`

---

## Self-Review Notes

- Spec coverage: this plan covers docs consolidation, per-skill boundaries, copy-ready parser/CLI support, style guidance placement, and remote switching.
- Placeholder scan: the plan includes exact file paths, commands, expected outputs, and concrete edit targets.
- Type consistency: `CopyReadyPayload`, copy-ready section names, and CLI command names match the installed implementation described in the spec and current installed files.
