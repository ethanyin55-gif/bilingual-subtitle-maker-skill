---
name: bilingual-subtitle-maker
description: Create review-ready Chinese-English SRT subtitles from audio files, transcripts, or rough cuts. Use when Codex needs to transcribe interview/documentary audio with Whisper, translate English speech for Chinese-first reviewers, preserve source wording, clean filler words, segment captions, control line length, and validate .srt timing/text for edit-review workflows.
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

3. Apply language policy:

- English speech: output two text lines, Chinese translation first and cleaned English source second.
- Chinese speech: output Chinese-only unless the user explicitly asks for bilingual subtitles.
- Mixed speech: English segments are bilingual; Chinese segments are Chinese-only by default.

4. Segment for subtitles, not transcripts:

- Cue in-time should start when the sentence begins, not when the semantic keyword appears.
- Cue out-time may hold slightly after speech for review readability.
- Split by sentence, comma, or natural pause.
- Do not leave dangling one-word tails such as `me`, `it`, `that`, or `to me`.
- Keep English source close to the speaker. Do not paraphrase unless line length forces a small compression.

5. Clean English lightly:

- Remove `um`, `uh`, repeated accidental words, and obvious false starts.
- Keep meaningful discourse words when they affect tone or logic.
- Preserve names, dates, numbers, and source phrasing as much as practical.

6. Enforce screen readability:

- Chinese first line: target 22 characters or fewer.
- English second line: hard target 50 characters or fewer so it stays one on-screen line.
- No sentence-ending punctuation on either line.
- Capitalize the first English letter of each subtitle line.

7. Validate bilingual `.srt` files:

```bash
python3 scripts/validate_bilingual_srt.py "/path/to/final_bilingual.srt"
```

Use the warnings to revise line length, lowercase starts, terminal punctuation, or timing overlaps.

## Resources

- `scripts/transcribe_audio.sh`: local Whisper transcription wrapper with word timestamp support.
- `scripts/validate_bilingual_srt.py`: structural and style validator for Chinese-English two-line SRT files.
- `assets/subtitle-brief.md`: reusable intake brief.
- `references/style-guide.md`: compact style rules for review-copy bilingual subtitles.
