#!/usr/bin/env python3
"""Fetch a YouTube video's public metadata and transcript.

Runs inside .github/workflows/video-transcript.yml on a GitHub runner because
the Claude Code sandbox cannot reach YouTube. Utility only: it prints what it
finds between clear markers and writes the same to --out-dir. It never writes
canon, mechanics, or anything under reference/ or mirrors/.
"""
import argparse
import json
import os
import re
import subprocess
import sys


def dump_meta(video_id: str) -> dict:
    url = f"https://www.youtube.com/watch?v={video_id}"
    proc = subprocess.run(
        ["yt-dlp", "--skip-download", "--dump-single-json", "--no-warnings", url],
        capture_output=True, text=True, check=False,
    )
    if proc.returncode != 0:
        print(f"yt-dlp metadata failed: {proc.stderr.strip()[:2000]}", file=sys.stderr)
        return {}
    return json.loads(proc.stdout)


def transcript_via_api(video_id: str, langs: list[str]) -> list[dict] | None:
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        return None
    try:
        api = YouTubeTranscriptApi()
        fetched = api.fetch(video_id, languages=langs)
        return [{"start": s.start, "duration": s.duration, "text": s.text} for s in fetched]
    except Exception as exc:  # noqa: BLE001 - report and fall back
        print(f"youtube-transcript-api failed: {exc!r}"[:2000], file=sys.stderr)
        return None


def transcript_via_ytdlp(video_id: str, langs: list[str], out_dir: str) -> list[dict] | None:
    url = f"https://www.youtube.com/watch?v={video_id}"
    proc = subprocess.run(
        [
            "yt-dlp", "--skip-download", "--write-subs", "--write-auto-subs",
            "--sub-langs", ",".join(langs), "--sub-format", "vtt", "--no-warnings",
            "-o", os.path.join(out_dir, "%(id)s.%(ext)s"), url,
        ],
        capture_output=True, text=True, check=False,
    )
    if proc.returncode != 0:
        print(f"yt-dlp subtitles failed: {proc.stderr.strip()[:2000]}", file=sys.stderr)
    vtts = sorted(f for f in os.listdir(out_dir) if f.endswith(".vtt"))
    if not vtts:
        return None
    lines: list[dict] = []
    last = None
    ts = re.compile(r"^(\d\d):(\d\d):(\d\d)\.(\d{3}) --> ")
    with open(os.path.join(out_dir, vtts[0]), encoding="utf-8") as fh:
        start = 0.0
        for raw in fh:
            raw = raw.rstrip("\n")
            m = ts.match(raw)
            if m:
                h, mi, s, ms = (int(x) for x in m.groups())
                start = h * 3600 + mi * 60 + s + ms / 1000
                continue
            if not raw or raw.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")):
                continue
            text = re.sub(r"<[^>]+>", "", raw).strip()
            if text and text != last:
                lines.append({"start": start, "duration": 0.0, "text": text})
                last = text
    return lines


def fmt_time(seconds: float) -> str:
    seconds = int(seconds)
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--video-id", required=True)
    ap.add_argument("--languages", default="en,en-US,en-GB")
    ap.add_argument("--out-dir", default="transcript_out")
    args = ap.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)
    langs = [x.strip() for x in args.languages.split(",") if x.strip()]

    meta = dump_meta(args.video_id)
    keep = {
        k: meta.get(k) for k in (
            "id", "title", "channel", "uploader", "upload_date", "duration_string",
            "view_count", "like_count", "categories", "tags", "chapters", "description",
        )
    }
    with open(os.path.join(args.out_dir, "metadata.json"), "w", encoding="utf-8") as fh:
        json.dump(keep, fh, indent=2, ensure_ascii=False)

    print("=== VIDEO METADATA BEGIN ===")
    for k in ("id", "title", "channel", "uploader", "upload_date", "duration_string", "view_count", "like_count", "categories", "tags"):
        print(f"{k}: {keep.get(k)}")
    if keep.get("chapters"):
        print("chapters:")
        for ch in keep["chapters"]:
            print(f"  {fmt_time(ch.get('start_time', 0))}  {ch.get('title')}")
    print("description:")
    print(keep.get("description") or "(none)")
    print("=== VIDEO METADATA END ===")

    lines = transcript_via_api(args.video_id, langs) or transcript_via_ytdlp(args.video_id, langs, args.out_dir)
    print("=== TRANSCRIPT BEGIN ===")
    if not lines:
        print("(no transcript available)")
    else:
        with open(os.path.join(args.out_dir, "transcript.txt"), "w", encoding="utf-8") as fh:
            for seg in lines:
                row = f"[{fmt_time(seg['start'])}] {seg['text']}"
                print(row)
                fh.write(row + "\n")
    print("=== TRANSCRIPT END ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
