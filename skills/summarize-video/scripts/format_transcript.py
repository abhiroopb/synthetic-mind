#!/usr/bin/env python3
"""Convert SRT transcript to readable markdown with periodic timestamp links.

Usage: python3 format_transcript.py <srt_file> <video_url> [--interval SECONDS] [-o OUTPUT]
"""

import argparse
import re


def parse_srt(text):
    """Parse SRT into list of (start_seconds, text) entries."""
    entries = []
    blocks = re.split(r"\n\n+", text.strip())
    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue
        ts_match = re.match(r"(\d{2}):(\d{2}):(\d{2})", lines[1])
        if not ts_match:
            continue
        h, m, s = int(ts_match.group(1)), int(ts_match.group(2)), int(ts_match.group(3))
        secs = h * 3600 + m * 60 + s
        txt = " ".join(line.strip() for line in lines[2:] if line.strip())
        entries.append((secs, txt))
    return entries


def fmt_ts(secs):
    h, rem = divmod(secs, 3600)
    m, s = divmod(rem, 60)
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def group_paragraphs(entries, interval):
    """Group entries into paragraphs by time interval."""
    paragraphs = []
    current_texts = []
    para_start = 0

    for secs, txt in entries:
        if current_texts and secs - para_start >= interval:
            paragraphs.append((para_start, " ".join(current_texts)))
            current_texts = []
            para_start = secs
        if not current_texts:
            para_start = secs
        current_texts.append(txt)

    if current_texts:
        paragraphs.append((para_start, " ".join(current_texts)))

    return paragraphs


def main():
    parser = argparse.ArgumentParser(description="Convert SRT to markdown with timestamp links")
    parser.add_argument("srt_file", help="Path to SRT file")
    parser.add_argument("video_url", help="Base video URL for timestamp links")
    parser.add_argument("--interval", type=int, default=30, help="Seconds between paragraphs (default: 30)")
    parser.add_argument("-o", "--output", default="transcript.md", help="Output file (default: transcript.md)")
    parser.add_argument("--title", default=None, help="Video title for the header")
    args = parser.parse_args()

    with open(args.srt_file) as f:
        srt = f.read()

    entries = parse_srt(srt)
    paragraphs = group_paragraphs(entries, args.interval)

    title = args.title or "Transcript"
    lines = [
        f"# {title} - Transcript\n",
        f"> [Watch Video]({args.video_url})\n",
        "---\n",
    ]

    for start, text in paragraphs:
        ts_link = f"[{fmt_ts(start)}]({args.video_url}?st={start})"
        lines.append(f"**{ts_link}** {text}\n")

    md = "\n".join(lines)
    with open(args.output, "w") as f:
        f.write(md)

    print(f"Written {args.output}: {len(md)} chars, {len(paragraphs)} paragraphs")


if __name__ == "__main__":
    main()
