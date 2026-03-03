"""
EdgeForge Pruning Stage

Implements model pruning for size and compute reduction.
"""

import logging
from typing import Dict, Any
import torch
import torch.nn as nn
import torch.nn.utils.prune as prune

from edgeforge.core.pipeline import PipelineStage

logger = logging.getLogger(__name__)


class PruningStage(PipelineStage):
    """
    Pruning stage for model compression.
    
    Supports:
    - Magnitude pruning (unstructured)
    - Structured pruning (channels, filters)
    - Movement pruning
    - L1/L2 norm pruning
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("prune", config)
    
    def execute(self, model: nn.Module, context: Dict[str, Any]) -> nn.Module:
        """Execute pruning on the model."""
        method = self.config.get("method", "magnitude")
        sparsity = self.config.get("sparsity", 0.5)
        
        logger.info(f"Pruning model with method: {method}, sparsity: {sparsity}")
        
        if method == "magnitude":
            return self._prune_magnitude(model, sparsity)
        elif method == "structured":
            return self._prune_structured(model, sparsity)
        elif method == "l1_norm":
            return self._prune_l1(model, sparsity)
        else:
            logger.warning(f"Unknown pruning method: {method}, skipping")
            return model
    
    def _prune_magnitude(self, model: nn.Module, sparsity: float) -> nn.Module:
        """Apply magnitude-based unstructured pruning."""
        logger.info(f"Applying magnitude pruning with {sparsity:.1%} sparsity")
        
        # Prune all Conv2d and Linear layers
        parameters_to_prune = []
        for name, module in model.named_modules():
            if isinstance(module, (nn.Conv2d, nn.Linear)):
                parameters_to_prune.append((module, 'weight'))
        
        # Apply global unstructured pruning
        prune.global_unstructured(
            parameters_to_prune,
            pruning_method=prune.L1Unstructured,
            amount=sparsity,
        )
        
        # Make pruning permanent
        for module, param_name in parameters_to_prune:
            prune.remove(module, param_name)
        
        # Calculate actual sparsity
        total_params = 0
        zero_params = 0
        for module, _ in parameters_to_prune:
            weight = module.weight
            total_params += weight.numel()
            zero_params += (weight == 0).sum().item()
        
        actual_sparsity = zero_params / total_params if total_params > 0 else 0
        logger.info(f"Magnitude pruning complete. Actual sparsity: {actual_sparsity:.1%}")
        
        context["metrics"]["pruning_sparsity"] = actual_sparsity
        
        return model
    
    def _prune_structured(self, model: nn.Module, sparsity: float) -> nn.Module:
        """
        Apply structured pruning (removes entire channels/filters).
        Hardware-friendly for ARM NEON and similar architectures.
        """
        logger.info(f"Applying structured pruning with {sparsity:.1%} sparsity")
        
        block_size = self.config.get("block_size", (1, 4))
        logger.info(f"Block size: {block_size}")
        
        # Structured pruning for Conv2d layers
        for name, module in model.named_modules():
            if isinstance(module, nn.Conv2d):
                # Prune entire output channels
                prune.ln_structured(
                    module,
                    name='weight',
                    amount=sparsity,
                    n=2,
                    dim=0  # Output channels
                )
                prune.remove(module, 'weight')
        
        logger.info("Structured pruning complete")
        return model
    
    def _prune_l1(self, model: nn.Module, sparsity: float) -> nn.Module:
        """Apply L1-norm based pruning."""
        logger.info(f"Applying L1 pruning with {sparsity:.1%} sparsity")
        
        for name, module in model.named_modules():
            if isinstance(module, (nn.Conv2d, nn.Linear)):
                prune.l1_unstructured(module, name='weight', amount=sparsity)
                prune.remove(module, 'weight')
        
        logger.info("L1 pruning complete")
        return model
