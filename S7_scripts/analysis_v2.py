"""査読対応の再解析（2026-09-09）: 交差表の三値化・非対称性の二層化・信頼区間・モダリティ別。"""
import csv, io, json
from collections import Counter, defaultdict
from scipy.stats import beta as Beta, fisher_exact
import statsmodels.api as sm
import numpy as np

BASE = ""   # project root holding 02_データ/ and 03_解析/; set if run from elsewhere
rows = [r for r in csv.DictReader(io.open(BASE+"02_データ/frame_all_v1.csv", encoding="utf-8")) if r.get("type")]
years = {r[0]: int(r[1]) for r in list(csv.reader(io.open(BASE+"02_データ/years_verified.csv", encoding="utf-8")))[1:] if r and r[1]}

def wilson(k, n, z=1.96):
    if n == 0: return (0.0, 0.0)
    p = k/n; d = 1+z*z/n
    c = (p + z*z/(2*n))/d
    h = z*np.sqrt(p*(1-p)/n + z*z/(4*n*n))/d
    return (max(0, c-h), min(1, c+h))

def pct(k, n):
    lo, hi = wilson(k, n)
    return f"{k}/{n} = {100*k/n:.0f}% [95% CI {100*lo:.0f}--{100*hi:.0f}]"

out = {}

# --- 1. 供給源を三値に整理 ---
def source_class(t):
    if t == "A自己": return "self"
    if t[0] in "BCE": return "observer_or_design"
    return "mixed_undetermined"   # D妥当性・F留保・G混合

for r in rows: r["source_class"] = source_class(r["type"])
cross = defaultdict(Counter)
for r in rows: cross[r["declared_construct"]][r["source_class"]] += 1

print("=== 表3（修正版）宣言 × 供給源 ===")
cols = ["self", "observer_or_design", "mixed_undetermined"]
print(f"{'宣言':22}{'本人':>6}{'観察者/設計':>12}{'混合・未確定':>14}{'計':>6}")
tot = Counter()
for dc in ["person-state", "others-perception", "unstated", "本人不在の対象"]:
    c = cross[dc]; s = sum(c[x] for x in cols)
    print(f"{dc:22}{c['self']:>6}{c['observer_or_design']:>12}{c['mixed_undetermined']:>14}{s:>6}")
    for x in cols: tot[x] += c[x]
print(f"{'合計':22}{tot['self']:>6}{tot['observer_or_design']:>12}{tot['mixed_undetermined']:>14}{sum(tot.values()):>6}")
out["cross"] = {dc: dict(cross[dc]) for dc in cross}

# --- 2. 主要比率に信頼区間 ---
n = len(rows)
print("\n=== 主要比率と95%信頼区間（Wilson） ===")
print("  正解が本人        :", pct(sum(1 for r in rows if r["source_class"]=="self"), n))
print("  問題のセル        :", pct(sum(1 for r in rows if r["problem_cell"]=="YES"), n))
print("  測定対象の宣言なし:", pct(sum(1 for r in rows if r["declared_construct"]=="unstated"), n))
print("  一致度型          :", pct(sum(1 for r in rows if r["type"]=="C一致度"), n))

# --- 3. 照合の非対称を二層で ---
vd = Counter(r["validation_direction"] for r in rows)
narrow_self = vd.get("self→observer", 0); narrow_obs = vd.get("observer→self", 0)
broad_self = narrow_self + vd.get("self→protocol", 0)
print("\n=== 表4（修正版）照合の非対称 ===")
print(f"  狭義 self→observer {narrow_self} : observer→self {narrow_obs}")
print(f"  広義 本人が検証される側 {broad_self} : 観察者が検証される側 {narrow_obs}")
out["asymmetry"] = {"narrow": [narrow_self, narrow_obs], "broad": [broad_self, narrow_obs]}

# --- 4. モダリティ × 供給源 ---
MOD = {"VA/multi":"multimodal/VA", "facial":"facial", "text":"text", "physio":"physiological",
       "gesture":"body", "multimodal":"multimodal/VA"}
print("\n=== 表（新規）モダリティ × 供給源 ===")
mm = defaultdict(Counter)
for r in rows: mm[MOD.get(r["modality_hint"], r["modality_hint"])][r["source_class"]] += 1
print(f"{'モダリティ':16}{'本人':>6}{'観察者/設計':>12}{'混合':>8}{'計':>6}")
for k, c in sorted(mm.items(), key=lambda x: -sum(x[1].values())):
    s = sum(c.values()); print(f"{k:16}{c['self']:>6}{c['observer_or_design']:>12}{c['mixed_undetermined']:>8}{s:>6}")
out["modality"] = {k: dict(v) for k, v in mm.items()}

# --- 5. 年代 × 問題のセル: ロジスティック回帰 ---
Y, X, names = [], [], []
for r in rows:
    d = r["dataset"].strip()
    if d == "ISEAR" or d not in years: continue
    Y.append(1 if r["problem_cell"]=="YES" else 0); X.append(years[d]); names.append(d)
X = np.array(X, float); Y = np.array(Y, float)
Xc = sm.add_constant(X - X.mean())
res = sm.Logit(Y, Xc).fit(disp=0)
b = res.params[1]; se = res.bse[1]; p = res.pvalues[1]
print(f"\n=== 年代のロジスティック回帰（n={len(Y)}・年は中心化） ===")
print(f"  係数 b={b:+.4f}  SE={se:.4f}  p={p:.3f}")
print(f"  オッズ比 OR={np.exp(b):.3f}  95%CI [{np.exp(b-1.96*se):.3f}, {np.exp(b+1.96*se):.3f}]")
print(f"  → 10年あたりのOR={np.exp(10*b):.2f} [{np.exp(10*(b-1.96*se)):.2f}, {np.exp(10*(b+1.96*se)):.2f}]")
out["logit_year"] = {"n": len(Y), "b": b, "se": se, "p": p, "OR": float(np.exp(b))}

io.open(BASE+"03_解析/stats/analysis_v2.json", "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1, default=str))
