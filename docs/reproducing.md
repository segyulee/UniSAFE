# Reproducing an evaluation

1. Obtain access to the gated UniSAFE dataset.
2. Record the target model checkpoint, official code revision, and decoding
   settings.
3. Run every supported task and write the predictions JSONL described in
   [data-format.md](data-format.md).
4. Run each automated judge into a separate output file with `--resume`.
5. Archive the prediction and judgment files with the experiment configuration.

Add `--limit 5` for a small API smoke test. Use `--task TI` (repeatable) to run
only selected task types.

The paper uses Gemini 2.5 Pro, GPT-5 nano, and Qwen2.5-VL-72B as independent
judges. Judge output files are intentionally left unmerged so that each decision
and failure remains directly auditable.

Keep credentials in environment variables or a secret manager. Review gated
cases and generated outputs before moving them outside the secured experiment
environment.
