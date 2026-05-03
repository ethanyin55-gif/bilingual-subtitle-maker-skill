# Bilingual Subtitle Maker Skill

Bilingual Subtitle Maker is a Codex skill for creating review-ready Chinese-English `.srt` subtitles from interview, documentary, and creator-economy video audio.

It covers the full path from audio to subtitle file: local Whisper transcription, word-level timing, subtitle-aware segmentation, Chinese-first bilingual subtitle creation, source-preserving cleanup of English speech, practical line-length control, and SRT validation before import into editing software.

The skill is designed for edit-review workflows rather than final broadcast delivery. It helps editors quickly produce readable bilingual subtitles for watching, reviewing, and revising a cut, while preserving the original speaker's wording as much as possible.

## What It Does

- Transcribes audio with local Whisper and word-level timestamps
- Turns transcript-like output into subtitle-like cues
- Produces Chinese-over-English bilingual SRT for English speech
- Keeps Chinese speech Chinese-only by default
- Removes only low-information speech clutter such as `um`, `uh`, obvious stutters, and accidental immediate repeats
- Avoids dangling one-word subtitle tails
- Keeps English to one on-screen line, targeting 50 characters or fewer
- Removes sentence-ending punctuation and capitalizes English line starts
- Validates SRT numbering, timing, line count, line length, punctuation, and capitalization

## Install

With the Codex skills installer:

```bash
npx skills add https://github.com/ethanyin55-gif/bilingual-subtitle-maker-skill --global
```

Manual install:

```bash
mkdir -p ~/.codex/skills
cp -R skills/bilingual-subtitle-maker ~/.codex/skills/
```

## Requirements

The transcription helper uses local Whisper:

```bash
python3 -m pip install -U openai-whisper
```

Whisper also needs `ffmpeg`:

```bash
brew install ffmpeg
```

Models are cached by default in:

```bash
${XDG_CACHE_HOME:-$HOME/.cache}/whisper
```

Set `WHISPER_MODEL_DIR` if you want a different shared model cache.

## Quick Start

Ask Codex:

```text
Use $bilingual-subtitle-maker to create bilingual subtitles.
Audio: /absolute/path/to/interview.mp3
Topic: A designer discusses a product collaboration
Keywords: speaker names, brand names, product names, locations
Audience: Chinese-first reviewers
```

Codex can run:

```bash
WHISPER_WORD_TIMESTAMPS=True \
WHISPER_LANGUAGE=en \
WHISPER_INITIAL_PROMPT="brand names, people names, product names" \
zsh skills/bilingual-subtitle-maker/scripts/transcribe_audio.sh "/absolute/path/to/audio.mp3"
```

Then Codex edits the raw transcript into a final `.srt` and validates it:

```bash
python3 skills/bilingual-subtitle-maker/scripts/validate_bilingual_srt.py "/path/to/final_bilingual.srt"
```

## Example Request

```text
Use $bilingual-subtitle-maker to create review-ready bilingual SRT subtitles.

Audio: /absolute/path/to/founder-interview.mp3
Topic: An independent designer talks about building a toy brand and working with manufacturing partners
Keywords: designer name, brand name, product line name, city names, factory terms
Audience: Chinese-first reviewers
Style: Natural documentary subtitles, not final broadcast copy
```

## Example Output

```srt
1
00:00:00,000 --> 00:00:02,860
我叫 Maya Chen
So my name is Maya Chen

2
00:00:03,640 --> 00:00:06,200
我是这个玩具品牌的创作者
I am the creator of this toy brand

3
00:00:06,360 --> 00:00:10,420
我们最早是在 2021 年开始合作
We first started working together in 2021
```

## Subtitle Rules

- English speech: Chinese line first, English source line second
- Chinese speech: Chinese-only by default
- English source: preserve original wording and sentence shape whenever possible
- English cleanup: remove only obvious fillers, stutters, false starts, and immediate repeats that do not change meaning
- Do not paraphrase, smooth, rewrite, or swap in cleaner phrasing just because it reads better
- If a line is too long, prefer splitting into another cue before compressing wording
- Subtitle timing takes priority over sentence merging
- Do not merge two spoken parts into one cue across a noticeable pause
- Never bridge a multi-second silence just to keep a fuller sentence together
- English line length: 50 characters or fewer
- Chinese line length: target 22 characters, review limit 28
- No terminal punctuation at line ends
- English line starts are capitalized
- Split at sentences, commas, and natural pauses
- Do not leave dangling tails such as `me`, `it`, `that`, or `to me`

## Privacy

This repo contains workflow instructions and helper scripts only. Do not commit audio, raw transcripts, client footage, generated subtitles, model files, or private project briefs.

## License

MIT License. See `LICENSE`.

## Repository Layout

```text
skills/bilingual-subtitle-maker/
├── SKILL.md
├── agents/openai.yaml
├── assets/subtitle-brief.md
├── references/style-guide.md
└── scripts/
    ├── transcribe_audio.sh
    └── validate_bilingual_srt.py
```

## Repository Description

A Codex skill for turning audio into review-ready Chinese-English SRT subtitles with Whisper transcription, subtitle-aware segmentation, translation guidance, and validation.
