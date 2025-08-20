"""
Hello ML - A simple introduction to machine learning concepts
"""

import torch
import torch.nn as nn

class SimpleModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.linear2 = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        x = self.linear1(x)
        x = self.relu(x)
        x = self.linear2(x)
        return x

if __name__ == "__main__":
    model = SimpleModel(10, 20, 5)
    x = torch.randn(1, 10)
    output = model(x)
    print(f"Model output shape: {output.shape}")
    print("Hello ML! 🚀")
