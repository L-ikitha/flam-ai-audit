layers = 28
kv_heads = 8
head_dim = 128
bytes_per_value = 2

gpu_memory_gb = 24
gpu_utilization = 0.92
overhead_gb = 1.6
sequence_length = 4096

# K and V are both stored.
kv_bytes_per_token = (
    2
    * layers
    * kv_heads
    * head_dim
    * bytes_per_value
)

sequence_bytes = kv_bytes_per_token * sequence_length

usable_memory_gb = gpu_memory_gb * gpu_utilization
kv_memory_gb = usable_memory_gb - overhead_gb

sequences = kv_memory_gb / (sequence_bytes / 1_000_000_000)

print("KV-cache calculation")
print("--------------------")
print(f"KV bytes/token:              {kv_bytes_per_token:,}")
print(f"KV KiB/token:                {kv_bytes_per_token / 1024:.1f}")
print(f"4096-token sequence bytes:   {sequence_bytes:,}")
print(f"4096-token sequence MiB:     {sequence_bytes / (1024**2):.1f}")
print(f"Usable GPU memory (GB):      {usable_memory_gb:.2f}")
print(f"KV memory after overhead:    {kv_memory_gb:.2f} GB")
print(f"Approx. sequences:           {sequences:.2f}")
print(f"Max whole sequences:         {int(sequences)}")