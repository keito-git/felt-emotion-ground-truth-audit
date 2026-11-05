"""規則ベースの自動再導出（2026-09-09）

目的: 供給源の判定が分析者個人の解釈にどれだけ依存しているかを測る。
方法: 原典の抽出テキストに対し、事前に固定した語彙規則のみで
      「本人の記録の有無」「観察者の記録の有無」を再導出し、分析者の判定と比較する。

注意: これは**人間の第二コーダーの代わりではない**。
      得られる一致度は「分析者の判定 対 規則ベース再導出」であり、
      inter-coder reliability として報告してはならない。
"""
import csv, io, os, re, glob

BASE = ""   # project root holding 02_データ/ and 03_解析/; set if run from elsewhere
TXT = BASE + "02_データ/txt/"

# データセット名 → 抽出テキストのファイル名
ALIAS = {
    "IEMOCAP": "IEMOCAP_Busso2008", "SEND": "1912.05008", "TEC": "TEC_Mohammad2012",
    "EmoBank": "EmoBank_Buechel2017", "SSEC": "SSEC_Schuff2017", "CMU-MOSEI": "MOSEI_Zadeh2018",
    "DailyDialogs": "DailyDialog", "AffectiveText": "AffectiveText_S07", "Tales": "Tales_Alm2005",
    "CASME II": "CASMEII", "DEAP": "DEAP_Koelstra2012", "WESAD": "WESAD_Schmidt2018",
    "AMIGOS": "AMIGOS_1702.02510", "Aff-Wild2": "AffWild2", "CK+": "CKplus",
    "fb-valence-arousal": "fbVA_W16", "EMOTIC": "EMOTIC2", "THEATER Corpus": "THEATER",
}

# 事前に固定した語彙規則
SELF = re.compile(
    r"self-assessment|self-report|self report|self-rating|self-evaluation|self-annotat"
    r"|participants (rated|reported)|subjects .{0,20}(rated|reported)"
    r"|SAM\b|self-assessment manikin|posed|instructed to (perform|pose|express)"
    r"|emotion-word hashtag|self-labeled", re.I)
OBS = re.compile(
    r"annotator|annotators|external annotation|observers|raters|judges|coders?\b"
    r"|Mechanical Turk|crowdsourc|FACS coder|inter-annotator|inter-rater|majority vot", re.I)


def load(ds):
    name = ALIAS.get(ds, ds)
    for cand in (name, name.replace(" ", "_"), name.replace("+", "plus")):
        p = TXT + cand + ".txt"
        if os.path.exists(p):
            return open(p, encoding="utf-8", errors="ignore").read().replace("\n", " ")
    hits = glob.glob(TXT + ds.split()[0] + "*.txt")
    return open(hits[0], encoding="utf-8", errors="ignore").read().replace("\n", " ") if hits else None


def kappa(a, b):
    """2値ラベル列の Cohen's kappa"""
    n = len(a)
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    pa1 = sum(a) / n
    pb1 = sum(b) / n
    pe = pa1 * pb1 + (1 - pa1) * (1 - pb1)
    return (po - pe) / (1 - pe) if pe < 1 else float("nan"), po


rows = [r for r in csv.DictReader(io.open(BASE + "02_データ/frame_all_v1.csv", encoding="utf-8")) if r.get("type")]
an_self, ru_self, an_obs, ru_obs, used, missing, disagree = [], [], [], [], [], [], []

for r in rows:
    ds = r["dataset"].strip()
    t = load(ds)
    if not t:
        missing.append(ds)
        continue
    a_self = 0 if r["self_record"].startswith(("なし", "—")) else 1
    a_obs = 0 if r["observer_record"].startswith(("なし", "—")) else 1
    r_self = 1 if SELF.search(t) else 0
    r_obs = 1 if OBS.search(t) else 0
    an_self.append(a_self); ru_self.append(r_self)
    an_obs.append(a_obs); ru_obs.append(r_obs)
    used.append(ds)
    if a_self != r_self or a_obs != r_obs:
        disagree.append((ds, f"本人 分析者{a_self}/規則{r_self}", f"観察者 分析者{a_obs}/規則{r_obs}"))

k1, p1 = kappa(an_self, ru_self)
k2, p2 = kappa(an_obs, ru_obs)
print(f"照合できた件数: {len(used)}   抽出テキスト無し: {len(missing)}")
print(f"本人の記録の有無  : 一致率 {p1:.3f}  kappa {k1:.3f}")
print(f"観察者の記録の有無: 一致率 {p2:.3f}  kappa {k2:.3f}")
print(f"\n不一致 {len(disagree)} 件:")
for d in disagree:
    print("  ", d[0], "|", d[1], "|", d[2])
print("\n抽出テキスト無し:", ", ".join(missing))
