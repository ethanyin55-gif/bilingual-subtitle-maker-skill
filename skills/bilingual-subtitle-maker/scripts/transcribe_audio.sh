#!/usr/bin/env zsh
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  zsh tools/subtitles/scripts/transcribe_audio.sh /absolute/path/to/audio.wav

Optional environment variables:
  WHISPER_MODEL=tiny|base|small|medium|large|turbo  Default: turbo
  WHISPER_MODEL_DIR=/path/to/model/cache              Default: ${XDG_CACHE_HOME:-$HOME/.cache}/whisper
  WHISPER_LANGUAGE=en|zh|auto                       Default: auto
  WHISPER_WORD_TIMESTAMPS=True|False                Default: False
  WHISPER_INITIAL_PROMPT="keyword list"             Default: empty
  SUBTITLE_OUT_DIR=output/subtitles                 Default: output/subtitles
USAGE
}

if [[ $# -lt 1 ]]; then
  usage
  exit 2
fi

audio_path="$1"

if [[ ! -f "$audio_path" ]]; then
  echo "Audio file not found: $audio_path" >&2
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required but was not found." >&2
  exit 1
fi

if ! python3 -c "import whisper" >/dev/null 2>&1; then
  echo "Python package 'whisper' is not installed for python3." >&2
  echo "Do not install automatically; confirm the environment first." >&2
  exit 1
fi

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "ffmpeg is required by Whisper but was not found." >&2
  exit 1
fi

model="${WHISPER_MODEL:-turbo}"
language="${WHISPER_LANGUAGE:-auto}"
initial_prompt="${WHISPER_INITIAL_PROMPT:-}"
out_root="${SUBTITLE_OUT_DIR:-output/subtitles}"
default_cache="${XDG_CACHE_HOME:-$HOME/.cache}/whisper"
model_dir="${WHISPER_MODEL_DIR:-$default_cache}"
word_timestamps="${WHISPER_WORD_TIMESTAMPS:-False}"

base_name="$(basename "$audio_path")"
stem="${base_name%.*}"
safe_stem="${stem//[^A-Za-z0-9._-]/_}"
run_id="$(date +%Y%m%d-%H%M%S)"
out_dir="${out_root}/${safe_stem}-${run_id}/whisper_raw"

mkdir -p "$out_dir" "$model_dir"

args=(
  python3 -m whisper "$audio_path"
  --model "$model"
  --model_dir "$model_dir"
  --output_dir "$out_dir"
  --output_format all
  --task transcribe
  --condition_on_previous_text False
  --word_timestamps "$word_timestamps"
)

if [[ "$language" != "auto" ]]; then
  args+=(--language "$language")
fi

if [[ -n "$initial_prompt" ]]; then
  args+=(--initial_prompt "$initial_prompt")
fi

echo "Audio: $audio_path"
echo "Model: $model"
echo "Model dir: $model_dir"
echo "Language: $language"
echo "Word timestamps: $word_timestamps"
echo "Output: $out_dir"

"${args[@]}"

echo
echo "Whisper raw outputs:"
echo "$out_dir"
