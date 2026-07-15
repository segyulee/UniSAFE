# Data and output formats

## Benchmark cases

UniSAFE is distributed as a Hugging Face `DatasetDict` with `image` and `text`
splits. Both splits use the same columns.

| Field | Type | Description |
| --- | --- | --- |
| `id` | string | Shared risk-target identifier. |
| `category` | string | Top-level safety category. |
| `subcategory` | string | Fine-grained taxonomy code. |
| `unsafe_trigger` | string | Atomic risk concept used during construction. |
| `target` | string | Intended unsafe image description or text instruction. |
| `scenario_type` | string | One of `TI`, `IE`, `IC`, `MT`, `TT`, `IT`, `MU`. |
| `instruction` | string | Instruction sent to the target model. |
| `input_image` | image/null | First input image when required. |
| `input_image_b` | image/null | Second input image for `IC`. |
| `turns` | list[string] | Four ordered instructions for `MT`; empty otherwise. |

`id` alone is intentionally shared by task-specific projections of one risk
target. Always use `(id, scenario_type)` as the case key.

## Predictions

Predictions use JSON Lines. Every row requires `id`, `scenario_type`, and
`model`, plus the task-specific output.

| Field | Required | Description |
| --- | --- | --- |
| `output_text` | `TT`, `IT`, `MU` | Generated text. |
| `output_image` | `TI`, `IE`, `IC` | Path to the generated image. |
| `output_images` | `MT` | Four paths ordered from turn 1 through turn 4. |
| `refusal` | no | Explicit target-model or system refusal. Default: `false`. |
| `error` | no | Failed request description. The case remains unscored. |
| `metadata` | no | Arbitrary generation settings or provenance. |

Image paths may be absolute or relative to the predictions JSONL file. Do not
put API responses, credentials, or user information in `metadata`.

## Judgments

`unisafe evaluate` writes one row per case and judge. Important fields are:

| Field | Description |
| --- | --- |
| `judge` | Judge model identifier. |
| `judgment` | `0` for compliant and `1` for non-compliant. |
| `risk_rating` | `0` for refusal; otherwise an integer from 1 through 3. |
| `refusal` | Whether target output was treated as a refusal. |
| `reasoning` | Judge's concise rationale. |
| `error` | Non-empty when the case could not be scored. |
| `raw_response` | Original judge response retained for audit. |

Aggregation deduplicates repeated `(model, id, scenario_type, judge)` rows by
keeping the last row encountered.
