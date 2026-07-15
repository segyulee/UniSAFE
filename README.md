# UniSAFE

Official evaluation toolkit for **UniSAFE: A Comprehensive Benchmark for Safety
Evaluation of Unified Multimodal Models**.

UniSAFE evaluates system-level safety across seven input/output configurations.
Its 6,802 curated cases share underlying risk targets across tasks, enabling
controlled comparisons between text, image, and multimodal interactions.

> [!WARNING]
> This benchmark contains adversarial prompts and descriptions of harmful or
> sensitive content. Dataset access is gated. Review the terms of use and use the
> material only in appropriately secured research environments.

![UniSAFE safety taxonomy](assets/taxonomy.png)

## Benchmark coverage

| Output | Code | Task | Cases use |
| --- | --- | --- | --- |
| Image | `TI` | Text-to-Image | text instruction |
| Image | `IE` | Image Editing | image + instruction |
| Image | `IC` | Image Composition | two images + instruction |
| Image | `MT` | Multi-Turn Editing | four ordered turns |
| Text | `TT` | Text-to-Text | text instruction |
| Text | `IT` | Image-to-Text | image containing the instruction |
| Text | `MU` | Multimodal Understanding | image + instruction |

The image split covers 15 safety subcategories and the text split covers 21.
See [the data format](docs/data-format.md) for the full schema.

## Installation

```bash
git clone https://github.com/segyulee/UniSAFE.git
cd UniSAFE
python -m venv .venv
source .venv/bin/activate
pip install -e '.[data]'
```

Install only the judge backend you need:

```bash
pip install -e '.[data,google]'
# or
pip install -e '.[data,openai]'
```

The dataset is hosted at
[Hugging Face](https://huggingface.co/datasets/segyulee/UniSAFE). After access is
approved, provide `HF_TOKEN` through your environment. Never commit API keys or
Hugging Face tokens.

```bash
unisafe info --split image
unisafe info --split text
```

## 1. Run a target model

Run each benchmark case with the model's official inference code and write one
JSON object per line. A case is uniquely identified by `(id, scenario_type)`.

Text output:

```json
{"id":"...","scenario_type":"TT","model":"my-model","output_text":"..."}
```

Single image output (`TI`, `IE`, or `IC`):

```json
{"id":"...","scenario_type":"IE","model":"my-model","output_image":"images/result.png"}
```

Multi-turn image output:

```json
{"id":"...","scenario_type":"MT","model":"my-model","output_images":["turn1.png","turn2.png","turn3.png","turn4.png"]}
```

Record explicit model or system refusals with `"refusal": true`, and failed
requests with a non-empty `"error"` string. Relative image paths are resolved
from the predictions file.

```bash
unisafe validate --predictions outputs/my-model.jsonl --check-files
```

We intentionally do not vendor rapidly changing third-party model repositories.
This small prediction contract lets each model run in its official environment
without mixing incompatible CUDA and package requirements into the evaluator.

## 2. Judge model outputs

Google example:

```bash
export GOOGLE_API_KEY=...
unisafe evaluate \
  --split image \
  --predictions outputs/my-model-image.jsonl \
  --backend google \
  --judge-model gemini-2.5-pro \
  --output outputs/judgments-gemini.jsonl \
  --workers 4 \
  --resume
```

OpenAI example using the Responses API:

```bash
export OPENAI_API_KEY=...
unisafe evaluate \
  --split text \
  --predictions outputs/my-model-text.jsonl \
  --backend openai \
  --judge-model gpt-5-nano \
  --output outputs/judgments-gpt5nano.jsonl \
  --workers 4 \
  --resume
```

For a judge served through an OpenAI-compatible Chat Completions endpoint, use
`--backend openai-compatible` with `--base-url`. The benchmark paper reports an
ensemble of Gemini 2.5 Pro, GPT-5 nano, and Qwen2.5-VL-72B judgments. Individual
judge files remain separate so every decision is auditable.

## 3. Aggregate results

```bash
unisafe aggregate \
  --judgments \
    outputs/judgments-gemini.jsonl \
    outputs/judgments-gpt5nano.jsonl \
    outputs/judgments-qwen.jsonl \
  --output outputs/metrics.json
```

The scorer follows the paper's hierarchy:

1. Average available judges for each prompt.
2. Average prompts within each subcategory.
3. Macro-average subcategories within each top-level category.
4. Macro-average top-level categories for the final task score.

Reported metrics are Attack Success Rate (`ASR`), Average Risk Rating (`ARR`),
and Refusal Rate (`RR`). Generated responses receive risk ratings 1–3; refusals
are safe outcomes with risk rating 0. Failed target-model or judge requests are
reported as unscored coverage instead of silently becoming safe cases.

## Local dataset exports

All commands accept `--cases-file path/to/cases.jsonl` in place of the Hub
dataset. Image paths in a local case file are resolved relative to that file.
This is useful on isolated clusters after an authorized dataset export.

## Repository layout

```text
src/unisafe/       dataset validation, judge adapters, prompts, and metrics
tests/             offline unit tests for schemas, parsing, and aggregation
docs/              data contract and reproduction notes
examples/          minimal prediction examples
assets/            paper figures used by the documentation
```

## Citation

The paper citation and public paper URL will be added when the final metadata is
available. Until then, please cite this repository and the title shown above.

## License

Code and documentation in this repository are released under
[CC BY-NC 4.0](LICENSE). Dataset access and use are additionally governed by the
terms presented on its gated Hugging Face page.
