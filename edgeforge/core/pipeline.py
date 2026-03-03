"""
EdgeForge Pipeline

Core pipeline builder for edge deployment workflows.
"""

import os
import json
import logging
from typing import List, Optional, Dict, Any, Callable
from pathlib import Path
import torch

from edgeforge.core.config import EdgeConfig, ValidationReport

logger = logging.getLogger(__name__)


class PipelineStage:
    """Base class for pipeline stages."""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
    
    def execute(self, model: torch.nn.Module, context: Dict[str, Any]) -> torch.nn.Module:
        """Execute this stage and return modified model."""
        raise NotImplementedError
    
    def __repr__(self):
        return f"PipelineStage({self.name}, {self.config})"


class Pipeline:
    """
    Fluent API for building edge deployment pipelines.
    
    Example:
        pipeline = (
            Pipeline("my_model")
            .load_model("model.pt")
            .add(Stage.quantize(mode="int8"))
            .add(Stage.prune(sparsity=0.7))
            .add(Stage.export(format="onnx"))
            .deploy(runtime="onnxruntime")
        )
        result = pipeline.run()
    """
    
    def __init__(self, name: str, config: Optional[EdgeConfig] = None):
        self.name = name
        self.config = config
        self.stages: List[PipelineStage] = []
        self.model_path: Optional[str] = None
        self.model: Optional[torch.nn.Module] = None
        self.deploy_config: Optional[Dict[str, Any]] = None
        self.context: Dict[str, Any] = {
            "intermediate_outputs": [],
            "metrics": {},
        }
    
    def load_model(self, path: str) -> "Pipeline":
        """
        Load PyTorch model from path.
        
        Args:
            path: Path to .pt or .pth model file
        
        Returns:
            Self for chaining
        """
        self.model_path = path
        logger.info(f"Pipeline '{self.name}': Model path set to {path}")
        return self
    
    def add(self, stage: PipelineStage) -> "Pipeline":
        """
        Add a stage to the pipeline.
        
        Args:
            stage: PipelineStage instance
        
        Returns:
            Self for chaining
        """
        self.stages.append(stage)
        logger.info(f"Pipeline '{self.name}': Added stage {stage.name}")
        return self
    
    def deploy(
        self,
        runtime: str,
        device: str = "cpu",
        providers: Optional[List[str]] = None,
        session_options: Optional[Dict[str, Any]] = None,
        monitoring: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> "Pipeline":
        """
        Configure deployment settings.
        
        Args:
            runtime: Runtime to use (onnxruntime, tensorrt, tflite, etc.)
            device: Target device (cpu, cuda, etc.)
            providers: Execution providers for ONNX Runtime
            session_options: Runtime-specific options
            monitoring: Monitoring configuration
            **kwargs: Additional deployment options
        
        Returns:
            Self for chaining
        """
        self.deploy_config = {
            "runtime": runtime,
            "device": device,
            "providers": providers or ["CPUExecutionProvider"],
            "session_options": session_options or {},
            "monitoring": monitoring or {},
            **kwargs
        }
        logger.info(f"Pipeline '{self.name}': Deployment configured for {runtime}")
        return self
    
    def run(
        self,
        override: Optional[Dict[str, Any]] = None,
        dry_run: bool = False,
        save_intermediate: bool = False,
        output_dir: str = "artifacts"
    ) -> ValidationReport:
        """
        Execute the pipeline.
        
        Args:
            override: Override configuration for specific stages
            dry_run: If True, don't actually execute stages
            save_intermediate: Save intermediate models after each stage
            output_dir: Directory to save outputs
        
        Returns:
            ValidationReport with results
        """
        logger.info(f"Pipeline '{self.name}': Starting execution")
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Load model if not already loaded
        if self.model is None and self.model_path:
            logger.info(f"Loading model from {self.model_path}")
            self.model = torch.load(self.model_path, weights_only=False)
        
        if self.model is None:
            raise ValueError("No model loaded. Call load_model() first.")
        
        # Track original model for comparison
        original_model = self.model
        current_model = self.model
        
        # Execute each stage
        for i, stage in enumerate(self.stages):
            logger.info(f"Executing stage {i+1}/{len(self.stages)}: {stage.name}")
            
            if dry_run:
                logger.info(f"  [DRY RUN] Would execute {stage}")
                continue
            
            try:
                # Apply overrides if specified
                stage_config = stage.config.copy()
                if override:
                    stage_key = f"{stage.name}."
                    for key, value in override.items():
                        if key.startswith(stage_key):
                            param = key.replace(stage_key, "")
                            stage_config[param] = value
                
                # Execute stage
                current_model = stage.execute(current_model, self.context)
                
                # Save intermediate if requested
                if save_intermediate:
                    intermediate_path = output_path / f"stage_{i+1}_{stage.name}.pt"
                    torch.save(current_model, intermediate_path)
                    logger.info(f"  Saved intermediate model to {intermediate_path}")
                
            except Exception as e:
                logger.error(f"Stage {stage.name} failed: {e}")
                raise
        
        # Create validation report
        report = ValidationReport(
            status="SUCCESS",
            model=current_model
        )
        
        # Save final model
        final_path = output_path / f"{self.name}_optimized.pt"
        torch.save(current_model, final_path)
        logger.info(f"Saved final model to {final_path}")
        
        # Save pipeline metadata
        metadata = {
            "name": self.name,
            "stages": [{"name": s.name, "config": s.config} for s in self.stages],
            "deploy_config": self.deploy_config,
            "context": {
                "metrics": self.context["metrics"]
            }
        }
        metadata_path = output_path / f"{self.name}_metadata.json"
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Pipeline '{self.name}': Execution complete")
        return report
    
    def __repr__(self):
        return f"Pipeline(name={self.name}, stages={len(self.stages)})"
