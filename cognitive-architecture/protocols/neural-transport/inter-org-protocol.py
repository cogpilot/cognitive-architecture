#!/usr/bin/env python3
"""
Neural Transport Protocol for Inter-Organization Communication

This module implements the neural transport channels between GitHub organizations,
enabling context-preserving communication and knowledge sharing across
organizational boundaries.
"""

import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import requests
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class NeuralChannel:
    """Represents a neural transport channel between organizations."""
    source_org: str
    target_org: str
    channel_type: str
    bandwidth: int
    latency: float
    established_at: datetime
    context_preservation: bool
    transport_protocol: str

@dataclass
class ContextPacket:
    """Represents a context packet being transmitted across channels."""
    source_org: str
    target_org: str
    content_type: str
    content: Dict[str, Any]
    timestamp: datetime
    priority: int
    context_hash: str
    dependencies: List[str]

class InterOrgNeuralTransport:
    """
    Implements neural transport channels between GitHub organizations.
    
    This class manages the establishment, maintenance, and optimization of
    communication channels that preserve context across organizational boundaries.
    """
    
    def __init__(self, github_token: str, base_url: str = "https://api.github.com"):
        self.github_token = github_token
        self.base_url = base_url
        self.channels: Dict[str, NeuralChannel] = {}
        self.context_cache: Dict[str, ContextPacket] = {}
        self.headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "cogpilot-neural-transport/1.0"
        }
    
    def establish_channel(self, source_org: str, target_org: str, 
                         channel_type: str = "standard") -> NeuralChannel:
        """
        Establish a neural transport channel between two organizations.
        
        Args:
            source_org: Source organization name
            target_org: Target organization name
            channel_type: Type of channel (standard, high-bandwidth, low-latency)
            
        Returns:
            NeuralChannel: The established channel
        """
        channel_id = f"{source_org}->{target_org}"
        
        # Check if channel already exists
        if channel_id in self.channels:
            logger.info(f"Channel {channel_id} already exists")
            return self.channels[channel_id]
        
        # Determine channel characteristics based on type
        bandwidth, latency = self._calculate_channel_specs(channel_type)
        
        # Create new channel
        channel = NeuralChannel(
            source_org=source_org,
            target_org=target_org,
            channel_type=channel_type,
            bandwidth=bandwidth,
            latency=latency,
            established_at=datetime.now(),
            context_preservation=True,
            transport_protocol="github-api"
        )
        
        self.channels[channel_id] = channel
        logger.info(f"Established {channel_type} channel: {channel_id}")
        
        return channel
    
    def _calculate_channel_specs(self, channel_type: str) -> tuple[int, float]:
        """Calculate bandwidth and latency for different channel types."""
        specs = {
            "standard": (1000, 50.0),      # 1kbps, 50ms
            "high-bandwidth": (10000, 100.0),  # 10kbps, 100ms
            "low-latency": (500, 10.0),    # 500bps, 10ms
            "ultra-low-latency": (200, 5.0)  # 200bps, 5ms
        }
        return specs.get(channel_type, specs["standard"])
    
    def transmit_context(self, source_org: str, target_org: str, 
                        content: Dict[str, Any], content_type: str = "issue",
                        priority: int = 1) -> Optional[ContextPacket]:
        """
        Transmit context across a neural transport channel.
        
        Args:
            source_org: Source organization
            target_org: Target organization
            content: Content to transmit
            content_type: Type of content (issue, pr, discussion, etc.)
            priority: Transmission priority (1=low, 5=high)
            
        Returns:
            ContextPacket: The transmitted packet, or None if transmission failed
        """
        channel_id = f"{source_org}->{target_org}"
        
        if channel_id not in self.channels:
            logger.warning(f"No channel established: {channel_id}")
            return None
        
        # Create context packet
        packet = ContextPacket(
            source_org=source_org,
            target_org=target_org,
            content_type=content_type,
            content=content,
            timestamp=datetime.now(),
            priority=priority,
            context_hash=self._generate_context_hash(content),
            dependencies=self._extract_dependencies(content)
        )
        
        # Transmit based on content type
        success = self._transmit_by_type(packet)
        
        if success:
            self.context_cache[packet.context_hash] = packet
            logger.info(f"Successfully transmitted context: {packet.context_hash}")
            return packet
        else:
            logger.error(f"Failed to transmit context: {packet.context_hash}")
            return None
    
    def _transmit_by_type(self, packet: ContextPacket) -> bool:
        """Transmit context based on content type."""
        try:
            if packet.content_type == "issue":
                return self._transmit_issue(packet)
            elif packet.content_type == "pr":
                return self._transmit_pull_request(packet)
            elif packet.content_type == "discussion":
                return self._transmit_discussion(packet)
            elif packet.content_type == "code":
                return self._transmit_code(packet)
            else:
                logger.warning(f"Unknown content type: {packet.content_type}")
                return False
        except Exception as e:
            logger.error(f"Transmission error: {e}")
            return False
    
    def _transmit_issue(self, packet: ContextPacket) -> bool:
        """Transmit context via GitHub issue creation."""
        # This would create an issue in the target org with context
        # For now, we'll simulate successful transmission
        logger.info(f"Simulating issue transmission: {packet.content.get('title', 'No title')}")
        return True
    
    def _transmit_pull_request(self, packet: ContextPacket) -> bool:
        """Transmit context via GitHub pull request."""
        logger.info(f"Simulating PR transmission: {packet.content.get('title', 'No title')}")
        return True
    
    def _transmit_discussion(self, packet: ContextPacket) -> bool:
        """Transmit context via GitHub discussion."""
        logger.info(f"Simulating discussion transmission: {packet.content.get('title', 'No title')}")
        return True
    
    def _transmit_code(self, packet: ContextPacket) -> bool:
        """Transmit context via code repository."""
        logger.info(f"Simulating code transmission: {packet.content.get('repository', 'No repo')}")
        return True
    
    def _generate_context_hash(self, content: Dict[str, Any]) -> str:
        """Generate a hash for context content."""
        import hashlib
        content_str = json.dumps(content, sort_keys=True)
        return hashlib.sha256(content_str.encode()).hexdigest()[:16]
    
    def _extract_dependencies(self, content: Dict[str, Any]) -> List[str]:
        """Extract dependencies from content."""
        dependencies = []
        
        # Extract repository dependencies
        if "repository" in content:
            dependencies.append(f"repo:{content['repository']}")
        
        # Extract user dependencies
        if "user" in content:
            dependencies.append(f"user:{content['user']}")
        
        # Extract organization dependencies
        if "organization" in content:
            dependencies.append(f"org:{content['organization']}")
        
        return dependencies
    
    def get_channel_status(self, source_org: str, target_org: str) -> Optional[Dict[str, Any]]:
        """Get the status of a specific channel."""
        channel_id = f"{source_org}->{target_org}"
        
        if channel_id not in self.channels:
            return None
        
        channel = self.channels[channel_id]
        
        # Calculate channel health metrics
        uptime = (datetime.now() - channel.established_at).total_seconds()
        health_score = self._calculate_health_score(channel)
        
        return {
            "channel_id": channel_id,
            "source_org": channel.source_org,
            "target_org": channel.target_org,
            "channel_type": channel.channel_type,
            "bandwidth": channel.bandwidth,
            "latency": channel.latency,
            "uptime_seconds": uptime,
            "health_score": health_score,
            "context_preservation": channel.context_preservation,
            "transport_protocol": channel.transport_protocol
        }
    
    def _calculate_health_score(self, channel: NeuralChannel) -> float:
        """Calculate a health score for the channel (0.0 to 1.0)."""
        # Simple health calculation based on uptime and performance
        uptime_hours = (datetime.now() - channel.established_at).total_seconds() / 3600
        
        # Health increases with uptime (up to 24 hours)
        uptime_score = min(uptime_hours / 24.0, 1.0)
        
        # Health based on channel type (better types = higher base score)
        type_scores = {
            "standard": 0.7,
            "high-bandwidth": 0.8,
            "low-latency": 0.9,
            "ultra-low-latency": 0.95
        }
        type_score = type_scores.get(channel.channel_type, 0.5)
        
        # Combine scores
        health_score = (uptime_score * 0.3) + (type_score * 0.7)
        
        return round(health_score, 2)
    
    def list_active_channels(self) -> List[Dict[str, Any]]:
        """List all active neural transport channels."""
        active_channels = []
        
        for channel_id, channel in self.channels.items():
            status = self.get_channel_status(channel.source_org, channel.target_org)
            if status:
                active_channels.append(status)
        
        # Sort by health score (descending)
        active_channels.sort(key=lambda x: x["health_score"], reverse=True)
        
        return active_channels
    
    def optimize_channel(self, source_org: str, target_org: str) -> bool:
        """
        Optimize a neural transport channel for better performance.
        
        Args:
            source_org: Source organization
            target_org: Target organization
            
        Returns:
            bool: True if optimization was successful
        """
        channel_id = f"{source_org}->{target_org}"
        
        if channel_id not in self.channels:
            logger.warning(f"Cannot optimize non-existent channel: {channel_id}")
            return False
        
        channel = self.channels[channel_id]
        
        # Upgrade channel type if possible
        if channel.channel_type == "standard":
            channel.channel_type = "high-bandwidth"
            channel.bandwidth, channel.latency = self._calculate_channel_specs("high-bandwidth")
            logger.info(f"Upgraded {channel_id} to high-bandwidth")
            return True
        elif channel.channel_type == "high-bandwidth":
            channel.channel_type = "low-latency"
            channel.bandwidth, channel.latency = self._calculate_channel_specs("low-latency")
            logger.info(f"Upgraded {channel_id} to low-latency")
            return True
        
        logger.info(f"Channel {channel_id} already at optimal configuration")
        return True
    
    def close_channel(self, source_org: str, target_org: str) -> bool:
        """
        Close a neural transport channel.
        
        Args:
            source_org: Source organization
            target_org: Target organization
            
        Returns:
            bool: True if channel was successfully closed
        """
        channel_id = f"{source_org}->{target_org}"
        
        if channel_id not in self.channels:
            logger.warning(f"Cannot close non-existent channel: {channel_id}")
            return False
        
        # Remove channel
        del self.channels[channel_id]
        
        # Clean up related context cache entries
        self._cleanup_context_cache(source_org, target_org)
        
        logger.info(f"Closed channel: {channel_id}")
        return True
    
    def _cleanup_context_cache(self, source_org: str, target_org: str):
        """Clean up context cache entries for a closed channel."""
        keys_to_remove = []
        
        for key, packet in self.context_cache.items():
            if (packet.source_org == source_org and 
                packet.target_org == target_org):
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del self.context_cache[key]
        
        if keys_to_remove:
            logger.info(f"Cleaned up {len(keys_to_remove)} context cache entries")

def main():
    """Demo of the neural transport system."""
    # Initialize transport system (would need actual GitHub token)
    transport = InterOrgNeuralTransport("demo-token")
    
    # Establish channels between organizations
    print("🚀 Establishing neural transport channels...")
    
    # cogpilot ↔ cogcities
    channel1 = transport.establish_channel("cogpilot", "cogcities", "high-bandwidth")
    print(f"✓ Established {channel1.channel_type} channel: cogpilot → cogcities")
    
    # cogpilot ↔ cosmo-enterprise
    channel2 = transport.establish_channel("cogpilot", "cosmo-enterprise", "low-latency")
    print(f"✓ Established {channel2.channel_type} channel: cogpilot → cosmo-enterprise")
    
    # cogcities ↔ cosmo-enterprise
    channel3 = transport.establish_channel("cogcities", "cosmo-enterprise", "standard")
    print(f"✓ Established {channel3.channel_type} channel: cogcities → cosmo-enterprise")
    
    # Transmit some context
    print("\n📡 Transmitting context across channels...")
    
    context1 = {
        "type": "architectural_pattern",
        "title": "Fractal Organization Principles",
        "description": "Self-similar structures at all scales",
        "repository": "cogpilot/cognitive-architecture",
        "priority": "high"
    }
    
    packet1 = transport.transmit_context("cogpilot", "cogcities", context1, "issue", 5)
    if packet1:
        print(f"✓ Transmitted context: {packet1.content['title']}")
    
    # Show channel status
    print("\n📊 Channel Status:")
    active_channels = transport.list_active_channels()
    for channel in active_channels:
        print(f"  {channel['channel_id']}: {channel['channel_type']} "
              f"(Health: {channel['health_score']:.2f})")
    
    # Optimize a channel
    print("\n🔧 Optimizing channels...")
    transport.optimize_channel("cogcities", "cosmo-enterprise")
    
    # Show final status
    print("\n📊 Final Channel Status:")
    final_channels = transport.list_active_channels()
    for channel in final_channels:
        print(f"  {channel['channel_id']}: {channel['channel_type']} "
              f"(Health: {channel['health_score']:.2f})")

if __name__ == "__main__":
    main()