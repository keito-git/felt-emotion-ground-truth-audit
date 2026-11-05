# S8. Procedural detail moved from the manuscript

This file records the parts of the procedure that the manuscript states in summary form. The
protocol as frozen before data collection is in `S6_protocol.md`; this file describes how it was
executed.

## S8.1 The eight coded items

For each dataset, the dataset paper, the datasheet and the distribution page were read, and the
following were recorded.

1. Whether a record originating from the person exists, and in what form (continuous self-rating,
   categorical self-report, statement of intent by a performer, label assigned by the writer of a
   text, and so on).
2. Whether a record originating from observers exists, with how many raters and of what kind
   (crowdworkers, trained annotators, experts, the experimenter).
3. Which label is presented as the criterion in the released resource.
4. What reason, if any, is attached to that selection.
5. What construct the dataset declares that its labels measure.
6. In which direction validation runs where two records coexist.
7. The configuration of the scene of elicitation (solitary elicitation, interpersonal interaction,
   instructed expression, existing resources and observation).
8. Whether a judgement was possible at all; where it was not, the item was recorded as undecidable
   together with the places searched.

Every judgement carries a verbatim quotation and its location, given in `S2_quotations.md` for the
datasets named in the manuscript and in the coding note of `S1_coding_table.csv` for the remainder.

## S8.2 Retrieval and exclusion rules of the downstream audit

Four datasets were audited: a dialogue corpus (IEMOCAP), a posed facial expression corpus (CK+), a
large-scale facial image corpus (AffectNet) and a text corpus that separates the writer's and the
reader's perspective (EmoBank).

1. Lists of citing papers were retrieved from the public interface of a bibliographic database and
   sorted in descending order of citation count.
2. Full texts were obtained where openly available. Papers whose text could not be obtained were
   recorded as exclusions and the next paper in the ranking was examined.
3. Duplicates were removed using a normalised string taken from the opening of each text.
4. Papers were then excluded by rule if they describe themselves as surveys or reviews, if their
   purpose is to present a new resource, or if they mention the dataset fewer than three times in
   the body text. The last condition is a proxy for citation without use.
5. For each dataset a caveat stated in the original document was defined in advance, together with
   the search terms for it: the existence of the speakers' own ratings (IEMOCAP), the fact that
   labels correspond to the emotion requested by the experimenter (CK+), the limitation of the
   annotation regime (AffectNet), and the fact that the writer's perspective is inferred (EmoBank).
6. Judgements were restricted to the first 85% of each text so that occurrences in reference lists
   do not count as mentions.

The retrieved lists, the exclusion counts under each rule and the analysed counts are in
`S5_downstream_audit/`. The target of 20 analysed papers per dataset set by the rule was not reached
for three of the four, which is reported in the manuscript as a limitation.

## S8.3 Statistical procedure

- Proportions are reported with 95% confidence intervals computed by the Wilson method.
- The association between the elicitation scene and the source of ground truth is tested with
  Fisher's exact test; odds ratios are reported with 95% confidence intervals after the Haldane
  correction.
- Four resources whose assignment to an elicitation scene was debatable, either because they combine
  individual and group conditions or because it is arguable whether speaking alone is an
  interpersonal narrative, were reversed individually and then jointly. The resulting range of p is
  reported in the manuscript and in `S7_tables_moved_from_the_manuscript.md`.
- Change over time was examined by logistic regression with the presence of the discrepant cell as
  the dependent variable and the centred year of first public release as the explanatory variable.
  Years follow the primary document; only where no statement could be confirmed were they fixed by
  exact title matching in a bibliographic database, with the provenance recorded per resource in
  `S3_publication_years.csv`. Where the year of early access differs from the year of the printed
  issue, the year of first public release is taken.
- Because the sample is small, non-significant results are reported with the width of their
  intervals and are not read as the absence of an effect.

## S8.4 The lexical re-derivation

An automatic re-derivation was run over the same documents using rules fixed in advance. The first
version required only the occurrence of a term, which returned as positive any document that
mentioned self-report anywhere, including in related work. The second version requires the
co-occurrence of a term denoting the agent of collection with a verb denoting collection or
instruction, and determines mechanically whether a record originating from the person and a record
originating from observers are present. Agreement with the manual coding is κ = 0.49. This is not an
inter-rater reliability; it is a measure of how far the judgements reduce to lexical cues.
