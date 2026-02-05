#!/usr/bin/env python3
"""
YouTube Design Concept Extractor
=================================
Extracts transcript + keyframes from a YouTube video and produces
a structured markdown reference document ready for agent consumption.

Usage:
    python3 tools/yt-design-extractor.py <youtube_url> [options]

Examples:
    python3 tools/yt-design-extractor.py "https://youtu.be/eVnQFWGDEdY"
    python3 tools/yt-design-extractor.py "https://youtu.be/eVnQFWGDEdY" --interval 30
    python3 tools/yt-design-extractor.py "https://youtu.be/eVnQFWGDEdY" --scene-detect
    python3 tools/yt-design-extractor.py "https://youtu.be/eVnQFWGDEdY" --interval 15 --scene-detect

Requirements:
    pip install yt-dlp youtube-transcript-api Pillow
    apt install ffmpeg
"""

import argparse
import json
import os
import re
import subprocess
import sys
import textwrap
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Transcript extraction
# ---------------------------------------------------------------------------

def extract_video_id(url: str) -> str:
    """Pull the 11-char video ID out of any common YouTube URL format."""
    patterns = [
        r"(?:v=|/v/|youtu\.be/)([a-zA-Z0-9_-]{11})",
        r"(?:embed/)([a-zA-Z0-9_-]{11})",
        r"(?:shorts/)([a-zA-Z0-9_-]{11})",
    ]
    for pat in patterns:
        m = re.search(pat, url)
        if m:
            return m.group(1)
    # Maybe the user passed a bare ID
    if re.match(r"^[a-zA-Z0-9_-]{11}$", url):
        return url
    sys.exit(f"Could not extract video ID from: {url}")


def get_video_metadata(url: str) -> dict:
    """Use yt-dlp to pull title, description, chapters, duration, etc."""
    cmd = [
        "yt-dlp",
        "--dump-json",
        "--no-download",
        "--no-playlist",
        url,
    ]
    print("[*] Fetching video metadata …")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        sys.exit(f"yt-dlp metadata failed:\n{result.stderr}")
    return json.loads(result.stdout)


def get_transcript(video_id: str) -> list[dict] | None:
    """Grab the transcript via youtube-transcript-api. Returns list of
    {text, start, duration} dicts, or None if unavailable."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        print("[*] Fetching transcript …")
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id)
        # Convert FetchedTranscript to list of dicts
        entries = []
        for snippet in transcript:
            entries.append({
                "text": snippet.text,
                "start": snippet.start,
                "duration": snippet.duration,
            })
        return entries
    except Exception as e:
        print(f"[!] Transcript unavailable ({e}). Will proceed without it.")
        return None


# ---------------------------------------------------------------------------
# Keyframe extraction
# ---------------------------------------------------------------------------

def download_video(url: str, out_dir: Path) -> Path:
    """Download the video at 720p max to keep file size sane."""
    out_template = str(out_dir / "video.%(ext)s")
    cmd = [
        "yt-dlp",
        "-f", "bestvideo[height<=720]+bestaudio/best[height<=720]/best",
        "--merge-output-format", "mp4",
        "-o", out_template,
        "--no-playlist",
        url,
    ]
    print("[*] Downloading video (720p max) …")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    if result.returncode != 0:
        sys.exit(f"yt-dlp download failed:\n{result.stderr}")

    # Find the downloaded file
    for f in out_dir.iterdir():
        if f.name.startswith("video.") and f.suffix in (".mp4", ".mkv", ".webm"):
            return f
    sys.exit("Download succeeded but could not locate video file.")


def extract_frames_interval(video_path: Path, out_dir: Path,
                            interval: int = 30) -> list[Path]:
    """Extract one frame every `interval` seconds."""
    frames_dir = out_dir / "frames"
    frames_dir.mkdir(exist_ok=True)
    pattern = str(frames_dir / "frame_%04d.png")
    cmd = [
        "ffmpeg", "-i", str(video_path),
        "-vf", f"fps=1/{interval}",
        "-q:v", "2",
        pattern,
        "-y",
    ]
    print(f"[*] Extracting frames every {interval}s …")
    subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    frames = sorted(frames_dir.glob("frame_*.png"))
    print(f"    → captured {len(frames)} frames")
    return frames


def extract_frames_scene(video_path: Path, out_dir: Path,
                         threshold: float = 0.3) -> list[Path]:
    """Use ffmpeg scene-change detection to grab visually distinct frames."""
    frames_dir = out_dir / "frames_scene"
    frames_dir.mkdir(exist_ok=True)
    pattern = str(frames_dir / "scene_%04d.png")
    cmd = [
        "ffmpeg", "-i", str(video_path),
        "-vf", f"select='gt(scene,{threshold})',showinfo",
        "-vsync", "vfr",
        "-q:v", "2",
        pattern,
        "-y",
    ]
    print(f"[*] Extracting scene-change frames (threshold={threshold}) …")
    subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    frames = sorted(frames_dir.glob("scene_*.png"))
    print(f"    → captured {len(frames)} scene-change frames")
    return frames


# ---------------------------------------------------------------------------
# Markdown assembly
# ---------------------------------------------------------------------------

def fmt_timestamp(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def group_transcript(entries: list[dict], chunk_seconds: int = 60) -> list[dict]:
    """Merge transcript snippets into chunks of roughly `chunk_seconds`."""
    if not entries:
        return []
    groups = []
    current = {"start": entries[0]["start"], "text": ""}
    for e in entries:
        if e["start"] - current["start"] >= chunk_seconds and current["text"]:
            groups.append(current)
            current = {"start": e["start"], "text": ""}
        current["text"] += " " + e["text"]
    if current["text"]:
        groups.append(current)
    for g in groups:
        g["text"] = g["text"].strip()
    return groups


def build_markdown(meta: dict, transcript: list[dict] | None,
                   interval_frames: list[Path], scene_frames: list[Path],
                   out_dir: Path, interval: int) -> Path:
    """Assemble the final reference markdown document."""
    title = meta.get("title", "Untitled Video")
    channel = meta.get("channel", meta.get("uploader", "Unknown"))
    duration = meta.get("duration", 0)
    description = meta.get("description", "")
    chapters = meta.get("chapters") or []
    video_url = meta.get("webpage_url", "")
    tags = meta.get("tags") or []

    lines: list[str] = []

    # --- Header ---
    lines.append(f"# {title}\n")
    lines.append(f"> **Source:** [{channel}]({video_url})  ")
    lines.append(f"> **Duration:** {fmt_timestamp(duration)}  ")
    lines.append(f"> **Extracted:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  ")
    if tags:
        lines.append(f"> **Tags:** {', '.join(tags[:15])}")
    lines.append("")

    # --- Description ---
    if description:
        lines.append("## Video Description\n")
        # Trim excessively long descriptions
        desc = description[:3000]
        lines.append(f"```\n{desc}\n```\n")

    # --- Chapters ---
    if chapters:
        lines.append("## Chapters\n")
        lines.append("| Timestamp | Title |")
        lines.append("|-----------|-------|")
        for ch in chapters:
            ts = fmt_timestamp(ch.get("start_time", 0))
            lines.append(f"| `{ts}` | {ch.get('title', '')} |")
        lines.append("")

    # --- Transcript ---
    if transcript:
        grouped = group_transcript(transcript, chunk_seconds=60)
        lines.append("## Transcript\n")
        lines.append("<details><summary>Full transcript (click to expand)</summary>\n")
        for g in grouped:
            ts = fmt_timestamp(g["start"])
            lines.append(f"**[{ts}]** {g['text']}\n")
        lines.append("</details>\n")

        # Also create a condensed key-points section with timestamps
        lines.append("## Transcript (Condensed Segments)\n")
        lines.append("Use these timestamped segments to cross-reference with frames.\n")
        for g in grouped:
            ts = fmt_timestamp(g["start"])
            # First ~200 chars of each chunk as a preview
            preview = g["text"][:200]
            if len(g["text"]) > 200:
                preview += " …"
            lines.append(f"- **`{ts}`** — {preview}")
        lines.append("")

    # --- Keyframes ---
    all_frames = []
    if interval_frames:
        lines.append(f"## Keyframes (every {interval}s)\n")
        lines.append("Visual reference frames captured at regular intervals.\n")
        for i, f in enumerate(interval_frames):
            rel = os.path.relpath(f, out_dir)
            ts = fmt_timestamp(i * interval)
            lines.append(f"### Frame at `{ts}`\n")
            lines.append(f"![frame-{ts}]({rel})\n")
            all_frames.append((ts, rel))
        lines.append("")

    if scene_frames:
        lines.append("## Scene-Change Frames\n")
        lines.append("Frames captured when the visual content changed significantly.\n")
        for i, f in enumerate(scene_frames):
            rel = os.path.relpath(f, out_dir)
            lines.append(f"### Scene {i+1}\n")
            lines.append(f"![scene-{i+1}]({rel})\n")
        lines.append("")

    # --- Frame index (for quick reference) ---
    if all_frames:
        lines.append("## Frame Index\n")
        lines.append("| Timestamp | File |")
        lines.append("|-----------|------|")
        for ts, rel in all_frames:
            lines.append(f"| `{ts}` | `{rel}` |")
        lines.append("")

    # --- Footer ---
    lines.append("---\n")
    lines.append("*Generated by `yt-design-extractor.py` — review and curate ")
    lines.append("the content above, then feed this file to your agent.*\n")

    md_path = out_dir / "extracted-reference.md"
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[✓] Markdown reference written to {md_path}")
    return md_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Extract design concepts from a YouTube video into a "
                    "structured markdown reference document.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              %(prog)s "https://youtu.be/eVnQFWGDEdY"
              %(prog)s "https://youtu.be/eVnQFWGDEdY" --interval 15 --scene-detect
              %(prog)s "https://youtu.be/eVnQFWGDEdY" -o ./my-output
        """),
    )
    parser.add_argument("url", help="YouTube video URL or ID")
    parser.add_argument(
        "-o", "--output-dir",
        help="Output directory (default: ./yt-extract-<video_id>)",
    )
    parser.add_argument(
        "--interval", type=int, default=30,
        help="Seconds between keyframe captures (default: 30)",
    )
    parser.add_argument(
        "--scene-detect", action="store_true",
        help="Also extract frames on scene changes (good for visual-heavy videos)",
    )
    parser.add_argument(
        "--scene-threshold", type=float, default=0.3,
        help="Scene change sensitivity 0.0-1.0, lower = more frames (default: 0.3)",
    )
    parser.add_argument(
        "--transcript-only", action="store_true",
        help="Skip video download, only fetch transcript + metadata",
    )
    parser.add_argument(
        "--chunk-seconds", type=int, default=60,
        help="Group transcript into chunks of N seconds (default: 60)",
    )

    args = parser.parse_args()

    video_id = extract_video_id(args.url)
    out_dir = Path(args.output_dir or f"./yt-extract-{video_id}")
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Metadata
    meta = get_video_metadata(args.url)

    # Dump raw metadata for future reference
    (out_dir / "metadata.json").write_text(
        json.dumps(meta, indent=2, default=str), encoding="utf-8"
    )
    print(f"    Title:    {meta.get('title')}")
    print(f"    Channel:  {meta.get('channel', meta.get('uploader'))}")
    print(f"    Duration: {fmt_timestamp(meta.get('duration', 0))}")

    # 2. Transcript
    transcript = get_transcript(video_id)

    # 3. Keyframes
    interval_frames: list[Path] = []
    scene_frames: list[Path] = []

    if not args.transcript_only:
        video_path = download_video(args.url, out_dir)
        interval_frames = extract_frames_interval(
            video_path, out_dir, interval=args.interval
        )
        if args.scene_detect:
            scene_frames = extract_frames_scene(
                video_path, out_dir, threshold=args.scene_threshold
            )
        # Clean up video file to save space
        print(f"[*] Removing downloaded video to save space …")
        video_path.unlink(missing_ok=True)
    else:
        print("[*] --transcript-only: skipping video download")

    # 4. Build markdown
    md_path = build_markdown(
        meta, transcript, interval_frames, scene_frames, out_dir, args.interval
    )

    # Summary
    print("\n" + "=" * 60)
    print("DONE! Output directory:", out_dir)
    print("=" * 60)
    print(f"  Reference doc : {md_path}")
    print(f"  Metadata      : {out_dir / 'metadata.json'}")
    if interval_frames:
        print(f"  Interval frames: {len(interval_frames)} in frames/")
    if scene_frames:
        print(f"  Scene frames   : {len(scene_frames)} in frames_scene/")
    print()
    print("Next steps:")
    print("  1. Review extracted-reference.md")
    print("  2. Curate/annotate the content for your agent")
    print("  3. Feed the file to Claude to generate a SKILL.md or agent definition")


if __name__ == "__main__":
    main()
