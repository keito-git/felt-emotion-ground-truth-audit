"""Fetch citing papers for a dataset paper via Semantic Scholar Graph API.

Protocol (frozen 2026-09-06): take citing papers in descending citation count,
inspect in order, keep those that actually train/evaluate on the dataset,
until 20 are collected. This script only retrieves the candidate list.
"""
import json, sys, time, urllib.parse, urllib.request

API = "https://api.semanticscholar.org/graph/v1"
FIELDS = "title,year,citationCount,externalIds,openAccessPdf,venue"


def get(url: str, tries: int = 4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "WhoseGold/1.0"})
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.load(r)
        except Exception as e:  # rate limit or transient
            if i == tries - 1:
                raise
            time.sleep(5 * (i + 1))


def search_paper(query: str):
    u = f"{API}/paper/search?query={urllib.parse.quote(query)}&limit=5&fields=title,year,citationCount,externalIds"
    return get(u).get("data", [])


def citing(paper_id: str, limit: int = 500):
    out, offset = [], 0
    while offset < limit:
        u = f"{API}/paper/{paper_id}/citations?offset={offset}&limit=100&fields={FIELDS}"
        d = get(u)
        rows = d.get("data", [])
        if not rows:
            break
        out += [r["citingPaper"] for r in rows]
        offset += 100
        time.sleep(1.5)
    return out


if __name__ == "__main__":
    q = sys.argv[1]
    hits = search_paper(q)
    for h in hits:
        print(h.get("year"), h.get("citationCount"), h.get("paperId"), h.get("title"))
