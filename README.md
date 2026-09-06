# Flam AI Team Intern Assignment — The Audit

This repository contains my submission for the **Flam AI Team Intern — The Audit** take-home assignment.

The assignment focuses on:
- Tokenizer auditing and multilingual evaluation
- GPU KV-cache capacity analysis
- Throughput anomaly investigation
- Engineering decision-making under constraints

## Repository Structure

```text
starter_kit/
│
├── README.md
├── REPORT_v0.md
├── fertility.py
├── bench/
│   ├── bench_log.csv
│   └── model_spec.md
│
├── corpus_sample/
│   ├── eng_sample.txt
│   └── hin_sample.txt
│
└── my_submission/
    ├── AI_USAGE.md
    ├── NOTEBOOK.md
    │
    ├── partA/
    │   ├── corpus/
    │   ├── download_corpus.py
    │   ├── check_corpus.py
    │   ├── corrected_analysis.py
    │   ├── measure_split_bug.py
    │   ├── measure_aggregation.py
    │   ├── test_nfc.py
    │   ├── test_split.py
    │   └── recommendation_memo.md
    │
    ├── partB/
    │   ├── kv_cache_calculation.py
    │   ├── analyze_throughput.py
    │   └── answers.md
    │
    └── partC/
        └── memo.md
