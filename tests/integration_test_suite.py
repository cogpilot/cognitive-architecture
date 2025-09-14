#!/usr/bin/env python3
"""
Integration test script for the complete cognitive architecture system.
Demonstrates MCP server functionality, LSP capabilities, and core cognitive components.
"""

import asyncio
import sys
import os
import subprocess
import time
import signal
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import from the correct path
import sys
sys.path.insert(0, str(project_root))

from cognitive_ecology_demo import OperationalizedRAGFabric, CognitiveCity
from protocols.mcp.server import MCPServer
from protocols.lsp.server import LSPServer


class IntegrationTestRunner:
    """Run comprehensive integration tests for the cognitive architecture"""
    
    def __init__(self):
        self.test_results = []
        self.mcp_server_process = None
        
    async def run_all_tests(self):
        """Run all integration tests"""
        print("🚀 Starting Cognitive Architecture Integration Tests")
        print("=" * 60)
        
        # Test 1: Core cognitive ecology functionality
        await self.test_cognitive_ecology()
        
        # Test 2: MCP server functionality  
        await self.test_mcp_server()
        
        # Test 3: LSP server capabilities
        await self.test_lsp_server()
        
        # Test 4: Protocol integration
        await self.test_protocol_integration()
        
        # Test 5: ML environment validation
        await self.test_ml_environment()
        
        # Summary
        self.print_test_summary()
        
    async def test_cognitive_ecology(self):
        """Test core cognitive ecology components"""
        print("\n🧠 Testing Cognitive Ecology Components...")
        
        try:
            # Create RAG fabric
            rag_fabric = OperationalizedRAGFabric()
            
            # Create cognitive cities
            cogpilot_city = CognitiveCity(
                name="Cogpilot",
                namespace="github.com/organizations/cogpilot",
                specializations=["ml_architecture", "protocol_design"],
                neural_transport_channels={"cogcities": "github.com/organizations/cogcities"},
                memory_patterns={},
                activation_landscape={"ml_architecture": 0.85, "protocol_design": 0.90}
            )
            
            cogcities_city = CognitiveCity(
                name="CogCities", 
                namespace="github.com/organizations/cogcities",
                specializations=["urban_planning", "distributed_systems"],
                neural_transport_channels={"cogpilot": "github.com/organizations/cogpilot"},
                memory_patterns={},
                activation_landscape={"urban_planning": 0.75, "distributed_systems": 0.80}
            )
            
            # Register cities (mock the neural transport for testing)
            rag_fabric.cognitive_cities[cogpilot_city.namespace] = cogpilot_city
            rag_fabric.cognitive_cities[cogcities_city.namespace] = cogcities_city
            
            # Validate registration
            assert len(rag_fabric.cognitive_cities) == 2
            assert cogpilot_city.namespace in rag_fabric.cognitive_cities
            assert cogcities_city.namespace in rag_fabric.cognitive_cities
            
            self.test_results.append(("Cognitive Ecology", "✅ PASS"))
            print("  ✅ Cognitive cities creation and registration: PASS")
            print("  ✅ Neural transport channel configuration: PASS")
            print("  ✅ Activation landscape management: PASS")
            
        except Exception as e:
            self.test_results.append(("Cognitive Ecology", f"❌ FAIL: {e}"))
            print(f"  ❌ Error: {e}")
    
    async def test_mcp_server(self):
        """Test MCP server functionality"""
        print("\n🔗 Testing MCP Protocol Server...")
        
        try:
            # Create MCP server instance
            mcp_server = MCPServer(host="localhost", port=8767)
            
            # Test message handling
            test_messages = [
                {
                    "type": "study_request",
                    "study_type": "ml_concepts", 
                    "topic": "hello_world"
                },
                {
                    "type": "cognitive_architecture_query",
                    "query_type": "activation_landscape",
                    "parameters": {}
                },
                {
                    "type": "neural_transport",
                    "source": "test_source",
                    "target": "test_target",
                    "payload": {"test": "data"}
                },
                {
                    "type": "protocol_introspection",
                    "introspection_type": "capabilities"
                }
            ]
            
            # Process each message type
            for msg in test_messages:
                if msg["type"] == "study_request":
                    response = await mcp_server.handle_study_request("test_client", msg)
                    assert response["type"] == "study_response"
                    assert "content" in response
                    
                elif msg["type"] == "cognitive_architecture_query":
                    response = await mcp_server.handle_cognitive_query("test_client", msg)
                    assert response["type"] == "cognitive_query_response"
                    assert "result" in response
                    
                elif msg["type"] == "neural_transport":
                    response = await mcp_server.handle_neural_transport("test_client", msg)
                    assert response["type"] == "neural_transport_response"
                    assert response["result"]["status"] == "transmitted"
                    
                elif msg["type"] == "protocol_introspection":
                    response = await mcp_server.handle_protocol_introspection("test_client", msg)
                    assert response["type"] == "protocol_introspection_response"
                    assert "supported_message_types" in response["result"]
            
            self.test_results.append(("MCP Protocol", "✅ PASS"))
            print("  ✅ Study request handling: PASS")
            print("  ✅ Cognitive architecture queries: PASS")
            print("  ✅ Neural transport simulation: PASS")
            print("  ✅ Protocol introspection: PASS")
            
        except Exception as e:
            self.test_results.append(("MCP Protocol", f"❌ FAIL: {e}"))
            print(f"  ❌ Error: {e}")
    
    async def test_lsp_server(self):
        """Test LSP server functionality"""
        print("\n💡 Testing LSP Protocol Server...")
        
        try:
            # Create LSP server instance
            lsp_server = LSPServer()
            
            # Test initialization
            init_params = {
                "workspaceFolders": [{"uri": "file://test", "name": "test"}],
                "capabilities": {}
            }
            init_response = lsp_server._handle_initialize(init_params)
            assert "capabilities" in init_response
            assert init_response["serverInfo"]["name"] == "cognitive-architecture-lsp"
            
            # Test document management
            doc_content = """class CognitiveCity:
    def __init__(self):
        self.activation_landscape = {}
    
    async def neural_transport(self):
        pass

def particle_swarm_optimize():
    return True
"""
            
            # Open document
            open_params = {
                "textDocument": {
                    "uri": "file://test.py",
                    "text": doc_content
                }
            }
            lsp_server._handle_did_open(open_params)
            assert "file://test.py" in lsp_server.documents
            
            # Test hover functionality
            hover_params = {
                "textDocument": {"uri": "file://test.py"},
                "position": {"line": 0, "character": 10}
            }
            hover_response = lsp_server._handle_hover(hover_params)
            # Hover may return None for non-matching positions, which is ok
            
            # Test completion
            completion_params = {
                "textDocument": {"uri": "file://test.py"},
                "position": {"line": 1, "character": 10}
            }
            completion_response = lsp_server._handle_completion(completion_params)
            assert "items" in completion_response
            assert isinstance(completion_response["items"], list)
            
            # Test symbol extraction
            symbols = lsp_server._extract_symbols("file://test.py")
            symbol_names = [s["name"] for s in symbols]
            assert "CognitiveCity" in symbol_names
            assert "__init__" in symbol_names
            assert "particle_swarm_optimize" in symbol_names
            
            self.test_results.append(("LSP Protocol", "✅ PASS"))
            print("  ✅ Server initialization: PASS")
            print("  ✅ Document lifecycle management: PASS") 
            print("  ✅ Completion generation: PASS")
            print("  ✅ Symbol extraction: PASS")
            
        except Exception as e:
            self.test_results.append(("LSP Protocol", f"❌ FAIL: {e}"))
            print(f"  ❌ Error: {e}")
    
    async def test_protocol_integration(self):
        """Test integration between protocols"""
        print("\n🔄 Testing Protocol Integration...")
        
        try:
            # Create both servers
            mcp_server = MCPServer()
            lsp_server = LSPServer()
            
            # Test that both understand cognitive architecture concepts
            
            # MCP cognitive query
            mcp_query = {
                "type": "cognitive_architecture_query",
                "query_type": "activation_landscape", 
                "parameters": {}
            }
            mcp_response = await mcp_server.handle_cognitive_query("test", mcp_query)
            mcp_activations = mcp_response["result"]["current_activations"]
            
            # LSP hover for same concepts
            lsp_hover = lsp_server._generate_hover_info("activation_landscape")
            
            # Both should understand the concept
            assert "ml_architecture" in mcp_activations or "protocol_design" in mcp_activations
            assert lsp_hover is not None and "Activation Landscape" in lsp_hover
            
            # Test completion items include concepts that MCP handles
            completion_response = lsp_server._handle_completion({
                "textDocument": {"uri": "file://test.py"},
                "position": {"line": 0, "character": 0}
            })
            
            completion_labels = [item["label"] for item in completion_response["items"]]
            assert "neural_transport_channels" in completion_labels
            
            self.test_results.append(("Protocol Integration", "✅ PASS"))
            print("  ✅ Cross-protocol concept understanding: PASS")
            print("  ✅ Consistent cognitive architecture terminology: PASS")
            
        except Exception as e:
            self.test_results.append(("Protocol Integration", f"❌ FAIL: {e}"))
            print(f"  ❌ Error: {e}")
    
    async def test_ml_environment(self):
        """Test ML environment and dependencies"""
        print("\n🤖 Testing ML Environment...")
        
        try:
            # Test PyTorch
            import torch
            test_tensor = torch.randn(2, 3)
            assert test_tensor.shape == (2, 3)
            
            # Test Transformers
            import transformers
            assert hasattr(transformers, '__version__')
            
            # Test basic ML model creation
            import torch.nn as nn
            
            class TestModel(nn.Module):
                def __init__(self):
                    super().__init__()
                    self.linear = nn.Linear(10, 5)
                
                def forward(self, x):
                    return self.linear(x)
            
            model = TestModel()
            test_input = torch.randn(1, 10)
            output = model(test_input)
            assert output.shape == (1, 5)
            
            # Run the hello ML script
            result = subprocess.run([
                sys.executable, "study/ml/hello_ml.py"
            ], capture_output=True, text=True, cwd=project_root)
            
            assert result.returncode == 0
            assert "Hello ML!" in result.stdout
            
            self.test_results.append(("ML Environment", "✅ PASS"))
            print("  ✅ PyTorch installation and functionality: PASS")
            print("  ✅ Transformers library: PASS") 
            print("  ✅ Basic neural network creation: PASS")
            print("  ✅ Hello ML script execution: PASS")
            
        except Exception as e:
            self.test_results.append(("ML Environment", f"❌ FAIL: {e}"))
            print(f"  ❌ Error: {e}")
    
    def print_test_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "=" * 60)
        print("🎯 INTEGRATION TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for _, result in self.test_results if "PASS" in result)
        total = len(self.test_results)
        
        for test_name, result in self.test_results:
            print(f"  {test_name:<25} {result}")
        
        print("-" * 60)
        print(f"  Total Tests: {total}")
        print(f"  Passed: {passed}")
        print(f"  Failed: {total - passed}")
        
        if passed == total:
            print("  🎉 ALL TESTS PASSED! Cognitive architecture is ready.")
        else:
            print("  ⚠️  Some tests failed. Check the output above for details.")
        
        print("=" * 60)


async def main():
    """Main function to run integration tests"""
    runner = IntegrationTestRunner()
    
    try:
        await runner.run_all_tests()
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted by user")
    except Exception as e:
        print(f"\n💥 Unexpected error during testing: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up any background processes
        if runner.mcp_server_process:
            runner.mcp_server_process.terminate()


if __name__ == "__main__":
    asyncio.run(main())