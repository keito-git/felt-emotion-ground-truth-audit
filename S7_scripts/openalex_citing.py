"""被引用論文リストを OpenAlex から取得する（プロトコル §6 の標本規則用）。

- キー不要。urllib は環境の SSL 証明書問題があるため curl を subprocess で呼ぶ。
- 出力は被引用数の降順（規則: 上位から実使用20件に達するまで確認する）。
"""
import json, subprocess, sys, urllib.parse

MAILTO = "your-address@example.org"  # OpenAlex の polite pool（レート優遇）


def api(path: str) -> dict:
    url = f"https://api.openalex.org/{path}"
    sep = "&" if "?" in url else "?"
    url = f"{url}{sep}mailto={MAILTO}"
    out = subprocess.run(["curl", "-s", "--max-time", "60", "-A", "WhoseGold/1.0", url],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def find_work(title: str):
    q = urllib.parse.quote(title)
    d = api(f"works?search={q}&per-page=5&select=id,title,publication_year,cited_by_count")
    return d.get("results", [])


def citing_works(work_id: str, pages: int = 4):
    wid = work_id.rsplit("/", 1)[-1]
    rows = []
    for p in range(1, pages + 1):
        d = api(f"works?filter=cites:{wid}&sort=cited_by_count:desc&per-page=50&page={p}"
                f"&select=id,title,publication_year,cited_by_count,primary_location,open_access")
        r = d.get("results", [])
        if not r:
            break
        rows += r
    return rows


if __name__ == "__main__":
    mode, arg = sys.argv[1], sys.argv[2]
    if mode == "find":
        for w in find_work(arg):
            print(w["cited_by_count"], w["publication_year"], w["id"], w["title"][:80])
    else:
        for w in citing_works(arg):
            oa = (w.get("open_access") or {}).get("oa_url") or ""
            print(f'{w["cited_by_count"]}\t{w["publication_year"]}\t{w["id"].rsplit("/",1)[-1]}\t{w["title"][:70]}\t{oa}')
