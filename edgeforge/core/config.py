"""
EdgeForge Configuration Classes

Defines configuration objects and enums for edge deployment.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict, Any


class TargetDevice(Enum):
    """Supported target devices for edge deployment."""
    
    # ARM Processors
    ARM_CORTEX_A53 = "arm_cortex_a53"
    ARM_CORTEX_A72 = "arm_cortex_a72"
    ARM_CORTEX_A76 = "arm_cortex_a76"
    
    # NVIDIA Edge
    JETSON_NANO = "jetson_nano"
    JETSON_TX2 = "jetson_tx2"
    JETSON_XAVIER = "jetson_xavier"
    JETSON_ORIN = "jetson_orin"
    
    # Google Edge
    CORAL_EDGE_TPU = "coral_edge_tpu"
    CORAL_DEV_BOARD = "coral_dev_board"
    
    # Qualcomm
    SNAPDRAGON_855 = "snapdragon_855"
    SNAPDRAGON_888 = "snapdragon_888"
    
    # Apple
    APPLE_NEURAL_ENGINE = "apple_neural_engine"
    
    # Generic
    GENERIC_ARM = "generic_arm"
    GENERIC_X86 = "generic_x86"
    GENERIC_GPU = "generic_gpu"


class TargetFormat(Enum):
    """Supported export formats."""
    
    ONNX = "onnx"
    TENSORRT = "tensorrt"
    TFLITE = "tflite"
    COREML = "coreml"
    NCNN = "ncnn"
    MNN = "mnn"
    PYTORCH = "pytorch"


class QuantizationMode(Enum):
    """Quantization modes."""
    
    NONE = "none"
    INT8_SYMMETRIC = "int8_symmetric"
    INT8_ASYMMETRIC = "int8_asymmetric"
    INT4_PER_CHANNEL = "int4_per_channel"
    MIXED_PRECISION = "mixed_precision"
    TERNARY = "ternary"
    BINARY = "binary"


class PruningMethod(Enum):
    """Pruning methods."""
    
    NONE = "none"
    MAGNITUDE = "magnitude"
    MOVEMENT = "movement"
    L1_NORM = "l1_norm"
    L2_NORM = "l2_norm"
    STRUCTURED = "structured"


class ValidationMetrics:
    """Validation metrics with thresholds."""
    
    @staticmethod
    def ACCURACY(threshold: float):
        return {"type": "accuracy", "threshold": threshold}
    
    @staticmethod
    def LATENCY(max_p95_ms: float):
        return {"type": "latency", "max_p95_ms": max_p95_ms}
    
    @staticmethod
    def MEMORY(max_mb: float):
        return {"type": "memory", "max_mb": max_mb}
    
    @staticmethod
    def NUMERICAL_STABILITY(max_divergence: float):
        return {"type": "numerical_stability", "max_divergence": max_divergence}


@dataclass
class EdgeConfig:
    """
    Configuration for edge deployment.
    
    Args:
        target: Target device for deployment
        max_latency_ms: Maximum acceptable latency in milliseconds
        min_accuracy: Minimum acceptable accuracy (0.0-1.0)
        power_budget_mw: Power budget in milliwatts
        format: Target export format
        quantization_mode: Quantization strategy
        pruning_method: Pruning strategy
        max_memory_mb: Maximum memory footprint in MB
        batch_size: Inference batch size
        num_threads: Number of threads for inference
    """
    
    target: TargetDevice
    max_latency_ms: float
    min_accuracy: float
    format: str = "onnx"
    power_budget_mw: Optional[float] = None
    quantization_mode: QuantizationMode = QuantizationMode.INT8_SYMMETRIC
    pruning_method: PruningMethod = PruningMethod.NONE
    max_memory_mb: Optional[float] = None
    batch_size: int = 1
    num_threads: int = 4
    custom_options: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.custom_options is None:
            self.custom_options = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            "target": self.target.value if isinstance(self.target, TargetDevice) else self.target,
            "max_latency_ms": self.max_latency_ms,
            "min_accuracy": self.min_accuracy,
            "format": self.format,
            "power_budget_mw": self.power_budget_mw,
            "quantization_mode": self.quantization_mode.value if isinstance(self.quantization_mode, QuantizationMode) else self.quantization_mode,
            "pruning_method": self.pruning_method.value if isinstance(self.pruning_method, PruningMethod) else self.pruning_method,
            "max_memory_mb": self.max_memory_mb,
            "batch_size": self.batch_size,
            "num_threads": self.num_threads,
            "custom_options": self.custom_options,
        }


@dataclass
class ValidationReport:
    """Validation results report."""
    
    status: str = "PENDING"
    accuracy_drop: float = 0.0
    latency_stats: Optional[Dict[str, float]] = None
    memory_mb: float = 0.0
    output_similarity: float = 0.0
    size_reduction: float = 0.0
    model: Optional[Any] = None
    errors: list = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
        if self.latency_stats is None:
            self.latency_stats = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert report to dictionary."""
        return {
            "status": self.status,
            "accuracy_drop": self.accuracy_drop,
            "latency_stats": self.latency_stats,
            "memory_mb": self.memory_mb,
            "output_similarity": self.output_similarity,
            "size_reduction": self.size_reduction,
            "errors": self.errors,
        }
