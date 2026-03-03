"""
Example: Deploy Matrix Protocol Agent to Edge Device

This example demonstrates deploying a trading agent to Raspberry Pi 4
with quantization, pruning, and ONNX export.
"""

import torch
import torch.nn as nn
from edgeforge import Pipeline, Stage, EdgeConfig, TargetDevice


# Define a simple trading agent model
class MatrixProtocolAgent(nn.Module):
    """Simple trading signal processor."""
    
    def __init__(self, input_dim=50, hidden_dim=128, output_dim=3):
        super().__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers=2, batch_first=True)
        self.fc1 = nn.Linear(hidden_dim, 64)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(64, output_dim)
    
    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        out = self.fc1(lstm_out[:, -1, :])
        out = self.relu(out)
        out = self.fc2(out)
        return out


def main():
    # Create and save a dummy model
    model = MatrixProtocolAgent()
    torch.save(model, "matrix_agent_original.pt")
    print(f"Original model saved: matrix_agent_original.pt")
    
    # Configure edge deployment
    config = EdgeConfig(
        target=TargetDevice.ARM_CORTEX_A72,  # Raspberry Pi 4
        max_latency_ms=5.0,
        min_accuracy=0.90,
        format="onnx"
    )
    
    # Build optimization pipeline
    pipeline = (
        Pipeline("matrix_protocol_agent", config)
        .load_model("matrix_agent_original.pt")
        
        # Stage 1: Quantize to INT8
        .add(Stage.quantize(
            mode="int8_symmetric",
            weight_bits=8,
            activation_bits=8
        ))
        
        # Stage 2: Prune to 70% sparsity
        .add(Stage.prune(
            method="magnitude",
            sparsity=0.7
        ))
        
        # Stage 3: Optimize graph
        .add(Stage.optimize(
            fuse_ops=True,
            constant_folding=True
        ))
        
        # Stage 4: Export to ONNX
        .add(Stage.export(
            format="onnx",
            opset_version=17,
            dynamic_axes={"input": {0: "batch", 1: "sequence"}}
        ))
        
        # Stage 5: Deploy
        .deploy(
            runtime="onnxruntime",
            device="cpu",
            session_options={
                "inter_op_num_threads": 4,
                "intra_op_num_threads": 1
            }
        )
    )
    
    # Execute pipeline
    result = pipeline.run(
        output_dir="artifacts/matrix_agent",
        save_intermediate=True
    )
    
    print(f"\nPipeline execution complete!")
    print(f"Status: {result.status}")
    print(f"Artifacts saved to: artifacts/matrix_agent/")
    
    # Print expected improvements
    print("\n" + "="*60)
    print("Expected Performance Improvements:")
    print("="*60)
    print(f"Model Size:     ~75% reduction (INT8 + 70% sparsity)")
    print(f"Latency:        ~40-60% reduction (quantization + fusion)")
    print(f"Memory:         ~70% reduction (INT8 + pruning)")
    print(f"Power:          ~50% reduction (INT8 operations)")
    print("="*60)


if __name__ == "__main__":
    main()
