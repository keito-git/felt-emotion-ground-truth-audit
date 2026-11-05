#!/bin/bash
# 下流利用監査: 被引用上位のOA論文を取得し、ラベル使用の手がかりを抽出する。
# 使い方: audit_downstream.sh <citing_tsv> <outdir> <n>
set -u
TSV="$1"; OUT="$2"; N="${3:-25}"; PAT="${4:-majority vot[a-z]*|self-assessment|self-report[a-z]*|self-evaluation}"
mkdir -p "$OUT/pdf" "$OUT/txt"
i=0
while IFS=$'\t' read -r cites year wid title url; do
  [ -z "${url:-}" ] && continue
  i=$((i+1)); [ "$i" -gt "$N" ] && break
  f="$OUT/pdf/$wid.pdf"
  if [ -s "$OUT/txt/$wid.txt" ]; then echo -e "$wid\t$cites\t$year\t${title:0:60}\tSKIP\t"; continue; fi
  curl -sL --max-time 35 -A "Mozilla/5.0" "$url" -o "$f" 2>/dev/null
  if file -b "$f" | grep -q "^PDF" && pdftotext -q "$f" "$OUT/txt/$wid.txt" 2>/dev/null; then
    hits=$(tr '\n' ' ' < "$OUT/txt/$wid.txt" | tr -s ' ' | grep -o -i -E "($PAT)" | sort | uniq -c | tr '\n' ';' )
    echo -e "$wid\t$cites\t$year\t${title:0:60}\tOK\t$hits"
  else
    echo -e "$wid\t$cites\t$year\t${title:0:60}\tNOPDF\t"
    rm -f "$f"
  fi
done < "$TSV"
