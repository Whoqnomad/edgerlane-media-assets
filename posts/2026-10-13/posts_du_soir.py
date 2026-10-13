import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "engine"))
import lib
lib.DATE_TAG = "MAR. 13.10.2026"
from lib import *

POSTS = {}
LEGAL = "Contenu informatif, pas un conseil en investissement."
RED = "#E5303A"
GOLD = "#F5B80B"
T = 3


def var(v, up):
    col = GREEN if up else RED
    arrow = "▲" if up else "▼"
    return f'<span style="color:{col}">{arrow} {v}</span>'


# ---------- SLIDE 1 : tableau de bord ----------
def s1():
    rows = [
        ("CAC 40", "clôture 17h30", "7 825 pts", var("0,10 %", False)),
        ("S&amp;P 500", "en séance · 17h05", "7 798 pts", var("0,12 %", False)),
        ("NASDAQ", "en séance · 17h05", "27 184 pts", var("0,23 %", False)),
        ("BRENT", "vers 16h20", "105,98 $", var("0,6 %", False)),
        ("OR", "vers 17h05", "4 195 $", var("0,1 %", True)),
        ("EUR/USD", "fin d'après-midi", "1,1188", var("0,3 %", True)),
        ("TAUX US 10 ANS", "vers 17h05", "5,22 %", '<span style="color:#9aa0aa">−2 pb</span>'),
    ]
    h = ""
    for name, when, val, v in rows:
        h += f"""<div style="display:grid;grid-template-columns:1.25fr 1fr .8fr;align-items:center;padding:14px 30px;border-radius:18px;background:rgba(255,255,255,.035);border:1px solid rgba(255,255,255,.08)">
<div><div style="font-size:30px;font-weight:900;letter-spacing:.5px">{name}</div><div class="mono" style="font-size:18px;color:#6d727c;margin-top:4px">{when}</div></div>
<div style="font-size:36px;font-weight:900;text-align:right">{val}</div>
<div style="font-size:28px;font-weight:900;text-align:right">{v}</div></div>"""
    body = f"""
<div style="position:absolute;top:160px;left:64px">{tag('eco','MARCHÉS')}</div>
<div class="h1" style="position:absolute;top:240px;left:64px;right:64px;font-size:80px">La séance en<br><span class="acc">1 coup d'œil</span></div>
<div style="position:absolute;top:430px;left:64px;right:64px;display:flex;flex-direction:column;gap:10px">{h}</div>
<div class="swipe" style="bottom:150px">CE QUI A BOUGÉ <em>→</em></div>"""
    POSTS["soir_01_seance-13-oct.png"] = page("eco", body, 0, T,
        "Sources : Boursorama, Yahoo Finance, Reuters, Trading Economics")


# ---------- SLIDE 2 : ce qui a fait bouger ----------
def s2():
    def card(n, title, big, txt, color=GOLD):
        return f"""<div class="card" style="padding:28px 32px;display:flex;gap:26px;align-items:flex-start">
<div class="mono acc" style="font-size:28px;font-weight:700;min-width:46px">{n}</div>
<div style="flex:1"><div style="display:flex;justify-content:space-between;align-items:baseline;gap:20px">
<div style="font-size:31px;font-weight:900;text-transform:uppercase;letter-spacing:-.3px">{title}</div>
<div class="h1" style="font-size:46px;color:{color};white-space:nowrap">{big}</div></div>
<div class="mut" style="font-size:24px;line-height:1.35;margin-top:10px">{txt}</div></div></div>"""
    body = f"""
<div style="position:absolute;top:160px;left:64px">{tag('eco','CE QUI A BOUGÉ')}</div>
<div class="h1" style="position:absolute;top:240px;left:64px;right:64px;font-size:76px">Les puces<br><span class="acc">décrochent</span></div>
<div style="position:absolute;top:440px;left:64px;right:64px;display:flex;flex-direction:column;gap:18px">
{card('01','Micron','−5,8 %',"Des informations sur les progrès du chinois CXMT dans les puces mémoire pèsent sur le secteur (vers 16h10).",RED)}
{card('02','Kospi (Séoul)','−5,5 %',"Samsung et SK Hynix entraînent la Bourse sud-coréenne, Tokyo cède 1,8 %.",RED)}
{card('03','Banques US','mitigé',"Goldman Sachs bat les attentes (17,01 $ par action contre 13,02 $). JPMorgan déçoit (5,57 $ contre 5,90 $).","#fff")}
{card('04','Luxe à Paris','LVMH',"Ventes trimestrielles sous les attentes : le luxe freine le CAC 40.","#fff")}
</div>"""
    POSTS["soir_02_ce-qui-a-bouge.png"] = page("eco", body, 1, T,
        "Sources : AP, TheStreet, Zonebourse · mar. 13 oct. 2026")


# ---------- SLIDE 3 : agenda de demain ----------
def s3():
    rows = [
        ("CE SOIR 19H00", "eco", "Fed : discours de Thomas Barkin"),
        ("CE SOIR 22H00", "eco", "Fed : discours de Susan Collins"),
        ("MER. 12H45", "eco", "Résultats Bank of America (T3)"),
        ("MER. AVANT OUV.", "eco", "Résultats Morgan Stanley (date prévue)"),
        ("MER. 14H30", "eco", "Inflation US (CPI) sept. · attendu 3,6 % sur 1 an"),
    ]
    h = ""
    for d, c, t in rows:
        k = CAT[c]
        h += f"""<div style="display:flex;align-items:center;gap:24px;padding:22px 28px;border-radius:18px;background:rgba(255,255,255,.035);border:1px solid rgba(255,255,255,.08);border-left:5px solid {k['c']}">
<div class="mono" style="font-size:21px;min-width:200px;color:{k['c']}">{d}</div>
<div style="flex:1;font-size:26px;font-weight:800;line-height:1.25">{t}</div></div>"""
    body = f"""
<div style="position:absolute;top:160px;left:64px"><div class="tag" style="border-color:rgba(255,255,255,.35)"><b style="background:#fff;box-shadow:none"></b>AGENDA<span>· HEURES DE PARIS</span></div></div>
<div class="h1" style="position:absolute;top:240px;left:64px;font-size:76px">Demain,<br>à <span style="color:#F5B80B">sur</span><span style="color:#3B6BFF">veil</span><span style="color:#E5303A">ler</span></div>
<div style="position:absolute;top:440px;left:64px;right:64px;display:flex;flex-direction:column;gap:12px">{h}</div>
<div class="mut" style="position:absolute;top:1000px;left:64px;right:64px;font-size:21px;line-height:1.35">CPI : 3,4 % sur 1 an en août. Inflation sous-jacente attendue à 2,5 %. Consensus, pas une certitude.</div>
<div style="position:absolute;top:1080px;left:64px;right:64px;font-size:30px;font-weight:800">Journalise tes trades sur <span style="color:#F5B80B">edgerlane.com</span></div>
<div style="position:absolute;top:1135px;left:64px;right:64px;font-size:21px;color:#9aa0aa">{LEGAL}</div>"""
    POSTS["soir_03_agenda-14-oct.png"] = page("mix", body, 2, T,
        "Sources : Zonebourse, Bank of America, Barchart, Kiplinger, FinancialJuice")


for f in (s1, s2, s3):
    f()
