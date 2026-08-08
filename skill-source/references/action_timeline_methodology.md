# Single-Person Action Timeline — 0.1-Second Extraction

This skill's primary use case (per the user's own framing) is a reference video of one person performing an action sequence — a dance, a gesture routine, a demo, a transformation. This file is the mirror image of the 0.1s timing-chart methodology used in this system's sister skills (`minimax-h3-director-prompt`, `minimax-h3-instagram-style-director`, `minimax-h3-commercial-ad-director`): those skills *plan* a 0.1s chart to generate new footage; this skill *extracts* a 0.1s chart by observing existing footage. The chart format is the same for a reason — an extracted chart from this skill can be handed almost directly to a sister skill's generation workflow when the goal is "recreate this action with a new subject."

MiniMax H3 renders at 24fps (≈0.0417s/frame), so 0.1s ≈ 2.4 frames — the same resolution ceiling applies here: don't claim finer distinctions than roughly 2-3 frames can actually support.

## What to extract

For the person's movement specifically (as distinct from camera movement, which belongs in the shot-level `camera` fields from `deconstruction_schema.md`):

- **Pose/position changes:** where a limb, the torso, or the head starts and ends a distinct movement, timestamped to 0.1s.
- **Speed and easing:** does the movement start slow and accelerate, move at constant speed, or snap quickly and settle — this determines whether the eventual prompt should use language like "gradually," "suddenly," or "steadily."
- **Pauses and holds:** any moment the person is genuinely still, even briefly — these are as structurally important as the movements themselves, and are exactly the kind of detail that gets lost if you only describe the "high points" of an action.
- **Contact events:** a hand touching an object, a foot landing, a turn completing — these are natural timestamp anchors, easier to pin down precisely than a continuous motion's midpoint.
- **Direction and path:** not just "she moves her arm" but where from and to, and along what path (straight, arcing, circular).

## Extraction procedure

1. Use the dense-sampling ffmpeg command from `deconstruction_schema.md` (8fps or higher) across the action's full duration — 2fps is too coarse to place a contact event or a pause boundary accurately.
2. Step through the extracted frames in order. For each frame, note the pose state in a few words (not a full sentence yet) and its timestamp.
3. Group consecutive frames with materially the same pose into a single row spanning that time range — this is the same "don't chart every tick, chart every change" principle from the sister skills' planning methodology, just applied in reverse: you're compressing observed frames into beats, not expanding planned beats into frames.
4. Mark each beat's confidence — a clean, well-lit, front-on action reads at `high` confidence; a fast, motion-blurred, or partially occluded movement should be marked `medium` or `low`, and described in terms of what's actually visible (e.g., "arm blurs upward, exact final hand position unclear") rather than smoothed into a confident-sounding guess.

## Chart format

| t (s) | pose/position state | note |
|---|---|---|
| 0.0–1.2 | standing, arms at sides, facing camera | held pose, high confidence |
| 1.2–1.9 | right arm rises from side to shoulder height, elbow leading | steady speed, high confidence |
| 1.9–2.0 | hand makes contact with the product on the shelf | contact event, anchor point |
| 2.0–3.4 | torso rotates roughly 30° toward camera while lifting the product | gradual acceleration, medium confidence — partial motion blur on the rotation |

## Where this feeds into the final prompt

Per `layer_contract.md`, the `actions` layer is judged independently from `camera`. When `actions: preserve`, this chart's beats become the action-description sentences in the final prompt's shot body, written as observable behavior (what the body visibly does) rather than as an inferred internal state ("she looks confident" is not something you extracted from the frames — "shoulders squared, chin lifted" is). When `actions: adapt`, keep this chart's timing and contact-event structure but re-describe the specific movement for the new subject/context. When `actions: replace`, this chart still tells you how much time the corresponding new action has to work with at each beat, even though its content is being rebuilt — the durations from the reference are a useful pacing reference even when the movement itself changes.
