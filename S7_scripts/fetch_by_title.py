"""データセット論文を題名から探し、OpenAlex が持つ OA 本文URLで取得する。
使い方: python3 fetch_by_title.py "<保存名>" "<検索題名>"
"""
import json, os, subprocess, sys, urllib.parse

BASE = os.path.join(os.path.dirname(__file__), "..", "..", "02_データ")
MAILTO = "your-address@example.org"


def api(path):
    url = f"https://api.openalex.org/{path}" + ("&" if "?" in path else "?") + f"mailto={MAILTO}"
    out = subprocess.run(["curl", "-s", "--max-time", "60", url], capture_output=True, text=True).stdout
    return json.loads(out) if out.strip().startswith("{") else {}


def best(title):
    q = urllib.parse.quote(title)
    d = api(f"works?search={q}&per-page=5&select=id,title,publication_year,cited_by_count,open_access,best_oa_location,primary_location")
    res = d.get("results", [])
    return res[0] if res else None


def oa_url(w):
    for k in ("best_oa_location", "primary_location"):
        loc = w.get(k) or {}
        u = loc.get("pdf_url") or (loc.get("landing_page_url") if k == "best_oa_location" else None)
        if u:
            return u
    return (w.get("open_access") or {}).get("oa_url")


if __name__ == "__main__":
    name, title = sys.argv[1], sys.argv[2]
    w = best(title)
    if not w:
        print(f"NG {name}: 検索ヒットなし"); sys.exit(1)
    u = oa_url(w)
    print(f"   {w['publication_year']} cited={w['cited_by_count']} {w['title'][:70]}")
    if not u:
        print(f"NG {name}: OA本文なし（購読誌の可能性）"); sys.exit(2)
    pdf = os.path.join(BASE, "pdfs", f"{name}.pdf"); txt = os.path.join(BASE, "txt", f"{name}.txt")
    subprocess.run(["curl", "-sL", "--max-time", "45", "-A", "Mozilla/5.0", u, "-o", pdf])
    ft = subprocess.run(["file", "-b", pdf], capture_output=True, text=True).stdout
    if not ft.startswith("PDF"):
        os.remove(pdf); print(f"NG {name}: PDFでない ({u[:60]})"); sys.exit(3)
    subprocess.run(["pdftotext", "-q", pdf, txt])
    print(f"OK {name}: {open(txt, encoding='utf-8', errors='ignore').read().split().__len__()}w  {u[:70]}")
