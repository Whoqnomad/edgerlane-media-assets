"""Rend un module de posts en PNG 1080x1350.
Usage : python3 engine/render.py <module_posts.py> <dossier_sortie>
Le module doit importer `from lib import *` et remplir le dict POSTS {nom_fichier.png: html}.
"""
import sys, os, importlib.util
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
mod_path, out = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location("posts_mod", mod_path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
from playwright.sync_api import sync_playwright
os.makedirs(out, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1350})
    for name, html in m.POSTS.items():
        pg.set_content(html); pg.wait_for_timeout(150)
        pg.screenshot(path=os.path.join(out, name), clip={"x": 0, "y": 0, "width": 1080, "height": 1350}); print(name)
    b.close()
