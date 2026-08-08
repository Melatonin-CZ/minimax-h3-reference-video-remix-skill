# MiniMax H3 Reference Video Remix Skill

English | 简体中文

## English

### Overview
This skill deconstructs reference videos and builds MiniMax H3 (Hailuo 3.0) remix prompts from evidence-first extraction.
It is optimized for shot-level analysis, 0.1-second action timelines, OCR-sensitive text capture, and layer-by-layer preserve/adapt/replace policies.

### Highlights
- Supports both deconstruction-only and remix-output workflows
- Uses official MiniMax H3 field syntax (base + full-reference guides)
- Includes OCR-precision protocol (with Chinese text accuracy emphasis)
- Includes optional Python validators for deconstruction/remix JSON checks
- Runtime-agnostic Agent Skill format (Claude Code/Cowork + Codex CLI)

### Install
Main install guide: `skill-source/INSTALL.md`

Packaged file:
- `minimax-h3-reference-video-remix.skill`

### Requirements
- `ffmpeg` and `ffprobe` available in your runtime environment for real video extraction
- Python 3 for optional validators in `skill-source/scripts/`

### Main Docs
- Core workflow: `skill-source/SKILL.md`
- References: `skill-source/references/`
- Validation scripts: `skill-source/scripts/`

### Typical Use
Use this skill when you want to analyze an existing video (shots, motion, text, audio) and then recreate or remix it with controlled layer-level changes.

## 简体中文

### 概述
这个 skill 用于对参考视频进行证据优先的拆解，并生成 MiniMax H3（Hailuo 3.0）重制提示词。
它重点支持镜头级分析、0.1 秒动作时间线、OCR 文本精读，以及分层 preserve/adapt/replace 策略。

### 亮点
- 同时支持“仅拆解”和“拆解后重制”两类工作流
- 使用官方 MiniMax H3 字段语法（基础模式 + 全参考模式）
- 提供 OCR 精度流程，特别强调中文画面文字准确性
- 内置可选 Python 校验脚本，用于 deconstruction/remix JSON 检查
- 采用跨运行时 Agent Skill 标准（兼容 Claude Code/Cowork 与 Codex CLI）

### 安装
安装说明见：`skill-source/INSTALL.md`

打包文件：
- `minimax-h3-reference-video-remix.skill`

### 运行要求
- 真实视频拆解需在运行环境可用 `ffmpeg` / `ffprobe`
- `skill-source/scripts/` 下可选校验脚本需要 Python 3

### 主要文档
- 核心流程：`skill-source/SKILL.md`
- 参考资料：`skill-source/references/`
- 校验脚本：`skill-source/scripts/`

### 适用场景
当你需要先精确拆解现有视频（镜头、动作、文字、音频），再按层控制“保留/改写/替换”生成可执行重制提示词时，使用此 skill。
