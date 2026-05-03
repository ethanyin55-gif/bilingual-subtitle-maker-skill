---
name: bilingual-subtitle-maker
description: Create review-ready Chinese-English SRT subtitles from audio files, transcripts, or rough cuts. Use when Codex needs to transcribe interview/documentary audio with Whisper, translate English speech for Chinese-first reviewers, preserve source wording, do source-preserving cleanup only, segment captions, control line length, and validate .srt timing/text for edit-review workflows.
---

# Bilingual Subtitle Maker

Use this skill to produce review-copy subtitles, not final broadcast subtitles. Prioritize fast editorial usability: accurate timing, readable lines, preserved source meaning, and easy import into editing software.

## Inputs

Ask for or infer:

- Audio file path, or an existing transcript/SRT.
- Main topic and context for the clip.
- Keywords: names, brands, places, works, jargon, likely mishearings.
- Source language: English, Chinese, or mixed.
- Audience language. Default: Chinese-first reviewers.

Use `assets/subtitle-brief.md` as a lightweight intake template when the user wants a repeatable brief.

## Workflow

1. Transcribe with word timestamps when audio is available:

```bash
WHISPER_WORD_TIMESTAMPS=True zsh scripts/transcribe_audio.sh "/absolute/path/to/audio.mp3"
```

Set `WHISPER_LANGUAGE=en` or `WHISPER_LANGUAGE=zh` when the language is known. Add names and terms with `WHISPER_INITIAL_PROMPT`.

2. Treat Whisper as the ear, not the editor. Read the raw `.json` word timestamps and rough `.srt`; then create a human subtitle pass.

2.5. Verify language before translating:

- If a segment is spoken in Chinese, transcribe it directly as Chinese.
- Never take a Chinese segment misheard as English, then translate that English back into Chinese.
- In mixed or uncertain audio, inspect suspicious segments and run a Chinese-language pass on Chinese speech when needed.
- Treat language verification as mandatory for Chinese sections because mistranscribed English intermediates can drift far from the source.

3. Apply language policy:

- English speech: output two text lines, Chinese translation first and source-preserving English second.
- Chinese speech: output Chinese-only unless the user explicitly asks for bilingual subtitles.
- Mixed speech: English segments are bilingual; Chinese segments are Chinese-only by default.
- Before final delivery, reconcile mixed interview sections against raw Chinese-pass transcripts so recovered Chinese lines are not dropped during assembly.

4. Segment for subtitles, not transcripts:

- Cue in-time should start when the sentence begins, not when the semantic keyword appears.
- Cue out-time may hold slightly after speech for review readability.
- Time each cue independently from its own spoken burst.
- Do not derive cue N+1 from cue N's out-time if cue N may already be wrong.
- Split by actual spoken bursts, not by semantic full-sentence completion.
- If the speaker stops, breathes, trails off, or restarts, that is usually a subtitle break.
- Split by spoken pauses, sentence restarts, commas, or natural pauses.
- Subtitle timing is stricter than sentence completeness.
- Do not merge two spoken parts into one cue across a noticeable pause just to make a fuller sentence.
- Never bridge a multi-second silence between phrases or sentences.
- If one cue overlaps or crowds the next cue, treat that cue as the local timing error and re-check it against the source audio instead of pushing downstream cues later.
- Do not leave dangling one-word tails such as `me`, `it`, `that`, or `to me`.
- Keep English source as close to the speaker's actual wording as possible.
- Do not paraphrase, smooth, or replace phrasing just because a cleaner sentence sounds better.
- If a line is long, prefer splitting into another cue before compressing wording.
- Only compress wording as a last resort after splitting is no longer practical.

5. Clean English lightly:

- Remove `um`, `uh`, obvious stutters, immediate repeated words, and false starts that clearly do not change meaning.
- Keep meaningful discourse words when they affect tone, logic, character, or emphasis.
- Preserve names, dates, numbers, colloquial phrasing, and source wording as much as practical.
- Do not upgrade grammar, replace colloquial wording with neater wording, or substitute approximate equivalents such as changing `back in like 2018` into `around 2018` unless the user explicitly asks for cleanup beyond subtitle review use.

6. Enforce screen readability:

- Chinese first line: target 22 characters or fewer.
- English second line: hard target 50 characters or fewer so it stays one on-screen line.
- No sentence-ending punctuation on either line.
- Capitalize the first English letter of each subtitle line.

7. Validate review `.srt` files:

```bash
python3 scripts/validate_bilingual_srt.py "/path/to/final_bilingual.srt"
```

Use the warnings to revise line length, lowercase starts, terminal punctuation, timing overlaps, long cue durations, and suspicious cue gaps.

8. Run a completeness check on Chinese interview sections:

- For every range that was re-run with `WHISPER_LANGUAGE=zh`, compare the recovered raw transcript against the final `.srt`.
- If the raw Chinese pass contains usable subtitle text that is absent from the final `.srt`, treat that as an assembly bug and fix it before delivery.
- Do not mark the subtitle file complete while Chinese interview sections still have unexplained long gaps.
- Do not mark the subtitle file complete while unresolved overlap errors still exist; fix the conflicting cue itself rather than cascading later cue times.

## Resources

- `scripts/transcribe_audio.sh`: local Whisper transcription wrapper with word timestamp support.
- `scripts/validate_bilingual_srt.py`: structural and style validator for mixed review SRT files with zh-only and zh/en cues.
- `assets/subtitle-brief.md`: reusable intake brief.
- `references/style-guide.md`: compact style rules for review-copy bilingual subtitles.
