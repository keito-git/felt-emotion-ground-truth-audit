"""規則ベースの自動再導出 v2（文脈制約つき）2026-09-09

v1 は語の出現のみを見たため、関連研究で self-report に触れただけの論文も陽性となり
ほぼ全件が1になった（kappa 0.011）。v2 は「その資料において実際に収集されたか」を
捉えるため、収集主体と収集動詞の共起を要求する。

これは人間の第二コーダーの代わりではない。得られる一致度は
「分析者の判定 対 規則ベース再導出」であり、inter-coder reliability ではない。
"""
import csv, glob, io, os, re

BASE = ""   # project root holding 02_データ/ and 03_解析/; set if run from elsewhere
TXT = BASE + "02_データ/txt/"
ALIAS = {
    "IEMOCAP": "IEMOCAP_Busso2008", "SEND": "1912.05008", "TEC": "TEC_Mohammad2012",
    "EmoBank": "EmoBank_Buechel2017", "SSEC": "SSEC_Schuff2017", "CMU-MOSEI": "MOSEI_Zadeh2018",
    "DailyDialogs": "DailyDialog", "AffectiveText": "AffectiveText_S07", "Tales": "Tales_Alm2005",
    "CASME II": "CASMEII", "DEAP": "DEAP_Koelstra2012", "WESAD": "WESAD_Schmidt2018",
    "AMIGOS": "AMIGOS_1702.02510", "Aff-Wild2": "AffWild2", "CK+": "CKplus",
    "fb-valence-arousal": "fbVA_W16", "EMOTIC": "EMOTIC2", "THEATER Corpus": "THEATER",
}
SELF = re.compile(
    r"(participants|subjects|users|speakers|actors|targets|posers?|expressers?)[^.]{0,110}"
    r"(self-report|self-assessment|self-assessed|self-rat|self-annotat|rated (their|his|her) own"
    r"|reported (their|his|her)|were (asked|instructed) to (rate|report|perform|pose|express)|SAM\b)"
    r"|(self-report|self-assessment)s?[^.]{0,90}(were|was) (collected|obtained|acquired|filled|completed|taken)"
    r"|we (collected|obtained|acquired|took)[^.]{0,70}self-report"
    r"|emotion-word hashtags?[^.]{0,60}(label|annotat)", re.I)
OBS = re.compile(
    r"(annotated|labeled|labelled|rated|coded|evaluated) by [^.]{0,70}"
    r"(annotator|rater|coder|judge|worker|observer|expert|assistant|evaluator|student)"
    r"|(\d+|two|three|four|five|six|seven|eight|nine|ten|several|multiple) "
    r"(trained |naive |na\\\"ive |external |independent |certified )*"
    r"(annotator|rater|coder|judge|observer|evaluator)s"
    r"|Mechanical Turk|crowdsourc(ed|ing)", re.I)


def load(ds):
    name = ALIAS.get(ds, ds)
    for c in (name, name.replace(" ", "_"), name.replace("+", "plus")):
        p = TXT + c + ".txt"
        if os.path.exists(p):
            return open(p, encoding="utf-8", errors="ignore").read().replace("\n", " ")
    h = glob.glob(TXT + ds.split()[0] + "*.txt")
    return open(h[0], encoding="utf-8", errors="ignore").read().replace("\n", " ") if h else None


def kappa(a, b):
    n = len(a)
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    p1, p2 = sum(a) / n, sum(b) / n
    pe = p1 * p2 + (1 - p1) * (1 - p2)
    return ((po - pe) / (1 - pe) if pe < 1 else float("nan")), po


rows = [r for r in csv.DictReader(io.open(BASE + "02_データ/frame_all_v1.csv", encoding="utf-8")) if r.get("type")]
A, R, B, S, dis = [], [], [], [], []
for r in rows:
    ds = r["dataset"].strip()
    t = load(ds)
    if not t:
        continue
    a = 0 if r["self_record"].startswith(("なし", "—")) else 1
    b = 0 if r["observer_record"].startswith(("なし", "—")) else 1
    x = 1 if SELF.search(t) else 0
    y = 1 if OBS.search(t) else 0
    A.append(a); R.append(x); B.append(b); S.append(y)
    if a != x:
        dis.append((ds, a, x))

k1, p1 = kappa(A, R)
k2, p2 = kappa(B, S)
print(f"n={len(A)}")
print(f"本人の記録の有無  : 一致率 {p1:.3f}  kappa {k1:.3f}")
print(f"観察者の記録の有無: 一致率 {p2:.3f}  kappa {k2:.3f}")
print(f"\n本人の記録で不一致 {len(dis)} 件:")
for d in dis:
    print(f"   {d[0]:22} 分析者{d[1]} / 規則{d[2]}")
