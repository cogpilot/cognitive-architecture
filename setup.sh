#!/bin/bash

# Copilot Collaboration Workspace Setup Script
# This script initializes the development environment for ML/NN/MCP/LSP study

set -e

echo "🚀 Initializing Copilot Collaboration Workspace..."

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

# Check if required tools are installed
check_requirements() {
    print_status "Checking requirements..."
    
    # Check Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_success "Python found: $PYTHON_VERSION"
    else
        print_error "Python 3 is required but not installed"
        exit 1
    fi
    
    # Check Node.js
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        print_success "Node.js found: $NODE_VERSION"
    else
        print_error "Node.js is required but not installed"
        exit 1
    fi
    
    # Check npm
    if command -v npm &> /dev/null; then
        NPM_VERSION=$(npm --version)
        print_success "npm found: $NPM_VERSION"
    else
        print_error "npm is required but not installed"
        exit 1
    fi
}

# Set up Python environment
setup_python() {
    print_status "Setting up Python environment..."
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        print_status "Creating Python virtual environment..."
        python3 -m venv venv
        print_success "Virtual environment created"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    print_status "Upgrading pip..."
    pip install --upgrade pip
    
    # Install requirements
    if [ -f "requirements.txt" ]; then
        print_status "Installing Python dependencies..."
        pip install -r requirements.txt
        print_success "Python dependencies installed"
    else
        print_warning "requirements.txt not found, installing basic packages..."
        pip install torch transformers jupyter pytest
    fi
}

# Set up Node.js environment
setup_nodejs() {
    print_status "Setting up Node.js environment..."
    
    # Install npm dependencies
    if [ -f "package.json" ]; then
        print_status "Installing Node.js dependencies..."
        npm install
        print_success "Node.js dependencies installed"
    else
        print_warning "package.json not found, installing basic packages..."
        npm install typescript @types/node
    fi
}

# Create directory structure
create_directories() {
    print_status "Creating directory structure..."
    
    # Study directories
    mkdir -p study/{ml,nn,kc,protocols}
    mkdir -p specs/{grammars,protocols,schemas}
    mkdir -p protocols/{mcp,lsp,custom}
    mkdir -p models/{experiments,checkpoints,configs}
    mkdir -p docs/{learning,api,tutorials}
    mkdir -p tests/{unit,integration,protocols}
    
    print_success "Directory structure created"
}

# Set environment variables
setup_environment() {
    print_status "Setting up environment variables..."
    
    # Create .env file if it doesn't exist
    if [ ! -f ".env" ]; then
        cat > .env << EOF
# Copilot Collaboration Environment Variables
WORKSPACE_TYPE=copilot-collab
STUDY_MODE=enabled
DEBUG_LEVEL=info

# ML/NN Configuration
ML_FRAMEWORKS=torch,tensorflow,jax,sklearn
NN_ARCHITECTURES=transformer,cnn,rnn,gnn
MODEL_TYPES=llm,vision,multimodal,embedding

# Protocol Configuration
MCP_VERSION=2024.11.05
LSP_VERSION=3.17.0
PROTOCOL_MODE=development

# Knowledge Components
KC_DOMAINS=nlp,cv,reasoning,planning
FORMAL_SPECS=bnf,ebnf,antlr,pegjs

# Development Settings
LOG_FORMAT=structured
TRACE_ENABLED=true
EOF
        print_success "Environment file created"
    else
        print_warning ".env file already exists, skipping creation"
    fi
}

# Initialize Git repository
setup_git() {
    print_status "Setting up Git repository..."
    
    if [ ! -d ".git" ]; then
        git init
        print_success "Git repository initialized"
        
        # Create .gitignore
        cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
venv/
env/
.env

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Model files
*.pth
*.ckpt
*.h5
models/checkpoints/

# Temporary files
*.tmp
*.temp
EOF
        print_success ".gitignore created"
    else
        print_warning "Git repository already exists"
    fi
}

# Validate installation
validate_setup() {
    print_status "Validating setup..."
    
    # Check Python packages
    if source venv/bin/activate && python -c "import torch; print(f'PyTorch: {torch.__version__}')" 2>/dev/null; then
        print_success "PyTorch validation passed"
    else
        print_warning "PyTorch validation failed"
    fi
    
    if source venv/bin/activate && python -c "import transformers; print(f'Transformers: {transformers.__version__}')" 2>/dev/null; then
        print_success "Transformers validation passed"
    else
        print_warning "Transformers validation failed"
    fi
    
    # Check Node.js packages
    if npm list typescript &>/dev/null; then
        print_success "TypeScript validation passed"
    else
        print_warning "TypeScript validation failed"
    fi
}

# Create sample files
create_samples() {
    print_status "Creating sample files..."
    
    # Create a simple study script
    if [ ! -f "study/ml/hello_ml.py" ]; then
        cat > study/ml/hello_ml.py << 'EOF'
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
EOF
        print_success "Sample ML script created"
    fi
    
    # Create a simple protocol test
    if [ ! -f "protocols/mcp/test_client.py" ]; then
        cat > protocols/mcp/test_client.py << 'EOF'
"""
Simple MCP client for testing protocol communication
"""

import asyncio
import websockets
import json

async def test_mcp_connection():
    uri = "ws://localhost:8765"
    
    try:
        async with websockets.connect(uri) as websocket:
            # Send a test message
            test_message = {
                "type": "study_request",
                "study_type": "ml_concepts",
                "topic": "hello_world"
            }
            
            await websocket.send(json.dumps(test_message))
            response = await websocket.recv()
            
            print(f"Server response: {response}")
            
    except Exception as e:
        print(f"Connection failed: {e}")
        print("Make sure the MCP server is running!")

if __name__ == "__main__":
    asyncio.run(test_mcp_connection())
EOF
        print_success "Sample MCP client created"
    fi
}

# Main setup function
main() {
    echo "🎯 Copilot Collaboration Workspace Setup"
    echo "========================================"
    
    check_requirements
    setup_python
    setup_nodejs
    create_directories
    setup_environment
    setup_git
    validate_setup
    create_samples
    
    echo ""
    echo "🎉 Setup completed successfully!"
    echo ""
    print_success "Next steps:"
    echo "  1. Activate Python environment: source venv/bin/activate"
    echo "  2. Start MCP server: python protocols/mcp/server.py"
    echo "  3. Test connection: python protocols/mcp/test_client.py"
    echo "  4. Explore study materials in the study/ directory"
    echo "  5. Check documentation in docs/ directory"
    echo ""
    print_status "Happy learning! 🚀"
}

# Run main function
main "$@"
