# MiniMax H3 Reference-Video Remix System — Index & Model Facts

This folder is a companion system to the two existing local guides:

- `VIDEO_PROMPT_WRITING_GUIDE_base_en.md` — the official T2VA / I2VA / FL2VA / L2VA prompt format (shot syntax, camera-motion vocabulary, speaker/dialogue tags, `overall_soundscape`, `non_diegetic_music`).
- `VIDEO_PROMPT_WRITING_GUIDE_ref_en.md` — the full-reference-mode format (`subject_definitions`, `summary`, `retention_analysis`, `detailed_description`) for prompts built from reference images/video/audio. This is the primary output target for this skill, since its whole job is describing an actual reference video precisely.

Those two files remain the **ground-truth syntax**. Everything in this folder is written to be dropped on top of that syntax, not to replace it.

## Files in this folder

| File | Purpose |
|---|---|
| `model_facts.md` | This file — index, plus grounded technical facts about the MiniMax H3 model itself |
| `deconstruction_schema.md` | How to segment a reference video into shots and record what's in each one, as a Markdown table and/or JSON |
| `layer_contract.md` | The preserve / adapt / replace / omit policy system for deciding what to keep from the reference and what to change |
| `ocr_text_precision.md` | A dedicated protocol for reading on-screen text accurately, including Chinese, where misreads are costly |
| `action_timeline_methodology.md` | How to extract a single person's movement at 0.1-second resolution from the reference footage |
| `certification_checklist.md` | The combined "certificate" checklist — what a deconstruction and final prompt must satisfy |
| `worked_example.md` | One fully worked, explicitly illustrative walkthrough from a hypothetical reference video to a certified full-reference prompt |

This skill also ships two zero-dependency validator scripts in `../scripts/` (adapted from the open-source project this skill is built on — see `SKILL.md`'s attribution note): `validate_deconstruction.py` checks a structured deconstruction JSON, `validate_remix.py` checks a finished prompt against a source and a contract.

Recommended reading order for a new task: `certification_checklist.md` (checklist) → `deconstruction_schema.md` (how to segment and record) → `ocr_text_precision.md` + `action_timeline_methodology.md` (precision protocols) → `layer_contract.md` (decide what to keep/change) → `worked_example.md` (see it done end to end) → write the final prompt in the syntax from the base/ref guides.

## MiniMax H3 — grounded technical facts

These facts come from the model's public specs and from a third-party prompting guide (PixelDojo) that ran matched-pair generation tests on the live model on 2026-08-03. Where a technique's effect was actually tested rather than assumed, that's noted — treat it as more reliable than general folklore about "what AI video models like."

**Hard limits**
- Output: 2K resolution (2560×1440 class), 24 fps, native stereo audio baked into the file.
- Duration: 5–15 seconds in one generation, whole seconds only as a *ceiling* — a 15.0s target is the maximum single-clip length, which is exactly the length used throughout this system.
- Six aspect ratios (21:9 to 9:16), all at 2K; ignored in first/last-frame mode, where the supplied image sets the shape.
- Prompt field: up to ~7,000 characters — enough for a full shot list plus sound design in one request.
- Modes are inferred from what's attached: no media = text-to-video (T2VA); a start frame (+ optional end frame) = image-to-video (I2VA/FL2VA/L2VA); up to nine reference assets = full-reference mode. Reference images and first/last-frame are mutually exclusive.

**Behaviors confirmed by matched-pair testing (i.e., not just folklore)**
1. **The camera drifts by default.** If a prompt says nothing about camera motion, the model invents continuous drift and often cuts between two setups on its own, even inside a 5-second clip. If a shot is meant to be static, say so explicitly and name the moves that must *not* happen (no push-in, no handheld, no zoom, no dolly) rather than only saying "static" — the explicit refusal is what reliably held a locked-off frame in testing.
2. **Structure buys obedience, not prettiness.** A bare one-line prompt still produces a competent, well-lit clip — but it is the model's own film (its own shot choices, its own cuts). The full Subject → Action → Scene/Environment → Style → Camera → Audio structure doesn't necessarily look better, but it reliably executes the *specific* shot asked for.
3. **Timed beats work, and the end-state is what does the work.** Sequencing several actions in one plain sentence already comes out roughly in the right order (H3 is good at implicit sequencing). What timed beats add is that the model reliably hits the *stated end condition* of each beat (e.g., "the bench is now empty") rather than merely gesturing at it.
4. **Fifteen seconds is tight for five beats.** In a 15s / 5-beat test, the first four beats landed on time; the fifth (and hardest — a prop hand-off) was compressed and never finished. Practical budgeting: allow ~4 seconds for any beat that involves a prop change, hand-off, or costume/state change; ~2–3 seconds is enough for a pure camera move or a simple pose change. The *last* beat in a sequence is the one most likely to get squeezed — put the shot you most need in the middle of the timeline, not at the very end.
5. **Observable behavior beats emotion words.** "She looks anxious and nervous" produces a generic to-camera performance. Naming the physical cues instead — fixed downward gaze, still fingers, raised shoulders, one held breath — gets followed literally and held for the shot's full duration. This system's timing charts are built around this finding: every beat is written as a visible action, never a mood label.
6. **On-screen text: type the exact string.** Describing text ("a title card with the chapter name") gets *a* title card with wording the model invents. Spelling the string out verbatim, with case/weight/position named, gets exactly that string.
7. **First/last-frame interpolation lands precisely**, including fine background detail — this is the most precise control surface the model offers and is the mechanical basis for FL2VA prompts in the base guide.
8. **Audio is directed, not just described.** An undirected clip gets a flat ambience bed; naming sound events in the order they occur, plus what runs underneath, produces a track with real dynamics (quiet floors, transient hits at the moments named). This maps directly onto the base guide's `overall_soundscape` / `non_diegetic_music` split.
9. **Reference-image role labeling and negative lists were not shown to change output** in controlled tests, when each reference could only plausibly fill one slot, or when the negative was for something the model wasn't inclined to add anyway. Both are free to include and are still worth writing (role language matters more once two references *could* plausibly fill the same slot, e.g. two people), but they are not what makes a prompt succeed or fail — camera specificity, timed end-states, and observable behavior are the load-bearing elements.

These nine points, plus the base/ref guide's own syntax, are the technical foundation the rest of this system is built on.
