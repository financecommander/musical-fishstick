# EdgeForge Quick Reference

## Installation

```bash
git clone https://github.com/financecommander/musical-fishstick.git edgeforge
cd edgeforge
pip install -e .
```

## Basic Pipeline

```python
from edgeforge import Pipeline, Stage

pipeline = (
    Pipeline("my_model")
    .load_model("model.pt")
    .add(Stage.quantize(mode="int8_symmetric"))
    .add(Stage.prune(sparsity=0.7))
    .add(Stage.export(format="onnx"))
    .deploy(runtime="onnxruntime")
)

result = pipeline.run(output_dir="artifacts/")
```

## Quantization Modes

| Mode | Bits | Use Case |
|------|------|----------|
| `int8_symmetric` | 8 | General purpose, balanced |
| `int4_per_channel` | 4 | Aggressive compression |
| `mixed_precision` | 4-8 | Quality-critical layers |
| `ternary` | ~1.58 | Extreme compression (Triton) |

## Pruning Methods

| Method | Type | Hardware Optimization |
|--------|------|----------------------|
| `magnitude` | Unstructured | General |
| `structured` | Channel-wise | ARM NEON, SIMD |
| `l1_norm` | Unstructured | General |

## Target Devices

```python
from edgeforge import TargetDevice

TargetDevice.ARM_CORTEX_A72      # Raspberry Pi 4
TargetDevice.JETSON_NANO         # NVIDIA edge
TargetDevice.CORAL_EDGE_TPU      # Google TPU
TargetDevice.APPLE_NEURAL_ENGINE # Apple devices
```

## Export Formats

| Format | Runtime | Best For |
|--------|---------|----------|
| `onnx` | ONNX Runtime | Universal compatibility |
| `tensorrt` | TensorRT | NVIDIA GPUs |
| `tflite` | TFLite | Coral TPU, mobile |
| `coreml` | CoreML | Apple devices |

## Common Patterns

### Aggressive Compression
```python
.add(Stage.quantize(mode="int4_per_channel"))
.add(Stage.prune(sparsity=0.8))
```

### Quality-Focused
```python
.add(Stage.quantize(
    mode="mixed_precision",
    sensitive_layers=["attention", "output"]
))
.add(Stage.prune(sparsity=0.5))
```

### Mobile-Optimized
```python
.add(Stage.quantize(mode="ternary"))
.add(Stage.prune(method="structured", block_size=(1,4)))
```

## Configuration

```python
from edgeforge import EdgeConfig, TargetDevice

config = EdgeConfig(
    target=TargetDevice.ARM_CORTEX_A76,
    max_latency_ms=10.0,
    min_accuracy=0.95,
    format="onnx",
    max_memory_mb=100,
    num_threads=4
)

pipeline = Pipeline("my_model", config)
```

## Validation

```python
.add(Stage.validate(
    test_dataset="test.pkl",
    accuracy_threshold=0.92,
    latency_threshold_ms=8.0,
    memory_threshold_mb=50,
    rollback_on_fail=True
))
```

## Running Examples

```bash
# Matrix Protocol example
python examples/matrix_protocol_example.py

# Triton TNN example
python examples/triton_tnn_example.py
```

## File Structure

```
edgeforge/
├── edgeforge/          # Main package
│   ├── core/          # Pipeline and config
│   └── stages/        # Stage implementations
├── examples/          # Example deployments
├── docs/              # Documentation
└── tests/             # Tests (TODO)
```

## Performance Targets

- **Size**: 50-80% reduction
- **Latency**: 40-60% reduction  
- **Memory**: 70-85% reduction
- **Accuracy**: <5% degradation

## Tool Allocation

- **Grok**: DSL, deployment, integration (80%)
- **Claude**: Algorithms, optimization, memory (20%)

## Common Issues

### Model too large?
→ Increase sparsity, use INT4/ternary

### Accuracy degraded?
→ Use mixed-precision, reduce sparsity

### Slow inference?
→ Enable fusion, increase parallelism

## Next Steps

1. Read [Getting Started](docs/getting-started.md)
2. Run examples
3. Review [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
4. Check development roadmap

---

**Repository**: https://github.com/financecommander/musical-fishstick.git
