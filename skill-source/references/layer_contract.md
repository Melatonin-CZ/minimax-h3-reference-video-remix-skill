# Layer Contract — What to Keep, What to Change

Adapted from `penposs/remix-reference-video-prompt`'s layer-contract system (see `SKILL.md` attribution). The core idea: a reference video isn't one indivisible thing to either "keep" or "replace" — it's a stack of independent layers, and a remix request almost always means different things for different layers at once ("keep the camera work and timing, change who's in it").

## The four policies

| Policy | Meaning |
|---|---|
| `preserve` | Content, order, and function stay exactly as observed |
| `adapt` | The function/rhythm/trajectory is kept, but its concrete expression changes to fit new subject matter |
| `replace` | Rebuilt entirely from the user's new content |
| `omit` | Deliberately dropped |

## The layers

| Layer | What it covers |
|---|---|
| `timeline` | Total duration, segmentation, shot order, cut points |
| `camera` | Shot size, angle, position, motion type/amplitude/speed |
| `composition` | Subject placement, frame balance, foreground/midground/background relationship |
| `actions` | Action sequence, direction, path, speed, pauses — see `action_timeline_methodology.md` for single-person action specifically |
| `transitions` | Hard cuts, occlusion/mask transitions, match cuts, morphs, freeze frames |
| `text` | On-screen text/caption/poster content, position, entrance style and timing — see `ocr_text_precision.md` |
| `audio_timing` | Music beat hits, action-synced sound-effect triggers |
| `audio_style` | Music genre/timbre, ambient sound, voiceover style |
| `visuals` | Subject identity, hair/makeup, wardrobe, environment, lighting, color, material |
| `props` | Prop appearance, count, position, trajectory, function |
| `product_brand` | Product, packaging, label, brand mark, closing product beat |
| `narrative` | Information order, tension/conflict, selling point, emotional arc, ending function |

## Presets

### `visual_remix_locked` — "keep the shots, swap what's in them"
- `timeline`, `camera`, `composition`, `actions`, `transitions`, `audio_timing`: `preserve`
- `props`: `adapt` by default — motion and transition function stay, appearance can change
- `visuals`, `product_brand`, `text`, `audio_style`: `replace`
- `narrative`: `preserve`

### `camera_and_rhythm_only` — "keep the pacing and camera language, re-perform the content"
- `timeline`, `camera`, `composition`, `transitions`, `audio_timing`: `preserve`
- `actions`, `props`: `adapt` or `replace`
- `visuals`, `product_brand`, `text`, `audio_style`: `replace`
- `narrative`: `adapt` or `replace` depending on the user's goal

### `narrative_structure_only` — "borrow the structure of a proven format, not its specific imagery"
- `narrative`: `preserve` or `adapt`
- `timeline`: `adapt`
- Every other layer: `replace`

### `free_rebuild` — "keep only what I explicitly point to"
Every layer defaults to `replace` or `omit` except whatever the user explicitly names as an anchor to keep. **Only use this preset when the user has explicitly authorized full reconstruction** — never assume it.

## Notes on layers that are easy to misjudge

- A mask/occlusion transition's *shape and reveal behavior* can be `preserve` while what's *drawn inside* it is `visuals: replace` — these are two different layers even though they happen in the same moment.
- A prop's *swing direction and occlusion function* (e.g., it passes in front of the subject at a specific frame) can be `preserve` while the prop's *appearance* is `adapt`.
- A wardrobe change's *timing* can be `preserve` while *which outfit* appears at that beat is `replace`.
- A caption's *timing* can be `preserve` while its *text content and typography* is `replace` — timing and content are different layers.
- A drum hit or action-sync point can be `preserve` while the *instrument/timbre* producing it is `replace`.
- **"Keep the camera work" is not the same claim as "keep the actions."** Record and decide these two layers separately — this is the single most common conflation in remix requests, per the source project's own field notes, and it's just as true when the subject is a single person's choreography as when it's a product demo.

## The `remix-contract.json`

Use this to make the policy decisions explicit and machine-checkable before writing the final prompt:

```json
{
  "schema_version": 2,
  "mode": "selective_remix",
  "source": {
    "video": "reference-video.mp4",
    "prompt": null,
    "evidence": "video"
  },
  "output": {
    "deconstruction": "video-deconstruction.json",
    "prompt": "video-prompt-final.md",
    "target_syntax": "minimax-h3-full-reference"
  },
  "policy": {
    "timeline": "preserve",
    "camera": "preserve",
    "composition": "preserve",
    "actions": "adapt",
    "transitions": "preserve",
    "text": "replace",
    "audio_timing": "preserve",
    "audio_style": "replace",
    "visuals": "replace",
    "props": "adapt",
    "product_brand": "replace",
    "narrative": "adapt"
  },
  "locked": {
    "timeline": ["0.0-2.3s", "2.3-5.0s", "5.0-8.5s"],
    "required_phrases": [
      "static medium shot",
      "raises the bottle",
      "hard cut"
    ]
  },
  "validation": {
    "preserve_timeline": true,
    "direct_result_only": true
  },
  "limits": {
    "max_chars": 1600
  }
}
```

`locked.required_phrases` should be the shortest, most stable camera/action/transition phrases — never a phrase naming a subject, wardrobe item, or product that's actually being replaced, or the validator will incorrectly demand the old content survive into the new prompt.

`output.target_syntax` records which of this system's output formats the final prompt should use — `minimax-h3-full-reference` (the default when the actual reference video/images will be attached to the generation call) or `minimax-h3-t2va` (when the user only wants a self-contained text prompt with no attached reference asset). See `SKILL.md` step 5 for how this choice is made.
