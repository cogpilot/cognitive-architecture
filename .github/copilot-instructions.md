# Cognitive Architecture Repository

**ALWAYS follow these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.**

This repository implements a distributed AI development ecosystem focused on cognitive architectures, neural transport channels, and GitHub-based organizational intelligence patterns. The codebase combines Python-based AI/ML systems with Node.js/TypeScript for protocol implementations.

## Working Effectively

### Bootstrap, Build, and Test the Repository:
- `chmod +x setup.sh` - Make setup script executable  
- `./setup.sh` - **Full environment setup - NEVER CANCEL. Takes 2 minutes. Set timeout to 5+ minutes.**
- `source venv/bin/activate` - Activate Python virtual environment (required before running Python code)
- `python study/ml/hello_ml.py` - Quick ML environment validation (takes 1-2 seconds)
- `python cognitive_ecology_demo.py` - Test core cognitive architecture demo (takes <1 second)
- `python cognitive-ecology/demonstrate_living_architecture.py` - Extended architecture demo (takes <1 second, may show path warnings)

### Testing Commands:
- `python -m pytest tests/ -v` - Run unit tests (currently empty test directories, takes <1 second)
- `pytest --version` - Verify pytest installation
- `jupyter --version` - Verify Jupyter installation  

### Node.js Environment:
- `npm list` - Show installed Node.js packages (TypeScript, @types/node)
- `npx tsc --version` - Verify TypeScript compiler (v5.9.2)

### Additional Dependencies (install as needed):
- `pip install websockets` - Required for MCP protocol testing
- `pip install <package>` - Install additional Python packages in virtual environment

## Validation

### ALWAYS Manually Validate Changes:
- **Python Changes**: Run `source venv/bin/activate && python <script>` to test cognitive architecture demos
- **Protocol Changes**: Test MCP/LSP implementations with `python protocols/mcp/test_client.py` (requires server)
- **Setup Changes**: Run full `./setup.sh` to verify environment bootstrap still works
- **CRITICAL**: Test at least one complete cognitive architecture scenario:
  - `python cognitive_ecology_demo.py` - Should show particle swarm optimization and neural transport
  - `python study/ml/hello_ml.py` - Should show PyTorch model creation and output

### Build and Environment Timing:
- **NEVER CANCEL**: Setup script takes 2 minutes including PyTorch/Transformers installation
- **NEVER CANCEL**: Python dependency installation can take 60+ seconds  
- Individual demos run in <1 second
- Set timeouts to 5+ minutes for initial setup, 30+ seconds for dependency installations

### Manual Testing Scenarios:
1. **Fresh Environment Setup**: Run `./setup.sh` and verify all components install
2. **Cognitive Architecture Demo**: Run demos and verify neural transport output
3. **Development Environment**: Activate venv and test Python imports work
4. **Protocol Testing**: Test MCP client connection (will fail without server - expected)

## Repository Structure

### Key Directories:
```
.
├── .github/                     # GitHub workflows and configurations
├── cognitive-ecology/           # Core cognitive architecture implementations
├── cogpilot-forge/             # Copilot-specific integration components
├── protocols/                   # MCP, LSP, and custom protocol implementations
├── study/                      # ML/NN learning and example code
├── tests/                      # Test directories (unit, integration, protocols)
├── venv/                       # Python virtual environment (created by setup)
├── setup.sh                    # Main environment setup script
└── cognitive_ecology_demo.py   # Primary demo script
```

### Important Files:
- `ARCHITECTURE.md` - Detailed technical architecture documentation
- `setup.sh` - Environment setup automation (Python + Node.js)
- `cognitive_ecology_demo.py` - Main demonstration of cognitive architecture
- `cognitive-ecology/demonstrate_living_architecture.py` - Extended architecture demo
- `study/ml/hello_ml.py` - Simple ML validation script
- `protocols/mcp/test_client.py` - MCP protocol testing client

## Development Workflow

### Before Making Changes:
1. **ALWAYS** run `source venv/bin/activate` before Python work
2. Test current state with `python cognitive_ecology_demo.py`
3. Understand the cognitive architecture patterns being implemented

### After Making Changes:
1. **ALWAYS** test with cognitive architecture demos to ensure functionality
2. Run validation scenarios to ensure changes don't break core patterns
3. Test environment setup if modifying setup.sh or dependencies

### Common Tasks:
- **ML/NN Development**: Work in `study/` directory, always activate venv first
- **Protocol Development**: Work in `protocols/` directory, test with client scripts  
- **Cognitive Architecture**: Work in `cognitive-ecology/` directory, test with demos
- **Environment Changes**: Modify `setup.sh`, test full bootstrap process

## Technology Stack

### Python Environment:
- **PyTorch 2.8.0** - ML/NN framework (CUDA enabled)
- **Transformers 4.55.2** - Hugging Face transformers
- **Jupyter** - Interactive development environment
- **pytest** - Testing framework
- **websockets** - For MCP protocol communication

### Node.js Environment:  
- **TypeScript 5.9.2** - Type-safe JavaScript development
- **Node.js v20.19.4** - JavaScript runtime
- **npm 10.8.2** - Package manager

### Key Features:
- Distributed AI development ecosystem
- Cognitive architecture patterns
- Neural transport channel implementations  
- GitHub organizational intelligence integration
- Self-designing protocol systems
- Reproducible AI build patterns

## Troubleshooting

### Common Issues:
- **"Module not found" errors**: Run `source venv/bin/activate` first
- **Permission denied on setup.sh**: Run `chmod +x setup.sh`
- **MCP connection failures**: Expected when no server running, use for testing only
- **Path errors in demos**: Some demos reference hardcoded paths, focus on functional output
- **PyTorch installation timeout**: NEVER CANCEL, can take 60+ seconds

### Environment Validation:
```bash
source venv/bin/activate
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
python -c "import transformers; print(f'Transformers: {transformers.__version__}')"
npx tsc --version
```

## Time Expectations

- **Initial Setup**: 2 minutes (NEVER CANCEL)
- **Individual Demos**: <1 second each
- **Python Environment Activation**: Instant
- **Dependency Installation**: 30-60 seconds (NEVER CANCEL)
- **TypeScript Compilation**: <1 second for validation

**CRITICAL**: This repository focuses on cognitive architectures and distributed AI systems. Always validate that cognitive patterns and neural transport functionality work correctly after changes.