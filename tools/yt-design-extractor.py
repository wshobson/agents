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
    python3 tools/yt-design-extractor.py "https://youtu.be/eVnQFWGDEdY" --scene-detect --ocr
    python3 tools/yt-design-extractor.py "https://youtu.be/eVnQFWGDEdY" --full  # all features
    python3 tools/yt-design-extractor.py "https://youtu.be/eVnQFWGDEdY" --ocr --ocr-engine easyocr

Requirements:
    pip install yt-dlp youtube-transcript-api
    apt install ffmpeg

    Optional (OCR via Tesseract):
    pip install Pillow pytesseract
    apt install tesseract-ocr

    Optional (better OCR for stylized text):
    pip install easyocr

    Optional (color palette extraction):
    pip install colorthief
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import textwrap
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Optional

# Optional imports - gracefully degrade if not available
PILLOW_AVAILABLE = False
TESSERACT_AVAILABLE = False

try:
    from PIL import Image

    PILLOW_AVAILABLE = True
except ImportError:
    pass

try:
    import pytesseract

    TESSERACT_AVAILABLE = PILLOW_AVAILABLE
except ImportError:
    pass

try:
    import easyocr

    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False

try:
    from colorthief import ColorThief

    COLORTHIEF_AVAILABLE = True
except ImportError:
    COLORTHIEF_AVAILABLE = False

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
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        sys.exit("yt-dlp metadata fetch timed out after 120s.")
    if result.returncode != 0:
        sys.exit(f"yt-dlp metadata failed:\n{result.stderr}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as e:
        sys.exit(
            f"yt-dlp returned invalid JSON: {e}\nFirst 200 chars: {result.stdout[:200]}"
        )


def get_transcript(video_id: str) -> list[dict] | None:
    """Grab the transcript via youtube-transcript-api. Returns list of
    {text, start, duration} dicts, or None if unavailable."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        from youtube_transcript_api._errors import (
            TranscriptsDisabled,
            NoTranscriptFound,
            VideoUnavailable,
        )
    except ImportError:
        print("[!] youtube-transcript-api not installed. Skipping transcript.")
        return None

    try:
        print("[*] Fetching transcript …")
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id)
        entries = []
        for snippet in transcript:
            entries.append(
                {
                    "text": snippet.text,
                    "start": snippet.start,
                    "duration": snippet.duration,
                }
            )
        return entries
    except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable) as e:
        print(f"[!] Transcript unavailable ({e}). Will proceed without it.")
        return None


# ---------------------------------------------------------------------------
# Keyframe extraction
# ---------------------------------------------------------------------------


def download_video(url: str, out_dir: Path) -> Path:
    """Download video, preferring 720p or lower. Falls back to best available."""
    out_template = str(out_dir / "video.%(ext)s")
    cmd = [
        "yt-dlp",
        "-f",
        "bestvideo[height<=720]+bestaudio/best[height<=720]/best",
        "--merge-output-format",
        "mp4",
        "-o",
        out_template,
        "--no-playlist",
        url,
    ]
    print("[*] Downloading video (720p preferred) …")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    except subprocess.TimeoutExpired:
        sys.exit(
            "Video download timed out after 10 minutes. "
            "The video may be too large or your connection too slow."
        )
    if result.returncode != 0:
        sys.exit(f"yt-dlp download failed:\n{result.stderr}")

    # Find the downloaded file
    for f in out_dir.iterdir():
        if f.name.startswith("video.") and f.suffix in (".mp4", ".mkv", ".webm"):
            return f
    sys.exit("Download succeeded but could not locate video file.")


def extract_frames_interval(
    video_path: Path, out_dir: Path, interval: int = 30
) -> list[Path]:
    """Extract one frame every `interval` seconds."""
    frames_dir = out_dir / "frames"
    frames_dir.mkdir(exist_ok=True)
    pattern = str(frames_dir / "frame_%04d.png")
    cmd = [
        "ffmpeg",
        "-i",
        str(video_path),
        "-vf",
        f"fps=1/{interval}",
        "-q:v",
        "2",
        pattern,
        "-y",
    ]
    print(f"[*] Extracting frames every {interval}s …")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    except subprocess.TimeoutExpired:
        sys.exit("Frame extraction timed out after 10 minutes.")
    if result.returncode != 0:
        print(f"[!] ffmpeg frame extraction failed (exit code {result.returncode}):")
        print(f"    {result.stderr[:500]}")
        return []
    frames = sorted(frames_dir.glob("frame_*.png"))
    if not frames:
        print(
            "[!] WARNING: ffmpeg ran but produced no frames. "
            "The video may be too short or corrupted."
        )
    else:
        print(f"    → captured {len(frames)} frames")
    return frames


def extract_frames_scene(
    video_path: Path, out_dir: Path, threshold: float = 0.3
) -> list[Path]:
    """Use ffmpeg scene-change detection to grab visually distinct frames."""
    frames_dir = out_dir / "frames_scene"
    frames_dir.mkdir(exist_ok=True)
    pattern = str(frames_dir / "scene_%04d.png")
    cmd = [
        "ffmpeg",
        "-i",
        str(video_path),
        "-vf",
        f"select='gt(scene,{threshold})',showinfo",
        "-vsync",
        "vfr",
        "-q:v",
        "2",
        pattern,
        "-y",
    ]
    print(f"[*] Extracting scene-change frames (threshold={threshold}) …")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    except subprocess.TimeoutExpired:
        sys.exit("Scene-change frame extraction timed out after 10 minutes.")
    if result.returncode != 0:
        print(f"[!] ffmpeg scene detection failed (exit code {result.returncode}):")
        print(f"    {result.stderr[:500]}")
        return []
    frames = sorted(frames_dir.glob("scene_*.png"))
    if not frames:
        print("[!] No scene-change frames detected (try lowering --scene-threshold).")
    else:
        print(f"    → captured {len(frames)} scene-change frames")
    return frames


# ---------------------------------------------------------------------------
# OCR extraction
# ---------------------------------------------------------------------------


def ocr_frame_tesseract(frame_path: Path) -> str:
    """Extract text from a frame using Tesseract OCR. Converts to grayscale first."""
    if not TESSERACT_AVAILABLE:
        return ""
    try:
        img = Image.open(frame_path)
        if img.mode != "L":
            img = img.convert("L")
        text = pytesseract.image_to_string(img, config="--psm 6")
        return text.strip()
    except Exception as e:
        print(f"[!] OCR failed for {frame_path}: {e}")
        return ""


def ocr_frame_easyocr(frame_path: Path, reader) -> str:
    """Extract text from a frame using EasyOCR (better for stylized text)."""
    try:
        results = reader.readtext(str(frame_path), detail=0)
        return "\n".join(results).strip()
    except Exception as e:
        print(f"[!] OCR failed for {frame_path}: {e}")
        return ""


def run_ocr_on_frames(
    frames: list[Path], ocr_engine: str = "tesseract", workers: int = 4
) -> dict[Path, str]:
    """Run OCR on frames. Tesseract runs in parallel; EasyOCR sequentially.
    Returns {frame_path: text}."""
    if not frames:
        return {}

    results = {}

    if ocr_engine == "easyocr":
        if not EASYOCR_AVAILABLE:
            sys.exit(
                "EasyOCR was explicitly requested but is not installed.\n"
                "  Install: pip install torch torchvision --index-url "
                "https://download.pytorch.org/whl/cpu && pip install easyocr\n"
                "  Or use: --ocr-engine tesseract"
            )
        else:
            print("[*] Initializing EasyOCR (this may take a moment) …")
            reader = easyocr.Reader(["en"], gpu=False, verbose=False)

    if ocr_engine == "tesseract" and not TESSERACT_AVAILABLE:
        print("[!] Tesseract/pytesseract not installed, skipping OCR")
        return {}

    print(f"[*] Running OCR on {len(frames)} frames ({ocr_engine}) …")

    if ocr_engine == "easyocr":
        # EasyOCR doesn't parallelize well, run sequentially
        for i, frame in enumerate(frames):
            results[frame] = ocr_frame_easyocr(frame, reader)
            if (i + 1) % 10 == 0:
                print(f"    → processed {i + 1}/{len(frames)} frames")
    else:
        # Tesseract can run in parallel
        with ThreadPoolExecutor(max_workers=workers) as executor:
            future_to_frame = {
                executor.submit(ocr_frame_tesseract, f): f for f in frames
            }
            for i, future in enumerate(as_completed(future_to_frame)):
                frame = future_to_frame[future]
                try:
                    results[frame] = future.result()
                except Exception as e:
                    print(f"[!] OCR failed for {frame}: {e}")
                    results[frame] = ""
                if (i + 1) % 10 == 0:
                    print(f"    → processed {i + 1}/{len(frames)} frames")

    # Count frames with meaningful text
    with_text = sum(1 for t in results.values() if len(t) > 10)
    print(f"    → found text in {with_text}/{len(frames)} frames")

    return results


# ---------------------------------------------------------------------------
# Color palette extraction
# ---------------------------------------------------------------------------


def extract_color_palette(frame_path: Path, color_count: int = 6) -> list[tuple]:
    """Extract dominant colors from a frame. Returns list of RGB tuples."""
    if not COLORTHIEF_AVAILABLE:
        return []
    try:
        ct = ColorThief(str(frame_path))
        palette = ct.get_palette(color_count=color_count, quality=5)
        return palette
    except Exception as e:
        print(f"[!] Color extraction failed for {frame_path}: {e}")
        return []


def rgb_to_hex(rgb: tuple) -> str:
    """Convert RGB tuple to hex color string."""
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def analyze_color_palettes(frames: list[Path], sample_size: int = 10) -> dict:
    """Analyze color palettes across sampled frames."""
    if not COLORTHIEF_AVAILABLE:
        return {}
    if not frames:
        return {}

    # Sample frames evenly across the video
    step = max(1, len(frames) // sample_size)
    sampled = frames[::step][:sample_size]

    print(f"[*] Extracting color palettes from {len(sampled)} frames …")

    all_colors = []
    for frame in sampled:
        palette = extract_color_palette(frame)
        all_colors.extend(palette)

    if not all_colors:
        return {}

    # Find most common colors (rounded to reduce similar colors)
    def round_color(rgb, bucket_size=32):
        return tuple((c // bucket_size) * bucket_size for c in rgb)

    rounded = [round_color(c) for c in all_colors]
    most_common = Counter(rounded).most_common(12)

    return {
        "dominant_colors": [rgb_to_hex(c) for c, _ in most_common[:6]],
        "all_sampled_colors": [rgb_to_hex(c) for c in all_colors[:24]],
    }


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
    """Merge transcript snippets into chunks of at least `chunk_seconds` duration."""
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


def build_markdown(
    meta: dict,
    transcript: list[dict] | None,
    interval_frames: list[Path],
    scene_frames: list[Path],
    out_dir: Path,
    interval: int,
    ocr_results: Optional[dict[Path, str]] = None,
    color_analysis: Optional[dict] = None,
) -> Path:
    """Assemble the final reference markdown document."""
    title = meta.get("title", "Untitled Video")
    channel = meta.get("channel", meta.get("uploader", "Unknown"))
    duration = meta.get("duration", 0)
    description = meta.get("description", "")
    chapters = meta.get("chapters") or []
    video_url = meta.get("webpage_url", "")
    tags = meta.get("tags") or []

    ocr_results = ocr_results or {}
    color_analysis = color_analysis or {}

    lines: list[str] = []

    # --- Header ---
    lines.append(f"# {title}\n")
    lines.append(f"> **Source:** [{channel}]({video_url})  ")
    lines.append(f"> **Duration:** {fmt_timestamp(duration)}  ")
    lines.append(f"> **Extracted:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  ")
    if tags:
        lines.append(f"> **Tags:** {', '.join(tags[:15])}")
    lines.append("")

    # --- Color Palette (if extracted) ---
    if color_analysis.get("dominant_colors"):
        lines.append("## Color Palette\n")
        lines.append("Dominant colors detected across the video:\n")
        colors = color_analysis["dominant_colors"]
        # Create color swatches as a table
        lines.append("| Color | Hex |")
        lines.append("|-------|-----|")
        for hex_color in colors:
            # Unicode block for color preview (won't show actual color but placeholder)
            lines.append(f"| ████ | `{hex_color}` |")
        lines.append("")
        lines.append(f"*Full palette: {', '.join(f'`{c}`' for c in colors)}*\n")

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
            # Include OCR text if available
            ocr_text = ocr_results.get(f, "").strip()
            if ocr_text and len(ocr_text) > 5:
                lines.append("<details><summary>📝 Text detected in frame</summary>\n")
                lines.append(f"```\n{ocr_text}\n```")
                lines.append("</details>\n")
            all_frames.append((ts, rel, ocr_text))
        lines.append("")

    if scene_frames:
        lines.append("## Scene-Change Frames\n")
        lines.append("Frames captured when the visual content changed significantly.\n")
        for i, f in enumerate(scene_frames):
            rel = os.path.relpath(f, out_dir)
            lines.append(f"### Scene {i + 1}\n")
            lines.append(f"![scene-{i + 1}]({rel})\n")
            # Include OCR text if available
            ocr_text = ocr_results.get(f, "").strip()
            if ocr_text and len(ocr_text) > 5:
                lines.append("<details><summary>📝 Text detected in frame</summary>\n")
                lines.append(f"```\n{ocr_text}\n```")
                lines.append("</details>\n")
        lines.append("")

    # --- Visual Text Index (OCR summary) ---
    frames_with_text = [
        (ts, rel, txt) for ts, rel, txt in all_frames if txt and len(txt) > 10
    ]
    if frames_with_text:
        lines.append("## Visual Text Index\n")
        lines.append("Searchable index of all text detected in video frames.\n")
        lines.append("| Timestamp | Key Text (preview) |")
        lines.append("|-----------|-------------------|")
        for ts, rel, txt in frames_with_text:
            # First line or first 80 chars as preview
            preview = txt.split("\n")[0][:80].replace("|", "\\|")
            if len(txt) > 80:
                preview += "…"
            lines.append(f"| `{ts}` | {preview} |")
        lines.append("")

        # Full text dump for searchability
        lines.append("### All Detected Text (Full)\n")
        lines.append("<details><summary>Click to expand full OCR text</summary>\n")
        for ts, rel, txt in frames_with_text:
            lines.append(f"**[{ts}]**")
            lines.append(f"```\n{txt}\n```\n")
        lines.append("</details>\n")

    # --- Frame index (for quick reference) ---
    if all_frames:
        lines.append("## Frame Index\n")
        lines.append("| Timestamp | File | Has Text |")
        lines.append("|-----------|------|----------|")
        for ts, rel, txt in all_frames:
            has_text = "✓" if txt and len(txt) > 10 else ""
            lines.append(f"| `{ts}` | `{rel}` | {has_text} |")
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
              %(prog)s "https://youtu.be/eVnQFWGDEdY" --full
              %(prog)s "https://youtu.be/eVnQFWGDEdY" --interval 15 --scene-detect --ocr
              %(prog)s "https://youtu.be/eVnQFWGDEdY" --ocr --ocr-engine easyocr --colors
              %(prog)s "https://youtu.be/eVnQFWGDEdY" -o ./my-output
        """),
    )
    parser.add_argument("url", help="YouTube video URL or ID")
    parser.add_argument(
        "-o",
        "--output-dir",
        help="Output directory (default: ./yt-extract-<video_id>)",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=30,
        help="Seconds between keyframe captures (default: 30)",
    )
    parser.add_argument(
        "--scene-detect",
        action="store_true",
        help="Also extract frames on scene changes (good for visual-heavy videos)",
    )
    parser.add_argument(
        "--scene-threshold",
        type=float,
        default=0.3,
        help="Scene change sensitivity 0.0-1.0, lower = more frames (default: 0.3)",
    )
    parser.add_argument(
        "--transcript-only",
        action="store_true",
        help="Skip video download, only fetch transcript + metadata",
    )
    parser.add_argument(
        "--chunk-seconds",
        type=int,
        default=60,
        help="Group transcript into chunks of N seconds (default: 60)",
    )
    parser.add_argument(
        "--ocr",
        action="store_true",
        help="Run OCR on frames to extract on-screen text",
    )
    parser.add_argument(
        "--ocr-engine",
        choices=["tesseract", "easyocr"],
        default="tesseract",
        help="OCR engine: 'tesseract' (fast) or 'easyocr' (better for stylized text)",
    )
    parser.add_argument(
        "--colors",
        action="store_true",
        help="Extract color palette from frames",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Enable all features: scene-detect, OCR, and color extraction",
    )

    args = parser.parse_args()

    # --full enables everything
    if args.full:
        args.scene_detect = True
        args.ocr = True
        args.colors = True

    # Upfront dependency checks
    if not shutil.which("yt-dlp"):
        sys.exit(
            "Required tool 'yt-dlp' not found on PATH. Install with: pip install yt-dlp"
        )
    if not args.transcript_only and not shutil.which("ffmpeg"):
        sys.exit(
            "Required tool 'ffmpeg' not found on PATH. "
            "Install with: make install-ocr (or: brew install ffmpeg)"
        )

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

    # OCR and color analysis results
    ocr_results: dict[Path, str] = {}
    color_analysis: dict = {}

    if not args.transcript_only:
        video_path = download_video(args.url, out_dir)
        try:
            interval_frames = extract_frames_interval(
                video_path, out_dir, interval=args.interval
            )
            if args.scene_detect:
                scene_frames = extract_frames_scene(
                    video_path, out_dir, threshold=args.scene_threshold
                )
        finally:
            # Always clean up video file to save space
            print("[*] Removing downloaded video to save space …")
            video_path.unlink(missing_ok=True)

        # 4. OCR extraction
        if args.ocr:
            all_frames_for_ocr = interval_frames + scene_frames
            ocr_results = run_ocr_on_frames(
                all_frames_for_ocr,
                ocr_engine=args.ocr_engine,
            )
            # Save OCR results to JSON for reuse
            ocr_json = {str(k): v for k, v in ocr_results.items()}
            (out_dir / "ocr-results.json").write_text(
                json.dumps(ocr_json, indent=2), encoding="utf-8"
            )

        # 5. Color palette analysis
        if args.colors:
            all_frames_for_color = interval_frames + scene_frames
            color_analysis = analyze_color_palettes(all_frames_for_color)
            if color_analysis:
                (out_dir / "color-palette.json").write_text(
                    json.dumps(color_analysis, indent=2), encoding="utf-8"
                )
    else:
        print("[*] --transcript-only: skipping video download")

    # 6. Build markdown
    md_path = build_markdown(
        meta,
        transcript,
        interval_frames,
        scene_frames,
        out_dir,
        args.interval,
        ocr_results=ocr_results,
        color_analysis=color_analysis,
    )

    # Summary
    print("\n" + "=" * 60)
    print("DONE! Output directory:", out_dir)
    print("=" * 60)
    print(f"  Reference doc  : {md_path}")
    print(f"  Metadata       : {out_dir / 'metadata.json'}")
    if interval_frames:
        print(f"  Interval frames: {len(interval_frames)} in frames/")
    if scene_frames:
        print(f"  Scene frames   : {len(scene_frames)} in frames_scene/")
    if ocr_results:
        frames_with_text = sum(1 for t in ocr_results.values() if len(t) > 10)
        print(
            f"  OCR results    : {frames_with_text} frames with text → ocr-results.json"
        )
    if color_analysis:
        print(
            f"  Color palette  : {len(color_analysis.get('dominant_colors', []))} colors → color-palette.json"
        )
    print()
    print("Next steps:")
    print("  1. Review extracted-reference.md")
    print("  2. Curate/annotate the content for your agent")
    print("  3. Feed the file to Claude to generate a SKILL.md or agent definition")


if __name__ == "__main__":
    main()
