#!/usr/bin/env python3
"""
Cognitive Ecology Demonstration

This script demonstrates the complete cognitive ecology architecture including:
- Ecosystem orchestration with AI model cognitive cities
- GitHub Enterprise namespace architecture 
- Introspective protocol design systems
- Guix-inspired reproducible AI builds

It showcases the evolutionary dynamics of peace->war and core->edge mapped
to niche construction and adaptive transformation strategies.
"""

import asyncio
import json
import sys
import os
from pathlib import Path

# Add the current directory to the Python path
sys.path.append(str(Path(__file__).parent))

from ecosystem_orchestrator import demonstrate_cognitive_ecology
from github_enterprise_architecture import demonstrate_enterprise_architecture
from introspective_protocol_designer import demonstrate_introspective_protocol_design
from reproducible_ai_builder import demonstrate_reproducible_ai_builds


async def run_complete_demonstration():
    """Run the complete cognitive ecology demonstration"""
    
    print("🌟" * 30)
    print("  COGNITIVE ECOLOGY ARCHITECTURE")
    print("  Living AI Development Ecosystem")
    print("🌟" * 30)
    print()
    
    # Phase 1: Ecosystem Orchestration
    print("🏗️  PHASE 1: Ecosystem Orchestration")
    print("=" * 50)
    
    try:
        orchestrator = await demonstrate_cognitive_ecology()
        print("✅ Ecosystem orchestration completed successfully")
    except Exception as e:
        print(f"❌ Ecosystem orchestration failed: {e}")
        orchestrator = None
    
    print("\n" + "🔄" * 50 + "\n")
    
    # Phase 2: GitHub Enterprise Architecture  
    print("🏢 PHASE 2: GitHub Enterprise Architecture")
    print("=" * 50)
    
    try:
        enterprise, manifest = demonstrate_enterprise_architecture()
        print("✅ Enterprise architecture setup completed successfully")
    except Exception as e:
        print(f"❌ Enterprise architecture failed: {e}")
        enterprise, manifest = None, None
    
    print("\n" + "🔄" * 50 + "\n")
    
    # Phase 3: Introspective Protocol Design
    print("🧠 PHASE 3: Introspective Protocol Design")
    print("=" * 50)
    
    try:
        designer, new_protocol, evolved_protocol, ecosystem = await demonstrate_introspective_protocol_design()
        print("✅ Introspective protocol design completed successfully")
    except Exception as e:
        print(f"❌ Introspective protocol design failed: {e}")
        designer, new_protocol, evolved_protocol, ecosystem = None, None, None, None
    
    print("\n" + "🔄" * 50 + "\n")
    
    # Phase 4: Reproducible AI Builds
    print("📦 PHASE 4: Reproducible AI Build System")
    print("=" * 50)
    
    try:
        builder, blueprint, build_results = demonstrate_reproducible_ai_builds()
        print("✅ Reproducible build system demonstration completed successfully")
    except Exception as e:
        print(f"❌ Reproducible build system failed: {e}")
        builder, blueprint, build_results = None, None, None
    
    print("\n" + "🎯" * 50 + "\n")
    
    # Integration Summary
    print("🎯 INTEGRATION SUMMARY: Living Architecture")
    print("=" * 60)
    
    if all([orchestrator, enterprise, designer, builder]):
        print("🌟 All systems successfully integrated!")
        print()
        
        # Show the complete ecosystem
        print("🏛️  Cognitive Cities Established:")
        if hasattr(orchestrator, 'cities'):
            for city_name in orchestrator.cities.keys():
                print(f"   • {city_name}")
        
        print(f"\n🏢 Enterprise Namespaces: {len(manifest['namespaces']) if manifest else 0}")
        
        print(f"\n🧠 Protocol Organisms: {len(designer.protocol_ecosystem) if designer else 0}")
        
        print(f"\n📦 Build Components: {len(blueprint['components']) if blueprint else 0}")
        
        print("\n🔗 Neural Transport Channels:")
        if hasattr(orchestrator, 'transport_channels'):
            for channel_id in orchestrator.transport_channels.keys():
                print(f"   • {channel_id}")
        
        print("\n🌐 Evolutionary Dynamics:")
        print("   • Niche Construction (Peace/Innovation) ⟷ Core Focus")
        print("   • Adaptive Transformation (War/Commoditization) ⟷ Edge Focus")
        print("   • Protocols designing protocols through introspection")
        print("   • Reproducible builds enabling reliable evolution")
        
        print("\n🚀 Next Steps:")
        print("   1. Deploy cognitive cities to GitHub Enterprise")
        print("   2. Establish neural transport infrastructure")
        print("   3. Begin collaborative protocol evolution")
        print("   4. Scale to multiple AI model participants")
        print("   5. Monitor ecosystem health and adaptation")
        
    else:
        print("⚠️  Some systems encountered issues during demonstration")
        print("    Check individual phase outputs for details")
    
    print("\n" + "🌟" * 60)
    print("  COGNITIVE ECOLOGY ARCHITECTURE DEMONSTRATION COMPLETE")
    print("🌟" * 60)
    
    return {
        "orchestrator": orchestrator,
        "enterprise": enterprise,
        "manifest": manifest,
        "protocol_designer": designer,
        "build_system": builder,
        "integration_status": "complete" if all([orchestrator, enterprise, designer, builder]) else "partial"
    }


def save_demonstration_results(results: dict):
    """Save demonstration results to files"""
    
    output_dir = Path("/workspaces/aphroditecho/modproc/copilot-custom/cognitive-ecology/demo_results")
    output_dir.mkdir(exist_ok=True)
    
    # Save summary
    summary = {
        "demonstration_timestamp": "2025-08-19T12:00:00Z",
        "integration_status": results["integration_status"],
        "systems_tested": [
            "ecosystem_orchestrator",
            "github_enterprise_architecture", 
            "introspective_protocol_designer",
            "reproducible_ai_builder"
        ],
        "cognitive_cities_count": len(results["orchestrator"].cities) if results["orchestrator"] else 0,
        "enterprise_namespaces_count": len(results["manifest"]["namespaces"]) if results["manifest"] else 0,
        "protocol_organisms_count": len(results["protocol_designer"].protocol_ecosystem) if results["protocol_designer"] else 0,
        "readme": "This demonstration showcases a living architecture for AI development using GitHub Enterprise as a substrate for cognitive cities connected by neural transport channels."
    }
    
    with open(output_dir / "demonstration_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n📄 Demonstration results saved to: {output_dir}")


async def main():
    """Main entry point for the demonstration"""
    
    print("Initializing Cognitive Ecology Demonstration...")
    print("This may take a moment to set up all systems...\n")
    
    try:
        results = await run_complete_demonstration()
        save_demonstration_results(results)
        
        print("\n🎉 Demonstration completed successfully!")
        print("Check the demo_results directory for detailed outputs.")
        
    except KeyboardInterrupt:
        print("\n⏹️  Demonstration interrupted by user")
    except Exception as e:
        print(f"\n💥 Demonstration failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
