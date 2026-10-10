import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *

POSTS = {}  # filename -> html
LEGAL = "Contenu informatif, pas un conseil en investissement."


def iso_bars(values, labels, accent, ox, oy, s, base=3.0, k=2.2, w=1.0, gap=1.6, glow_last=True, fmt=None):
    iso = Iso(ox, oy, s)
    n = len(values)
    platform(iso, -1, -1, int(n * gap) + 2, 3, tone=.75)
    for i, v in enumerate(values):
        h = (v - base) * k + .4
        last = i == n - 1
        iso.box(i * gap, .2, .18, w, w, h, accent=accent if last else None, glow=last and glow_last, tone=1.0 + i * .06)
    return iso


# =====================================================================
# POST 1 — ÉCONOMIE · TAUX US (single, 3D)
# =====================================================================
def post1():
    vals = [3.90, 4.14, 4.30, 4.95, 5.36]
    labs = ["FÉV.", "6 MARS", "7 AVR.", "10 SEPT.", "7 OCT."]
    iso = Iso(470, 520, 62)
    for a in range(-2, 8):
        for b in range(-8, 2):
            if -2 <= a + b <= 1: iso.box(a, b, 0, .96, .96, .18, tone=.7)
    for i, v in enumerate(vals):
        h = (v - 3.4) * 2.6 + .3
        last = i == len(vals) - 1
        iso.box(i * 1.2, -i * 1.2, .18, 1.0, 1.0, h, accent="#F5B80B" if last else None, glow=last, tone=1 + i * .07)
    scene = iso.svg(1000, 560, "#F5B80B")
    body = f"""
<div style="position:absolute;top:160px;left:64px">{tag('eco','TAUX US')}</div>
<div class="h1" style="position:absolute;top:240px;left:64px;right:64px;font-size:84px">Le 10 ans US au plus<br>haut <span class="acc">depuis 2002</span></div>
<div style="position:absolute;top:420px;left:40px">{iso.svg(1000, 470, "#F5B80B")}</div>
<div style="position:absolute;top:900px;left:64px;right:64px;display:grid;grid-template-columns:repeat(5,1fr);gap:10px;text-align:center">
{''.join(f'<div><div class="mono" style="font-size:19px;color:#8b8f98">{l}</div><div style="font-size:{40 if i==4 else 32}px;font-weight:900;margin-top:4px;color:{"#F5B80B" if i==4 else "#fff"}">{str(v).replace(".", ",")} %</div></div>' for i,(l,v) in enumerate(zip(labs,vals)))}
</div>
<div class="card" style="position:absolute;left:64px;right:64px;top:1030px;padding:28px 34px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:26px">
  <div><div class="lbl">Fed (sept.)</div><div style="font-size:38px;font-weight:900;margin-top:8px">3,75–4 %</div><div class="mut" style="font-size:19px;margin-top:6px">1re hausse depuis 2023</div></div>
  <div><div class="lbl">Hausse fin oct. ?</div><div style="font-size:38px;font-weight:900;margin-top:8px">17 %</div><div class="mut" style="font-size:19px;margin-top:6px">proba CME FedWatch (7 oct.)</div></div>
  <div><div class="lbl">Impact</div><div style="font-size:24px;font-weight:800;margin-top:10px;line-height:1.2">Valorisations tech sous pression</div></div>
</div>"""
    POSTS["01_ECO_taux-us-10ans.png"] = page("eco", body, source="Sources : Anadolu, XTB, Reuters/CME FedWatch · pic en séance du mer. 7 oct. 2026")


# =====================================================================
# POST 2 — ÉCONOMIE · PÉTROLE (carrousel 6 slides)
# =====================================================================
def post2():
    T = 6
    GOLD = "#F5B80B"
    # --- slide 1 : cover with barrels
    iso = Iso(560, 500, 70)
    platform(iso, -1, -1, 6, 5, tone=.7)
    for (x, y) in [(0, 0), (1.25, 0), (2.5, 0), (0, 1.25), (1.25, 1.25), (2.5, 1.25), (0, 2.5), (1.25, 2.5)]:
        iso.cyl(x + .5, y + .5, .18, .42, 1.9, GOLD if (x, y) != (2.5, 2.5) else GOLD, glow=(x, y) == (1.25, 1.25))
    iso.cyl(1.25 + .5, .5, 2.1, .42, 1.9, GOLD, glow=True)
    iso.box(3.6, 2.5, .18, 1, 1, 2.6, tone=1.1)
    iso.box(3.6, 3.6, .18, 1, 1, 1.5, tone=1.0)
    iso.box(-1, 3.6, .18, 1, 1, 3.2, tone=1.15)
    iso.label(1.75, .5, 4.0, "BRENT · MER DU NORD", "Référence mondiale", color=GOLD, dx=-150, dy=-40)
    scene = iso.svg(1000, 500, GOLD)
    s1 = f"""
<div style="position:absolute;top:160px;left:64px">{tag('eco','PÉTROLE')}</div>
<div class="h1" style="position:absolute;top:240px;left:64px;right:64px;font-size:92px">Le pétrole<br>repasse les <span class="acc">100 $</span></div>
<div style="position:absolute;top:460px;left:40px">{scene}</div>
<div style="position:absolute;left:64px;top:985px">
  <div class="lbl">Baril de Brent · jeu. 8 oct.</div>
  <div style="display:flex;align-items:baseline;gap:22px;margin-top:6px"><div class="h1 acc" style="font-size:150px;letter-spacing:-4px">105 $</div>
  <div style="font-size:40px;font-weight:900;color:{GREEN}">▲ 4,2 %</div></div>
</div>
<div class="swipe">DÉCRYPTAGE <em>→</em></div>"""
    POSTS["02_ECO_petrole_1.png"] = page("eco", s1, 0, T, "Source : Zonebourse · cours en séance du jeu. 8 oct. 2026")

    # --- slide 2 : what happens
    def row(n, title, txt):
        return f"""<div class="card" style="padding:30px 34px;display:flex;gap:28px;align-items:flex-start">
<div class="mono acc" style="font-size:30px;font-weight:700;min-width:50px">{n}</div>
<div><div style="font-size:33px;font-weight:900;text-transform:uppercase;letter-spacing:-.3px">{title}</div>
<div class="mut" style="font-size:25px;line-height:1.35;margin-top:10px">{txt}</div></div></div>"""
    s2 = f"""
<div style="position:absolute;top:160px;left:64px">{tag('eco','PÉTROLE')}</div>
<div class="h1" style="position:absolute;top:240px;left:64px;font-size:76px">Ce qu'il faut<br><span class="acc">retenir</span></div>
<div style="position:absolute;top:470px;left:64px;right:64px;display:flex;flex-direction:column;gap:22px">
{row('01','Ormuz reste un goulot',"Le détroit tourne toujours à environ la moitié de ses flux d'avant-guerre (6 à 10 M de barils/jour selon les estimations).")}
{row('02','Nouvelle escalade',"L'Iran a intensifié ses attaques contre le trafic maritime d'Ormuz cette semaine.")}
{row('03','Retour au-dessus de 100 $',"Le Brent a clôturé au-dessus de 100 $ en début de semaine, puis a pris ~4 % jeudi, vers 105 $.")}
</div>"""
    POSTS["02_ECO_petrole_2.png"] = page("eco", s2, 1, T, "Sources : Bloomberg, HSBC, Market Index, Reuters, Zonebourse · 7-8 oct. 2026")

    # --- slide 3 : chart
    pts_raw = [("2026-03-06", 93.3), ("2026-03-09", 119), ("2026-03-20", 107), ("2026-05-05", 115), ("2026-05-07", 100),
               ("2026-06-26", 79), ("2026-07-23", 100), ("2026-08-04", 79), ("2026-09-09", 100.5), ("2026-09-10", 108),
               ("2026-09-25", 97.5), ("2026-10-01", 102.3), ("2026-10-08", 105)]
    st, en = "2026-03-01", "2026-10-15"
    pts = [(date_frac(d, st, en), v) for d, v in pts_raw]
    xl = [(date_frac(d, st, en), t) for d, t in [("2026-03-15", "MARS"), ("2026-04-15", "AVR."), ("2026-05-15", "MAI"), ("2026-06-15", "JUIN"),
                                                 ("2026-07-15", "JUIL."), ("2026-08-15", "AOÛT"), ("2026-09-15", "SEPT."), ("2026-10-08", "OCT.")]]
    ann = [(pts[1][0], 119, "119 $", "r"), (pts[5][0], 79, "< 80 $", "r"), (pts[-1][0], 105, "105 $", "l")]
    ch = line_chart(pts, 952, 560, GOLD, 70, 125, [70, 80, 90, 100, 110, 120], xl, annotate=ann, unit=" $", pad=(90, 40, 30, 50))
    s3 = f"""
<div style="position:absolute;top:160px;left:64px">{tag('eco','BRENT 2026')}</div>
<div class="h1" style="position:absolute;top:240px;left:64px;font-size:76px">Les montagnes<br><span class="acc">russes</span> du baril</div>
<div class="mut" style="position:absolute;top:440px;left:64px;font-size:24px">Brent, en $ par baril · repères clés depuis mars 2026</div>
<div class="card" style="position:absolute;top:500px;left:64px;right:64px;padding:26px 0 20px">{ch}</div>
<div style="position:absolute;top:1130px;left:64px;right:64px;font-size:21px;color:#6d727c;line-height:1.4">Points relevés dans la presse financière (clôtures et extrêmes en séance). Ce n'est pas une série quotidienne complète.</div>"""
    POSTS["02_ECO_petrole_3.png"] = page("eco", s3, 2, T, "Sources : BNP Paribas, Reuters, AP, OCBC, AFP, Argaam, Zonebourse")

    # --- slide 4 : bank scenarios
    def scen(bank, val, txt, w):
        return f"""<div class="card" style="padding:28px 32px">
<div style="display:flex;justify-content:space-between;align-items:baseline"><div class="lbl" style="color:#d9dbe0">{bank}</div><div class="h1 acc" style="font-size:58px">{val}</div></div>
<div style="height:10px;border-radius:5px;background:rgba(255,255,255,.08);margin:16px 0 14px;overflow:hidden"><div style="width:{w}%;height:100%;background:linear-gradient(90deg,rgba(245,184,11,.25),#F5B80B)"></div></div>
<div class="mut" style="font-size:23px;line-height:1.35">{txt}</div></div>"""
    s4 = f"""
<div style="position:absolute;top:160px;left:64px">{tag('eco','SCÉNARIOS')}</div>
<div class="h1" style="position:absolute;top:240px;left:64px;font-size:76px">Ce qu'anticipent<br>les <span class="acc">banques</span></div>
<div style="position:absolute;top:470px;left:64px;right:64px;display:flex;flex-direction:column;gap:20px">
{scen('GOLDMAN SACHS · risque haussier','120 $',"Possible si les attaques contre le transport maritime s'intensifient (début sept.).",100)}
{scen('HSBC · moyenne 2026','90 $',"Prévision relevée de 80 à 90 $. Marché rééquilibré pas avant mi-2027 (début sept.).",75)}
{scen('CONSENSUS REUTERS · moyenne 2026','89 $',"Sondage de 30 analystes (sept.) : fourchette de 77 à 98 $.",74)}
</div>
<div style="position:absolute;top:1150px;left:64px;right:64px;font-size:21px;color:#6d727c">Scénarios d'analystes, pas des certitudes.</div>"""
    POSTS["02_ECO_petrole_4.png"] = page("eco", s4, 3, T, "Sources : Bloomberg/Goldman Sachs, WSJ/HSBC, Reuters · sept. 2026")

    # --- slide 5 : market impact chain
    def node(lbl, big, sub, color="#fff"):
        return f"""<div class="card" style="padding:24px 30px;display:flex;justify-content:space-between;align-items:center">
<div><div class="lbl">{lbl}</div><div class="mut" style="font-size:21px;margin-top:6px">{sub}</div></div>
<div class="h1" style="font-size:52px;color:{color}">{big}</div></div>"""
    arrow = '<div style="text-align:center;color:#F5B80B;font-size:30px;line-height:1;margin:-4px 0">↓</div>'
    s5 = f"""
<div style="position:absolute;top:160px;left:64px">{tag('eco','IMPACT MARCHÉ')}</div>
<div class="h1" style="position:absolute;top:240px;left:64px;font-size:76px">L'effet <span class="acc">domino</span></div>
<div style="position:absolute;top:380px;left:64px;right:64px;display:flex;flex-direction:column;gap:12px">
{node('Pétrole','105 $','Brent, jeu. 8 oct.','#F5B80B')}{arrow}
{node('Inflation anticipée','3,9 %','à 1 an, sept. · plus haut depuis mai 2023')}{arrow}
{node('Taux US 10 ans','5,36 %','pic du 7 oct. · plus haut depuis 2002')}{arrow}
{node('EUR/USD','< 1,12','jeu. 8 oct. · dollar vers un plus haut 2026')}
</div>"""
    POSTS["02_ECO_petrole_5.png"] = page("eco", s5, 4, T, "Sources : Market Index, XTB, Anadolu · 7-8 oct. 2026")

    # --- slide 6 : watch + tip + CTA
    s6 = f"""
<div style="position:absolute;top:160px;left:64px">{tag('eco','À SURVEILLER')}</div>
<div class="h1" style="position:absolute;top:240px;left:64px;font-size:76px">La suite <span class="acc">cette semaine</span></div>
<div style="position:absolute;top:400px;left:64px;right:64px;display:flex;flex-direction:column;gap:14px">
  <div class="card" style="padding:22px 30px;display:flex;gap:26px;align-items:center"><div class="mono acc" style="font-size:24px;min-width:150px">MER. 14</div><div style="font-size:28px;font-weight:800">Inflation US (CPI) de septembre</div></div>
  <div class="card" style="padding:22px 30px;display:flex;gap:26px;align-items:center"><div class="mono acc" style="font-size:24px;min-width:150px">JEU. 15</div><div style="font-size:28px;font-weight:800">Prix à la production + ventes au détail US</div></div>
  <div class="card" style="padding:22px 30px;display:flex;gap:26px;align-items:center"><div class="mono acc" style="font-size:24px;min-width:150px">EN CONTINU</div><div style="font-size:28px;font-weight:800">Trafic dans le détroit d'Ormuz</div></div>
</div>
<div style="position:absolute;top:800px;left:64px;right:64px;padding:34px 36px;border-radius:22px;border:1.5px solid rgba(245,184,11,.5);background:rgba(245,184,11,.06)">
  <div class="lbl acc">Conseil du jour</div>
  <div style="font-size:34px;font-weight:800;line-height:1.3;margin-top:12px">Quand la volatilité monte, ta taille de position doit baisser. Ajuste ton risque à la volatilité, pas à ta conviction.</div>
</div>
<div style="position:absolute;top:1110px;left:64px;right:64px;font-size:30px;font-weight:800">Journalise tes trades sur <span class="acc">edgerlane.com</span></div>"""
    POSTS["02_ECO_petrole_6.png"] = page("eco", s6, 5, T, LEGAL)


# =====================================================================
# POST 3 — FRANCE · SPREAD OAT-BUND (single, 3D bars)
# =====================================================================
def post3():
    BLUE = "#3B6BFF"
    data = [("FÉV. 2026", 55, False), ("1ER AOÛT", 90, False), ("OCT. 2026", 140, True)]
    iso = Iso(380, 560, 66)
    for a in range(-2, 7):
        for b in range(-7, 2):
            if -2 <= a + b <= 1: iso.box(a, b, 0, .96, .96, .18, tone=.7)
    for i, (lab, v, hot) in enumerate(data):
        h = v / 30
        x = i * 1.25
        iso.box(x, -x, .18, 1.1, 1.1, h, accent=BLUE if hot else None, glow=hot, tone=1 + i * .08)
    # 2011 reference ghost bar
    x = 3 * 1.25
    h = 225 / 30
    a = iso.p(x, .1, .18); b = iso.p(x + 1.1, .1, .18 + h)
    iso.box(x, -x, .18, 1.1, 1.1, h, tone=.55)
    scene = iso.svg(1000, 520, BLUE, padtop=70)
    body = f"""
<div style="position:absolute;top:160px;left:64px">{tag('fr','DETTE')}</div>
<div class="h1" style="position:absolute;top:240px;left:64px;right:64px;font-size:80px">Le coût de la dette<br>française <span class="acc">s'envole</span></div>
<div class="mut" style="position:absolute;top:420px;left:64px;font-size:24px">Écart de taux France–Allemagne à 10 ans (spread OAT-Bund)</div>
<div style="position:absolute;top:470px;left:40px">{iso.svg(1000, 430, BLUE)}</div>
<div style="position:absolute;top:910px;left:64px;right:64px;display:grid;grid-template-columns:repeat(4,1fr);gap:10px;text-align:center">
<div><div class="mono" style="font-size:19px;color:#8b8f98">FÉV. 2026</div><div style="font-size:34px;font-weight:900;margin-top:4px">55 pb</div></div>
<div><div class="mono" style="font-size:19px;color:#8b8f98">1ER AOÛT</div><div style="font-size:34px;font-weight:900;margin-top:4px">≈90 pb</div></div>
<div><div class="mono" style="font-size:19px;color:#8b8f98">OCT. 2026</div><div style="font-size:42px;font-weight:900;margin-top:4px;color:#3B6BFF">140 pb</div></div>
<div><div class="mono" style="font-size:19px;color:#6d727c">CRISE 2011</div><div style="font-size:34px;font-weight:900;margin-top:4px;color:#6d727c">&gt; 225 pb</div></div>
</div>
<div class="card" style="position:absolute;left:64px;right:64px;top:1030px;padding:22px 34px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:24px">
  <div><div class="lbl">OAT 10 ans</div><div style="font-size:40px;font-weight:900;margin-top:8px">4,98 %</div><div class="mut" style="font-size:18px;margin-top:4px">2 oct. · plus haut depuis 2002</div></div>
  <div><div class="lbl">Dette / PIB</div><div style="font-size:40px;font-weight:900;margin-top:8px">119,3 %</div><div class="mut" style="font-size:18px;margin-top:4px">prévision 2026</div></div>
  <div><div class="lbl">Spread</div><div style="font-size:40px;font-weight:900;margin-top:8px">≈140 pb</div><div class="mut" style="font-size:18px;margin-top:4px">plus haut depuis 2011-12</div></div>
</div>"""
    POSTS["03_FRANCE_spread-oat-bund.png"] = page("fr", body, source="Sources : Allianz GI, Zonebourse, Boursier.com, QuiFinanza · 1-6 oct. 2026 · « ≈90 pb » déduit")


# =====================================================================
# POST 4 — FRANCE · BUDGET 2027 (carrousel 5 slides)
# =====================================================================
def post4():
    T = 5
    BLUE = "#3B6BFF"
    # cover : isometric "hémicycle" building
    iso = Iso(540, 470, 58)
    platform(iso, -2, -1, 9, 5, tone=.7)
    iso.box(-1, 0, .18, 7, 3, .35, tone=1.1)           # stylobate
    iso.box(-.6, .3, .53, 6.2, 2.4, .25, tone=1.2)
    for i in range(7):                                    # colonnes
        iso.box(-.4 + i * .95, 2.3, .78, .38, .38, 2.2, tone=1.35)
    iso.box(-.6, .3, .78, 6.2, 2.0, 2.2, tone=.9)       # corps
    iso.box(-.8, .1, 2.98, 6.6, 2.8, .32, accent=BLUE, glow=True)  # entablement
    iso.box(.6, .8, 3.3, 3.8, 1.4, .5, tone=1.2)
    iso.box(4.2, 3.6, .18, .9, .9, 2.4, tone=1.0)
    iso.box(-2, 3.4, .18, .9, .9, 1.4, tone=1.0)
    iso.label(2.5, 1.5, 3.8, "ASSEMBLÉE NATIONALE", "PLF 2027 en séance dès le 13 oct.", color=BLUE, dx=60, dy=-70)
    scene = iso.svg(1000, 500, BLUE)
    s1 = f"""
<div style="position:absolute;top:160px;left:64px">{tag('fr','BUDGET 2027')}</div>
<div class="h1" style="position:absolute;top:240px;left:64px;right:64px;font-size:84px">Budget 2027 :<br><span class="acc">le match commence</span></div>
<div style="position:absolute;top:500px;left:40px">{scene}</div>
<div style="position:absolute;left:64px;top:1010px">
  <div class="lbl">Effort budgétaire visé pour 2027</div>
  <div class="h1 acc" style="font-size:150px;letter-spacing:-4px;margin-top:6px">43 Md€</div>
</div>
<div class="swipe">EN 5 SLIDES <em>→</em></div>"""
    POSTS["04_FRANCE_budget2027_1.png"] = page("fr", s1, 0, T, "Sources : Public Sénat, Le Club des juristes · PLF présenté le 1er oct. 2026")

    def tile(lbl, big, sub):
        return f"""<div class="card" style="padding:30px 30px"><div class="lbl">{lbl}</div>
<div class="h1" style="font-size:66px;margin-top:14px">{big}</div><div class="mut" style="font-size:22px;margin-top:10px;line-height:1.3">{sub}</div></div>"""
    s2 = f"""
<div style="position:absolute;top:160px;left:64px">{tag('fr','LES CHIFFRES')}</div>
<div class="h1" style="position:absolute;top:240px;left:64px;font-size:76px">4 chiffres<br>à <span class="acc">connaître</span></div>
<div style="position:absolute;top:470px;left:64px;right:64px;display:grid;grid-template-columns:1fr 1fr;gap:20px">
{tile('Déficit visé','5 %','du PIB en 2027')}
{tile('Dette publique','121,7 %','du PIB en 2027, après 119,3 % en 2026')}
{tile('Charge de la dette','72,9 Md€','en 2027, contre 62,6 Md€ en 2026')}
{tile('OAT 10 ans','≈5 %','a frôlé ce seuil début octobre')}
</div>"""
    POSTS["04_FRANCE_budget2027_2.png"] = page("fr", s2, 1, T, "Sources : PLF 2027, rapport sur la dette du 6 oct., Zonebourse, Boursier.com")

    def li(t, s):
        return f"""<div style="display:flex;gap:22px;padding:24px 0;border-bottom:1px solid rgba(255,255,255,.08)">
<div style="width:12px;height:12px;border-radius:3px;background:{BLUE};margin-top:14px;flex:none;box-shadow:0 0 14px {BLUE}"></div>
<div><div style="font-size:30px;font-weight:800">{t}</div><div class="mut" style="font-size:23px;margin-top:6px">{s}</div></div></div>"""
    s3 = f"""
<div style="position:absolute;top:160px;left:64px">{tag('fr','CONTENU')}</div>
<div class="h1" style="position:absolute;top:240px;left:64px;font-size:76px">Ce que prévoit<br>le <span class="acc">texte</span></div>
<div style="position:absolute;top:440px;left:64px;right:64px">
{li('Retraites','Désindexation partielle des pensions au-delà de 1 260 €')}
{li('Impôt sur le revenu',"Plafond de l'abattement de 10 % abaissé de 4 439 € à 3 000 €")}
{li('APL','Gel en 2027 au niveau de 2026 (budget de la Sécu)')}
{li('Aviation','Nouvelle taxe sur les fournisseurs de kérosène')}
{li('Études sup.','Inscription payante en BTS et prépa pour les non-boursiers')}
</div>"""
    POSTS["04_FRANCE_budget2027_3.png"] = page("fr", s3, 2, T, "Sources : Public Sénat, Le Club des juristes / Le Monde · oct. 2026")

    s4 = f"""
<div style="position:absolute;top:160px;left:64px">{tag('fr','IMPACT MARCHÉ')}</div>
<div class="h1" style="position:absolute;top:240px;left:64px;font-size:76px">Pourquoi les marchés<br><span class="acc">regardent</span></div>
<div style="position:absolute;top:470px;left:64px;right:64px;display:flex;flex-direction:column;gap:18px">
  <div class="card" style="padding:28px 32px"><div class="lbl">Pas de majorité</div><div style="font-size:28px;font-weight:700;margin-top:10px;line-height:1.35">Le texte doit trouver des voix dans une Assemblée fragmentée, à quelques mois de la présidentielle.</div></div>
  <div class="card" style="padding:28px 32px"><div class="lbl">Scénario évoqué</div><div style="font-size:28px;font-weight:700;margin-top:10px;line-height:1.35">Pour la banque BBH, une reconduction du budget 2026 est l'issue la plus probable.</div></div>
  <div class="card" style="padding:28px 32px"><div class="lbl">Qui détient la dette ?</div><div style="font-size:28px;font-weight:700;margin-top:10px;line-height:1.35">Près de <span class="acc">57 %</span> par des non-résidents : très sensibles au risque perçu, donc au spread.</div></div>
</div>"""
    POSTS["04_FRANCE_budget2027_4.png"] = page("fr", s4, 3, T, "Sources : LCP, BBH (1er oct.), Allianz GI · oct. 2026")

    s5 = f"""
<div style="position:absolute;top:160px;left:64px">{tag('fr','À SURVEILLER')}</div>
<div class="h1" style="position:absolute;top:240px;left:64px;font-size:76px">Les dates <span class="acc">clés</span></div>
<div style="position:absolute;top:400px;left:64px;right:64px;display:flex;flex-direction:column;gap:14px">
  <div class="card" style="padding:24px 30px;display:flex;gap:26px;align-items:center"><div class="mono acc" style="font-size:24px;min-width:170px">MAR. 13 OCT.</div><div style="font-size:28px;font-weight:800">Début de l'examen en séance à l'Assemblée</div></div>
  <div class="card" style="padding:24px 30px;display:flex;gap:26px;align-items:center"><div class="mono acc" style="font-size:24px;min-width:170px">EN CONTINU</div><div style="font-size:28px;font-weight:800">Spread OAT-Bund et banques du CAC 40</div></div>
  <div class="card" style="padding:24px 30px;display:flex;gap:26px;align-items:center"><div class="mono acc" style="font-size:24px;min-width:170px">31 DÉC.</div><div style="font-size:28px;font-weight:800">Date limite d'adoption du budget</div></div>
</div>
<div style="position:absolute;top:840px;left:64px;right:64px;padding:34px 36px;border-radius:22px;border:1.5px solid rgba(59,107,255,.55);background:rgba(59,107,255,.07)">
  <div class="lbl acc">Conseil du jour</div>
  <div style="font-size:33px;font-weight:800;line-height:1.3;margin-top:12px">Un vote politique peut créer un gap à l'ouverture. Vérifie ton calendrier avant de garder une position la nuit.</div>
</div>
<div style="position:absolute;top:1130px;left:64px;right:64px;font-size:30px;font-weight:800">Journalise tes trades sur <span class="acc">edgerlane.com</span></div>"""
    POSTS["04_FRANCE_budget2027_5.png"] = page("fr", s5, 4, T, LEGAL)


# =====================================================================
# POST 5 — USA · MIDTERMS (single, 3D ballot box)
# =====================================================================
def post5():
    RED = "#E5303A"
    iso = Iso(540, 450, 64)
    platform(iso, -2, -1, 7, 5, tone=.7)
    iso.box(0, 0, .18, 2.6, 2.6, 2.4, tone=1.25)                 # urne
    iso.box(-.05, -.05, 2.58, 2.7, 2.7, .25, accent=RED, glow=True)  # couvercle
    # slot on lid
    p1, p2, p3, p4 = iso.p(.6, 1.2, 2.84), iso.p(2.0, 1.2, 2.84), iso.p(2.0, 1.45, 2.84), iso.p(.6, 1.45, 2.84)
    iso.raw(50, iso.poly([p1, p2, p3, p4], "#050506", "rgba(0,0,0,.6)"))
    # ballot entering
    iso.raw(51, iso.poly([iso.p(.85, 1.32, 2.84), iso.p(1.75, 1.32, 2.84), iso.p(1.75, 1.32, 4.1), iso.p(.85, 1.32, 4.1)], "#f2f2f2", "rgba(0,0,0,.3)"))
    # side bars : House / Senate
    for i, (h, acc) in enumerate([(1.6, None), (2.6, RED), (1.1, None)]):
        iso.box(2.9 + i * 1.0, 2.9, .18, .8, .8, h, accent=acc, glow=False, tone=1 + i * .1)
    iso.box(-1.6, 2.6, .18, .9, .9, 1.8, tone=1.1)
    iso.label(1.3, 1.3, 4.1, "CONGRÈS AMÉRICAIN", "Chambre + 1/3 du Sénat", color=RED, dx=-120, dy=-50)
    scene = iso.svg(1000, 460, RED)
    def st(big, txt):
        return f"""<div class="card" style="padding:24px 26px"><div class="h1" style="font-size:52px">{big}</div><div class="mut" style="font-size:20px;margin-top:8px;line-height:1.3">{txt}</div></div>"""
    body = f"""
<div style="position:absolute;top:160px;left:64px">{tag('us','MIDTERMS')}</div>
<div class="h1" style="position:absolute;top:240px;left:64px;right:64px;font-size:96px">Midterms US :<br><span class="acc">J-24</span></div>
<div style="position:absolute;top:450px;left:40px">{scene}</div>
<div style="position:absolute;left:64px;right:64px;top:930px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px">
{st('3 NOV.','Élections de mi-mandat')}
{st('20 / 23','midterms perdues en sièges par le parti au pouvoir')}
{st('+14,1 %','S&amp;P 500 en moyenne 6 mois après (depuis 1970)')}
</div>
<div style="position:absolute;left:64px;right:64px;top:1150px;font-size:21px;color:#6d727c">Enjeu : un Congrès divisé limiterait l'agenda fiscal de la Maison-Blanche. Les performances passées ne préjugent pas des performances futures.</div>"""
    POSTS["05_USA_midterms-j24.png"] = page("us", body, source="Sources : BBH (1er oct.), Zacks, Webull · statistiques historiques")


# =====================================================================
# POST 6 — AGENDA DE LA SEMAINE (single, multi-catégories)
# =====================================================================
def post6():
    rows = [
        ("MAR. 13", "fr", "Budget 2027 : début de l'examen en séance"),
        ("MAR. 13", "eco", "Résultats UnitedHealth et Wells Fargo"),
        ("MER. 14", "eco", "Inflation US (CPI) + inflation Chine de sept."),
        ("JEU. 15", "eco", "Prix à la production + ventes au détail US"),
        ("FIN OCT.", "eco", "Fed : hausse ? Proba ≈17 % (7 oct.)"),
        ("3 NOV.", "us", "Midterms américaines"),
    ]
    h = ""
    for d, c, t in rows:
        k = CAT[c]
        h += f"""<div style="display:flex;align-items:center;gap:24px;padding:24px 28px;border-radius:18px;background:rgba(255,255,255,.035);border:1px solid rgba(255,255,255,.08);border-left:5px solid {k['c']}">
<div class="mono" style="font-size:22px;min-width:130px;color:{k['c']}">{d}</div>
<div style="flex:1;font-size:27px;font-weight:800">{t}</div>
<div style="font-size:15px;font-weight:800;letter-spacing:2px;color:{k['c']};border:1px solid {k['c']};padding:5px 10px;border-radius:999px">{k['name'].replace('POLITIQUE ','')}</div></div>"""
    legend = "".join(f'<span style="display:inline-flex;align-items:center;gap:10px;margin-right:30px"><b style="width:14px;height:14px;border-radius:3px;background:{CAT[c]["c"]}"></b>{CAT[c]["name"]}</span>' for c in ("eco", "fr", "us"))
    body = f"""
<div style="position:absolute;top:160px;left:64px"><div class="tag" style="border-color:rgba(255,255,255,.35)"><b style="background:#fff;box-shadow:none"></b>AGENDA<span>· SEMAINE DU 12 OCT.</span></div></div>
<div class="h1" style="position:absolute;top:240px;left:64px;font-size:86px">La semaine<br>à <span style="color:#F5B80B">sur</span><span style="color:#3B6BFF">veil</span><span style="color:#E5303A">ler</span></div>
<div style="position:absolute;top:470px;left:64px;right:64px;display:flex;flex-direction:column;gap:14px">{h}</div>
<div style="position:absolute;top:1150px;left:64px;font-size:20px;font-weight:700;color:#9aa0aa;letter-spacing:2px">{legend}</div>"""
    POSTS["06_AGENDA_semaine-12-oct.png"] = page("mix", body, source="Sources : Admiral Markets, Tickzen, CME FedWatch, LCP · horaires à confirmer")


for f in (post1, post2, post3, post4, post5, post6):
    f()
