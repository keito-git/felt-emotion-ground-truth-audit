"""下流利用監査の最終集計（重複除去・除外規則の機械化）。2026-09-09"""
import glob, re, os, json

BASE = "03_解析/下流監査/"
SPEC = {
    "IEMOCAP":   ("IEMOCAP", r"self-assessment|self-report|self-evaluation"),
    "CKplus":    (r"CK\+|Cohn-Kanade", r"\brequested\b"),
    "AffectNet": ("AffectNet", r"single annotator|one annotator|two annotat"),
    "EmoBank":   ("EmoBank", r"perceived writer|actual writer|writer.s perspective|writer perspective|reader perspective"),
}
SURVEY = r"this (survey|review|paper (surveys|reviews))|we (survey|review) (the|recent)"
DATASETPAPER = r"we (present|introduce|release|describe) (a|the|our) (new )?(corpus|dataset|database)"

out = {}
for d, (name, pat) in SPEC.items():
    seen, rows = {}, []
    for f in sorted(glob.glob(BASE + d + "/txt/*.txt")):
        s = open(f, encoding="utf-8", errors="ignore").read().replace("\n", " ")
        key = re.sub(r"\W", "", s[:200].lower())[:80]
        if key in seen:
            continue
        seen[key] = 1
        body = s[:int(len(s) * 0.85)]
        rows.append((os.path.basename(f)[:-4], s, body, len(re.findall(name, body, re.I))))
    inc, hits = [], []
    exs = exd = exl = 0
    for wid, s, body, uses in rows:
        if re.search(SURVEY, s, re.I):
            exs += 1; continue
        if re.search(DATASETPAPER, s, re.I):
            exd += 1; continue
        if uses < 3:
            exl += 1; continue
        inc.append(wid)
        if re.search(pat, body, re.I):
            hits.append(wid)
    out[d] = {"pool": len(rows), "n": len(inc), "hits": len(hits), "hit_ids": hits,
              "exc_survey": exs, "exc_datasetpaper": exd, "exc_lowuse": exl}
    print(f"{d:10} 重複除去後 {len(rows):2d} → 分析対象 {len(inc):2d}  言及 {len(hits)}"
          f"   (除外 サーベイ{exs} 新データセット論文{exd} 実使用不明{exl})")

json.dump(out, open(BASE + "downstream_summary.json", "w"), ensure_ascii=False, indent=1)
