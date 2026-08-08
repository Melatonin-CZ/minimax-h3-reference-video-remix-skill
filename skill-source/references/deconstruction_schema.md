# Reference Video Deconstruction — Ingestion, Segmentation, and Recording

Adapted from the shot-table/JSON approach in `penposs/remix-reference-video-prompt` (see `SKILL.md` attribution), re-targeted so the recorded vocabulary maps directly onto `VIDEO_PROMPT_WRITING_GUIDE_base_en.md`'s camera-motion table instead of free-text descriptions — this is what makes the final prompt a mechanical compression step rather than a rewrite.

## 0. Extract before you analyze

You cannot deconstruct a video you haven't actually looked at frame by frame. If a video file is available in the working directory, use `ffmpeg`/`ffprobe` (both available in this environment) to turn it into something you can actually read with your image-viewing capability:

```bash
# Basic facts first: duration, fps, resolution
ffprobe -v error -show_entries format=duration:stream=width,height,r_frame_rate -of default=noprint_wrappers=1 input.mp4

# Baseline sampling: 2 frames per second, numbered sequentially
mkdir -p frames && ffmpeg -i input.mp4 -vf fps=2 frames/frame_%04d.png

# Cut/scene-change detection: catches hard cuts more reliably than fixed-interval sampling
mkdir -p cuts && ffmpeg -i input.mp4 -vf "select='gt(scene,0.3)',showinfo" -vsync vfr cuts/cut_%04d.png 2> cuts/scene_log.txt
grep pts_time cuts/scene_log.txt   # gives approximate timestamps for each detected cut

# Dense re-sampling around a specific window once you've found something worth reading closely
# (a poster, an on-screen caption, a fast action beat) — e.g. 10-15s window at 8fps:
ffmpeg -ss 00:00:04 -to 00:00:15 -i input.mp4 -vf fps=8 frames_dense/frame_%04d.png
```

Read the baseline frames first to get the overall shot structure, then go back and densely re-sample any window that contains text, a poster, or fast/ambiguous motion — the 2fps baseline is for structure, not for reading a caption or judging a single gesture's timing.

**Evidence discipline (non-negotiable):** only claim "based on the reference video" once you have actually extracted and viewed frames covering the relevant window. If you only have a prior prompt, a script, or a transcript and no actual video/frames, say so explicitly and work from `prompt_only` or `transcript_only` evidence — never describe inferred content as if it were observed. If a frame is blurry, low-resolution, or ambiguous, record it as `unknown` rather than guessing what a confident-sounding description implies you saw. This mirrors the source project's evidence-boundary rule and is the single most important discipline in this whole skill — a fabricated-but-confident deconstruction is worse than an honest, partial one.

## 1. Segment into shots

Start a new shot/segment whenever any of the following changes, same threshold as the source project:

- A hard cut or visible transition (wipe, mask, match cut, morph, freeze frame).
- Camera angle, shot size, or camera movement changes.
- The subject's primary action or the purpose of the action changes.
- The scene, time of day, wardrobe, or product-display stage changes.
- On-screen text, a sound cue, or the shot's narrative function changes noticeably.

Don't over-segment a single continuous take just to hit a target number of shots — a long unbroken shot can be recorded as one segment with internal action-phase notes rather than artificially split.

## 2. Record each shot — Markdown table (for human review)

| Time | Shot & framing | Subject action | Scene & visuals | Transition/text/sound | Function | Policy |
|---|---|---|---|---|---|---|
| 0.0–2.3s | Static medium shot, subject centered | Raises right hand, turns head to camera | Indoor studio, soft key light from left | Hard cut at 2.3s | Establish subject | camera: preserve, action: adapt |

Only the columns that matter for the user's actual goal need to be filled in with detail — see `certification_checklist.md`'s note on scoping depth to what the user asked for.

## 3. Record each shot — JSON (for downstream use / validation)

```json
{
  "schema_version": 1,
  "source": {
    "type": "video",
    "path_or_url": "reference-video.mp4",
    "evidence": "video"
  },
  "goal": "Preserve the camera rhythm, replace the subject and product for a new ad",
  "duration_seconds": 15,
  "shots": [
    {
      "shot_id": "S01",
      "start_seconds": 0.0,
      "end_seconds": 2.3,
      "camera": {
        "shot_size": "medium",
        "angle": "eye-level",
        "motion_type": "Static Shot",
        "amplitude": null,
        "speed": null
      },
      "composition": "subject centered, product held at chest height",
      "subject": "young woman, red jacket, holding a bottled drink",
      "action": "raises the bottle, twists the cap open",
      "environment": "white studio backdrop, hard frontal light",
      "lighting_palette": "high-key, neutral white balance",
      "props_product": "single glass bottle, red label",
      "transition_effects": "hard cut at end",
      "on_screen_text": null,
      "audio": "cap-twist click, soft fizz",
      "narrative_function": "establish subject and product",
      "policy": {
        "camera": "preserve",
        "action": "adapt",
        "visuals": "replace"
      },
      "confidence": "high"
    }
  ],
  "unknowns": []
}
```

Field notes:
- `camera.motion_type` must be one of the exact terms from `VIDEO_PROMPT_WRITING_GUIDE_base_en.md` §4.3 (`Static Shot`, `Push In`, `Pull Out`, `Pan Left/Right`, `Truck Left/Right`, `Tilt Up/Down`, `Pedestal Up/Down`, `Arc Shot`, `Tracking Shot`, `Shake Slightly/Strongly`, `POV`, `Roll Clockwise/Counterclockwise`) — recording it in this controlled vocabulary during deconstruction, not just at prompt-writing time, is what makes the final compression step mechanical rather than an interpretive rewrite.
- `amplitude`/`speed` follow the same guide's small/large and slow/fast vocabulary; leave `null` when the motion reads as medium/normal (the guide says to omit these when unremarkable).
- `on_screen_text` holds the exact verbatim string(s) seen in that shot — see `ocr_text_precision.md` before filling this in for any shot containing text.
- `source.evidence` is one of `video`, `prompt_only`, `transcript_only`, `mixed` — never claim `video` unless frames were actually extracted and viewed for that shot.
- Timestamps are seconds, decimals allowed to 0.1s precision (see `action_timeline_methodology.md` for when finer precision matters, specifically single-person action beats).
- `confidence` is `high`/`medium`/`low`; anything below `high` on a load-bearing field (on-screen text, a required-preserve camera move) should be flagged to the user rather than silently smoothed over.
- Unclear or unreadable fields get `null` and an entry in the top-level `unknowns` array — never invent a plausible-sounding value to fill a gap.
