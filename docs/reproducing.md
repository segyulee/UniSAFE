# Reproducing an evaluation

1. Request and receive access to the gated UniSAFE dataset.
2. Freeze each target model's checkpoint, decoding settings, and official code
   revision in your experiment log.
3. Run the target model separately for every supported task and create a
   predictions JSONL file. Preserve explicit refusals and request failures.
4. Validate the file and image paths with `unisafe validate --check-files`.
5. Run each automated judge into a separate output file with `--resume` enabled.
6. Aggregate all judge files in one command and archive the resulting metrics
   together with the prediction and judgment files.

For a smoke test, add `--limit 5` to `unisafe evaluate`. This limits API calls
after predictions have been matched to dataset cases.

## Reproducibility notes

- The paper uses three judge models. A single judge is supported for ablations,
  but should be reported as such.
- Refusals contribute Judgment 0 and Risk Rating 0. Missing model outputs and
  judge failures remain unscored and appear in the coverage section.
- `ASR` and `ARR` are taxonomy-balanced macro averages, not global micro
  averages over all rows.
- Image evaluation uses the task-specific context: generated image only for
  `TI`; original and generated images for `IE`; two originals and generated
  image for `IC`; and all four generated turns for `MT`.
- Text evaluation judges generated text as the decisive output. Input images and
  instructions are supplied only as task context.

## Securing runs

Use environment variables or your cluster's secret manager for credentials.
Keep predictions and judgments under an ignored `outputs/` directory until you
have reviewed them for harmful content, personal data, and licensing constraints.
Do not publish raw gated benchmark cases or model outputs without confirming
that their release is permitted.
