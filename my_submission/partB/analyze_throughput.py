import csv
from pathlib import Path

LOG = Path(__file__).parents[2] / "bench" / "bench_log.csv"

with open(LOG, newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

print("Throughput counter investigation")
print("=" * 90)

for row in rows:
    batch = int(row["batch_size"])
    prompt = int(row["prompt_len"])
    gen = int(row["gen_len"])
    requests = int(row["num_requests"])
    wall = float(row["wall_clock_s"])
    reported = float(row["reported_tok_s"])

    generated_tokens = requests * gen
    prompt_tokens = requests * prompt
    total_tokens = requests * (prompt + gen)

    gen_rate = generated_tokens / wall
    total_rate = total_tokens / wall
    prompt_rate = prompt_tokens / wall

    print(
        f"batch={batch:2d} prompt={prompt:4d} gen={gen:3d} "
        f"wall={wall:6.2f}s | reported={reported:7.1f} | "
        f"gen_rate={gen_rate:7.1f} | "
        f"total_rate={total_rate:7.1f} | "
        f"prompt_rate={prompt_rate:7.1f}"
    )