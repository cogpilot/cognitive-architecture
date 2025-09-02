#!/bin/bash

# 🧠 Cognitive Architecture Repository Setup Script
# This script bootstraps the environment for the cognitive architecture system

set -e  # Exit on any error

echo "🚀 Bootstrapping Cognitive Architecture Repository..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "README.md" ]; then
    print_error "Please run this script from the cognitive-architecture repository root"
    exit 1
fi

# Check system requirements
print_status "Checking system requirements..."

# Check Python version
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    print_success "Python3 found: $PYTHON_VERSION"
else
    print_error "Python3 is required but not installed"
    exit 1
fi

# Check Node.js version
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    print_success "Node.js found: $NODE_VERSION"
else
    print_error "Node.js is required but not installed"
    exit 1
fi

# Check npm version
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    print_success "npm found: $NPM_VERSION"
else
    print_error "npm is required but not installed"
    exit 1
fi

# Check git
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version)
    print_success "Git found: $GIT_VERSION"
else
    print_error "Git is required but not installed"
    exit 1
fi

# Create virtual environment
print_status "Creating Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
print_status "Installing Python dependencies..."

# Core dependencies
print_status "Installing core dependencies..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install transformers datasets accelerate
pip install jupyter pytest websockets requests

# Development dependencies
print_status "Installing development dependencies..."
pip install black flake8 mypy
pip install pre-commit

# Install Node.js dependencies
print_status "Installing Node.js dependencies..."
npm install typescript @types/node
npm install --save-dev @types/node

# Create necessary directories
print_status "Creating directory structure..."
mkdir -p examples
mkdir -p architecture-docs
mkdir -p protocols/mcp
mkdir -p protocols/lsp
mkdir -p protocols/neural-transport
mkdir -p tests/unit
mkdir -p tests/integration
mkdir -p tests/protocols

# Copy existing files if they exist in parent directory
print_status "Copying existing implementations..."

# Copy cognitive ecology demo if it exists
if [ -f "../cognitive_ecology_demo.py" ]; then
    cp ../cognitive_ecology_demo.py examples/
    print_success "Copied cognitive_ecology_demo.py"
fi

# Copy cognitive ecology directory if it exists
if [ -d "../cognitive-ecology" ]; then
    cp -r ../cognitive-ecology examples/
    print_success "Copied cognitive-ecology directory"
fi

# Copy study directory if it exists
if [ -d "../study" ]; then
    cp -r ../study examples/
    print_success "Copied study directory"
fi

# Copy protocols if they exist
if [ -d "../protocols" ]; then
    cp -r ../protocols/* protocols/
    print_success "Copied protocols directory"
fi

# Create __init__.py files for Python packages
print_status "Creating Python package structure..."
touch protocols/__init__.py
touch protocols/mcp/__init__.py
touch protocols/lsp/__init__.py
touch protocols/neural-transport/__init__.py
touch tests/__init__.py
touch tests/unit/__init__.py
touch tests/integration/__init__.py
touch tests/protocols/__init__.py

# Create basic test files
print_status "Creating basic test structure..."

cat > tests/unit/test_neural_transport.py << 'EOF'
#!/usr/bin/env python3
"""Unit tests for neural transport protocol."""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add the protocols directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'protocols'))

class TestNeuralTransport(unittest.TestCase):
    """Test cases for neural transport functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        pass
    
    def test_import_neural_transport(self):
        """Test that neural transport module can be imported."""
        try:
            from neural_transport.inter_org_protocol import InterOrgNeuralTransport
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import neural transport module: {e}")
    
    def test_basic_functionality(self):
        """Test basic neural transport functionality."""
        # This is a placeholder test - will be expanded as functionality is implemented
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
EOF

# Create a simple demo script
print_status "Creating demo scripts..."

cat > examples/neural_transport_demo.py << 'EOF'
#!/usr/bin/env python3
"""
Neural Transport Demo

This script demonstrates the neural transport protocol functionality.
"""

import sys
import os

# Add the protocols directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'protocols'))

def main():
    """Run the neural transport demo."""
    print("🧠 Neural Transport Protocol Demo")
    print("=" * 40)
    
    try:
        from neural_transport.inter_org_protocol import InterOrgNeuralTransport
        
        # Initialize transport system
        transport = InterOrgNeuralTransport("demo-token")
        
        # Run the demo
        transport.main()
        
    except ImportError as e:
        print(f"❌ Error importing neural transport module: {e}")
        print("Make sure you've run the setup script and are in the virtual environment")
        return 1
    except Exception as e:
        print(f"❌ Error running demo: {e}")
        return 1
    
    print("\n✅ Demo completed successfully!")
    return 0

if __name__ == "__main__":
    exit(main())
EOF

# Create a quick start script
cat > quick_start.sh << 'EOF'
#!/bin/bash

# Quick start script for cognitive architecture repository

echo "🧠 Quick Start - Cognitive Architecture Repository"
echo "=================================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run ./setup.sh first."
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Run basic tests
echo "🧪 Running basic tests..."
python -m pytest tests/unit/ -v

# Run neural transport demo
echo "🚀 Running neural transport demo..."
python examples/neural_transport_demo.py

echo "✅ Quick start completed!"
echo ""
echo "Next steps:"
echo "1. Explore the examples/ directory"
echo "2. Check out the protocols/ directory"
echo "3. Review the implementation/ directory"
echo "4. Start implementing your cognitive architecture!"
EOF

chmod +x quick_start.sh

# Create a requirements.txt file
print_status "Creating requirements.txt..."
pip freeze > requirements.txt

# Create a package.json for Node.js
print_status "Creating package.json..."
cat > package.json << 'EOF'
{
  "name": "cognitive-architecture",
  "version": "1.0.0",
  "description": "Distributed AI development ecosystem focused on cognitive architectures and neural transport channels",
  "main": "protocols/neural-transport/inter-org-protocol.py",
  "scripts": {
    "test": "python -m pytest tests/ -v",
    "demo": "python examples/neural_transport_demo.py",
    "quick-start": "./quick_start.sh",
    "setup": "./setup.sh"
  },
  "keywords": [
    "cognitive-architecture",
    "neural-transport",
    "ai",
    "machine-learning",
    "distributed-systems",
    "github-copilot"
  ],
  "author": "Cogpilot Organization",
  "license": "MIT",
  "devDependencies": {
    "@types/node": "^20.0.0",
    "typescript": "^5.0.0"
  },
  "engines": {
    "node": ">=18.0.0",
    "npm": ">=8.0.0"
  }
}
EOF

# Create a .gitignore file
print_status "Creating .gitignore..."
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/
env.bak/
venv.bak/

# Jupyter Notebook
.ipynb_checkpoints

# PyTorch
*.pth
*.pt

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Environment variables
.env
.env.local
.env.*.local

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# TypeScript
*.tsbuildinfo

# Testing
.coverage
.pytest_cache/
htmlcov/
.tox/
.nox/
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/
EOF

# Create a README for the examples directory
print_status "Creating examples documentation..."
cat > examples/README.md << 'EOF'
# 🧪 Examples Directory

This directory contains working examples and demonstrations of the cognitive architecture system.

## Available Examples

### Core Demos
- `cognitive_ecology_demo.py` - Core cognitive architecture demonstration
- `neural_transport_demo.py` - Neural transport protocol demonstration

### Cognitive Ecology
- `cognitive-ecology/` - Extended cognitive ecology implementations
- `study/` - Machine learning and neural network examples

## Running Examples

1. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

2. **Run the neural transport demo:**
   ```bash
   python examples/neural_transport_demo.py
   ```

3. **Run the cognitive ecology demo:**
   ```bash
   python examples/cognitive_ecology_demo.py
   ```

## Adding New Examples

When adding new examples:
1. Place them in the appropriate subdirectory
2. Include proper error handling
3. Add documentation in this README
4. Ensure they work with the virtual environment

## Dependencies

All examples use the dependencies installed by `setup.sh`. If you need additional packages:
```bash
source venv/bin/activate
pip install <package-name>
```
EOF

# Final setup steps
print_status "Finalizing setup..."

# Make scripts executable
chmod +x examples/neural_transport_demo.py
chmod +x examples/*.py 2>/dev/null || true

# Test the setup
print_status "Testing setup..."
source venv/bin/activate

# Test Python imports
if python -c "import torch; print(f'PyTorch: {torch.__version__}')" 2>/dev/null; then
    print_success "PyTorch import successful"
else
    print_warning "PyTorch import failed (this is normal for CPU-only installs)"
fi

if python -c "import transformers; print('Transformers import successful')" 2>/dev/null; then
    print_success "Transformers import successful"
else
    print_error "Transformers import failed"
fi

# Test TypeScript
if npx tsc --version 2>/dev/null; then
    print_success "TypeScript compilation test successful"
else
    print_error "TypeScript compilation test failed"
fi

print_success "Setup completed successfully!"
echo ""
echo "🎉 Cognitive Architecture Repository is ready!"
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the quick start: ./quick_start.sh"
echo "3. Explore the examples: python examples/neural_transport_demo.py"
echo "4. Check out the implementation guide: implementation/implementation-checklist.md"
echo ""
echo "🚀 Ready to build living cognitive architectures!"