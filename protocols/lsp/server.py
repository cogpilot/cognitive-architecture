"""
Language Server Protocol (LSP) implementation for cognitive architecture files.
Provides language support for cognitive architecture DSL and configuration files.
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional, Union
import sys
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LSPServer:
    """Language Server Protocol implementation for cognitive architecture"""
    
    def __init__(self):
        self.capabilities = self._get_capabilities()
        self.documents: Dict[str, str] = {}  # URI -> content
        self.workspace_folders: List[str] = []
        
    def _get_capabilities(self) -> Dict[str, Any]:
        """Define server capabilities"""
        return {
            "textDocumentSync": 1,  # Full document sync
            "hoverProvider": True,
            "completionProvider": {
                "triggerCharacters": [".", ":", "@"],
                "resolveProvider": False
            },
            "signatureHelpProvider": {
                "triggerCharacters": ["(", ","]
            },
            "definitionProvider": True,
            "referencesProvider": True,
            "documentHighlightProvider": True,
            "documentSymbolProvider": True,
            "workspaceSymbolProvider": True,
            "codeActionProvider": True,
            "documentFormattingProvider": True,
            "renameProvider": True
        }
    
    async def start_server(self):
        """Start the LSP server with stdio communication"""
        logger.info("Starting LSP server for cognitive architecture")
        
        while True:
            try:
                # Read header
                header = await self._read_header()
                if not header:
                    break
                
                # Read content
                content_length = header.get("Content-Length", 0)
                if content_length == 0:
                    continue
                
                content = await self._read_content(content_length)
                if not content:
                    continue
                
                # Process message
                await self._process_message(content)
                
            except Exception as e:
                logger.error(f"LSP server error: {e}")
                break
        
        logger.info("LSP server stopped")
    
    async def _read_header(self) -> Optional[Dict[str, Any]]:
        """Read LSP message header"""
        header = {}
        while True:
            line = sys.stdin.readline().strip()
            if not line:
                if header:
                    break
                else:
                    return None
            
            if ":" in line:
                key, value = line.split(":", 1)
                header[key.strip()] = int(value.strip()) if value.strip().isdigit() else value.strip()
        
        return header
    
    async def _read_content(self, length: int) -> Optional[str]:
        """Read LSP message content"""
        try:
            content = sys.stdin.read(length)
            return content if content else None
        except:
            return None
    
    async def _process_message(self, content: str):
        """Process incoming LSP message"""
        try:
            message = json.loads(content)
            method = message.get("method", "")
            params = message.get("params", {})
            msg_id = message.get("id")
            
            # Route message based on method
            if method == "initialize":
                response = self._handle_initialize(params)
                await self._send_response(msg_id, response)
            elif method == "initialized":
                # Client initialization complete
                pass
            elif method == "textDocument/didOpen":
                self._handle_did_open(params)
            elif method == "textDocument/didChange":
                self._handle_did_change(params)
            elif method == "textDocument/didClose":
                self._handle_did_close(params)
            elif method == "textDocument/hover":
                response = self._handle_hover(params)
                await self._send_response(msg_id, response)
            elif method == "textDocument/completion":
                response = self._handle_completion(params)
                await self._send_response(msg_id, response)
            elif method == "textDocument/definition":
                response = self._handle_definition(params)
                await self._send_response(msg_id, response)
            elif method == "textDocument/documentSymbol":
                response = self._handle_document_symbol(params)
                await self._send_response(msg_id, response)
            elif method == "shutdown":
                await self._send_response(msg_id, None)
            elif method == "exit":
                sys.exit(0)
            else:
                logger.warning(f"Unhandled method: {method}")
                
        except json.JSONDecodeError:
            logger.error("Invalid JSON in LSP message")
        except Exception as e:
            logger.error(f"Error processing LSP message: {e}")
    
    def _handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialize request"""
        self.workspace_folders = params.get("workspaceFolders", [])
        
        return {
            "capabilities": self.capabilities,
            "serverInfo": {
                "name": "cognitive-architecture-lsp",
                "version": "1.0.0"
            }
        }
    
    def _handle_did_open(self, params: Dict[str, Any]):
        """Handle textDocument/didOpen notification"""
        text_document = params.get("textDocument", {})
        uri = text_document.get("uri", "")
        text = text_document.get("text", "")
        
        self.documents[uri] = text
        logger.info(f"Opened document: {uri}")
    
    def _handle_did_change(self, params: Dict[str, Any]):
        """Handle textDocument/didChange notification"""
        text_document = params.get("textDocument", {})
        uri = text_document.get("uri", "")
        changes = params.get("contentChanges", [])
        
        if changes and uri in self.documents:
            # For simplicity, assume full document sync
            self.documents[uri] = changes[0].get("text", "")
            logger.info(f"Changed document: {uri}")
    
    def _handle_did_close(self, params: Dict[str, Any]):
        """Handle textDocument/didClose notification"""
        text_document = params.get("textDocument", {})
        uri = text_document.get("uri", "")
        
        if uri in self.documents:
            del self.documents[uri]
            logger.info(f"Closed document: {uri}")
    
    def _handle_hover(self, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Handle textDocument/hover request"""
        text_document = params.get("textDocument", {})
        position = params.get("position", {})
        uri = text_document.get("uri", "")
        
        if uri not in self.documents:
            return None
        
        # Get word at position
        word = self._get_word_at_position(uri, position)
        if not word:
            return None
        
        # Generate hover info based on cognitive architecture concepts
        hover_info = self._generate_hover_info(word)
        if not hover_info:
            return None
        
        return {
            "contents": {
                "kind": "markdown",
                "value": hover_info
            }
        }
    
    def _handle_completion(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle textDocument/completion request"""
        text_document = params.get("textDocument", {})
        position = params.get("position", {})
        uri = text_document.get("uri", "")
        
        # Generate completion items for cognitive architecture
        completion_items = self._generate_completion_items()
        
        return {
            "isIncomplete": False,
            "items": completion_items
        }
    
    def _handle_definition(self, params: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
        """Handle textDocument/definition request"""
        text_document = params.get("textDocument", {})
        position = params.get("position", {})
        uri = text_document.get("uri", "")
        
        # Find definition locations (simplified implementation)
        word = self._get_word_at_position(uri, position)
        if not word:
            return None
        
        # For demo purposes, return mock definition
        return [{
            "uri": uri,
            "range": {
                "start": {"line": 0, "character": 0},
                "end": {"line": 0, "character": len(word)}
            }
        }]
    
    def _handle_document_symbol(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Handle textDocument/documentSymbol request"""
        text_document = params.get("textDocument", {})
        uri = text_document.get("uri", "")
        
        if uri not in self.documents:
            return []
        
        # Extract symbols from cognitive architecture files
        return self._extract_symbols(uri)
    
    def _get_word_at_position(self, uri: str, position: Dict[str, Any]) -> Optional[str]:
        """Get word at given position in document"""
        if uri not in self.documents:
            return None
        
        content = self.documents[uri]
        lines = content.split('\n')
        line_num = position.get("line", 0)
        char_num = position.get("character", 0)
        
        if line_num >= len(lines):
            return None
        
        line = lines[line_num]
        if char_num >= len(line):
            return None
        
        # Find word boundaries (including underscores)
        start = char_num
        end = char_num
        
        while start > 0 and (line[start - 1].isalnum() or line[start - 1] == '_'):
            start -= 1
        
        while end < len(line) and (line[end].isalnum() or line[end] == '_'):
            end += 1
        
        return line[start:end] if start < end else None
    
    def _generate_hover_info(self, word: str) -> Optional[str]:
        """Generate hover information for cognitive architecture terms"""
        hover_map = {
            "CognitiveCity": "**CognitiveCity**: A GitHub organization functioning as a cognitive city with neural transport capabilities.",
            "ContextualMemoryPattern": "**ContextualMemoryPattern**: Patterns of action and execution traces for progressive encoding.",
            "OperationalizedRAGFabric": "**OperationalizedRAGFabric**: Links project imperatives to agent-based issue clustering.",
            "NeuralTransportNetwork": "**NeuralTransportNetwork**: High-bandwidth communication system between cognitive cities.",
            "particle_swarm": "**Particle Swarm**: LLM-as-particle-swarm-accelerator for distributed cognition optimization.",
            "activation_landscape": "**Activation Landscape**: Current state of cognitive activation across different specializations.",
            "salience_score": "**Salience Score**: Measure of importance/relevance of a memory pattern or cognitive element.",
            "enterprise_ai": "**Enterprise AI**: AI systems designed for enterprise-scale cognitive architectures.",
            "neural_transport": "**Neural Transport**: Communication protocol for inter-organizational cognitive data transfer."
        }
        
        return hover_map.get(word)
    
    def _generate_completion_items(self) -> List[Dict[str, Any]]:
        """Generate completion items for cognitive architecture"""
        items = [
            {
                "label": "CognitiveCity",
                "kind": 7,  # Class
                "detail": "GitHub organization as cognitive city",
                "documentation": "Represents a GitHub organization functioning as a cognitive city"
            },
            {
                "label": "ContextualMemoryPattern", 
                "kind": 7,  # Class
                "detail": "Memory pattern for cognitive encoding",
                "documentation": "Patterns of action and execution traces"
            },
            {
                "label": "neural_transport_channels",
                "kind": 5,  # Field
                "detail": "Dict[str, str]",
                "documentation": "Neural transport communication channels"
            },
            {
                "label": "activation_landscape",
                "kind": 5,  # Field
                "detail": "Dict[str, float]",
                "documentation": "Current cognitive activation state"
            },
            {
                "label": "salience_score",
                "kind": 5,  # Field
                "detail": "float",
                "documentation": "Importance score of memory pattern"
            },
            {
                "label": "particle_swarm_optimize",
                "kind": 2,  # Method
                "detail": "async def particle_swarm_optimize(pattern)",
                "documentation": "Optimize memory encoding using particle swarm"
            },
            {
                "label": "register_cognitive_city",
                "kind": 2,  # Method
                "detail": "async def register_cognitive_city(city)",
                "documentation": "Register new cognitive city in network"
            }
        ]
        
        return items
    
    def _extract_symbols(self, uri: str) -> List[Dict[str, Any]]:
        """Extract symbols from cognitive architecture document"""
        if uri not in self.documents:
            return []
        
        content = self.documents[uri]
        symbols = []
        lines = content.split('\n')
        
        # Simple symbol extraction (can be enhanced)
        for line_num, line in enumerate(lines):
            line = line.strip()
            
            # Class definitions
            if line.startswith('class '):
                class_name = line.split()[1].split('(')[0].rstrip(':')
                symbols.append({
                    "name": class_name,
                    "kind": 5,  # Class
                    "range": {
                        "start": {"line": line_num, "character": 0},
                        "end": {"line": line_num, "character": len(line)}
                    },
                    "selectionRange": {
                        "start": {"line": line_num, "character": 6},
                        "end": {"line": line_num, "character": 6 + len(class_name)}
                    }
                })
            
            # Function definitions
            elif line.startswith('def ') or line.startswith('async def '):
                func_start = line.find('def ') + 4
                func_name = line[func_start:].split('(')[0]
                symbols.append({
                    "name": func_name,
                    "kind": 12,  # Function
                    "range": {
                        "start": {"line": line_num, "character": 0},
                        "end": {"line": line_num, "character": len(line)}
                    },
                    "selectionRange": {
                        "start": {"line": line_num, "character": func_start},
                        "end": {"line": line_num, "character": func_start + len(func_name)}
                    }
                })
        
        return symbols
    
    async def _send_response(self, msg_id: Optional[Union[str, int]], result: Any):
        """Send LSP response"""
        response = {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": result
        }
        
        content = json.dumps(response)
        header = f"Content-Length: {len(content)}\r\n\r\n"
        
        sys.stdout.write(header + content)
        sys.stdout.flush()
    
    async def _send_notification(self, method: str, params: Dict[str, Any]):
        """Send LSP notification"""
        notification = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params
        }
        
        content = json.dumps(notification)
        header = f"Content-Length: {len(content)}\r\n\r\n"
        
        sys.stdout.write(header + content)
        sys.stdout.flush()


async def main():
    """Main function to start the LSP server"""
    server = LSPServer()
    try:
        await server.start_server()
    except KeyboardInterrupt:
        logger.info("LSP server shutdown requested")
    except Exception as e:
        logger.error(f"LSP server error: {e}")


if __name__ == "__main__":
    asyncio.run(main())