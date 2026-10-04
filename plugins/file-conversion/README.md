# File conversion

Guidance for converting local files with installed tools, preserving originals, and
checking the results. The workflow uses local files and local output paths. It does
not call hosted conversion services or upload files.

## Prerequisites

Install only the tools required for the requested route, under the session's existing
permission policy:

- FFmpeg and FFprobe for audio/video; available codecs depend on the build.
- ImageMagick 7 (`magick`) for images; formats such as HEIC and PDF may need delegates
  or a compatible local policy.
- Pandoc for supported structured document formats such as Markdown and DOCX.
- LibreOffice (`soffice`) for supported office-document exports, including PDF.
- Python 3 for CSV/JSON data conversion using the standard library.

The plugin supplies guidance, not these executables. The agent checks what is already
installed, inspects the source, and chooses a supported route. On Windows, executable
names and shell syntax may differ. No account or API key is required.

## Use and limits

Provide a local file or a retrievable URL, the target format, and any quality or
layout requirements. Results go into a fresh directory without replacing the original.
The skill includes examples and checks for media, images, documents, and tabular data.

Support depends on the installed readers, writers, codecs, fonts, and available memory
and disk space. Conversion may change layout, color, transparency, or compression.
PDF-to-Word is not guaranteed; scanned PDFs require local OCR tools and a separate
layout review. Unsupported routes stop with an explanation.

URL inputs can first be retrieved through an already-authorized method; report an
access gap if retrieval is unavailable. Conversion runs on local copies and local assets.
For documents with external links or macros, use an environment with network access
blocked and macros disabled, or stop. A temporary profile alone provides neither control.

## Migration from version 1

Version 2.0 removes the ChangeThisFile service integration and the bundled
`skills/file-conversion/scripts/convert.sh` upload script. Existing calls to that
script must be replaced with the appropriate local tool; there is no drop-in script
replacement. The plugin and skill names remain `file-conversion`.

Aadil Razvi authored the original hosted-service integration. Repository maintainers
rewrote version 2.0 for local tools and maintain the current workflow.
