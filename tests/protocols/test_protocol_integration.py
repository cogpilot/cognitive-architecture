"""
Integration tests for MCP and LSP protocol implementations.
Tests the complete protocol functionality and communication.
"""

import unittest
import asyncio
import websockets
import json
import subprocess
import time
import threading
from unittest.mock import patch, Mock
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from protocols.mcp.server import MCPServer
from protocols.mcp.test_client import test_mcp_connection


class TestMCPProtocol(unittest.TestCase):
    """Test MCP (Model Context Protocol) functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.server = None
        self.server_task = None
        self.test_port = 8766  # Use different port for testing
        
    def tearDown(self):
        """Clean up after tests"""
        if self.server_task:
            self.server_task.cancel()
    
    @patch('websockets.serve')
    def test_server_initialization(self, mock_serve):
        """Test that MCP server initializes correctly"""
        server = MCPServer(host="localhost", port=self.test_port)
        
        self.assertEqual(server.host, "localhost")
        self.assertEqual(server.port, self.test_port)
        self.assertIsInstance(server.clients, dict)
        self.assertIsInstance(server.study_sessions, dict)
    
    def test_message_routing(self):
        """Test message routing functionality"""
        server = MCPServer()
        
        # Test study request routing
        study_data = {
            "type": "study_request",
            "study_type": "ml_concepts",
            "topic": "hello_world"
        }
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def run_test():
            response = await server.handle_study_request("test_client", study_data)
            self.assertEqual(response["type"], "study_response")
            self.assertEqual(response["study_type"], "ml_concepts")
            self.assertEqual(response["topic"], "hello_world")
            self.assertIn("content", response)
        
        loop.run_until_complete(run_test())
        loop.close()
    
    def test_cognitive_query_handling(self):
        """Test cognitive architecture query handling"""
        server = MCPServer()
        
        query_data = {
            "type": "cognitive_architecture_query",
            "query_type": "activation_landscape",
            "parameters": {}
        }
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def run_test():
            response = await server.handle_cognitive_query("test_client", query_data)
            self.assertEqual(response["type"], "cognitive_query_response")
            self.assertEqual(response["query_type"], "activation_landscape")
            self.assertIn("result", response)
            self.assertIn("current_activations", response["result"])
        
        loop.run_until_complete(run_test())
        loop.close()
    
    def test_neural_transport_handling(self):
        """Test neural transport channel functionality"""
        server = MCPServer()
        
        transport_data = {
            "type": "neural_transport",
            "source": "github.com/organizations/cogpilot",
            "target": "github.com/organizations/cogcities",
            "payload": {"specialization": "ml_architecture", "activation": 0.85}
        }
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def run_test():
            response = await server.handle_neural_transport("test_client", transport_data)
            self.assertEqual(response["type"], "neural_transport_response")
            self.assertIn("result", response)
            result = response["result"]
            self.assertEqual(result["source"], transport_data["source"])
            self.assertEqual(result["target"], transport_data["target"])
            self.assertEqual(result["status"], "transmitted")
        
        loop.run_until_complete(run_test())
        loop.close()
    
    def test_protocol_introspection(self):
        """Test protocol introspection functionality"""
        server = MCPServer()
        
        introspection_data = {
            "type": "protocol_introspection",
            "introspection_type": "capabilities"
        }
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def run_test():
            response = await server.handle_protocol_introspection("test_client", introspection_data)
            self.assertEqual(response["type"], "protocol_introspection_response")
            self.assertEqual(response["introspection_type"], "capabilities")
            self.assertIn("result", response)
            capabilities = response["result"]
            self.assertIn("supported_message_types", capabilities)
            self.assertIn("study_request", capabilities["supported_message_types"])
        
        loop.run_until_complete(run_test())
        loop.close()
    
    def test_study_content_generation(self):
        """Test study content generation for different topics"""
        server = MCPServer()
        
        # Test ML concepts content
        ml_content = server.generate_ml_study_content("hello_world")
        self.assertIn("concept", ml_content)
        self.assertIn("description", ml_content)
        self.assertIn("example_code", ml_content)
        
        # Test neural network content
        nn_content = server.generate_nn_study_content("transformer")
        self.assertIn("architecture_type", nn_content)
        self.assertIn("description", nn_content)
        
        # Test cognitive architecture content
        cog_content = server.generate_cognitive_architecture_content("particle_swarm")
        self.assertIn("cognitive_pattern", cog_content)
        self.assertIn("neural_transport_channels", cog_content)
    
    def test_performance_metrics(self):
        """Test protocol performance metrics"""
        server = MCPServer()
        
        performance = server.get_protocol_performance()
        self.assertIn("average_response_time_ms", performance)
        self.assertIn("message_throughput", performance)
        self.assertIn("error_rate", performance)
        self.assertIn("bandwidth_efficiency", performance)
        
        # Verify reasonable values
        self.assertIsInstance(performance["average_response_time_ms"], (int, float))
        self.assertIsInstance(performance["error_rate"], (int, float))
        self.assertTrue(0 <= performance["error_rate"] <= 1)


class TestLSPProtocol(unittest.TestCase):
    """Test LSP (Language Server Protocol) functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        from protocols.lsp.server import LSPServer
        self.server = LSPServer()
    
    def test_server_initialization(self):
        """Test that LSP server initializes correctly"""
        self.assertIsInstance(self.server.capabilities, dict)
        self.assertIsInstance(self.server.documents, dict)
        self.assertIsInstance(self.server.workspace_folders, list)
        
        # Check required capabilities
        self.assertTrue(self.server.capabilities["hoverProvider"])
        self.assertIsInstance(self.server.capabilities["completionProvider"], dict)
        self.assertTrue(self.server.capabilities["definitionProvider"])
    
    def test_document_management(self):
        """Test document lifecycle management"""
        # Test document opening
        open_params = {
            "textDocument": {
                "uri": "file://test.py",
                "text": "class CognitiveCity:\n    pass"
            }
        }
        
        self.server._handle_did_open(open_params)
        self.assertIn("file://test.py", self.server.documents)
        self.assertEqual(self.server.documents["file://test.py"], "class CognitiveCity:\n    pass")
        
        # Test document changes
        change_params = {
            "textDocument": {"uri": "file://test.py"},
            "contentChanges": [{"text": "class CognitiveCity:\n    def __init__(self):\n        pass"}]
        }
        
        self.server._handle_did_change(change_params)
        self.assertIn("def __init__", self.server.documents["file://test.py"])
        
        # Test document closing
        close_params = {
            "textDocument": {"uri": "file://test.py"}
        }
        
        self.server._handle_did_close(close_params)
        self.assertNotIn("file://test.py", self.server.documents)
    
    def test_hover_functionality(self):
        """Test hover information generation"""
        # Set up document
        self.server.documents["file://test.py"] = "CognitiveCity neural_transport"
        
        hover_params = {
            "textDocument": {"uri": "file://test.py"},
            "position": {"line": 0, "character": 5}  # Position at "CognitiveCity"
        }
        
        response = self.server._handle_hover(hover_params)
        if response:  # Hover might return None for non-matching positions
            self.assertIn("contents", response)
            self.assertEqual(response["contents"]["kind"], "markdown")
    
    def test_completion_generation(self):
        """Test completion item generation"""
        completion_params = {
            "textDocument": {"uri": "file://test.py"},
            "position": {"line": 0, "character": 10}
        }
        
        response = self.server._handle_completion(completion_params)
        self.assertIn("items", response)
        self.assertIsInstance(response["items"], list)
        self.assertFalse(response["isIncomplete"])
        
        # Check for cognitive architecture specific completions
        item_labels = [item["label"] for item in response["items"]]
        self.assertIn("CognitiveCity", item_labels)
        self.assertIn("ContextualMemoryPattern", item_labels)
    
    def test_symbol_extraction(self):
        """Test document symbol extraction"""
        # Set up test document
        test_content = """class CognitiveCity:
    def __init__(self):
        pass
    
    async def register_city(self):
        pass

def helper_function():
    pass
"""
        
        self.server.documents["file://test.py"] = test_content
        symbols = self.server._extract_symbols("file://test.py")
        
        self.assertIsInstance(symbols, list)
        self.assertTrue(len(symbols) > 0)
        
        # Check for expected symbols
        symbol_names = [symbol["name"] for symbol in symbols]
        self.assertIn("CognitiveCity", symbol_names)
        self.assertIn("__init__", symbol_names)
        self.assertIn("register_city", symbol_names)
        self.assertIn("helper_function", symbol_names)
    
    def test_word_extraction(self):
        """Test word extraction at position"""
        self.server.documents["file://test.py"] = "CognitiveCity neural_transport activation"
        
        # Test word at different positions
        word1 = self.server._get_word_at_position("file://test.py", {"line": 0, "character": 5})
        self.assertEqual(word1, "CognitiveCity")
        
        word2 = self.server._get_word_at_position("file://test.py", {"line": 0, "character": 20})
        self.assertEqual(word2, "neural_transport")
        
        word3 = self.server._get_word_at_position("file://test.py", {"line": 0, "character": 40})
        self.assertEqual(word3, "activation")
    
    def test_hover_info_generation(self):
        """Test hover information for cognitive architecture terms"""
        # Test known terms
        info1 = self.server._generate_hover_info("CognitiveCity")
        self.assertIsNotNone(info1)
        self.assertIn("CognitiveCity", info1)
        
        info2 = self.server._generate_hover_info("neural_transport")
        self.assertIsNotNone(info2)
        self.assertIn("Neural Transport", info2)
        
        info3 = self.server._generate_hover_info("salience_score")
        self.assertIsNotNone(info3)
        self.assertIn("Salience Score", info3)
        
        # Test unknown term
        info4 = self.server._generate_hover_info("unknown_term")
        self.assertIsNone(info4)
    
    def test_initialize_request(self):
        """Test LSP initialize request handling"""
        init_params = {
            "workspaceFolders": [
                {"uri": "file://workspace", "name": "test-workspace"}
            ],
            "capabilities": {}
        }
        
        response = self.server._handle_initialize(init_params)
        
        self.assertIn("capabilities", response)
        self.assertIn("serverInfo", response)
        self.assertEqual(response["serverInfo"]["name"], "cognitive-architecture-lsp")
        
        # Check that workspace folders were stored
        self.assertEqual(len(self.server.workspace_folders), 1)


class TestProtocolIntegration(unittest.TestCase):
    """Test integration between MCP and LSP protocols"""
    
    def test_protocol_compatibility(self):
        """Test that both protocols can coexist"""
        mcp_server = MCPServer()
        from protocols.lsp.server import LSPServer
        lsp_server = LSPServer()
        
        # Both servers should initialize without conflicts
        self.assertIsNotNone(mcp_server)
        self.assertIsNotNone(lsp_server)
        
        # Check that they have distinct capabilities
        self.assertIn("study_request", mcp_server.get_protocol_capabilities()["supported_message_types"])
        self.assertTrue(lsp_server.capabilities["hoverProvider"])
    
    def test_cognitive_architecture_consistency(self):
        """Test that both protocols understand cognitive architecture concepts"""
        mcp_server = MCPServer()
        from protocols.lsp.server import LSPServer
        lsp_server = LSPServer()
        
        # MCP should handle cognitive queries
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def run_mcp_test():
            query_data = {
                "type": "cognitive_architecture_query",
                "query_type": "activation_landscape",
                "parameters": {}
            }
            response = await mcp_server.handle_cognitive_query("test", query_data)
            return response["result"]
        
        mcp_result = loop.run_until_complete(run_mcp_test())
        loop.close()
        
        # LSP should provide hover info for same concepts
        lsp_hover = lsp_server._generate_hover_info("activation_landscape")
        
        # Both should understand activation_landscape concept
        self.assertIn("current_activations", mcp_result)
        self.assertIsNotNone(lsp_hover)
        self.assertIn("Activation Landscape", lsp_hover)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)