"""
Example: Deploy Triton Ternary Network to Mobile

This example demonstrates deploying a ternary neural network
optimized for XNOR operations on mobile devices.
"""

import torch
import torch.nn as nn
from edgeforge import Pipeline, Stage, TargetDevice


class TritonTNN(nn.Module):
    """Simple ternary neural network."""
    
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool2d(2, 2)
    
    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = x.view(-1, 64 * 7 * 7)
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x


def main():
    # Create and save model
    model = TritonTNN()
    torch.save(model, "triton_tnn_fp32.pt")
    print(f"Original TNN saved: triton_tnn_fp32.pt")
    
    # Build ternary optimization pipeline
    pipeline = (
        Pipeline("triton_tnn_mobile")
        .load_model("triton_tnn_fp32.pt")
        
        # Stage 1: Ternarize weights {-1, 0, +1}
        .add(Stage.quantize(
            mode="ternary",
            weight_bits=2,  # Ternary uses ~1.58 bits
            activation_bits=8
        ))
        
        # Stage 2: Structured pruning for NEON
        .add(Stage.prune(
            method="structured",
            sparsity=0.5,
            block_size=(1, 4)  # ARM NEON 128-bit SIMD
        ))
        
        # Stage 3: Graph optimization
        .add(Stage.optimize(
            fuse_ops=True,
            rewrite_patterns=["ternary_matmul_to_xnor"]
        ))
        
        # Stage 4: Export to ONNX
        .add(Stage.export(
            format="onnx",
            opset_version=17,
            custom_ops=["TernaryMatMul", "TernaryConv2d"]
        ))
        
        # Stage 5: Convert to ncnn for mobile
        .add(Stage.convert(
            target_format="ncnn",
            vulkan_support=False,
            fp16_arithmetic=False
        ))
        
        .deploy(
            runtime="ncnn",
            device="cpu",
            num_threads=4
        )
    )
    
    # Execute
    result = pipeline.run(
        output_dir="artifacts/triton_tnn",
        save_intermediate=True
    )
    
    print(f"\nTernary deployment complete!")
    print(f"Status: {result.status}")
    
    print("\n" + "="*60)
    print("Ternary Network Benefits:")
    print("="*60)
    print(f"Model Size:     ~95% reduction (2-bit ternary)")
    print(f"Compute:        XNOR + popcount operations")
    print(f"Memory:         Minimal footprint (<10MB)")
    print(f"Power:          Extremely low (bit operations)")
    print("="*60)


if __name__ == "__main__":
    main()
