---
name: minimax-h3-reference-video-remix
description: Analyze a reference video — especially a single person's action/gesture/dance — into a structured deconstruction (shots, camera, actions timed to 0.1s, on-screen text with accurate Chinese OCR, posters/captions, transitions, audio), then produce a MiniMax H3 (Hailuo 3.0) prompt that keeps, adapts, or replaces each layer, in the field syntax from VIDEO_PROMPT_WRITING_GUIDE_base_en.md / _ref_en.md. Use to deconstruct, break down, analyze, or reverse-engineer a video; extract a prompt from a video; remix or recut a reference video with a new subject/product/text; keep the camera/timing/choreography but swap who or what is in it; or precisely transcribe on-screen text/posters, especially Chinese. Trigger even without "MiniMax" or "H3" named — "break this video down shot by shot," "recreate this dance with my character," "read the text on that poster" all qualify.
---

# MiniMax H3 Reference-Video Remix & Deconstruction

Turn an existing reference video into either (a) a structured, accurate deconstruction of what's actually in it, or (b) a new MiniMax H3 prompt that reuses some of its layers (camera, timing, choreography, transitions...) while changing others (subject, product, text, audio style...), or both. The distinguishing discipline of this skill, versus writing a prompt from scratch, is **evidence-first extraction**: nothing gets described as coming from the video unless it was actually watched, and nothing illegible — especially Chinese on-screen text — gets smoothed into a confident-sounding guess.

Adapted from the open-source [`penposs/remix-reference-video-prompt`](https://github.com/penposs/remix-reference-video-prompt) skill (work-mode taxonomy, the layer-contract system, the shot-deconstruction schema, and both validator scripts are ported from it — see file headers for exactly what was reused vs. rewritten). This skill retargets that system onto MiniMax H3's actual output syntax, adds practical `ffmpeg`-based video-ingestion steps, adds a dedicated Chinese-inclusive OCR precision protocol, and adds a 0.1s single-person-action extraction methodology that mirrors and interoperates with this project's sister skills (`minimax-h3-director-prompt`, `minimax-h3-instagram-style-director`, `minimax-h3-commercial-ad-director`) — those skills *plan* a 0.1s chart to generate new footage; this one *extracts* one from footage that already exists.

**Compatibility:** like its sister skills, this one relies only on the common Agent Skills baseline (`name`/`description` frontmatter, plain-prose instructions, relative-path reference files, portable Python scripts) with no Claude-only extensions, so it runs the same way under Claude Code/Cowork and Codex CLI. See `INSTALL.md`.

## Before you start: gather what you need

1. **The actual video (or a clear substitute).** This skill's whole value is extraction accuracy — if no video file is available, say so and ask for one, or explicitly fall back to `prompt_only`/`transcript_only` evidence mode if the user only has a text description of a video they remember. Never write a deconstruction that reads as if a video was watched when it wasn't. **If nothing is available yet — no video, no description — do not show the user a placeholder shot table or JSON with realistic-looking timestamps/camera terms "as a preview."** A table with plausible numbers in it reads as extracted content even when labeled hypothetical; describe the target format in prose instead (what fields/columns it will have) and wait for real input. `worked_example.md`'s placeholder table is an exception made only because it's clearly framed as this skill's own internal documentation, not a reply to a live request.
2. **What the user wants out of this.** Just the deconstruction? A full remix prompt? Which layers should survive unchanged and which should change? If they said something like "keep the camera and timing but put my product in her hand," that's already most of a layer contract — reflect it back explicitly rather than re-deriving it from scratch.
3. **Work mode** (see below) — infer it from what they asked for if they didn't name one, and state the inference back to them.
4. **Output syntax target** — will the actual reference video/images be attached to the generation call (→ full-reference mode, `VIDEO_PROMPT_WRITING_GUIDE_ref_en.md`), or does the user want a self-contained text prompt with no attached asset (→ plain T2VA, `VIDEO_PROMPT_WRITING_GUIDE_base_en.md`)? Ask if it's not obvious from context — this changes the entire output format, not just a detail.

## Work modes

| Mode | What it means | When to use it |
|---|---|---|
| `deconstruct_only` | Produce the structured breakdown; no new prompt | User wants to understand/document a video, not regenerate it |
| `deconstruct_and_prompt` | Full deconstruction, then a prompt that mirrors it closely | User wants an accurate MiniMax H3 recreation of the same video |
| `selective_remix` | Deconstruct, then apply an explicit per-layer policy (some preserve, some replace) | The common case — "keep X, change Y" (see `references/layer_contract.md`) |
| `visual_remix_locked` | Preset: lock timeline/camera/composition/actions/transitions, replace visuals/text/product/audio style | "Same shots and choreography, totally different look" |
| `free_rebuild` | Only explicitly-named anchors are kept; everything else is freely rebuilt | **Only when the user explicitly authorizes full reconstruction** — never inferred or assumed as a default |

If the request is ambiguous between `selective_remix` and one of the named presets, default to naming the closest preset and confirming it, rather than silently building a custom policy the user didn't ask for.

## The workflow

### 1. Read the model facts once

`references/model_facts.md` carries the same hard limits and tested behaviors as the sister skills (camera drifts unless forbidden, timed beats need a stated end-state, observable behavior beats emotion words, the last beat in a sequence risks compression). They apply to the *output* prompt exactly as much as in the generation-only skills.

### 2. Extract, don't assume

Follow `references/deconstruction_schema.md` §0 for the actual `ffmpeg`/`ffprobe` commands: probe duration/resolution, sample frames at baseline fps, run scene-change detection to find real cut points, and dense-resample any window that needs closer reading. This step is non-negotiable for `evidence: video` — a deconstruction "from" a video that was never actually sampled is exactly the failure mode this skill exists to prevent.

- For any on-screen text (captions, posters, labels, signs) — and *especially* Chinese text — follow `references/ocr_text_precision.md` in full before writing down a reading. This is where silent, confident-looking errors are most likely.
- For the single-person action/gesture/dance sequence that's usually this skill's main subject, follow `references/action_timeline_methodology.md` to build a 0.1s pose/contact-event chart, not just a shot-level action summary.

### 3. Write the structured deconstruction

Segment into shots per the boundary rules in `references/deconstruction_schema.md` §1, and fill out either the Markdown table (§2) or the full JSON schema (§3) — JSON when the deconstruction needs to be machine-validated or handed to a remix step, the table when a quick human-readable breakdown is what's wanted. Camera terms must come only from `VIDEO_PROMPT_WRITING_GUIDE_base_en.md` §4.3's controlled vocabulary — never free-text camera description.

### 4. Decide the layer policy

If the mode is anything other than `deconstruct_only`, open `references/layer_contract.md`, pick a preset or build a custom per-layer policy across all twelve layers, and write (at least mentally, or as an actual `remix-contract.json` if the task is complex enough to benefit from one) which of `preserve`/`adapt`/`replace`/`omit` applies to each. Pay special attention to the layers noted as "easy to misjudge" — camera vs. actions is the single most common conflation.

### 5. Choose the output syntax and write the prompt

Confirm (from step 0.4) whether the target is full-reference mode or T2VA, then write the final prompt in that exact field syntax. Preserved layers become concrete, observable-behavior prose pulled from the deconstruction and the action chart; replaced layers become the user's actual new content, never a placeholder. `references/worked_example.md` shows one full pass through this sequence end to end (explicitly labeled hypothetical — no real video was analyzed for it, since none was available while building this skill; use it only as a structural template).

The final prompt must describe finished, renderable content only — never narrate the remix process itself (no "the original subject was replaced with...", no "if this conflicts with the reference..."). That kind of language belongs in your working notes or the `remix-contract.json`, never in what gets sent to the model.

### 6. Certify before handing it back

Work through `references/certification_checklist.md` in full. If a `remix-contract.json` exists, validate the deconstruction against `scripts/validate_deconstruction.py` and the finished prompt against `scripts/validate_remix.py`:

```bash
python3 scripts/validate_deconstruction.py --input video-deconstruction.json
python3 scripts/validate_remix.py --contract remix-contract.json --prompt video-prompt-final.md
```

Both scripts are zero-dependency (standard library only) and print `ERROR:` lines on failure or an `_OK` summary line on success.

## Output format

Give the user, in this order (skip parts they didn't ask for — if they only want the final prompt, lead with that and keep the deconstruction as internal working material):

1. A short line naming the work mode, evidence type, and output-syntax choice (and why, if inferred rather than stated).
2. The deconstruction (table or JSON) — only if the mode calls for showing it, or the user asked to see it.
3. The layer policy actually applied (one line per layer, or the full `remix-contract.json` if one was built) — only for remix modes.
4. The final prompt, in a fenced code block, in the exact field syntax it needs to be pasted into the model as.
5. One or two lines confirming what the certification checks caught or confirmed, and explicitly flagging any on-screen text that couldn't be read with confidence.

See `references/external_references.md` for the outside sources consulted on video-to-prompt reverse-engineering practice and Chinese OCR accuracy — informative background, not a source of new syntax rules.
