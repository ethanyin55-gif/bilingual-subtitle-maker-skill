# Review Subtitle Style Guide

## Output Shape

- English source audio: Chinese translation on line 1, English source on line 2.
- Chinese source audio: Chinese-only by default.
- Mixed audio: English segments bilingual; Chinese segments Chinese-only by default.
- Chinese speech must be transcribed directly in Chinese, not reconstructed by translating mistaken English ASR.
- Before delivery, compare Chinese review-pass transcript ranges against the final SRT so recovered Chinese lines are not dropped.
- Use `.srt` unless the user asks for another format.

## Timing

- Use word-level timestamps when possible.
- Start each cue when the spoken sentence or phrase begins.
- Time each cue independently from its own spoken burst.
- Segment by actual spoken bursts, not by semantic full-sentence completion.
- If the speaker stops, breathes, trails off, or restarts, the subtitle should usually break there.
- End cues at sentence ends, commas, or natural pauses.
- Subtitle timing is stricter than sentence completeness.
- Do not merge across a noticeable pause just to keep two related thoughts in one subtitle.
- Never hold one cue across a multi-second silence between spoken parts.
- If one cue overlaps the next, fix that cue against the audio instead of shifting all later cues.
- Review long inter-cue gaps carefully in interview sections; they may signal missing subtitles rather than true silence.
- Avoid transcript-like long blocks.
- Avoid mechanical splits that leave a single dangling word.

## Text

- Keep English as close to source wording and sentence shape as possible.
- Remove only meaningless fillers, obvious stutters, immediate repeats, and clear false starts that do not change meaning.
- Do not paraphrase, smooth, or swap in cleaner wording just because it reads better.
- Prefer another subtitle cue over rewriting the sentence.
- Do not remove meaningful hesitation when it matters to character or story.
- Translate for review clarity, not literary polish.
- Keep terminology consistent across the file.

## Line Limits

- Chinese: target 22 characters, review limit 28.
- English: target and review limit 50 characters.
- If English would wrap into two on-screen lines, split into another cue.

## Punctuation and Capitalization

- Do not use terminal punctuation at line ends.
- Internal commas are allowed when they improve reading.
- Capitalize the first English letter of each cue.
