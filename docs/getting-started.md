# Getting Started with EdgeForge

EdgeForge is a Python-embedded DSL for optimizing and deploying ML models to edge devices. This guide will walk you through your first deployment.

## Installation

### Basic Installation

```bash
git clone https://github.com/financecommander/musical-fishstick.git edgeforge
cd edgeforge
pip install -e .
```

### Install with Optional Dependencies

```bash
# GPU support
pip install -e ".[gpu]"

# TensorRT support
pip install -e ".[tensorrt]"

# TFLite support
pip install -e ".[tflite]"

# All formats
pip install -e ".[all]"

# Development tools
pip install -e ".[dev]"
```

## Quick Start

### 1. Prepare Your Model

EdgeForge works with PyTorch models. Save your model:

```python
import torch
import torch.nn as nn

# Your model
model = MyModel()

# Save it
torch.save(model, "my_model.pt")
```

### 2. Create a Pipeline

```python
from edgeforge import Pipeline, Stage, EdgeConfig, TargetDevice

# Configure for your target device
config = EdgeConfig(
    target=TargetDevice.ARM_CORTEX_A76,
    max_latency_ms=10.0,
    min_accuracy=0.95,
    format="onnx"
)

# Build pipeline
pipeline = (
    Pipeline("my_deployment", config)
    .load_model("my_model.pt")
    .add(Stage.quantize(mode="int8_symmetric"))
    .add(Stage.prune(sparsity=0.7))
    .add(Stage.export(format="onnx"))
    .deploy(runtime="onnxruntime")
)
```

### 3. Run the Pipeline

```python
result = pipeline.run(
    output_dir="artifacts/my_deployment",
    save_intermediate=True
)

print(f"Status: {result.status}")
```

## Core Concepts

### Pipeline Stages

EdgeForge uses a stage-based approach:

1. **Quantization** - Reduce precision (INT8, INT4, ternary)
2. **Pruning** - Remove unnecessary weights
3. **Optimization** - Graph-level optimizations
4. **Export** - Convert to edge formats
5. **Validation** - Verify quality gates
6. **Deployment** - Deploy to runtime

### Stage Types

#### Quantization Stage

```python
Stage.quantize(
    mode="mixed_precision",          # int8, int4, ternary, etc.
    weight_bits=4,                    # Bits for weights
    activation_bits=8,                # Bits for activations
    sensitive_layers=["attention"]   # Keep high precision
)
```

#### Pruning Stage

```python
Stage.prune(
    method="structured",    # magnitude, structured, l1_norm
    sparsity=0.7,          # 70% weights removed
    block_size=(1, 4)      # SIMD-friendly blocks
)
```

#### Export Stage

```python
Stage.export(
    format="onnx",              # onnx, tensorrt, tflite
    opset_version=17,           # ONNX opset
    dynamic_axes={              # Dynamic dimensions
        "input": {0: "batch"}
    }
)
```

## Target Devices

EdgeForge supports multiple edge devices:

```python
from edgeforge import TargetDevice

# ARM processors
TargetDevice.ARM_CORTEX_A53
TargetDevice.ARM_CORTEX_A72
TargetDevice.ARM_CORTEX_A76

# NVIDIA edge
TargetDevice.JETSON_NANO
TargetDevice.JETSON_XAVIER

# Google edge
TargetDevice.CORAL_EDGE_TPU

# Apple
TargetDevice.APPLE_NEURAL_ENGINE
```

## Configuration

### EdgeConfig

```python
config = EdgeConfig(
    target=TargetDevice.ARM_CORTEX_A76,
    max_latency_ms=10.0,        # Maximum latency
    min_accuracy=0.95,          # Minimum accuracy
    power_budget_mw=500,        # Power budget
    format="onnx",              # Export format
    max_memory_mb=100,          # Memory limit
    batch_size=1,               # Inference batch size
    num_threads=4               # CPU threads
)
```

## Examples

### Example 1: Basic Quantization

```python
pipeline = (
    Pipeline("basic_quant")
    .load_model("model.pt")
    .add(Stage.quantize(mode="int8_symmetric"))
    .add(Stage.export(format="onnx"))
    .deploy(runtime="onnxruntime")
)

result = pipeline.run(output_dir="artifacts/")
```

### Example 2: Aggressive Compression

```python
pipeline = (
    Pipeline("aggressive")
    .load_model("model.pt")
    .add(Stage.quantize(mode="int4_per_channel"))
    .add(Stage.prune(sparsity=0.8))
    .add(Stage.optimize(fuse_ops=True))
    .add(Stage.export(format="onnx"))
    .deploy(runtime="onnxruntime")
)

result = pipeline.run(output_dir="artifacts/")
```

### Example 3: Edge TPU Deployment

```python
config = EdgeConfig(
    target=TargetDevice.CORAL_EDGE_TPU,
    max_latency_ms=50.0,
    min_accuracy=0.92,
    format="tflite"
)

pipeline = (
    Pipeline("edge_tpu", config)
    .load_model("model.pt")
    .add(Stage.quantize(mode="int8_symmetric"))
    .add(Stage.export(format="tflite"))
    .deploy(runtime="tflite_edgetpu")
)

result = pipeline.run(output_dir="artifacts/")
```

## Advanced Features

### Mixed-Precision Quantization

```python
Stage.quantize(
    mode="mixed_precision",
    weight_bits=4,
    activation_bits=8,
    sensitive_layers=["attention", "output"],
    calibration_dataset="calibration_data.pkl"
)
```

### Structured Pruning for NEON

```python
Stage.prune(
    method="structured",
    sparsity=0.7,
    block_size=(1, 4),  # Optimized for ARM NEON
    sparsity_schedule="cubic"
)
```

### Validation with Rollback

```python
Stage.validate(
    test_dataset="test_data.pkl",
    accuracy_threshold=0.92,
    latency_threshold_ms=8.0,
    memory_threshold_mb=50,
    rollback_on_fail=True
)
```

## Best Practices

### 1. Start Conservative

Begin with INT8 quantization and moderate pruning:

```python
.add(Stage.quantize(mode="int8_symmetric"))
.add(Stage.prune(sparsity=0.5))
```

### 2. Use Calibration Data

For best quantization results, use representative data:

```python
.add(Stage.quantize(
    mode="int8_symmetric",
    calibration_dataset="production_samples.pkl"
))
```

### 3. Validate Early

Add validation stages to catch issues:

```python
.add(Stage.validate(
    test_dataset="validation.pkl",
    accuracy_threshold=0.90,
    rollback_on_fail=True
))
```

### 4. Save Intermediate Models

During development, save each stage:

```python
pipeline.run(
    save_intermediate=True,
    output_dir="artifacts/"
)
```

## Troubleshooting

### Model Too Large

Try more aggressive compression:
- Increase pruning sparsity
- Use INT4 or ternary quantization
- Apply knowledge distillation

### Accuracy Degradation

- Use mixed-precision quantization
- Mark sensitive layers
- Use calibration dataset
- Reduce pruning sparsity

### Slow Inference

- Enable operator fusion
- Use hardware-specific optimizations
- Reduce model size further
- Increase parallelism

## Next Steps

- Read [API Reference](api-reference.md) for detailed documentation
- See [Examples](../examples/) for complete use cases
- Review [Quantization Strategies](quantization.md)
- Learn about [Hardware Optimization](hardware.md)
