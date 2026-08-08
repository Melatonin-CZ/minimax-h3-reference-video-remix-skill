# Worked Example (Illustrative — Not Derived From an Actual Video)

**This example is hypothetical.** No real reference video was extracted or viewed to produce it. It exists only to show the shape of a finished deconstruction → layer contract → final prompt sequence. Per the evidence-discipline rule in `deconstruction_schema.md`, a real task must replace every part of this with content actually extracted from actual frames — never pattern-match the *content* of this example onto a real video, only its *structure*.

**Scenario:** a hypothetical 8-second vertical reference video of one person doing a single continuous product-reveal gesture, ending on a product held toward camera with a Chinese poster board visible in the background for the last 2 seconds. The user says: "keep the camera and the timing and her gesture, but put my own skincare bottle in her hand and swap out the background poster for my own text — full reference mode, I'll attach the video."

## Step 1 — Extraction (hypothetical ffmpeg output, described not shown)

Baseline 2fps pass shows one continuous shot, no hard cuts. Scene-change detection confirms no cut points above threshold. Dense 8fps re-sample across 0.0–8.0s used for the action chart. Dense re-sample + crop used on the 6.0–8.0s window where the background poster is legible.

## Step 2 — Action chart (per `action_timeline_methodology.md`)

| t (s) | pose/position state | note |
|---|---|---|
| 0.0–1.5 | standing, both hands at sides, product off-screen | held pose, high confidence |
| 1.5–3.0 | right arm reaches off-frame right, torso turns slightly | steady speed, high confidence |
| 3.0–3.4 | hand closes around product (off-screen pickup) | contact event, anchor point |
| 3.4–5.8 | arm brings product into frame, rising toward chest height | gradual, high confidence |
| 5.8–6.3 | product raised to shoulder height, presented toward camera | contact/hold, anchor point |
| 6.3–8.0 | held presentation pose, slight forward lean | held pose, high confidence |

## Step 3 — Text extraction (per `ocr_text_precision.md`, hypothetical)

Background poster board, visible 6.0–8.0s: cropped and re-read character by character. Hypothetical result: "焕新肌肤" (four characters, simplified forms, sans-serif, high confidence at the cropped resolution). Since this element is being replaced per the user's request, its exact reading matters less for the final prompt than for the deconstruction record — but it's still verified rather than guessed, since the deconstruction should be accurate regardless of what happens to a layer afterward.

## Step 4 — Deconstruction (abridged JSON)

```json
{
  "schema_version": 2,
  "source": {
    "type": "video",
    "path_or_url": "reference-video.mp4",
    "evidence": "video"
  },
  "goal": "single continuous product-reveal gesture, subject and product to be replaced",
  "duration_seconds": 8.0,
  "shots": [
    {
      "shot_id": "shot-01",
      "start_seconds": 0.0,
      "end_seconds": 8.0,
      "camera": {
        "shot_size": "medium shot",
        "angle": "eye-level",
        "motion_type": "Static Shot",
        "amplitude": null,
        "speed": null
      },
      "composition": "subject centered, product enters from frame-right at 3.4s",
      "subject": "one adult woman, casual top, facing camera",
      "action": "reaches off-frame, picks up product, raises and presents it toward camera, holds",
      "environment": "plain studio background with a poster board visible from 6.0s",
      "lighting_palette": "soft even front lighting, neutral background tone",
      "props_product": "unlabeled bottle-shaped product",
      "transition_effects": "none — single continuous shot",
      "on_screen_text": {
        "content": "焕新肌肤",
        "window_seconds": [6.0, 8.0],
        "confidence": "high"
      },
      "audio": "ambient room tone, no dialogue, no music",
      "narrative_function": "product reveal / presentation beat",
      "policy": {
        "camera": "preserve",
        "actions": "preserve",
        "text": "replace",
        "props": "replace",
        "visuals": "replace"
      },
      "confidence": "high"
    }
  ],
  "unknowns": []
}
```

## Step 5 — Layer contract (abridged)

Preset: closest to `visual_remix_locked`, with `product_brand` and `text` explicitly `replace` per the user's request; `visuals` (the performer's identity) stays `preserve` since the user only asked to swap the product and the poster, not the person. `timeline`, `camera`, `composition`, `actions`: `preserve`. `required_phrases`: `"static medium shot"`, `"reaches off-frame"`, `"raises the product"` — camera/action phrasing only, nothing naming the specific old product or old poster text, since those are being replaced.

## Step 6 — Choosing output syntax (per `SKILL.md` step 5)

User said "I'll attach the video" → full-reference mode. Task type: `[reference generation]` — new content generated using the reference video as a style/motion anchor, product and text swapped.

## Step 7 — Final prompt (full-reference mode, per `VIDEO_PROMPT_WRITING_GUIDE_ref_en.md`)

```
[reference generation] A woman stands centered in a plain studio setting with soft, even front lighting. She reaches off-frame to her right, turns her torso slightly, and picks up a skincare bottle. Static medium shot, eye-level, camera locked throughout. She raises the product smoothly toward her chest and then to shoulder height, presenting it directly toward camera, and holds the pose with a slight forward lean. A poster board behind her reads "焕新亮采" in bold sans-serif characters, visible from the moment she completes the presentation gesture. Ambient room tone only, no dialogue, no music. The woman's identity, wardrobe, and the studio's lighting and background tone match <Subject 1> exactly; only the product and poster text change from the reference.
```

Notes on why this prompt looks the way it does: no sentence explains that anything was "replaced" or references the deconstruction — it states final content directly, per Stage 5 of `certification_checklist.md`. The action chart's beat timing (reach → contact → rise → present → hold) is compressed into the prose rather than listed as a literal table, since a single continuous shot with `camera: preserve` doesn't need `[Shot N] At MM:SS.mmm` markers — those only appear at actual cut points, and this hypothetical example has none. A multi-shot example would show at least one such marker; see `VIDEO_PROMPT_WRITING_GUIDE_base_en.md` §4.4 for that syntax.
