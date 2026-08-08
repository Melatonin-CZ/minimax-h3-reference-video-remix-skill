# External References

Background research consulted while building this skill, beyond the two ground-truth guide files and the `penposs/remix-reference-video-prompt` repo (see `SKILL.md` for that attribution). These are cited for the specific claims they support — this skill's actual rules always come from the two `VIDEO_PROMPT_WRITING_GUIDE_*.md` files first; outside sources only inform *how to extract information accurately*, never override the model's own syntax.

## Reverse-engineering prompts from reference video

General video-to-prompt reverse-engineering guidance converges on a few points this skill already follows structurally: break the clip into style, subject, environment, motion, camera language, and lighting before writing anything; treat prompt length as a real constraint rather than something more is always better (consistent with this system's ~1600-character ceiling and the base guide's own conciseness rules); and prefer iterative, one-layer-at-a-time refinement over rewriting a whole prompt when a first attempt doesn't match — which is exactly what the layer-contract's per-layer policy structure in `layer_contract.md` is designed to support.
- [Reverse-Engineer Any Video Into a Prompt — Lovart](https://www.lovart.ai/blog/reverse-engineer-video-into-prompt)
- [How to Extract Prompt from Video — PromptCreek](https://www.promptcreek.com/blog/how-to-extract-prompt-from-video-reverse-engineer-ai-video-prompts)

## Chinese OCR accuracy

Confirms the core premise behind `ocr_text_precision.md`: Chinese characters routinely differ by a single stroke, which leaves far less error margin than Latin-script OCR (no alphabet-level spell-check fallback exists), and recognition accuracy tends to decline as string length grows — reinforcing why this skill's protocol reads character-by-character rather than word-by-word and treats longer captions/posters as needing extra scrutiny, not less. Video-specific OCR pipelines also confirm that caption/text detection needs to happen as its own pass before recognition (localize the text region, then read it) — the same order this skill's crop-then-read procedure follows.
- [The Best OCR for Chinese Text — Curtis Chau, Medium](https://medium.com/@curtis.chau/the-best-ocr-for-chinese-text-what-works-for-simplified-and-traditional-f0ae7af22b79)
- [End-to-End Subtitle Detection and Recognition for Videos in East Asian Languages (arXiv)](https://arxiv.org/pdf/1611.06159)

## MiniMax Hailuo / H3 prompt structure (third-party guides)

Third-party writeups converge with this system's own base-guide rules on two points worth flagging explicitly: (1) subject-consistency prompts work best as a brief subject reference followed by a specific action ("the red-haired woman... turns her head slowly to face the camera"), which matches this skill's rule to describe preserved subjects as observable behavior rather than restating identity repeatedly; (2) the model responds better to narrative, script-like prompt flow than to a disconnected checklist of attributes — reinforcing why the final prompt step in `worked_example.md` compresses the action chart into flowing prose instead of listing chart rows verbatim. These are third-party observations, not part of the two ground-truth guide files, and are noted here as corroboration rather than as a source of new syntax rules.
- [MiniMax Hailuo H3 Prompt Guide — Mixio Studio](https://mixio.studio/hailuo-h3-prompt-guide)
- [MiniMax H3 Prompt Guide: control every reference input — OmniArt](https://omniart.studio/blog/tutorials-how-to-guides/minimax-h3-prompt-guide)
