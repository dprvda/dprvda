"""Render the profile banner as a self-contained SVG with all text as paths.

Usage: python -I banner.py <fonts_dir> <out.svg>
"""
import sys
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen

FONTS = Path(sys.argv[1])
OUT = Path(sys.argv[2])

INK = "#17140e"
PAPER = "#f6f3ec"
MUTED = "#a39d8e"
SIGNAL = "#c8401f"
BRASS = "#a98a4f"

W, H = 1280, 452


class Face:
    def __init__(self, file, **axes):
        blob = hb.Blob.from_file_path(str(FONTS / file))
        self.face = hb.Face(blob)
        self.font = hb.Font(self.face)
        self.font.set_variations(axes)
        self.upem = self.face.upem

    def shape(self, text):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.font, buf, {"kern": True, "liga": True})
        return buf.glyph_infos, buf.glyph_positions


def text(face, s, size, x, y, fill, tracking=0.0, anchor="start"):
    """Return (svg, width). tracking is in em."""
    infos, positions = face.shape(s)
    scale = size / face.upem
    track = tracking * face.upem
    width = sum(p.x_advance + track for p in positions) - track
    if anchor == "end":
        x -= width * scale
    elif anchor == "middle":
        x -= width * scale / 2
    parts = []
    pen_x = 0.0
    for info, pos in zip(infos, positions):
        pen = SVGPathPen(None)
        face.font.draw_glyph_with_pen(info.codepoint, pen)
        d = pen.getCommands()
        if d:
            gx = pen_x + pos.x_offset
            parts.append(f'<path transform="translate({gx:.1f} {-pos.y_offset:.1f})" d="{d}"/>')
        pen_x += pos.x_advance + track
    svg = (
        f'<g fill="{fill}" transform="translate({x:.2f} {y:.2f}) scale({scale:.5f} {-scale:.5f})">'
        + "".join(parts)
        + "</g>"
    )
    return svg, width * scale


display = Face("Fraunces.ttf", opsz=144, wght=380, SOFT=0, WONK=0)
display_it = Face("FrauncesItalic.ttf", opsz=144, wght=380, SOFT=30, WONK=1)
caps = Face("InstrumentSans.ttf", wght=600, wdth=100)

M = 64  # outer margin
els = []

# Faint editorial grid
for gx in range(M, W - M + 1, 96):
    els.append(f'<line x1="{gx}" y1="0" x2="{gx}" y2="{H}" stroke="{PAPER}" stroke-opacity="0.035"/>')

# Top line
numero = Face("Fraunces.ttf", opsz=9, wght=500, SOFT=0, WONK=0)
s, w1 = text(numero, "№", 21, M, 65, SIGNAL)
els.append(s)
s, w2 = text(caps, " 00 —", 17, M + w1, 64, SIGNAL, tracking=0.16)
els.append(s)
w = w1 + w2
s, _ = text(caps, "DANYLO PRAVDA · BUSINESS-AUTOMATION ENGINEER · KYIV", 17, M + w + 10, 64, MUTED, tracking=0.16)
els.append(s)
s, w = text(caps, "BUILDING DAILY", 17, W - M, 64, PAPER, tracking=0.16, anchor="end")
els.append(s)
dot_x = W - M - w - 16
els.append(f'<circle class="pulse" cx="{dot_x}" cy="59" r="4.5" fill="{SIGNAL}"/>')
els.append(f'<line x1="{M}" y1="86" x2="{W - M}" y2="86" stroke="{PAPER}" stroke-opacity="0.22"/>')

# Headline
s, _ = text(display, "Machines that run", 96, M - 4, 196, PAPER, tracking=-0.015)
els.append(s)
s, w = text(display_it, "whole businesses", 96, M - 2, 290, PAPER, tracking=-0.01)
els.append(s)
s, _ = text(display, ".", 96, M - 2 + w + 2, 290, SIGNAL)
els.append(s)

# Figures, as published on pravda.systems
fig_num = Face("Fraunces.ttf", opsz=144, wght=340, SOFT=0, WONK=0)
figures = [("18", "SYSTEMS BUILT"), ("11", "LIVE ON OWN DOMAINS"), ("22", "RESEARCH REPORTS")]
label_x = W - M - max(text(caps, label, 14, 0, 0, MUTED, tracking=0.16)[1] for _, label in figures)
for i, (n, label) in enumerate(figures):
    fy = 150 + i * 66
    s, _ = text(fig_num, n, 50, label_x - 18, fy, PAPER, anchor="end")
    els.append(s)
    s, _ = text(caps, label, 14, label_x, fy - 7, MUTED, tracking=0.16)
    els.append(s)
    if i:
        els.append(f'<line x1="{label_x - 90}" y1="{fy - 50}" x2="{W - M}" y2="{fy - 50}" stroke="{PAPER}" stroke-opacity="0.12"/>')

# Conveyor: a process goes in, an automation comes out
belt_y = 342
node_x = 760
left_a, left_b = M + 150, node_x - 22
right_a, right_b = node_x + 22, W - M - 180
s, _ = text(caps, "PROCESS IN", 15, M, belt_y + 4, MUTED, tracking=0.16)
els.append(s)
s, _ = text(caps, "AUTOMATION OUT", 15, W - M, belt_y + 4, PAPER, tracking=0.16, anchor="end")
els.append(s)
els.append(f'<line x1="{left_a}" y1="{belt_y}" x2="{left_b}" y2="{belt_y}" stroke="{PAPER}" stroke-opacity="0.22"/>')
els.append(f'<line x1="{right_a}" y1="{belt_y}" x2="{right_b}" y2="{belt_y}" stroke="{SIGNAL}" stroke-opacity="0.55"/>')

step = 48
defs = [
    f'<clipPath id="inbelt"><rect x="{left_a}" y="{belt_y - 12}" width="{left_b - left_a}" height="24"/></clipPath>',
    f'<clipPath id="outbelt"><rect x="{right_a}" y="{belt_y - 12}" width="{right_b - right_a}" height="24"/></clipPath>',
]
boxes_in = "".join(
    f'<rect x="{x}" y="{belt_y - 5}" width="10" height="10" fill="none" stroke="{MUTED}" stroke-width="1.2"/>'
    for x in range(left_a - step, left_b + step, step)
)
boxes_out = "".join(
    f'<rect x="{x}" y="{belt_y - 5}" width="10" height="10" fill="{SIGNAL}"/>'
    for x in range(right_a - step, right_b + step, step)
)
els.append(f'<g clip-path="url(#inbelt)"><g class="belt">{boxes_in}</g></g>')
els.append(f'<g clip-path="url(#outbelt)"><g class="belt">{boxes_out}</g></g>')

# The machine in the middle
els.append(f'<circle cx="{node_x}" cy="{belt_y}" r="18" fill="{INK}" stroke="{PAPER}" stroke-opacity="0.8"/>')
els.append(f'<circle class="spin" cx="{node_x}" cy="{belt_y}" r="11" fill="none" stroke="{SIGNAL}" stroke-width="2" stroke-dasharray="10 7.3"/>')
els.append(f'<circle cx="{node_x}" cy="{belt_y}" r="3" fill="{PAPER}"/>')
s, _ = text(caps, "AGENTS", 13, node_x, belt_y + 38, MUTED, tracking=0.2, anchor="middle")
els.append(s)

# Footer
els.append(f'<line x1="{M}" y1="{H - 62}" x2="{W - M}" y2="{H - 62}" stroke="{PAPER}" stroke-opacity="0.22"/>')
s, _ = text(caps, "5 YEARS OF 3D FOR GLOBAL BRANDS  →  AGENT SYSTEMS SINCE MARCH 2026", 15, M, H - 30, MUTED, tracking=0.16)
els.append(s)
s, _ = text(caps, "PRAVDA.SYSTEMS", 15, W - M, H - 30, PAPER, tracking=0.16, anchor="end")
els.append(s)
els.append(f'<rect x="0" y="{H - 4}" width="{W}" height="4" fill="{SIGNAL}"/>')

style = f"""
.belt {{ animation: belt 2.4s linear infinite; }}
@keyframes belt {{ from {{ transform: translateX(0); }} to {{ transform: translateX({step}px); }} }}
.pulse {{ animation: pulse 1.6s ease-in-out infinite; }}
@keyframes pulse {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: .25; }} }}
.spin {{ transform-origin: {node_x}px {belt_y}px; animation: spin 3s linear infinite; }}
@keyframes spin {{ to {{ transform: rotate(360deg); }} }}
@media (prefers-reduced-motion: reduce) {{ .belt, .pulse, .spin {{ animation: none; }} }}
"""

svg = (
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'role="img" aria-label="Danylo Pravda — Machines that run whole businesses.">'
    f"<title>Danylo Pravda — Machines that run whole businesses.</title>"
    f"<style>{style}</style><defs>{''.join(defs)}</defs>"
    f'<clipPath id="frame"><rect width="{W}" height="{H}" rx="10"/></clipPath>'
    f'<g clip-path="url(#frame)"><rect width="{W}" height="{H}" fill="{INK}"/>'
    + "".join(els)
    + "</g></svg>"
)
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(svg)
print(OUT, len(svg))
