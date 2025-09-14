"""
Unit tests for the cognitive ecology demonstration components.
Tests the core cognitive architecture functionality.
"""

import unittest
import asyncio
from unittest.mock import Mock, patch
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from cognitive_ecology_demo import (
    CognitiveCity, 
    ContextualMemoryPattern, 
    OperationalizedRAGFabric
)


class TestCognitiveCity(unittest.TestCase):
    """Test the CognitiveCity dataclass functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.cognitive_city = CognitiveCity(
            name="TestCity",
            namespace="github.com/test/test-org",
            specializations=["ml_architecture", "protocol_design"],
            neural_transport_channels={"target": "github.com/test/target-org"},
            memory_patterns={},
            activation_landscape={"ml_architecture": 0.8, "protocol_design": 0.9}
        )
    
    def test_cognitive_city_creation(self):
        """Test that CognitiveCity can be created with proper attributes"""
        self.assertEqual(self.cognitive_city.name, "TestCity")
        self.assertEqual(self.cognitive_city.namespace, "github.com/test/test-org")
        self.assertIn("ml_architecture", self.cognitive_city.specializations)
        self.assertIn("protocol_design", self.cognitive_city.specializations)
        self.assertEqual(self.cognitive_city.activation_landscape["ml_architecture"], 0.8)
    
    def test_activation_landscape_updates(self):
        """Test that activation landscape can be modified"""
        self.cognitive_city.activation_landscape["new_skill"] = 0.7
        self.assertIn("new_skill", self.cognitive_city.activation_landscape)
        self.assertEqual(self.cognitive_city.activation_landscape["new_skill"], 0.7)


class TestContextualMemoryPattern(unittest.TestCase):
    """Test the ContextualMemoryPattern functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.memory_pattern = ContextualMemoryPattern(
            pattern_id="test_pattern_001",
            priority_profile={"ml_architecture": 0.9, "protocol_design": 0.8},
            execution_trace=[{"action": "encode", "result": "success"}],
            embedding_vector=[0.1, 0.2, 0.3],
            salience_score=0.85,
            organization_context="github.com/test/test-org"
        )
    
    def test_memory_pattern_creation(self):
        """Test ContextualMemoryPattern creation"""
        self.assertEqual(self.memory_pattern.pattern_id, "test_pattern_001")
        self.assertEqual(self.memory_pattern.salience_score, 0.85)
        self.assertEqual(len(self.memory_pattern.embedding_vector), 3)
    
    def test_priority_profile_access(self):
        """Test priority profile functionality"""
        self.assertEqual(self.memory_pattern.priority_profile["ml_architecture"], 0.9)
        self.assertEqual(self.memory_pattern.priority_profile["protocol_design"], 0.8)
    
    def test_execution_trace_appending(self):
        """Test that execution trace can be extended"""
        initial_length = len(self.memory_pattern.execution_trace)
        self.memory_pattern.execution_trace.append({"action": "validate", "result": "passed"})
        self.assertEqual(len(self.memory_pattern.execution_trace), initial_length + 1)


class TestOperationalizedRAGFabric(unittest.TestCase):
    """Test the OperationalizedRAGFabric functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.rag_fabric = OperationalizedRAGFabric()
        self.test_city = CognitiveCity(
            name="TestCity",
            namespace="github.com/test/test-org",
            specializations=["ml_architecture"],
            neural_transport_channels={},
            memory_patterns={},
            activation_landscape={}
        )
    
    def test_rag_fabric_initialization(self):
        """Test that OperationalizedRAGFabric initializes correctly"""
        self.assertIsInstance(self.rag_fabric.cognitive_cities, dict)
        self.assertIsInstance(self.rag_fabric.memory_patterns, dict)
        self.assertEqual(len(self.rag_fabric.cognitive_cities), 0)
    
    @patch('cognitive_ecology_demo.NeuralTransportNetwork')
    def test_register_cognitive_city(self, mock_neural_transport):
        """Test registering a cognitive city"""
        # Mock the neural transport network
        mock_transport_instance = Mock()
        mock_transport_instance.establish_channels.return_value = asyncio.Future()
        mock_transport_instance.establish_channels.return_value.set_result(None)
        mock_neural_transport.return_value = mock_transport_instance
        
        # Create new fabric with mocked transport
        rag_fabric = OperationalizedRAGFabric()
        rag_fabric.neural_transport = mock_transport_instance
        
        # Test registration
        async def run_test():
            await rag_fabric.register_cognitive_city(self.test_city)
            self.assertIn("github.com/test/test-org", rag_fabric.cognitive_cities)
            self.assertEqual(rag_fabric.cognitive_cities["github.com/test/test-org"], self.test_city)
        
        # Run the async test
        asyncio.run(run_test())
    
    def test_memory_pattern_storage(self):
        """Test that memory patterns can be stored and retrieved"""
        test_pattern = ContextualMemoryPattern(
            pattern_id="test_001",
            priority_profile={"test": 0.5},
            execution_trace=[],
            embedding_vector=None,
            salience_score=0.7,
            organization_context="test_org"
        )
        
        self.rag_fabric.memory_patterns["test_001"] = test_pattern
        self.assertIn("test_001", self.rag_fabric.memory_patterns)
        self.assertEqual(self.rag_fabric.memory_patterns["test_001"], test_pattern)


if __name__ == '__main__':
    unittest.main()