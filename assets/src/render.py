"""Render the profile README images in Beamline's Prism look, dark and light.

Usage: python -I render.py <fonts_dir> <out_dir>
Writes hero, numbers and card-<id> images (dark and light) at 2x; convert to WebP for the README.
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

FONTS = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
OUT.mkdir(parents=True, exist_ok=True)

GRAIN = (
    "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='g'%3E"
    "%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix "
    "values='1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 0 0 0 0 .05'/%3E%3C/filter%3E%3Crect width='160' height='160' "
    "filter='url(%23g)'/%3E%3C/svg%3E\") 0 0 / 160px 160px"
)

# Prism tokens (ui/styles/presets/prism.css), resolved per scheme.
THEMES = {
    "dark": dict(
        page="oklch(0.118 0.001 270)",
        surface_bg="linear-gradient(165deg, rgb(255 255 255 / .06), rgb(255 255 255 / .018) 55%, rgb(255 255 255 / .012))",
        surface_edge="0 0 0 1px rgb(255 255 255 / .07), 0 30px 60px -36px rgb(0 0 0 / .85)",
        rim="rgb(255 255 255 / .16)",
        ink="oklch(0.985 0 0)",
        ink2="oklch(0.77 0.002 270)",
        ink3="oklch(0.63 0.003 270)",
        line="oklch(0.265 0.002 270)",
        mark="linear-gradient(100deg, oklch(0.99 0 0) 20%, oklch(0.72 0.004 270))",
        warm="oklch(0.6 0.17 42 / .16)",
        cool="oklch(0.5 0.14 245 / .16)",
        beam_glow=".55",
        chip="rgb(255 255 255 / .05)",
        chip_edge="rgb(255 255 255 / .09)",
    ),
    "light": dict(
        page="oklch(0.972 0.001 270)",
        surface_bg="linear-gradient(165deg, rgb(255 255 255 / .92), rgb(255 255 255 / .74) 55%, rgb(255 255 255 / .68))",
        surface_edge="0 0 0 1px rgb(20 22 30 / .09), 0 30px 60px -36px rgb(20 22 30 / .22)",
        rim="rgb(255 255 255 / 1)",
        ink="oklch(0.17 0.003 270)",
        ink2="oklch(0.4 0.003 270)",
        ink3="oklch(0.49 0.003 270)",
        line="oklch(0.885 0.002 270)",
        mark="linear-gradient(100deg, oklch(0.17 0.003 270) 20%, oklch(0.46 0.004 270))",
        warm="oklch(0.9 0.07 60 / .5)",
        cool="oklch(0.88 0.06 240 / .5)",
        beam_glow=".3",
        chip="rgb(20 22 30 / .035)",
        chip_edge="rgb(20 22 30 / .1)",
    ),
}

LOGO = """<svg viewBox="0 0 100 100" width="{s}" height="{s}"><defs><linearGradient id="lg{k}" x1="42.5" y1="84" x2="57.5" y2="16"
gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#0065c1"/><stop offset=".5" stop-color="#009eb9"/>
<stop offset="1" stop-color="#e6581b"/></linearGradient></defs>
<polygon points="25.41,19.76 -2.51,50 25.41,80.24 34.59,71.76 12.31,50 34.59,28.24" fill="var(--ink)"/>
<polygon points="65.41,28.24 87.69,50 65.41,71.76 74.59,80.24 102.51,50 74.59,19.76" fill="var(--ink)"/>
<line x1="42.5" y1="84" x2="57.5" y2="16" stroke="url(#lg{k})" stroke-width="9.4"/></svg>"""


def css(t):
    return f"""
@font-face {{ font-family: Geist; src: url('file://{FONTS}/Geist.ttf'); font-weight: 100 900; }}
@font-face {{ font-family: GeistMono; src: url('file://{FONTS}/GeistMono.ttf'); font-weight: 100 900; }}
@font-face {{ font-family: Serif; src: url('file://{FONTS}/InstrumentSerif-Italic.woff2'); font-style: italic; }}
:root {{ --ink: {t['ink']}; --ink2: {t['ink2']}; --ink3: {t['ink3']}; --line: {t['line']}; }}
* {{ box-sizing: border-box; margin: 0; }}
html, body {{ background: transparent; }}
body {{ font-family: Geist, sans-serif; color: var(--ink); -webkit-font-smoothing: antialiased; padding: 24px; }}
.frame {{ position: relative; overflow: hidden; border-radius: 22px; background: {GRAIN}, {t['page']};
  box-shadow: {t['surface_edge']}; }}
.frame::before {{ content: ""; position: absolute; inset: 0; pointer-events: none; border-radius: inherit;
  background: radial-gradient(60rem 26rem at 108% -10%, {t['warm']}, transparent 70%),
              radial-gradient(52rem 26rem at -8% 112%, {t['cool']}, transparent 70%); }}
.frame::after {{ content: ""; position: absolute; inset: 0; border-radius: inherit; pointer-events: none;
  background: linear-gradient(90deg, {t['rim']}, transparent 55%) 0 0 / 100% 1px no-repeat,
              linear-gradient(180deg, {t['rim']}, transparent 60%) 0 0 / 1px 100% no-repeat; }}
.surface {{ position: relative; border-radius: 16px; background: {t['surface_bg']}; box-shadow: {t['surface_edge']}; }}
.label {{ font-family: GeistMono, monospace; font-size: 13px; letter-spacing: .08em; text-transform: uppercase; color: var(--ink3); }}
.chip {{ display: inline-flex; align-items: center; gap: 8px; height: 30px; padding: 0 12px; border-radius: 999px;
  background: {t['chip']}; box-shadow: inset 0 0 0 1px {t['chip_edge']}; font-size: 14px; color: var(--ink2); }}
.dot {{ width: 7px; height: 7px; border-radius: 50%; }}
.serif {{ font-family: Serif, serif; font-style: italic; font-weight: 400; letter-spacing: -0.01em; }}
.mark {{ background: {t['mark']}; -webkit-background-clip: text; background-clip: text; color: transparent; }}
"""


def beam(t, w, h):
    g = t["beam_glow"]
    return f"""<svg class="beam" width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="position:absolute;inset:0;pointer-events:none">
<defs><linearGradient id="bg" x1="{w*0.55}" y1="{h}" x2="{w}" y2="0" gradientUnits="userSpaceOnUse">
<stop offset="0" stop-color="#0065c1" stop-opacity="0"/><stop offset=".25" stop-color="#0065c1"/>
<stop offset=".55" stop-color="#009eb9"/><stop offset=".8" stop-color="#d0506a"/><stop offset="1" stop-color="#e6581b"/></linearGradient>
<filter id="b1" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="28"/></filter>
<filter id="b2" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter></defs>
<path d="M {w*0.5} {h+40} C {w*0.8} {h*0.85}, {w*0.95} {h*0.45}, {w+60} {-30}" fill="none" stroke="url(#bg)" stroke-width="90" opacity="{g}" filter="url(#b1)"/>
<path d="M {w*0.5} {h+40} C {w*0.8} {h*0.85}, {w*0.95} {h*0.45}, {w+60} {-30}" fill="none" stroke="url(#bg)" stroke-width="14" opacity=".85" filter="url(#b2)"/>
<path d="M {w*0.5} {h+40} C {w*0.8} {h*0.85}, {w*0.95} {h*0.45}, {w+60} {-30}" fill="none" stroke="url(#bg)" stroke-width="2.2"/>
</svg>"""


def hero(t):
    w, h = 1232, 520
    return f"""<div class="frame" id="shot" style="width:{w}px;height:{h}px;padding:56px 64px">
{beam(t, w, h)}
<div style="position:relative;display:flex;flex-direction:column;height:100%">
  <div style="display:flex;gap:10px">
    <span class="chip"><span class="dot" style="background:#3fb950"></span>Kyiv · open to projects</span>
  </div>
  <h1 class="mark" style="margin-top:42px;font-size:104px;line-height:.98;font-weight:500;letter-spacing:-0.045em">Danylo Pravda</h1>
  <div class="serif" style="margin-top:6px;font-size:76px;line-height:1.05;color:var(--ink2)">designer turned agent engineer.</div>
  <p style="margin-top:28px;max-width:720px;font-size:20px;line-height:1.5;color:var(--ink2)">
    Five years of 3D for L'Oréal, Crocs, Lacoste and Breitling.<br>Since March 2026, I build AI-agent systems that do real work.</p>
  <div style="margin-top:auto;display:flex;gap:28px" class="label">
    <span>3D → agents · March 2026</span><span>18 systems · 11 live</span><span>pravda.systems</span>
  </div>
</div></div>"""


def numbers(t):
    items = [
        ("30.4K", "contributions", "since March 2026"),
        ("312B", "Claude Code tokens", "#1 all-time on ccgather"),
        ("89", "repositories", "since March 2026"),
        ("11", "systems live", "on their own domains"),
    ]
    cells = "".join(
        f"""<div style="flex:1;padding:28px 32px;{'border-left:1px solid var(--line);' if i else ''}">
<div class="mark" style="font-size:52px;font-weight:500;letter-spacing:-0.04em;line-height:1">{n}</div>
<div style="margin-top:14px;font-size:17px;color:var(--ink)">{a}</div>
<div style="margin-top:2px;font-size:15px;color:var(--ink3)">{b}</div></div>"""
        for i, (n, a, b) in enumerate(items)
    )
    return f'<div class="frame" id="shot" style="width:1232px;display:flex">{cells}</div>'


CARDS = {
    "beamline": dict(
        label="Now · my open project", dot="#009eb9",
        title='Beamline <span class="serif" style="font-size:1.08em">UI</span>',
        body="React components and complete screens that coding agents can actually design with. 200+ components, 50+ screens.",
        foot="beamline.io", logo=True,
    ),
    "automations": dict(
        label="11 live · own domains", dot="#3fb950",
        title='Business <span class="serif" style="font-size:1.08em">automations</span>',
        body="Bespoke machines for real jobs: listings, quotes, client reports, invoices, product video, creative approvals.",
        foot="pravda.systems/work",
    ),
    "trading": dict(
        label="Production · paper mode", dot="#e6581b",
        title='A trading system, <span class="serif" style="font-size:1.08em">solo</span>',
        body="Bitcoin 5-minute markets: 21 µs decisions, 11 live venues, 2,948 tests, 13 commit gates with no bypass.",
        foot="case study",
    ),
    "agents": dict(
        label="One-person scale", dot="#a78bfa",
        title='Agent <span class="serif" style="font-size:1.08em">infrastructure</span>',
        body="A cited memory for agents, an approval rail on my phone, and one cockpit over a fleet of coding sessions.",
        foot="Commonplace · Signet · ADE",
    ),
}


def card(t, key, side):
    c = CARDS[key]
    gutter = "padding-right:11px" if side == "left" else "padding-left:11px"
    logo = (
        f'<div style="position:absolute;right:30px;top:28px">{LOGO.format(s=44, k=key)}</div>' if c.get("logo") else ""
    )
    return f"""<div id="shot" style="width:616px;{gutter}"><div class="frame" style="height:256px;padding:30px 32px;display:flex;flex-direction:column">
{logo}
<div class="label" style="display:flex;align-items:center;gap:10px;position:relative"><span class="dot" style="background:{c['dot']}"></span>{c['label']}</div>
<div style="position:relative;margin-top:26px;font-size:38px;font-weight:500;letter-spacing:-0.035em;line-height:1.05">{c['title']}</div>
<p style="position:relative;margin-top:14px;font-size:17px;line-height:1.5;color:var(--ink2);max-width:500px">{c['body']}</p>
<div class="label" style="position:relative;margin-top:auto;color:var(--ink2)">{c['foot']} &nbsp;→</div>
</div></div>"""


def page(t, inner):
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{css(t)}</style></head><body>{inner}</body></html>"


jobs = [("hero", hero), ("numbers", numbers)] + [(f"card-{k}", (lambda t, k=k, i=i: card(t, k, "left" if i % 2 == 0 else "right"))) for i, k in enumerate(CARDS)]
with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(device_scale_factor=2, viewport={"width": 1400, "height": 900})
    pg = ctx.new_page()
    for name, fn in jobs:
        for theme, t in THEMES.items():
            pg.set_content(page(t, fn(t)), wait_until="load")
            pg.evaluate("document.fonts.ready")
            pg.locator("#shot").screenshot(path=str(OUT / f"{name}-{theme}.webp"), omit_background=True)
            print(name, theme)
    browser.close()
