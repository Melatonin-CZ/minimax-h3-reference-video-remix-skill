# On-Screen Text Precision Protocol (Chinese-Inclusive)

`VIDEO_PROMPT_WRITING_GUIDE_base_en.md` §4.5 already requires on-screen text to be preserved verbatim, in quotation marks, untranslated. This file is about how to actually *get* the verbatim string right before you write it down — a wrong character in a poster or caption is a silent, confident-looking error, exactly the kind evidence discipline exists to prevent.

## Why this needs its own protocol

Video-derived text is systematically harder to read correctly than a photo of text: motion blur, compression artifacts, small on-screen size, brief exposure, and stylized fonts all degrade legibility. Chinese text adds a specific failure mode on top of this: many characters differ by a single stroke or radical (己/已/巳, 未/末, 日/曰, 幸/辛), and a low-confidence read tends to silently resolve to the *more common* character rather than the *correct* one — which means the error looks plausible and won't be caught by a casual re-read. Simplified/Traditional variants (发/發, 国/國) and punctuation style (、vs, ，vs,) also need to be preserved as observed, not normalized to whatever's more familiar.

## Protocol

1. **Find every window where text is on screen.** Don't rely on the baseline 2fps sampling from `deconstruction_schema.md` — text can appear and disappear within less than half a second. Re-scan with dense sampling (8fps or higher) across any segment where a caption, poster, sign, or label might be present, including background elements, not just foreground captions.

2. **Re-sample at the sharpest available frame, and crop tight.** Motion blur is often worst mid-transition; find the frame where the text is most static and highest-contrast (often the frame furthest from a cut). Use `ffmpeg`'s crop filter to isolate just the text region at full resolution rather than reading it as a small element inside a full frame:
   ```bash
   ffmpeg -ss 00:00:04.200 -i input.mp4 -vframes 1 -vf "crop=400:120:200:600" text_crop_04200.png
   ```
   Adjust the crop rectangle to the text's actual bounding box; read the cropped image, not just the full frame.

3. **Read character by character for anything in Chinese (or any script you're not maximally confident in), not word by word.** Silently pattern-matching to "the word that would make sense here" is exactly how a single-stroke misread survives. If a character's identity depends on a stroke or radical that's genuinely ambiguous at the available resolution, don't resolve it to your best guess — mark it `unclear` and say which candidates you considered, per the `[unclear]` convention in `VIDEO_PROMPT_WRITING_GUIDE_ref_en.md` §5.4.

4. **Cross-check against context, but don't let context overrule what's actually visible.** If a product label plausibly reads one of two near-identical characters, note both readings and your best assessment, rather than silently picking one and presenting it as certain. It's fine (expected, even) to end up more confident from context — just don't skip the visual read and go straight to the contextual guess.

5. **Preserve exactly, including:**
   - Simplified vs. Traditional character forms, as actually shown — don't normalize.
   - Punctuation style (、，。！？ vs. their half-width Latin equivalents) as actually shown.
   - Line breaks and layout groupings, if they affect how the text should be understood (e.g., a two-line poster where line breaks are part of the design).
   - Any mixed-script text (Chinese + English + numerals together) exactly as combined on screen.
   - Stylization that changes legibility (outlined, mirrored, extreme kerning) — note it, since it may affect whether the source text is even reliably legible to a viewer, which matters for the `confidence` field in the deconstruction JSON.

6. **Record confidence per text element**, not just per shot — a shot's camera data can be `high` confidence while its on-screen text is `medium` or `low`. Use the deconstruction JSON's `confidence` field at the shot level for the dominant concern in that shot, but call out text-specific uncertainty explicitly in prose if it's lower confidence than the rest of the shot.

7. **Never invent a plausible poster/caption/label to fill a gap.** If text is present but genuinely illegible even after cropping and dense re-sampling, record it as `null`/`unclear`, note what's structurally known (its position, its approximate length, its entrance/exit style) without fabricating its content, and tell the user directly that this element couldn't be read with confidence.

## Applying this to the final prompt

Once a text element's content is confirmed, carry it into the final prompt exactly as the base guide requires: exact string in double quotation marks, untranslated, per §4.5. If the layer contract marks `text` as `replace`, the new text still needs the same verbatim-string treatment — write the user's actual replacement string, not a paraphrase of what it should convey.
