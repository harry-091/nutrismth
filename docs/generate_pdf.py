from __future__ import annotations

import re
import textwrap
from html import unescape
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "system_guide.html"
OUTPUT = ROOT / "NutriQuest_System_Guide.pdf"
TEXT_OUTPUT = ROOT / "NutriQuest_System_Guide_Text.pdf"


def html_to_lines(html: str) -> list[str]:
    text = html
    text = re.sub(r"<style.*?</style>", "", text, flags=re.S)
    text = re.sub(r"<head.*?</head>", "", text, flags=re.S)
    text = re.sub(r"<script.*?</script>", "", text, flags=re.S)

    replacements = {
        r"</h1>": "\n\n",
        r"</h2>": "\n\n",
        r"</h3>": "\n",
        r"</p>": "\n\n",
        r"</li>": "\n",
        r"<li>": "- ",
        r"</tr>": "\n",
        r"</th>": " | ",
        r"</td>": " | ",
        r"<br\s*/?>": "\n",
        r"</div>": "\n",
        r"</section>": "\n\n",
        r"<pre>": "\n",
        r"</pre>": "\n\n",
    }
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text, flags=re.I)

    text = re.sub(r"<[^>]+>", "", text)
    text = unescape(text)
    text = re.sub(r"\r", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    raw_lines = []
    for block in text.split("\n"):
        line = re.sub(r"\s+", " ", block).strip()
        raw_lines.append(line)

    wrapped_lines: list[str] = []
    for line in raw_lines:
        if not line:
            wrapped_lines.append("")
            continue
        if line.startswith("- "):
            bullet = line[2:]
            wrapped = textwrap.wrap(
                bullet,
                width=92,
                initial_indent="- ",
                subsequent_indent="  ",
            )
            wrapped_lines.extend(wrapped)
        else:
            wrapped = textwrap.wrap(line, width=94) or [""]
            wrapped_lines.extend(wrapped)

    return wrapped_lines


def pdf_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def build_pages(lines: list[str]) -> list[list[str]]:
    pages: list[list[str]] = []
    current: list[str] = []
    line_count = 0
    max_lines = 47

    for line in lines:
      extra = 1 if line else 0
      if line_count + 1 > max_lines:
          pages.append(current)
          current = []
          line_count = 0
      current.append(line)
      line_count += 1

    if current:
        pages.append(current)
    return pages


def make_content_stream(lines: list[str]) -> str:
    y = 790
    commands = ["BT", "/F1 11 Tf", "50 0 0 1 50 790 Tm", "14 TL"]
    first = True
    for line in lines:
        text = pdf_escape(line if line else " ")
        if first:
            commands.append(f"({text}) Tj")
            first = False
        else:
            commands.append("T*")
            commands.append(f"({text}) Tj")
        y -= 14
    commands.append("ET")
    return "\n".join(commands)


def write_pdf(pages: list[list[str]], output: Path) -> None:
    objects: list[bytes] = []

    def add_object(data: str | bytes) -> int:
        if isinstance(data, str):
            payload = data.encode("latin-1", errors="replace")
        else:
            payload = data
        objects.append(payload)
        return len(objects)

    font_id = add_object("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

    content_ids = []
    page_ids = []

    for page_lines in pages:
        stream = make_content_stream(page_lines).encode("latin-1", errors="replace")
        content_id = add_object(
            b"<< /Length "
            + str(len(stream)).encode("ascii")
            + b" >>\nstream\n"
            + stream
            + b"\nendstream"
        )
        content_ids.append(content_id)
        page_ids.append(0)

    pages_id = add_object("<< /Type /Pages /Kids [] /Count 0 >>")

    for index, content_id in enumerate(content_ids):
        page_obj = (
            f"<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 595 842] "
            f"/Resources << /Font << /F1 {font_id} 0 R >> >> "
            f"/Contents {content_id} 0 R >>"
        )
        page_ids[index] = add_object(page_obj)

    kids = " ".join(f"{page_id} 0 R" for page_id in page_ids)
    objects[pages_id - 1] = (
        f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>".encode("latin-1")
    )

    catalog_id = add_object(f"<< /Type /Catalog /Pages {pages_id} 0 R >>")

    pdf = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for index, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{index} 0 obj\n".encode("ascii"))
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")

    xref_start = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    pdf.extend(
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root {catalog_id} 0 R >>\n"
            f"startxref\n{xref_start}\n%%EOF\n"
        ).encode("ascii")
    )

    output.write_bytes(pdf)


def main() -> None:
    html = SOURCE.read_text(encoding="utf-8")
    lines = html_to_lines(html)
    text = "\n".join(lines)
    (ROOT / "system_guide.txt").write_text(text, encoding="utf-8")
    pages = build_pages(lines)
    write_pdf(pages, OUTPUT)
    try:
        result = subprocess.run(
            [
                "cupsfilter",
                "-i",
                "text/plain",
                "-m",
                "application/pdf",
                str(ROOT / "system_guide.txt"),
            ],
            check=True,
            capture_output=True,
        )
        TEXT_OUTPUT.write_bytes(result.stdout)
        print(f"Wrote {TEXT_OUTPUT}")
    except Exception as exc:
        print(f"Text PDF generation failed: {exc}")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
