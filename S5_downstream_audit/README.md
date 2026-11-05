# S5. Downstream audit

`summary.csv` reports, for each of the four datasets, how many citing papers with an openly
available full text remained after deduplication, how many were excluded by each rule, how many
were analysed, and how many mentioned the caveat stated in the original document.

`citing_papers_*.tsv` are the retrieved lists of citing papers in descending order of citation
count. The columns are the citation count, the publication year, the identifier in the
bibliographic database, the title and the open-access location where one exists.

Search terms used to detect the caveat were as follows.

| Dataset | Terms |
|---|---|
| IEMOCAP | self-assessment, self-report, self-evaluation |
| CK+ | requested |
| AffectNet | single annotator, one annotator, two annotators |
| EmoBank | perceived writer, actual writer, writer's perspective, reader perspective |

Judgements were restricted to the first 85 per cent of each text so that occurrences within
reference lists were not counted as positives.
