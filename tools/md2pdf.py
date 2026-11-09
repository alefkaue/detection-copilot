"""Converte um Markdown da documentação em PDF (para relatórios de fase e LinkedIn).

    python tools/md2pdf.py docs/relatorios/00-abertura-do-projeto.md docs/relatorios/00-abertura-do-projeto.pdf

Suporta: títulos (#, ##, ###), parágrafos, **negrito**, *itálico*, `código`, [links](url),
listas (-, 1.), caixas de seleção (- [ ]), tabelas (|), blocos de código (```), citações (>)
e regras horizontais (---). Requer: pip install reportlab
"""

from __future__ import annotations

import html
import re
import sys
from datetime import date
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    ListFlowable,
    ListItem,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ACCENT = colors.HexColor("#1f4e79")
MUTED = colors.HexColor("#5f6b7a")
CODE_BG = colors.HexColor("#f3f5f8")
BORDER = colors.HexColor("#d5dbe3")


def register_fonts() -> tuple[str, str, str, str]:
    """Usa Segoe UI/Consolas do Windows (acentos e símbolos); cai para Helvetica/Courier se não houver."""
    fonts = Path("C:/Windows/Fonts")
    try:
        pdfmetrics.registerFont(TTFont("UI", str(fonts / "segoeui.ttf")))
        pdfmetrics.registerFont(TTFont("UI-Bold", str(fonts / "segoeuib.ttf")))
        pdfmetrics.registerFont(TTFont("UI-Italic", str(fonts / "segoeuii.ttf")))
        pdfmetrics.registerFont(TTFont("Mono", str(fonts / "consola.ttf")))
        pdfmetrics.registerFontFamily("UI", normal="UI", bold="UI-Bold", italic="UI-Italic", boldItalic="UI-Bold")
        return "UI", "UI-Bold", "UI-Italic", "Mono"
    except Exception:
        return "Helvetica", "Helvetica-Bold", "Helvetica-Oblique", "Courier"


BODY, BOLD, ITALIC, MONO = register_fonts()
STYLES = {
    "h1": ParagraphStyle("h1", fontName=BOLD, fontSize=20, leading=25, textColor=ACCENT, spaceAfter=10, keepWithNext=1),
    "h2": ParagraphStyle("h2", fontName=BOLD, fontSize=14, leading=18, textColor=ACCENT, spaceBefore=12, spaceAfter=6, keepWithNext=1),
    "h3": ParagraphStyle("h3", fontName=BOLD, fontSize=11.5, leading=15, spaceBefore=8, spaceAfter=4, keepWithNext=1),
    "p": ParagraphStyle("p", fontName=BODY, fontSize=10, leading=14.5, spaceAfter=6, alignment=TA_LEFT),
    "cell": ParagraphStyle("cell", fontName=BODY, fontSize=8.8, leading=11.5),
    "cellh": ParagraphStyle("cellh", fontName=BOLD, fontSize=8.8, leading=11.5, textColor=colors.white),
    "quote": ParagraphStyle("quote", fontName=ITALIC, fontSize=9.8, leading=14, textColor=MUTED, leftIndent=10),
    "code": ParagraphStyle("code", fontName=MONO, fontSize=8, leading=10.5, backColor=CODE_BG,
                           borderPadding=6, leftIndent=4, rightIndent=4, spaceBefore=4, spaceAfter=8),
}


def inline(text: str) -> str:
    """Markdown inline → marcação do ReportLab."""
    text = html.escape(text, quote=False)
    codes: list[str] = []

    def keep_code(m: re.Match) -> str:
        codes.append(m.group(1))
        return f"\x00{len(codes) - 1}\x00"

    text = re.sub(r"`([^`]+)`", keep_code, text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<link href="\2" color="#1f4e79"><u>\1</u></link>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<![*\w])\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    text = re.sub(r"(?<!\w)_([^_]+)_(?!\w)", r"<i>\1</i>", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: f'<font name="{MONO}" size="8.6">{codes[int(m.group(1))]}</font>', text)


def make_table(rows: list[list[str]], width: float) -> Table:
    header, body = rows[0], rows[1:]
    data = [[Paragraph(inline(c), STYLES["cellh"]) for c in header]]
    data += [[Paragraph(inline(c), STYLES["cell"]) for c in r] + [""] * (len(header) - len(r)) for r in body]
    # Largura proporcional ao texto, com mínimo, para colunas longas não esmagarem as curtas.
    lengths = [max(len(r[i]) if i < len(r) else 0 for r in rows) for i in range(len(header))]
    # Largura mínima = maior palavra da coluna, para nunca quebrar uma palavra no meio.
    longest_word = [max((len(w) for r in rows if i < len(r) for w in r[i].split()), default=4) for i in range(len(header))]
    weights = [max(min(n, 60), longest_word[i] + 2) for i, n in enumerate(lengths)]
    col_widths = [width * w / sum(weights) for w in weights]
    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, CODE_BG]),
        ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return table


def parse(md: str, width: float) -> list:
    story: list = []
    lines = md.replace("\r\n", "\n").split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith("<!--"):  # comentários HTML
            while i < len(lines) and "-->" not in lines[i]:
                i += 1
            i += 1
            continue
        if stripped.startswith("```"):
            i += 1
            block = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                block.append(lines[i])
                i += 1
            story.append(Preformatted("\n".join(block), STYLES["code"]))
            i += 1
            continue
        if m := re.match(r"^(#{1,3})\s+(.*)", line):
            story.append(Paragraph(inline(m.group(2)), STYLES[f"h{len(m.group(1))}"]))
        elif stripped in {"---", "***"}:
            story.append(HRFlowable(width="100%", thickness=0.6, color=BORDER, spaceBefore=6, spaceAfter=6))
        elif stripped.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                    rows.append(cells)
                i += 1
            story += [make_table(rows, width), Spacer(1, 8)]
            continue
        elif stripped.startswith(">"):
            story.append(Paragraph(inline(stripped.lstrip("> ")), STYLES["quote"]))
        elif re.match(r"^\s*([-*]|\d+\.)\s+", line):
            items, ordered = [], bool(re.match(r"^\s*\d+\.", line))
            while i < len(lines) and re.match(r"^\s*([-*]|\d+\.)\s+", lines[i]):
                text = re.sub(r"^\s*([-*]|\d+\.)\s+", "", lines[i])
                text = re.sub(r"^\[ \]\s*", "☐ ", re.sub(r"^\[[xX]\]\s*", "☑ ", text))
                indent = (len(lines[i]) - len(lines[i].lstrip())) // 2
                items.append(ListItem(Paragraph(inline(text), STYLES["p"]), leftIndent=12 + indent * 12))
                i += 1
            story.append(ListFlowable(items, bulletType="1" if ordered else "bullet", start="1" if ordered else None,
                                      bulletFontName=BODY, bulletFontSize=9, leftIndent=14))
            continue
        elif stripped:
            para = [stripped]
            while i + 1 < len(lines) and lines[i + 1].strip() and not re.match(
                r"^\s*(#|\||>|```|[-*]\s|\d+\.\s|---)", lines[i + 1]
            ):
                i += 1
                para.append(lines[i].strip())
            story.append(Paragraph(inline(" ".join(para)), STYLES["p"]))
        i += 1
    return story


def footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont(BODY, 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(doc.leftMargin, 1.1 * cm, f"Detection Copilot · gerado em {date.today():%d/%m/%Y}")
    canvas.drawRightString(A4[0] - doc.rightMargin, 1.1 * cm, f"página {doc.page}")
    canvas.restoreState()


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.parent.mkdir(parents=True, exist_ok=True)
    title = next((ln[2:].strip() for ln in src.read_text(encoding="utf-8").splitlines() if ln.startswith("# ")), src.stem)
    doc = SimpleDocTemplate(str(out), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm,
                            topMargin=1.8 * cm, bottomMargin=1.8 * cm, title=title, author="alefkaue")
    doc.build(parse(src.read_text(encoding="utf-8"), doc.width), onFirstPage=footer, onLaterPages=footer)
    print(f"PDF gerado: {out}")


if __name__ == "__main__":
    main()
