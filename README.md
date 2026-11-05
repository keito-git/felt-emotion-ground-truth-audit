# Who Supplies the Ground Truth of Felt Emotion in Affective Datasets

Audit materials for the manuscript of the same title by Keito Inoshita (Faculty of Business and
Commerce, Kansai University), under review at *Behavior Research Methods*. The full citation is
added here once the article is published.

The study composes a sampling frame of 62 affective datasets as the union of the inclusion tables of
three peer-reviewed surveys, codes 59 of them from their primary documents, and records who is
admitted to supplying the criterion that each resource designates as its ground truth. This
repository holds every coded judgement, the verbatim quotation behind it, the frozen protocol, the
downstream audit of citing papers and the analysis scripts as executed.

## Contents

| File | Content |
|---|---|
| `S1_coding_table.csv` | The 59 coded datasets with the coded fields, namely modality, elicitation scene, presence of a record from the person and from observers, the designated ground truth, the source type, the declared measurement target, the direction of validation, whether the declaration and the source diverge, and the coding note |
| `S2_quotations.md` | Verbatim quotations from the primary documents for every dataset named in the manuscript, grouped by the decision they support |
| `S3_publication_years.csv` | The year of first public release for each dataset together with the provenance of that year |
| `S4_unverified_resources.md` | The three resources of the frame that could not be coded, with reasons, and the search record for the resource whose primary document could not be located |
| `S5_downstream_audit/` | The retrieved lists of citing papers, the exclusion counts under each rule, the analysed counts and the mentions found |
| `S6_protocol.md` | The audit protocol as frozen before data collection, with the additions recorded afterwards |
| `S7_scripts/` | The analysis scripts as executed, with the project path made relative and the address of the polite pool replaced by a placeholder |
| `S8_procedure_detail.md` | The procedure as executed: the eight coded items, the retrieval and exclusion rules of the downstream audit, the statistical procedure including the treatment of debatable assignments, and the lexical re-derivation |

## Reproducing the reported numbers

The statistical analysis runs from the repository root with no credentials and no network access:

```
python3 S7_scripts/analysis_v2.py
```

It reads `02_データ/frame_all_v1.csv` and `02_データ/years_verified.csv`, the working files from which
`S1_coding_table.csv` and `S3_publication_years.csv` were produced, and writes
`03_解析/stats/analysis_v2.json`. The copy of that file already in the repository is the output
produced for the manuscript, so a run that reproduces the reported numbers leaves it unchanged. It
requires `scipy`, `statsmodels` and `numpy`; the console output and the source comments are in
Japanese, as written.

`rule_recode.py`, `rule_recode_v2.py` and `downstream_final.py` read the extracted text of the
primary documents and of the citing papers, which is not redistributable, so they cannot be run from
this package alone. The lists in `S5_downstream_audit/` carry the identifiers from which those texts
can be re-retrieved with `openalex_citing.py`, `fetch_by_title.py` and `audit_downstream.sh`. Set a
contact address in place of the placeholder before running the retrieval scripts.
`S7_scripts/README.md` documents each script and the two edits made for release.

## What is not here

The primary documents of the 59 datasets and the citing papers of the downstream audit are the
published articles of other authors, so their extracted text is not redistributed. Every judgement
that rests on such a document is released with the verbatim quotation that produced it, in
`S2_quotations.md` or in the coding note of `S1_coding_table.csv`, and each document is cited in the
reference list of the manuscript.

The datasets themselves are existing public resources and are not redistributed here either. The
audit concerns their documentation, not their content.

## Licence

Creative Commons Attribution 4.0 International (CC BY 4.0). See `LICENSE`.
