"""
EdgeForge: Production-Grade Edge Deployment DSL for ML Models

Main exports for the EdgeForge package.
"""

__version__ = "0.1.0"

from edgeforge.core.pipeline import Pipeline
from edgeforge.core.config import EdgeConfig, TargetDevice, ValidationMetrics
from edgeforge.stages import Stage

__all__ = [
    "Pipeline",
    "Stage",
    "EdgeConfig",
    "TargetDevice",
    "ValidationMetrics",
]
