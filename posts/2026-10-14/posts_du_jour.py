import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "engine"))
import lib
lib.DATE_TAG = "MER. 14.10.2026"
from lib import *

POSTS = {}
LEGAL = "Contenu informatif, pas un conseil en investissement."
GOLD = "#F5B80B"
RED = "#E5303A"
T = 5


# ---------- SLIDE 1 : couverture 3D ----------
def s1():
    iso = Iso(470, 520, 62)
    for a in range(-2, 7):
        for b in range(-7, 2):
            if -2 <= a + b <= 1:
                iso.box(a, b, 0, .96, .96, .18, tone=.7)
    # barres : inflation sur 1 an, août (réel) vs sept. (consensus)
    data = [(2.4, False), (2.5, False), (3.4, False), (3.6, True)]
    for i, (v, hot) in enumerate(data):
        h = v * 1.25
        x = i * 1.3
        iso.box(x, -x, .18, 1.0, 1.0, h, accent=GOLD if hot else None, glow=hot, tone=1 + i * .07)
    scene = iso.svg(1000, 440, GOLD)
    cols = [("SOUS-JACENTE", "AOÛT", "2,4 %", "#fff"), ("SOUS-JACENTE", "SEPT. (CONS.)", "2,5 %", "#fff"),
            ("TOTALE", "AOÛT", "3,4 %", "#fff"), ("TOTALE", "SEPT. (CONS.)", "3,6 %", GOLD)]
    row = "".join(f'<div><div class="mono" style="font-size:16px;color:#6d727c">{a}</div><div class="mono" style="font-size:18px;color:#8b8f98;margin-top:2px">{b}</div>'
                  f'<div style="font-size:{40 if c == "#F5B80B" else 32}px;font-weight:900;margin-top:4px;color:{c}">{v}</div></div>' for a, b, v, c in cols)
    body = f"""
<div style="position:absolute;top:160px;left:64px">{tag('eco','INFLATION US')}</div>
<div class="h1" style="position:absolute;top:240px;left:64px;right:64px;font-size:84px">Inflation US :<br>le chiffre <span class="acc">de 14h30</span></div>
<div class="mut" style="position:absolute;top:420px;left:64px;font-size:24px">Indice des prix (CPI) de septembre · hausse sur 1 an</div>
<div style="position:absolute;top:470px;left:40px">{scene}</div>
<div style="position:absolute;top:925px;left:64px;right:64px;display:grid;grid-template-columns:repeat(4,1fr);gap:10px;text-align:center">{row}</div>
<div style="position:absolute;left:64px;top:1075px">
  <div class="lbl">Consensus · inflation totale sur 1 mois</div>
  <div class="h1 acc" style="font-size:96px;letter-spacing:-3px;margin-top:4px">+0,6 %</div>
</div>
<div class="swipe" style="bottom:150px">LES SCÉNARIOS <em>→</em></div>"""
    POSTS["01_ECO_cpi-us_1.png"] = page("eco", body, 0, T,
        "Sources : WSJ/Dow Jones via InvestmentNews, Kiplinger · consensus du mar. 13 oct.")


# ---------- SLIDE 2 : le consensus ----------
def s2():
    rows = [("Inflation totale · sur 1 mois", "+0,4 %", "+0,6 %", True),
            ("Inflation totale · sur 1 an", "3,4 %", "3,6 %", True),
            ("Sous-jacente · sur 1 mois", "+0,3 %", "+0,2 %", False),
            ("Sous-jacente · sur 1 an", "2,4 %", "2,5 %", True)]
    h = """<div style="display:grid;grid-template-columns:1.6fr .7fr .9fr;padding:0 30px 6px" class="lbl"><div></div><div style="text-align:right">Août</div><div style="text-align:right">Sept. (cons.)</div></div>"""
    for name, prev, cons, up in rows:
        arrow = '<span style="font-size:22px;color:#9aa0aa">▲</span>' if up else '<span style="font-size:22px;color:#9aa0aa">▼</span>'
        h += f"""<div style="display:grid;grid-template-columns:1.6fr .7fr .9fr;align-items:center;padding:24px 30px;border-radius:18px;background:rgba(255,255,255,.035);border:1px solid rgba(255,255,255,.08)">
<div style="font-size:27px;font-weight:800">{name}</div>
<div style="font-size:34px;font-weight:900;text-align:right;color:#9aa0aa">{prev}</div>
<div style="font-size:40px;font-weight:900;text-align:right;color:{GOLD}">{arrow} {cons}</div></div>"""
    body = f"""
<div style="position:absolute;top:160px;left:64px">{tag('eco','LE CONSENSUS')}</div>
<div class="h1" style="position:absolute;top:240px;left:64px;right:64px;font-size:76px">Ce qu'attendent<br>les <span class="acc">économistes</span></div>
<div style="position:absolute;top:460px;left:64px;right:64px;display:flex;flex-direction:column;gap:14px">{h}</div>
<div class="card" style="position:absolute;top:1010px;left:64px;right:64px;padding:24px 30px">
  <div style="font-size:24px;line-height:1.4;color:#d9dbe0"><b style="color:{GOLD}">Sous-jacente</b> = hors énergie et alimentation. C'est elle que la Fed regarde de près.</div>
</div>"""
    POSTS["01_ECO_cpi-us_2.png"] = page("eco", body, 1, T,
        "Sources : consensus WSJ/Dow Jones (InvestmentNews, 13 oct.) · août : BLS")


# ---------- SLIDE 3 : pourquoi ----------
def s3():
    def row(n, title, big, txt):
        return f"""<div class="card" style="padding:28px 32px;display:flex;gap:26px;align-items:flex-start">
<div class="mono acc" style="font-size:28px;font-weight:700;min-width:46px">{n}</div>
<div style="flex:1"><div style="display:flex;justify-content:space-between;align-items:baseline;gap:20px">
<div style="font-size:31px;font-weight:900;text-transform:uppercase;letter-spacing:-.3px">{title}</div>
<div class="h1 acc" style="font-size:46px;white-space:nowrap">{big}</div></div>
<div class="mut" style="font-size:24px;line-height:1.35;margin-top:10px">{txt}</div></div></div>"""
    body = f"""
<div style="position:absolute;top:160px;left:64px">{tag('eco','POURQUOI')}</div>
<div class="h1" style="position:absolute;top:240px;left:64px;right:64px;font-size:76px">L'essence fait<br><span class="acc">grimper</span> le chiffre</div>
<div style="position:absolute;top:460px;left:64px;right:64px;display:flex;flex-direction:column;gap:18px">
{row('01','Essence','≈ +10 %',"Hausse sur un mois en septembre, un record pour ce mois selon Cetera. Elle gonfle l'inflation totale.")}
{row('02','Sous-jacente','+0,2 %',"Attendue en ralentissement après +0,3 % en août : c'est le vrai test pour la Fed.")}
{row('03','La Fed','3,75–4 %',"Fourchette de taux après la hausse du 16 sept., la première depuis 2023. Prochaine réunion : 27-28 oct.")}
</div>"""
    POSTS["01_ECO_cpi-us_3.png"] = page("eco", body, 2, T,
        "Sources : InvestmentNews (13 oct.), Kiplinger (13 oct.), Admiral Markets · Fed : réunion du 16 sept.")


# ---------- SLIDE 4 : scénarios ----------
def s4():
    def scen(lbl, cond, txt, col):
        return f"""<div class="card" style="padding:26px 32px;border-left:5px solid {col}">
<div style="display:flex;justify-content:space-between;align-items:baseline;gap:20px"><div style="font-size:32px;font-weight:900;color:{col}">{lbl}</div><div class="mono" style="font-size:20px;color:#9aa0aa">{cond}</div></div>
<div style="font-size:24px;line-height:1.38;margin-top:12px;color:#d9dbe0">{txt}</div></div>"""
    body = f"""
<div style="position:absolute;top:160px;left:64px">{tag('eco','SCÉNARIOS')}</div>
<div class="h1" style="position:absolute;top:240px;left:64px;right:64px;font-size:76px">3 scénarios<br>pour <span class="acc">14h30</span></div>
<div style="position:absolute;top:450px;left:64px;right:64px;display:flex;align-items:center;justify-content:space-between" class="card">
  <div style="padding:22px 30px"><div class="lbl">Proba d'une hausse de la Fed le 28 oct.</div><div class="mut" style="font-size:19px;margin-top:6px">CME FedWatch · mar. 13 oct.</div></div>
  <div class="h1 acc" style="font-size:64px;padding:0 30px">23,8 %</div>
</div>
<div style="position:absolute;top:610px;left:64px;right:64px;display:flex;flex-direction:column;gap:16px">
{scen('PLUS CHAUD', 'sous-jacente ≥ 0,3 %', "La proba de hausse en octobre pourrait monter. Pression possible sur les taux, soutien au dollar, tech et or sous pression.", RED)}
{scen('CONFORME', 'totale ≈ 0,6 % · sous-jac. 0,2 %', "Réaction souvent brève. Le relais pourrait venir des prix à la production jeudi.", "#9aa0aa")}
{scen('PLUS DOUX', 'sous-jacente ≤ 0,1 %', "Les paris sur une hausse pourraient reculer : détente possible des taux, dollar plus faible.", GREEN)}
</div>"""
    POSTS["01_ECO_cpi-us_4.png"] = page("eco", body, 3, T,
        "Sources : CME FedWatch via InvestmentNews (13 oct.) · seuils et scénarios : Admiral Markets")


# ---------- SLIDE 5 : à surveiller + conseil ----------
def s5():
    def ag(d, t):
        return f'<div class="card" style="padding:22px 30px;display:flex;gap:26px;align-items:center"><div class="mono acc" style="font-size:24px;min-width:240px">{d}</div><div style="font-size:28px;font-weight:800">{t}</div></div>'
    body = f"""
<div style="position:absolute;top:160px;left:64px">{tag('eco','À SURVEILLER')}</div>
<div class="h1" style="position:absolute;top:240px;left:64px;font-size:76px">Les dates <span class="acc">clés</span></div>
<div style="position:absolute;top:400px;left:64px;right:64px;display:flex;flex-direction:column;gap:14px">
{ag('MER. 14 · 14H30','Inflation US (CPI) de septembre')}
{ag('JEU. 15','Prix à la production US (PPI)')}
{ag('27-28 OCT.','Réunion de la Fed · décision le 28')}
</div>
<div style="position:absolute;top:800px;left:64px;right:64px;padding:34px 36px;border-radius:22px;border:1.5px solid rgba(245,184,11,.5);background:rgba(245,184,11,.06)">
  <div class="lbl acc">Conseil du jour</div>
  <div style="font-size:33px;font-weight:800;line-height:1.3;margin-top:12px">Une stat majeure peut faire sauter ton stop avec du slippage. Décide avant 14h30 : position réduite, ou à plat pendant l'annonce.</div>
</div>
<div style="position:absolute;top:1130px;left:64px;right:64px;font-size:30px;font-weight:800">Journalise tes trades sur <span class="acc">edgerlane.com</span></div>"""
    POSTS["01_ECO_cpi-us_5.png"] = page("eco", body, 4, T, LEGAL)


for f in (s1, s2, s3, s4, s5):
    f()
