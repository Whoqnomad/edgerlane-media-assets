"""EDGERLANE MEDIA — moteur de rendu des posts Instagram (HTML/SVG -> PNG 1080x1350)."""
from datetime import datetime

W, H = 1080, 1350
CAT = {
    "eco":   {"name": "ÉCONOMIE",        "c": "#F5B80B", "dark": "#7a5a00", "rgb": "245,184,11"},
    "fr":    {"name": "POLITIQUE FRANCE", "c": "#3B6BFF", "dark": "#1a2f80", "rgb": "59,107,255"},
    "us":    {"name": "POLITIQUE USA",    "c": "#E5303A", "dark": "#7a1218", "rgb": "229,48,58"},
    "mix":   {"name": "AGENDA",           "c": "#FFFFFF", "dark": "#555",    "rgb": "255,255,255"},
}
GREEN = "#22C55E"
DATE_TAG = "SAM. 10.10.2026"

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px;background:#07080A;overflow:hidden}
body{font-family:'Inter',sans-serif;color:#fff;position:relative;-webkit-font-smoothing:antialiased}
.bg{position:absolute;inset:0;background:
  radial-gradient(900px 700px at 50% 42%, rgba(var(--rgb),.13), transparent 65%),
  radial-gradient(700px 500px at 50% 110%, rgba(255,255,255,.05), transparent 70%),
  linear-gradient(180deg,#0b0c0f 0%,#060708 100%)}
.grid{position:absolute;inset:0;opacity:.35;background-image:
  linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),
  linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);background-size:54px 54px;
  mask-image:radial-gradient(ellipse at 50% 45%,#000 30%,transparent 75%)}
.hdr{position:absolute;top:52px;left:64px;right:64px;display:flex;justify-content:space-between;align-items:center}
.logo{display:flex;align-items:center;gap:14px;font-weight:800;font-size:31px;letter-spacing:4px}
.logo .pill{background:#fff;color:#000;font-size:21px;letter-spacing:3px;padding:6px 13px 5px;border-radius:7px;font-weight:900}
.date{font-family:'Inter';font-weight:600;font-size:24px;letter-spacing:3px;color:#8b8f98}
.prog{position:absolute;top:112px;left:64px;right:64px;display:flex;gap:8px}
.prog i{flex:1;height:4px;border-radius:2px;background:rgba(255,255,255,.14)}
.prog i.on{background:var(--c)}
.prog i.done{background:rgba(255,255,255,.55)}
.tag{display:inline-flex;align-items:center;gap:14px;border:1.5px solid rgba(var(--rgb),.55);background:rgba(var(--rgb),.08);
  padding:11px 20px 10px 16px;border-radius:999px;font-weight:800;font-size:22px;letter-spacing:3px}
.tag b{width:16px;height:16px;border-radius:4px;background:var(--c);box-shadow:0 0 18px var(--c)}
.tag span{color:#9aa0aa;font-weight:700}
.h1{font-family:'Inter Display';font-weight:900;text-transform:uppercase;line-height:.95;letter-spacing:-1.5px}
.acc{color:var(--c)}
.mut{color:#9aa0aa}
.foot{position:absolute;left:64px;right:64px;bottom:46px;display:flex;justify-content:space-between;align-items:flex-end;
  font-size:19px;color:#6d727c;font-weight:500;letter-spacing:.3px}
.foot .site{font-weight:800;color:#d9dbe0;letter-spacing:2px;font-size:20px}
.card{background:linear-gradient(180deg,rgba(255,255,255,.055),rgba(255,255,255,.02));border:1px solid rgba(255,255,255,.09);border-radius:22px}
.lbl{font-size:20px;letter-spacing:3px;font-weight:800;color:#8b8f98;text-transform:uppercase}
.mono{font-family:'DejaVu Sans Mono',monospace}
.swipe{position:absolute;right:64px;bottom:96px;font-weight:800;font-size:22px;letter-spacing:3px;color:#fff;display:flex;align-items:center;gap:12px}
.swipe em{font-style:normal;color:var(--c);font-size:30px}
"""


def page(cat, body, idx=None, total=None, source="", extra_css=""):
    k = CAT[cat]
    prog = ""
    if total:
        segs = []
        for i in range(total):
            cls = "on" if i == idx else ("done" if i < idx else "")
            segs.append(f'<i class="{cls}"></i>')
        prog = f'<div class="prog">{"".join(segs)}</div>'
    else:
        prog = '<div class="prog"><i class="on"></i></div>'
    pager = f'{idx+1:02d} / {total:02d}' if total else ''
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}{extra_css}
:root{{--c:{k['c']};--rgb:{k['rgb']}}}</style></head><body>
<div class="bg"></div><div class="grid"></div>
<div class="hdr"><div class="logo">EDGERLANE <span class="pill">MEDIA</span></div><div class="date">{DATE_TAG}</div></div>
{prog}
{body}
<div class="foot"><div>{source}</div><div style="text-align:right"><div class="site">EDGERLANE.COM</div>{('<div style="margin-top:6px">'+pager+'</div>') if pager else ''}</div></div>
</body></html>"""


def tag(cat, sub):
    return f'<div class="tag"><b></b>{CAT[cat]["name"]}<span>· {sub}</span></div>'


# ---------------- Isometric engine ----------------
def _mix(hexc, f):
    hexc = hexc.lstrip('#')
    r, g, b = int(hexc[0:2], 16), int(hexc[2:4], 16), int(hexc[4:6], 16)
    return '#%02x%02x%02x' % (int(r*f), int(g*f), int(b*f))


class Iso:
    def __init__(self, ox, oy, s):
        self.ox, self.oy, self.s = ox, oy, s
        self.items = []  # (depth, svg)
        self.bb = [1e9, 1e9, -1e9, -1e9]

    def grow(self, x, y):
        b = self.bb
        b[0], b[1], b[2], b[3] = min(b[0], x), min(b[1], y), max(b[2], x), max(b[3], y)

    def p(self, x, y, z):
        q = (self.ox + (x - y) * self.s * 0.866, self.oy + (x + y) * self.s * 0.5 - z * self.s)
        self.grow(*q)
        return q

    def poly(self, pts, fill, stroke="rgba(255,255,255,.10)", sw=1.2, extra=""):
        d = " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)
        return f'<polygon points="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" {extra}/>'

    def box(self, x, y, z, w, d, h, accent=None, glow=False, tone=1.0, top_grad=True):
        P = self.p
        if accent:
            top, left, right = accent, _mix(accent, .62), _mix(accent, .40)
            stroke = "rgba(255,255,255,.35)"
        else:
            top = _mix("#3d424b", tone); left = _mix("#1d2026", tone); right = _mix("#121418", tone)
            stroke = "rgba(255,255,255,.11)"
        g = []
        f = ' filter="url(#glow)"' if glow else ''
        g.append(f'<g{f}>')
        g.append(self.poly([P(x, y+d, z), P(x+w, y+d, z), P(x+w, y+d, z+h), P(x, y+d, z+h)], left, stroke))
        g.append(self.poly([P(x+w, y, z), P(x+w, y+d, z), P(x+w, y+d, z+h), P(x+w, y, z+h)], right, stroke))
        g.append(self.poly([P(x, y, z+h), P(x+w, y, z+h), P(x+w, y+d, z+h), P(x, y+d, z+h)], top, stroke))
        # specular edge on top front corner
        a, b = P(x+w, y+d, z+h), P(x+w, y+d, z)
        g.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="rgba(255,255,255,{0.55 if accent else 0.22})" stroke-width="1.6"/>')
        g.append('</g>')
        self.items.append((x + y + z + (w + d) / 2, "".join(g)))

    def cyl(self, x, y, z, r, h, color, glow=False, bands=2):
        """Vertical cylinder (oil barrel) centred at x,y."""
        cx, cy_bot = self.p(x, y, z)
        _, cy_top = self.p(x, y, z + h)
        rx = r * self.s * 0.866 * 1.414 * .82
        ry = rx * 0.5
        dark, mid = _mix(color, .35), _mix(color, .7)
        gid = f"cg{abs(hash((x,y,z,color)))%99999}"
        f = ' filter="url(#glow)"' if glow else ''
        s = [f'<g{f}><defs><linearGradient id="{gid}" x1="0" x2="1"><stop offset="0" stop-color="{dark}"/><stop offset=".35" stop-color="{mid}"/><stop offset=".55" stop-color="{color}"/><stop offset="1" stop-color="{dark}"/></linearGradient></defs>']
        s.append(f'<path d="M{cx-rx:.1f},{cy_top:.1f} L{cx-rx:.1f},{cy_bot:.1f} A{rx:.1f},{ry:.1f} 0 0 0 {cx+rx:.1f},{cy_bot:.1f} L{cx+rx:.1f},{cy_top:.1f} Z" fill="url(#{gid})" stroke="rgba(255,255,255,.25)"/>')
        for k in range(1, bands + 1):
            yy = cy_bot + (cy_top - cy_bot) * k / (bands + 1)
            s.append(f'<path d="M{cx-rx:.1f},{yy:.1f} A{rx:.1f},{ry:.1f} 0 0 0 {cx+rx:.1f},{yy:.1f}" fill="none" stroke="rgba(0,0,0,.45)" stroke-width="3"/>')
            s.append(f'<path d="M{cx-rx:.1f},{yy-3:.1f} A{rx:.1f},{ry:.1f} 0 0 0 {cx+rx:.1f},{yy-3:.1f}" fill="none" stroke="rgba(255,255,255,.25)" stroke-width="1.2"/>')
        s.append(f'<ellipse cx="{cx:.1f}" cy="{cy_top:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{_mix(color,.85)}" stroke="rgba(255,255,255,.5)"/>')
        s.append(f'<ellipse cx="{cx:.1f}" cy="{cy_top:.1f}" rx="{rx*.72:.1f}" ry="{ry*.72:.1f}" fill="none" stroke="rgba(0,0,0,.3)" stroke-width="2"/>')
        s.append(f'<circle cx="{cx+rx*.35:.1f}" cy="{cy_top-ry*.1:.1f}" r="{rx*.09:.1f}" fill="{dark}"/></g>')
        self.items.append((x + y + z + .5, "".join(s)))

    def raw(self, depth, svg):
        self.items.append((depth, svg))

    def label(self, x, y, z, text, sub="", color="#fff", dx=40, dy=-70):
        """Leader-line callout from a 3D point."""
        a = self.p(x, y, z)
        bx, by = a[0] + dx, a[1] + dy
        anchor = "start" if dx >= 0 else "end"
        tx = bx + (10 if dx >= 0 else -10)
        self.grow(bx + (380 if dx >= 0 else -380), by - 50); self.grow(bx, by + 36)
        s = (f'<circle cx="{a[0]:.1f}" cy="{a[1]:.1f}" r="5" fill="{color}"/>'
             f'<polyline points="{a[0]:.1f},{a[1]:.1f} {bx:.1f},{by:.1f} {bx + (150 if dx>=0 else -150):.1f},{by:.1f}" fill="none" stroke="rgba(255,255,255,.55)" stroke-width="1.5"/>'
             f'<text x="{tx:.1f}" y="{by-14:.1f}" text-anchor="{anchor}" font-family="Inter" font-weight="800" font-size="30" letter-spacing="2" fill="{color}">{text}</text>')
        if sub:
            s += f'<text x="{tx:.1f}" y="{by+32:.1f}" text-anchor="{anchor}" font-family="Inter" font-weight="500" font-size="25" fill="#b4b8c0">{sub}</text>'
        self.items.append((999, s))

    def svg(self, w, h, accent="#fff", pad=40, padtop=60):
        body = "".join(s for _, s in sorted(self.items, key=lambda t: t[0]))
        x0, y0, x1, y1 = self.bb
        vb = f"{x0-pad:.0f} {y0-padtop:.0f} {x1-x0+2*pad:.0f} {y1-y0+pad+padtop:.0f}"
        return (f'<svg width="{w}" height="{h}" viewBox="{vb}" preserveAspectRatio="xMidYMid meet" overflow="visible" xmlns="http://www.w3.org/2000/svg"><defs>'
                f'<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="9" result="b"/>'
                f'<feFlood flood-color="{accent}" flood-opacity=".55"/><feComposite in2="b" operator="in" result="g"/>'
                f'<feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>{body}</svg>')


def platform(iso, x0, y0, n, m, tone=.8):
    for i in range(n):
        for j in range(m):
            iso.box(x0 + i, y0 + j, 0, .96, .96, .18, tone=tone)


# ---------------- Line chart ----------------
def line_chart(points, w, h, color, ymin, ymax, yticks, xlabels, pad=(70, 30, 30, 50), annotate=None, fmt=lambda v: f"{v}", unit=""):
    """points: list of (xfrac 0..1, value). xlabels: list of (xfrac, text)."""
    L, T, R, B = pad
    pw, ph = w - L - R, h - T - B
    X = lambda f: L + f * pw
    Y = lambda v: T + (1 - (v - ymin) / (ymax - ymin)) * ph
    rgbc = color
    s = [f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg"><defs>'
         f'<linearGradient id="lf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{rgbc}" stop-opacity=".35"/><stop offset="1" stop-color="{rgbc}" stop-opacity="0"/></linearGradient>'
         f'<filter id="lg"><feGaussianBlur stdDeviation="6"/></filter></defs>']
    for v in yticks:
        s.append(f'<line x1="{L}" x2="{w-R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="rgba(255,255,255,.08)" stroke-dasharray="3 6"/>')
        s.append(f'<text x="{L-16}" y="{Y(v)+7:.1f}" text-anchor="end" font-family="DejaVu Sans Mono" font-size="20" fill="#6d727c">{fmt(v)}{unit}</text>')
    for f, t in xlabels:
        s.append(f'<text x="{X(f):.1f}" y="{h-12}" text-anchor="middle" font-family="DejaVu Sans Mono" font-size="20" fill="#6d727c">{t}</text>')
    path = " ".join(f"{'M' if i==0 else 'L'}{X(f):.1f},{Y(v):.1f}" for i, (f, v) in enumerate(points))
    area = path + f" L{X(points[-1][0]):.1f},{Y(ymin):.1f} L{X(points[0][0]):.1f},{Y(ymin):.1f} Z"
    s.append(f'<path d="{area}" fill="url(#lf)"/>')
    s.append(f'<path d="{path}" fill="none" stroke="{rgbc}" stroke-width="7" opacity=".5" filter="url(#lg)"/>')
    s.append(f'<path d="{path}" fill="none" stroke="{rgbc}" stroke-width="4" stroke-linejoin="round"/>')
    for f, v in points:
        s.append(f'<circle cx="{X(f):.1f}" cy="{Y(v):.1f}" r="5" fill="#07080A" stroke="{rgbc}" stroke-width="2.5"/>')
    if annotate:
        for (f, v, txt, side) in annotate:
            x, y = X(f), Y(v)
            dx = 14 if side == "r" else -14
            anc = "start" if side == "r" else "end"
            s.append(f'<text x="{x+dx:.1f}" y="{y-16:.1f}" text-anchor="{anc}" font-family="Inter" font-weight="800" font-size="22" fill="#fff">{txt}</text>')
    lf, lv = points[-1]
    s.append(f'<circle cx="{X(lf):.1f}" cy="{Y(lv):.1f}" r="16" fill="{rgbc}" opacity=".25"/><circle cx="{X(lf):.1f}" cy="{Y(lv):.1f}" r="8" fill="{rgbc}"/>')
    s.append('</svg>')
    return "".join(s)


def date_frac(d, start, end):
    a, b, c = [datetime.strptime(x, "%Y-%m-%d") for x in (d, start, end)]
    return (a - b).days / (c - b).days
