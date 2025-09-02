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
