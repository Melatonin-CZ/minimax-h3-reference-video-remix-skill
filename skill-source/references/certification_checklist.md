# Certification Checklist — Reference Video Deconstruction & Remix Prompt

Work through in order. This checklist covers both the deconstruction and the final prompt — a task that's `deconstruct_only` stops after Stage 3; a task that also generates a prompt continues through Stage 6.

## Stage 0 — Mode and evidence

- [ ] The work mode is chosen and named: `deconstruct_only`, `deconstruct_and_prompt`, `selective_remix`, `visual_remix_locked`, or `free_rebuild` (see `SKILL.md` for the selection rules). If the user didn't state one explicitly, the inferred mode is stated back to them.
- [ ] `free_rebuild` is only used when the user explicitly authorized full reconstruction — never assumed.
- [ ] `source.evidence` is accurately set (`video`, `prompt_only`, `transcript_only`, or `mixed`) and nothing is described as "from the reference video" unless frames were actually extracted and viewed for that claim.

## Stage 1 — Extraction quality

- [ ] Video was actually processed with `ffmpeg` (baseline sampling + scene-change detection at minimum) rather than analyzed from assumption or from a filename/description alone.
- [ ] Any segment containing on-screen text was re-sampled densely and, where useful, cropped tight per `ocr_text_precision.md` — not read only from the baseline low-fps pass.
- [ ] Any single-person action sequence was charted at 0.1s resolution per `action_timeline_methodology.md`, not summarized only at the shot level.

## Stage 2 — Deconstruction completeness

- [ ] Shots are segmented at true boundaries (cut, camera change, action/purpose change, scene change, text/sound/function change) per `deconstruction_schema.md` — not over-segmented for its own sake, not under-segmented past a real boundary.
- [ ] Each shot's `camera.motion_type` uses only the controlled vocabulary from `VIDEO_PROMPT_WRITING_GUIDE_base_en.md` §4.3.
- [ ] Every on-screen text field is either a verified verbatim string (Chinese text checked character-by-character per `ocr_text_precision.md`) or explicitly marked unclear/unknown with the candidates considered — never a smoothed-over guess.
- [ ] Timestamps are chronological, non-overlapping, and each shot's end time exceeds its start time.
- [ ] Nothing in the deconstruction describes a shot that isn't actually in the source footage — no filled-in "probably also has..." content.
- [ ] If structured JSON output is needed, it validates against `scripts/validate_deconstruction.py`.

## Stage 3 — Layer policy

- [ ] Every layer in `layer_contract.md`'s table has an explicit policy (`preserve`/`adapt`/`replace`/`omit`), not left implicit.
- [ ] `camera` and `actions` are judged as separate layers, never conflated — "keep the shots" is not automatically "keep the choreography," and vice versa.
- [ ] Where a moment has two distinct layers overlapping (a mask's shape vs. what's drawn inside it; a prop's trajectory vs. its appearance; a caption's timing vs. its content), both are recorded separately per the "easy to misjudge" notes in `layer_contract.md`.
- [ ] If a `remix-contract.json` is being produced, its `required_phrases` are camera/action/transition phrases only — never a phrase naming content that's actually being replaced.

## Stage 4 — Choosing the output syntax

- [ ] The choice between full-reference-mode output (`VIDEO_PROMPT_WRITING_GUIDE_ref_en.md`, when the actual reference video/images will be attached to the generation call) and plain T2VA output (`VIDEO_PROMPT_WRITING_GUIDE_base_en.md`, when only a self-contained text prompt is wanted) is made deliberately and stated to the user, not defaulted silently.
- [ ] For full-reference mode: the task-type prefix in `summary` (`[reference generation]`, `[video editing]`, `[video continuation]`, combinations thereof) accurately reflects what's actually being asked for, per the rules in `VIDEO_PROMPT_WRITING_GUIDE_ref_en.md` §3.

## Stage 5 — Final prompt quality

- [ ] The prompt states final content directly — subject, scene, action, camera, transition, text, sound — and never explains the remix process ("the original subject was replaced with...", "if this conflicts with the reference..."). This is a hard rule carried over from the source project: process narration in a generation prompt actively confuses the model about what it's supposed to render.
- [ ] Preserved elements from the deconstruction actually appear in the final prompt; replaced elements use the user's real supplied content, not a placeholder description.
- [ ] Only necessary global-consistency constraints are stated (e.g., same person across shots, product must not distort, text must render accurately, camera stays locked) — the prompt isn't padded with restatements of things already implied.
- [ ] Length defaults to roughly the source material's own scale and stays under ~1600 characters unless the user specified otherwise.
- [ ] If the user only wants the final prompt, that's the only thing delivered — the deconstruction stays internal work, not pasted into the response.
- [ ] The finished prompt validates against `scripts/validate_remix.py` when structural preservation was promised (timeline, required phrases, character limit, no process-wording).

## Stage 6 — Final read-through

- [ ] Read the deconstruction once for internal consistency: do the timestamps, camera terms, and policies actually match what Stage 1-3 established, or did something drift during writing?
- [ ] Read the final prompt once as if you were the generation model receiving it cold: is every instruction concrete and renderable, with nothing that only makes sense if you already know what the original reference video looked like?
