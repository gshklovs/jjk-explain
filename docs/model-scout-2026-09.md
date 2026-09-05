# Video model scout — Sep 2026

Goal: cut cost-per-clip for seeded, talking-character shots below the current
MiniMax H3-Max `reference-to-video` baseline of **$0.08/s**. Findings below are
from fal.ai model pages (WebFetch/WebSearch only, no browser). Anything not
directly confirmed on a model page is flagged **[unverified]**.

## 1. MiniMax updates on fal

| Endpoint | Price/s | Refs | Notes |
|---|---|---|---|
| `minimax/h3-max/reference-to-video` (current pipeline model) | **$0.05 @480p / $0.08 @768p** | up to 12 files total (images+video+audio); first 4,096 tokens of refs free (~4 imgs @1024px), then $0.02/1k tokens; audio ≈$0.0016/s | Seed supported. Lip-sync described as "precise and natural." **This is cheaper than assumed** — 480p reference-to-video is $0.05/s, not $0.08/s flat. https://fal.ai/models/minimax/h3-max/reference-to-video |
| `minimax/h3/reference-to-video` (base H3, non-Max) | **$0.05 @480p / $0.06 @768p / $0.13 @2K / $0.16 @4K** | up to 9 images + 3 video clips + 3 audio clips; first 5 images free, then $0.08 each | Same reference/audio/lip-sync mechanism as Max, one quality tier down. https://fal.ai/models/minimax/h3/reference-to-video |
| `fal.ai/minimax-h3-max` landing page (turbo text/image-to-video) | $0.08/s @768p, **50% off first 14 days** ($0.04/s) | — | Landing page says reference-to-video "coming this week" — likely stale copy; the dedicated model page above is live and authoritative. Free tier: 5 gens/day up to 15s. https://fal.ai/minimax-h3-max **[unverified: promo end date, whether landing-page staleness affects reference-to-video availability]** |

**Actionable takeaway:** switching 480p reference-to-video shots from the assumed $0.08/s to the actual $0.05/s (H3-Max) saves 37% on every likeness/lip-sync shot with no quality tier change. Base H3 (non-Max) reference-to-video is cheaper still at $0.05-0.06/s but is one model generation behind Max in aesthetics/prompt-following.

## 2. Other fal.ai video models (reference/likeness + audio)

| Endpoint | Price/s (10s clip) | Max dur | Ref images | Ref video | Ref audio / lip-sync / native speech | Seed | Native audio | Notes |
|---|---|---|---|---|---|---|---|---|
| Kling 2.5 Turbo Pro (i2v) | $0.07/s ($0.35 base 5s + $0.07/s extra) | not stated | start+tail frame only | no | no | not documented | native audio gen (per search, unconfirmed on fetched page) | Cheaper than MiniMax turbo but **no multi-reference/elements on this specific endpoint** — elements live on Kling O1. https://fal.ai/models/fal-ai/kling-video/v2.5-turbo/pro/image-to-video |
| Kling O1 Reference-to-Video | $0.112/s (5s=$0.56, 10s=$1.12) | 5 or 10s | multi "elements," each with 1 frontal + multiple angle refs | no | not confirmed | not documented | not confirmed | Element-level identity lock, pricier than MiniMax H3 ref but has richer multi-angle character refs. https://fal.ai/models/fal-ai/kling-video/o1/reference-to-video |
| Kling O1 Video-to-Video Reference | $0.168/s (5s=$0.84,10s=$1.68) | 5/10s | up to 4 char/element images + style ref | yes (base ref video) | not confirmed | not documented | not confirmed | https://fal.ai/models/fal-ai/kling-video/o1/video-to-video/reference |
| Wan 2.7 reference-to-video | $0.10/s | ≥10s shown | ≥1 image | yes | not confirmed on this endpoint (Wan 2.5 docs elsewhere claim voice/ambience sync) | yes (seed present in output) | claimed elsewhere for Wan 2.5 | Pricier than MiniMax H3-Max 480p; **not cheaper**, skip. https://fal.ai/models/fal-ai/wan/v2.7/reference-to-video |
| Seedance 2.5 reference-to-video | ~$0.021/1k tokens ≈ **~$0.03-0.05/s effective at 480/720p** for typical frame sizes (token formula: h×w×(in+out dur)×24/1024) | up to 30s single pass | up to 50 combined images/video/audio/style refs | yes | audio used as "timing signal," lip-sync not explicitly confirmed | yes, explicit `seed` param | generates audio "jointly" with video | Cheapest-looking per-second among quality references, but pricing is token/resolution-dependent — needs a real cost calc before committing (see caveat below). https://fal.ai/models/bytedance/seedance-2.5/reference-to-video **[unverified: actual $/s at your resolution, exact lip-sync fidelity]** |
| Veo 3 / 3 Fast | Fast: $0.10-0.15/s; full: $0.20-0.40/s | — | none confirmed for likeness ref | no | no | — | yes | Too expensive and no reference/likeness support — drop from consideration. https://fal.ai/models/fal-ai/veo3.1 |
| LTX-2.3 / 2.5 | 2.3: $0.06-0.24/s by res; 2.5 Fast: $0.09-0.30/s | up to 20s | not primarily reference-driven | audio-to-video variant exists | native audio at every resolution, but not built for face/likeness lip-sync | not confirmed | yes, native | Good for cheap ambience/native audio on non-talking shots, not a likeness/lip-sync tool. https://fal.ai/ltx-2.5 |

## 3. Dedicated talking-avatar / lip-sync endpoints (hybrid route candidates)

These animate a still image + audio, or dub an existing silent clip — the basis for a "turbo silent clip + cheap dub" hybrid.

| Endpoint | Price | Input | Notes |
|---|---|---|---|
| Kling AI Avatar v2 Standard | **$0.0562/s** | 1 image + 1 audio file | Video length = audio length. Lip-sync described as core feature ("audio-matched facial movements"). Cheapest quality talking-head option found. https://fal.ai/models/fal-ai/kling-video/ai-avatar/v2/standard |
| Kling AI Avatar v2 Pro | $0.115/s | image + audio | Finer lip-sync, ~2x Standard price. https://fal.ai/models/fal-ai/kling-video/ai-avatar/v2/pro |
| Bytedance OmniHuman (v1) | $0.14/s | image + audio | https://fal.ai/models/fal-ai/bytedance/omnihuman |
| Bytedance OmniHuman v1.5 | $0.16/s | image + audio | 720p/1080p, 60s audio support, turbo mode. Pricier than Avatar v2. https://fal.ai/models/fal-ai/bytedance/omnihuman/v1.5 |
| PixVerse Lipsync | ~$0.04/s (one source) or $0.10-0.14/s (another, conflicting) | existing video + audio | **[unverified — conflicting price reports, re-check model page before relying on it]**. https://fal.ai/models/fal-ai/pixverse/lipsync |
| Sync Lipsync v2 / v2 Pro | $3/min ($0.05/s) standard tier; Pro $5/min ($0.083/s) | existing video + audio | Post-hoc dub of an existing silent clip — could dub a MiniMax turbo output. https://fal.ai/models/fal-ai/sync-lipsync/v2 |
| Sync Lipsync (v1) | $0.7/min ≈ **$0.0117/s** | existing video + audio | Cheapest post-hoc dub found, older/lower quality tier. https://fal.ai/models/fal-ai/sync-lipsync |
| LatentSync | $0.2 flat up to 40s, then $0.005/s | existing video + audio | Extremely cheap for dubbing but open-source model, likely lower fidelity than Sync v2. https://fal.ai/models/fal-ai/latentsync |
| VEED Lipsync v2 | $0.07/s | existing video + audio | https://fal.ai/veed-lipsync-v2 |

## 4. Ranked recommendations for a seeded, talking-character 6-shot / 70s video

Assume: 2 of 6 shots need character likeness + speech (the "hero" close-ups, ~10s each = 20s), 4 shots are silent/ambient turbo (~50s total).

**Route A — switch resolution tier only (near-zero effort).**
Use `minimax/h3-max/reference-to-video` at 480p instead of 768p for the 2 speaking shots: $0.05/s × 20s = **$1.00** (vs $1.60 today at 768p). Plus 4 turbo shots at $0.025-0.04/s × 50s ≈ $1.25-2.00. **Total ≈ $2.25-3.00**, down from ~$5-7. No pipeline change beyond a resolution flag — do this first regardless of anything else below.

**Route B — hybrid: turbo silent + Kling AI Avatar v2 Standard dub for speaking shots.**
Render the 2 speaking shots on MiniMax turbo (silent, image-to-video, seeded on the character stills) at $0.025-0.04/s × 20s ≈ $0.50-0.80, then animate a matching still separately with Kling AI Avatar v2 Standard driven by the Fish TTS line: $0.0562/s × 20s ≈ **$1.12**. Combine: **≈$1.6-1.9** for the speaking portion + $1.25-2.00 for the 4 ambient turbo shots = **Total ≈ $2.9-3.9**. Slightly more than Route A and adds a compositing step (avatar output is a talking head, not the full turbo scene), so it's best when a close-up talking-head cutaway is acceptable rather than requiring the character to speak while moving/acting in the wider scene.

**Route C — hybrid: turbo silent full-scene + Sync Lipsync v1 post-hoc dub.**
Render the 2 speaking shots fully on turbo (character moving/acting silently, seeded on stills), then run Sync Lipsync v1 over that output with the Fish TTS audio to dub the mouth: turbo $0.50-0.80 + Sync v1 dub at $0.0117/s × 20s ≈ $0.23 = **≈$0.73-1.03** for the speaking portion, plus $1.25-2.00 ambient = **Total ≈ $2.0-3.0**. Cheapest full-scene-preserving route found, but Sync v1 is the older/lower-fidelity lip-sync tier — quality risk on lip accuracy is real and should be spot-checked before committing. **[unverified: Sync v1 fidelity against MiniMax's own reference-audio lip-sync]**

**Overall ranking:**
1. **Route A** (just use 480p on the existing H3-Max reference endpoint) — lowest effort, ~55-60% cost cut, zero new integration risk. Do this immediately.
2. **Route C** (turbo + Sync v1 dub) — best cost if lip fidelity holds up on review; adds one API call and a stitch step.
3. **Route B** (turbo + Kling Avatar v2 Standard) — best if a talking-head cutaway shot is acceptable; slightly pricier and requires either a cutaway edit or a compositing step to keep the wider scene.

**Not recommended:** Wan 2.7 ($0.10/s, no cost advantage), Veo 3 (too expensive, no reference support), Kling O1 elements (richer refs but $0.11-0.17/s, pricier than MiniMax at 480p for this use case). Seedance 2.5 looked promising on paper (per-token pricing, up to 50 refs, 30s single-pass, explicit seed) but its cost per second depends on your exact resolution/frame math and its lip-sync fidelity is not explicitly confirmed — worth a real test render before trusting the number above.

## Caveats / unverified items
- Seedance 2.5 effective $/s is a formula, not a flat rate — get a real number by running the token math at your target resolution.
- PixVerse Lipsync price conflicts between sources ($0.04/s vs $0.10-0.14/s) — recheck before use.
- MiniMax H3-Max landing page says reference-to-video is "coming this week," but the dedicated reference-to-video model page is live with pricing — likely stale marketing copy, not a real gap.
- No fal promo/discount found for MiniMax H3-Max **reference-to-video** specifically (the 50% intro discount mentioned is on the base turbo text/image-to-video landing page, unclear if it extends to reference-to-video).
- Did not check Replicate — ran out of budget after fal.ai came back with a clear win (Route A). Worth a follow-up pass if Replicate pricing is needed for comparison.
