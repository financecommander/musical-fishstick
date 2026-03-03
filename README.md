# EdgeForge

**Production-Grade Edge Deployment DSL for ML Models**

EdgeForge is a Python-embedded Domain-Specific Language providing declarative macros for optimizing and deploying ML models to resource-constrained edge devices. Achieve **50-80% model size reduction** with **<5% accuracy degradation** while maintaining **sub-10ms inference latency**.

## Features

- 🎯 **Advanced Quantization**: 2/4/8-bit, mixed-precision, ternary networks
- 🔧 **Model Compression**: Structured pruning, knowledge distillation
- 📦 **Multi-Format Export**: ONNX, TensorRT, TFLite, CoreML, ncnn
- 🚀 **Hardware Optimization**: ARM NEON, Edge TPU, Hexagon DSP, Apple Neural Engine
- ✅ **Validation Gates**: Automatic accuracy/latency/memory testing with rollback
- 🔄 **Zero-Downtime Deploy**: Blue-green deployments with canary testing
- 📊 **Production Monitoring**: Prometheus metrics, health checks

## Quick Start

```python
from edgeforge import Pipeline, Stage, TargetDevice, EdgeConfig

config = EdgeConfig(
    target=TargetDevice.ARM_CORTEX_A76,
    max_latency_ms=10.0,
    min_accuracy=0.95,
    format="onnx"
)

pipeline = (
    Pipeline("my_model")
    .load_model("models/my_model.pt")
    .add(Stage.quantize(mode="mixed_precision", weight_bits=4))
    .add(Stage.prune(sparsity=0.7, method="structured"))
    .add(Stage.export(format="onnx", opset_version=17))
    .add(Stage.validate(
        test_dataset="test.pkl",
        accuracy_threshold=0.92,
        latency_threshold_ms=8.0
    ))
    .deploy(runtime="onnxruntime", device="cpu")
)

result = pipeline.run(output_dir="artifacts/")
```

## Installation

```bash
# Clone repository
git clone https://github.com/financecommander/musical-fishstick.git edgeforge
cd edgeforge

# Install dependencies
pip install -r requirements.txt

# Install EdgeForge
pip install -e .
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     EdgeForge DSL Layer                      │
│  @quantize(), @compress(), @optimize(), @deploy()            │
└───────────────────┬─────────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────────┐
│                  Optimization Engine                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Quantizer │  │ Pruner   │  │ Converter│  │ Validator│   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└───────────────────┬─────────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────────┐
│              Hardware Abstraction Layer                      │
│  ARM NEON | Qualcomm Hexagon | Edge TPU | Apple Neural      │
└───────────────────┬─────────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────────┐
│                 Runtime Targets                              │
│  ONNX Runtime | TFLite | TensorRT | ncnn | MNN              │
└─────────────────────────────────────────────────────────────┘
```

## Use Cases

### Matrix Protocol Trading Agents
Deploy HFT signal processing agents to Raspberry Pi 4 / Jetson Nano clusters with <5ms latency.

### Daily Stop Recipe Classifier
Run BERT-based classification on Google Coral Edge TPU with INT8 quantization.

### Triton Ternary Networks
Export ternary neural networks to mobile devices with XNOR operations.

## Performance Targets

| Metric | Baseline | EdgeForge Target |
|--------|----------|------------------|
| Model Size | 100% (FP32) | 12-25% |
| Inference Latency | 100% | 40-60% |
| Memory Footprint | 100% | 15-30% |
| Power Consumption | 100% | 50-70% |

## Documentation

- [Getting Started](docs/getting-started.md)
- [API Reference](docs/api-reference.md)
- [Quantization Strategies](docs/quantization.md)
- [Hardware Optimization](docs/hardware.md)
- [Deployment Guide](docs/deployment.md)
- [Examples](examples/)

## Development

### Tool Allocation Strategy

- **Grok Code Fast 1**: DSL syntax, code generation, deployment scripts (80% of work)
- **Claude Sonnet 4.5**: Optimization algorithms, quantization math, memory management (20% of work)

### Running Tests

```bash
pytest tests/ -v
```

### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT License - See [LICENSE](LICENSE)

## Citation

```bibtex
@software{edgeforge2026,
  title={EdgeForge: Production-Grade Edge Deployment DSL},
  author={Calculus Holdings LLC},
  year={2026},
  url={https://github.com/financecommander/musical-fishstick}
}
```

---

**Built for Matrix Protocol, Daily Stop, and Constitutional Tender platforms.**
