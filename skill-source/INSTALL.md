# Installing this skill

Same Agent Skills open-standard format as its sister skills (`minimax-h3-director-prompt`, `minimax-h3-instagram-style-director`, `minimax-h3-commercial-ad-director`): a folder with `SKILL.md` at the root (`name`/`description` frontmatter, plain-prose instructions) plus `references/` and `scripts/` folders. No hooks, no subagent frontmatter, no Claude-only extensions — works unmodified across the tools below.

The two validator scripts in `scripts/` are standard-library-only Python 3 (no `pip install` needed) — they're optional helpers invoked with `python3`, not a runtime dependency of the skill itself.

## Claude Code / Claude (Cowork)

- **Personal:** `~/.claude/skills/minimax-h3-reference-video-remix/`
- **Project-level:** `.claude/skills/minimax-h3-reference-video-remix/`
- In Cowork, open the packaged `.skill` file directly and install with the **Save skill** button.

## Codex CLI

- **Personal:** `~/.codex/skills/minimax-h3-reference-video-remix/`
- **Project-level:** `.codex/skills/minimax-h3-reference-video-remix/`
- **Shared Agent-Skills-standard location** (some Codex builds, Cursor, Gemini CLI): `.agents/skills/minimax-h3-reference-video-remix/`

If you have the `.skill` zip:

```bash
mkdir -p ~/.codex/skills
unzip minimax-h3-reference-video-remix.skill -d ~/.codex/skills/
```

Invoke explicitly with `$minimax-h3-reference-video-remix <request>`, browse via `/skills`, or let it auto-trigger on a matching request. If it doesn't load, check your Codex build's current skills directory (`codex --help`) — this has moved before.

## Requirements for actually analyzing video

This skill's extraction steps call `ffmpeg`/`ffprobe` on the reference video file (frame sampling, scene-change detection, dense re-sampling, cropping for OCR). These need to be available in whatever shell/sandbox the agent is running in, and the agent needs file access to the actual video. Without either, the skill should fall back to `prompt_only`/`transcript_only` evidence mode and say so explicitly — never write a deconstruction that implies frames were viewed when they weren't.

## What's inside

```
minimax-h3-reference-video-remix/
├── SKILL.md
├── INSTALL.md
├── references/
│   ├── VIDEO_PROMPT_WRITING_GUIDE_base_en.md   — MiniMax H3 field syntax (T2VA/I2VA/FL2VA/L2VA)
│   ├── VIDEO_PROMPT_WRITING_GUIDE_ref_en.md     — full-reference-mode field syntax
│   ├── model_facts.md                — model limits + tested prompting behavior
│   ├── deconstruction_schema.md      — ffmpeg ingestion steps, shot-segmentation rules, table + JSON schema
│   ├── layer_contract.md             — 12-layer preserve/adapt/replace/omit system + presets
│   ├── ocr_text_precision.md         — Chinese-inclusive on-screen text accuracy protocol
│   ├── action_timeline_methodology.md — 0.1s single-person action extraction (mirrors sister skills' planning method)
│   ├── certification_checklist.md    — pre-flight checklist, 7 stages
│   ├── worked_example.md             — one full pass, explicitly labeled hypothetical
│   └── external_references.md        — outside sources consulted (background, not new syntax rules)
└── scripts/
    ├── validate_deconstruction.py    — validates a deconstruction JSON's structure
    └── validate_remix.py             — validates a finished prompt against its remix-contract.json
```

## Attribution

The work-mode taxonomy, layer-contract concept, shot-deconstruction schema, and both validator scripts are adapted from the open-source [`penposs/remix-reference-video-prompt`](https://github.com/penposs/remix-reference-video-prompt) skill, retargeted onto MiniMax H3's own prompt syntax. See `SKILL.md` and the header comments in each adapted file for what was reused vs. rewritten.
