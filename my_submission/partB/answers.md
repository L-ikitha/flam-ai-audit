# Part B - Capacity Reconciliation

## B1. KV-cache capacity

### KV-cache arithmetic

Each token requires:

2 x 28 x 8 x 128 x 2 = 114,688 bytes

of KV cache, where the factors represent K and V, 28 layers,
8 KV heads, head dimension 128, and 2 bytes per fp16 value.

Therefore:

- KV cache per token = 114,688 bytes = 112 KiB
- KV cache for 4096 tokens = 469,762,048 bytes = 448 MiB

The usable GPU memory is:

24 GB x 0.92 = 22.08 GB

After subtracting the assumed 1.6 GB non-KV runtime overhead:

22.08 GB - 1.6 GB = 20.48 GB

Therefore, the approximate number of complete 4096-token
sequences is:

20.48 / 0.469762 ~= 43.6

So the simplified theoretical capacity is approximately:

**43 whole 4096-token sequences.**

### Reconciliation with the benchmark

This theoretical value should not be interpreted as a practically
safe batch size.

The benchmark reaches:

- Batch 24: 93% KV-cache utilization, 0 preemptions
- Batch 32: 97% KV-cache utilization, 7 preempted sequences
- Batch 48: 97% KV-cache utilization, 23 preempted sequences

Therefore, the calculated 43 sequences is a simplified theoretical
upper-bound estimate. The benchmark shows that scheduler/KV-cache
pressure appears well before 43 sequences can be considered safe
for this workload.

---

## B2. Long-context throughput anomaly

The long-context workload uses prompt_len=3584 and gen_len=512.

The reported throughput increases from 565.4 tok/s at batch 4 to
1607.4 tok/s at batch 24, but then falls to 1384.0 tok/s at batch 32
and 1298.5 tok/s at batch 48.

The throughput counter is counting both prompt and generated tokens.
For example, at batch 24:

24 x (3584 + 512) / 61.16 = 1607.3 tok/s,

which matches the reported 1607.4 tok/s. Therefore, this should not
be interpreted as 1607.4 generated tokens/s.

The actual generated-token rates are approximately:

- Batch 24: 200.9 generated tok/s
- Batch 32: 173.0 generated tok/s
- Batch 48: 162.3 generated tok/s

The log also shows increasing KV-cache pressure:

- Batch 24: 93% KV utilization, 0 preemptions
- Batch 32: 97% KV utilization, 7 preemptions
- Batch 48: 97% KV utilization, 23 preemptions

This indicates that increasing long-context concurrency beyond batch
24 causes KV-cache/scheduler pressure and sequence preemption. Useful
generated-token throughput therefore decreases rather than increasing
with larger batch sizes.

### Proposed configuration change

For this L4 deployment, cap long-context concurrency at batch 24, or
use a separate long-context serving pool with an equivalent concurrency
limit.

The largest tested long-context batch without preemptions is batch 24,
with approximately 200.9 generated tok/s. This is approximately 16.1%
higher than the 173.0 generated tok/s observed at batch 32 and
approximately 23.8% higher than the 162.3 generated tok/s observed at
batch 48.

The expected effect is to avoid the observed preemptions and preserve
the higher useful generation throughput demonstrated by the batch-24
configuration.

---

## B3. Correction to the previous report

The previous report misread the `reported_tok_s` column as generated-token
throughput. The benchmark evidence shows that this counter includes both
prompt and generated tokens.

For the batch-24 long-context run:

- prompt_len = 3584
- gen_len = 512
- num_requests = 24
- wall_clock_s = 61.16
- reported_tok_s = 1607.4

The reported throughput can be reproduced as:

24 x (3584 + 512) / 61.16
= 1607.3 tok/s

which matches the reported 1607.4 tok/s.

Therefore, the honest generated-token goodput can be calculated directly:

24 x 512 / 61.16
= 200.9 generated tok/s

It can also be calculated by removing the prompt-token contribution
from the reported counter:

1607.4 x 512 / (3584 + 512)
~= 200.9 generated tok/s

Both methods give approximately 200.9 generated tokens/s.

Therefore, the previous statement that longer prompts provide better
throughput was misleading. The higher reported throughput for the
3584-token prompt is largely because the counter includes the large
number of prompt tokens.

The previous estimate that batch 48 would provide approximately
3200 tok/s is also unsupported. The observed long-context reported
throughput is:

- Batch 24: 1607.4 tok/s
- Batch 32: 1384.0 tok/s
- Batch 48: 1298.5 tok/s

The honest generated-token goodput is:

- Batch 24: 200.9 tok/s
- Batch 32: 173.0 tok/s
- Batch 48: 162.3 tok/s

At the same time, KV-cache utilization reaches 93% at batch 24 and
97% at batches 32 and 48. Preemptions increase from 0 at batch 24
to 7 at batch 32 and 23 at batch 48.

The report should therefore have said that the long-context workload
is approaching KV-cache/scheduler capacity, and that increasing
concurrency beyond batch 24 reduces useful generated-token goodput
rather than scaling linearly.

---

## B4. Serving-stack metric

The most useful serving-stack metric to confirm the proposed mechanism
is a **KV-cache sequence preemption/recompute counter**.

Expected behavior:

- Batch 24: approximately 0 preemption events
- Batch 32: non-zero preemption events
- Batch 48: substantially more preemption events

This expectation is already supported by the benchmark's
`preempted_seqs` column:

- Batch 24: 0
- Batch 32: 7
- Batch 48: 23

The metric would confirm that the throughput degradation at higher
long-context concurrency is associated with KV-cache/scheduler
preemption rather than simply a measurement artifact.