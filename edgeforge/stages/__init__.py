"""
EdgeForge Stage Factory

Factory class for creating pipeline stages.
"""

from typing import Optional, Dict, Any, List
from edgeforge.core.pipeline import PipelineStage


class Stage:
    """
    Factory class for creating pipeline stages.
    
    Example:
        Stage.quantize(mode="int8", weight_bits=8)
        Stage.prune(sparsity=0.7, method="structured")
        Stage.export(format="onnx")
    """
    
    @staticmethod
    def quantize(
        mode: str = "int8_symmetric",
        weight_bits: int = 8,
        activation_bits: int = 8,
        scheme: str = "per_tensor_symmetric",
        calibration_method: str = "minmax",
        calibration_dataset: Optional[str] = None,
        percentile: float = 99.99,
        sensitive_layers: Optional[List[str]] = None,
        **kwargs
    ) -> PipelineStage:
        """
        Create a quantization stage.
        
        Args:
            mode: Quantization mode (int8_symmetric, mixed_precision, ternary, etc.)
            weight_bits: Bits for weight quantization
            activation_bits: Bits for activation quantization
            scheme: Quantization scheme (per_tensor, per_channel)
            calibration_method: Method for calibration (minmax, percentile, entropy)
            calibration_dataset: Path to calibration dataset
            percentile: Percentile for calibration (if using percentile method)
            sensitive_layers: List of layer names to keep high precision
        
        Returns:
            QuantizationStage instance
        """
        from edgeforge.stages.quantization import QuantizationStage
        
        config = {
            "mode": mode,
            "weight_bits": weight_bits,
            "activation_bits": activation_bits,
            "scheme": scheme,
            "calibration_method": calibration_method,
            "calibration_dataset": calibration_dataset,
            "percentile": percentile,
            "sensitive_layers": sensitive_layers or [],
            **kwargs
        }
        
        return QuantizationStage(config)
    
    @staticmethod
    def prune(
        method: str = "magnitude",
        sparsity: float = 0.5,
        sparsity_schedule: str = "linear",
        target_sparsity: Optional[float] = None,
        block_size: tuple = (1, 1),
        **kwargs
    ) -> PipelineStage:
        """
        Create a pruning stage.
        
        Args:
            method: Pruning method (magnitude, movement, l1_norm, l2_norm, structured)
            sparsity: Target sparsity (0.0-1.0)
            sparsity_schedule: Sparsity schedule (linear, cubic, exponential)
            target_sparsity: Final sparsity (if different from initial)
            block_size: Block size for structured pruning (e.g., (1, 4) for ARM NEON)
        
        Returns:
            PruningStage instance
        """
        from edgeforge.stages.pruning import PruningStage
        
        config = {
            "method": method,
            "sparsity": sparsity,
            "sparsity_schedule": sparsity_schedule,
            "target_sparsity": target_sparsity or sparsity,
            "block_size": block_size,
            **kwargs
        }
        
        return PruningStage(config)
    
    @staticmethod
    def distill(
        teacher_model: str,
        temperature: float = 3.0,
        alpha: float = 0.7,
        student_hidden_dim: Optional[int] = None,
        epochs: int = 10,
        **kwargs
    ) -> PipelineStage:
        """
        Create a knowledge distillation stage.
        
        Args:
            teacher_model: Path to teacher model
            temperature: Distillation temperature
            alpha: Weight for distillation loss (vs hard label loss)
            student_hidden_dim: Hidden dimension for student model
            epochs: Number of training epochs
        
        Returns:
            DistillationStage instance
        """
        from edgeforge.stages.distillation import DistillationStage
        
        config = {
            "teacher_model": teacher_model,
            "temperature": temperature,
            "alpha": alpha,
            "student_hidden_dim": student_hidden_dim,
            "epochs": epochs,
            **kwargs
        }
        
        return DistillationStage(config)
    
    @staticmethod
    def optimize(
        fuse_ops: bool = True,
        fuse_patterns: Optional[List[str]] = None,
        constant_folding: bool = True,
        eliminate_dead_code: bool = True,
        rewrite_patterns: Optional[List[str]] = None,
        **kwargs
    ) -> PipelineStage:
        """
        Create an optimization stage.
        
        Args:
            fuse_ops: Enable operator fusion
            fuse_patterns: Specific patterns to fuse (e.g., ["conv_bn_relu"])
            constant_folding: Enable constant folding
            eliminate_dead_code: Remove unused operations
            rewrite_patterns: Custom rewrite patterns
        
        Returns:
            OptimizationStage instance
        """
        from edgeforge.stages.optimization import OptimizationStage
        
        config = {
            "fuse_ops": fuse_ops,
            "fuse_patterns": fuse_patterns or ["conv_bn_relu", "linear_relu"],
            "constant_folding": constant_folding,
            "eliminate_dead_code": eliminate_dead_code,
            "rewrite_patterns": rewrite_patterns or [],
            **kwargs
        }
        
        return OptimizationStage(config)
    
    @staticmethod
    def export(
        format: str = "onnx",
        opset_version: int = 17,
        dynamic_axes: Optional[Dict[str, Dict[int, str]]] = None,
        optimization_level: str = "all",
        custom_ops: Optional[List[str]] = None,
        quantize_io: bool = False,
        **kwargs
    ) -> PipelineStage:
        """
        Create an export stage.
        
        Args:
            format: Target format (onnx, tensorrt, tflite, coreml)
            opset_version: ONNX opset version
            dynamic_axes: Dynamic axes for ONNX export
            optimization_level: Optimization level (all, basic, extended)
            custom_ops: Custom operators to include
            quantize_io: Quantize input/output
        
        Returns:
            ExportStage instance
        """
        from edgeforge.stages.export_stage import ExportStage
        
        config = {
            "format": format,
            "opset_version": opset_version,
            "dynamic_axes": dynamic_axes or {},
            "optimization_level": optimization_level,
            "custom_ops": custom_ops or [],
            "quantize_io": quantize_io,
            **kwargs
        }
        
        return ExportStage(config)
    
    @staticmethod
    def validate(
        test_dataset: str,
        metrics: Optional[List[Dict[str, Any]]] = None,
        accuracy_threshold: Optional[float] = None,
        latency_threshold_ms: Optional[float] = None,
        memory_threshold_mb: Optional[float] = None,
        rollback_on_fail: bool = True,
        **kwargs
    ) -> PipelineStage:
        """
        Create a validation stage.
        
        Args:
            test_dataset: Path to test dataset
            metrics: List of validation metrics
            accuracy_threshold: Minimum accuracy threshold
            latency_threshold_ms: Maximum latency threshold
            memory_threshold_mb: Maximum memory threshold
            rollback_on_fail: Rollback to previous model if validation fails
        
        Returns:
            ValidationStage instance
        """
        from edgeforge.stages.validation import ValidationStage
        
        # Build metrics list
        if metrics is None:
            metrics = []
            if accuracy_threshold is not None:
                from edgeforge.core.config import ValidationMetrics
                metrics.append(ValidationMetrics.ACCURACY(accuracy_threshold))
            if latency_threshold_ms is not None:
                from edgeforge.core.config import ValidationMetrics
                metrics.append(ValidationMetrics.LATENCY(latency_threshold_ms))
            if memory_threshold_mb is not None:
                from edgeforge.core.config import ValidationMetrics
                metrics.append(ValidationMetrics.MEMORY(memory_threshold_mb))
        
        config = {
            "test_dataset": test_dataset,
            "metrics": metrics,
            "rollback_on_fail": rollback_on_fail,
            **kwargs
        }
        
        return ValidationStage(config)
    
    @staticmethod
    def convert(
        target_format: str,
        source_format: str = "onnx",
        vulkan_support: bool = False,
        fp16_arithmetic: bool = False,
        **kwargs
    ) -> PipelineStage:
        """
        Create a format conversion stage.
        
        Args:
            target_format: Target format (ncnn, mnn, etc.)
            source_format: Source format
            vulkan_support: Enable Vulkan support
            fp16_arithmetic: Use FP16 arithmetic
        
        Returns:
            ConversionStage instance
        """
        from edgeforge.stages.conversion import ConversionStage
        
        config = {
            "target_format": target_format,
            "source_format": source_format,
            "vulkan_support": vulkan_support,
            "fp16_arithmetic": fp16_arithmetic,
            **kwargs
        }
        
        return ConversionStage(config)
