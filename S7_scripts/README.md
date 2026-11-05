# S7. Analysis scripts

These are the scripts as executed for the study. Two edits were made for release, and nothing else
was changed:

1. The absolute path of the project directory was replaced by a path relative to the project root.
   `BASE` is the directory holding `02_データ/` and `03_解析/`.
2. The address sent to the OpenAlex polite pool was replaced by a placeholder. Set `MAILTO` to your
   own address before running the retrieval scripts.

Source comments are in Japanese, as written.

| File | What it does | Which result it produces |
|---|---|---|
| `analysis_v2.py` | Statistical analysis over the coded frame: the cross-tabulation of declared target against source of ground truth, Wilson intervals for the main proportions, the two readings of the validation asymmetry, the breakdown by modality, and the logistic regression of the divergent cell on the year of release | The result tables of the manuscript and the temporal analysis |
| `rule_recode.py` | Rule-based re-derivation, first version. Lexical rules only | The superseded value reported as the first attempt |
| `rule_recode_v2.py` | Rule-based re-derivation, second version. Requires the co-occurrence of a collecting agent and a collecting verb, so that a mention of self-report in related work does not count | The agreement between the analyst's judgements and the rule-based re-derivation |
| `downstream_final.py` | Final tabulation of the downstream audit: de-duplication, the three exclusion rules, and the count of papers mentioning the caveat of the original document | The downstream audit table |
| `openalex_citing.py` | Retrieves lists of citing papers from OpenAlex in descending citation count | The candidate pool of the downstream audit |
| `fetch_by_title.py` | Locates a dataset paper by title and retrieves its open-access full text | The corpus of primary documents |
| `fetch_citing.py` | Earlier retrieval of citing papers through the Semantic Scholar Graph API. Superseded by `openalex_citing.py` | Not used for the reported results |
| `audit_downstream.sh` | Retrieves the open-access full texts of citing papers and extracts the lexical cues | The input of `downstream_final.py` |

## What cannot be redistributed

`rule_recode.py`, `rule_recode_v2.py` and `downstream_final.py` read the extracted text of the
primary documents and of the citing papers. Those texts are the published articles of other authors
and are not redistributable, so they are not included here. The coded judgements they were used to
check are in `S1_coding_table.csv`, the quotations behind the judgements are in `S2_quotations.md`,
and the retrieved lists of citing papers with their identifiers are in `S5_downstream_audit/`, from
which the texts can be re-retrieved with the scripts above.

`analysis_v2.py` reads `02_データ/frame_all_v1.csv` and `02_データ/years_verified.csv`. These are the
working files from which `S1_coding_table.csv` and `S3_publication_years.csv` were produced, and they
carry the same values under the column names used in the code.

In this repository those two working files are included at `02_データ/`, so `analysis_v2.py` runs
from the repository root with no further setup, and `03_解析/stats/analysis_v2.json` holds the output
it produced for the manuscript, for comparison.
