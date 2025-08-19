#!/bin/bash

# 🚀 Cogpilot Organization Forge Deployment Script
# Creates the actual repositories and sets up the foundational infrastructure

echo "🧠 Cogpilot Cognitive Architecture Forge"
echo "========================================"
echo ""

# Check if GitHub CLI is available
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) is required but not installed."
    echo "   Please install it from: https://cli.github.com/"
    exit 1
fi

# Check if user is authenticated
if ! gh auth status &> /dev/null; then
    echo "❌ Please authenticate with GitHub CLI first:"
    echo "   gh auth login"
    exit 1
fi

echo "✅ GitHub CLI authenticated and ready"
echo ""

# Organization settings
ORG="cogpilot"
BASE_DIR="/workspaces/aphroditecho/modproc/copilot-custom/cogpilot-forge"

echo "🎯 Target Organization: ${ORG}"
echo "📁 Source Directory: ${BASE_DIR}"
echo ""

# Repository configurations
declare -A REPOSITORIES=(
    ["cognitive-architecture"]="Foundational cognitive architecture for living AI development ecosystem"
    ["particle-swarm-accelerator"]="LLM-as-particle-swarm-accelerator implementations for distributed cognition"
    ["operationalized-rag-fabric"]="RAG fabric linking project imperatives to agent-based issue clustering"
    ["neural-transport-channels"]="Inter-org communication protocols and neural transport channel management"
    ["living-architecture-demos"]="Working examples and demonstrations of living architecture intelligence"
)

# Function to create repository
create_repository() {
    local repo_name=$1
    local description=$2
    
    echo "🏗️ Creating repository: ${repo_name}"
    
    # Create repository in the organization
    gh repo create "${ORG}/${repo_name}" \
        --public \
        --description "${description}" \
        --org "${ORG}" \
        --add-readme
    
    if [ $? -eq 0 ]; then
        echo "  ✅ Repository created: https://github.com/${ORG}/${repo_name}"
        
        # Add topics for discoverability
        gh repo edit "${ORG}/${repo_name}" \
            --add-topic "cognitive-architecture" \
            --add-topic "ai-development" \
            --add-topic "living-systems" \
            --add-topic "ordo-ab-chao"
            
        echo "  🏷️ Topics added for discoverability"
    else
        echo "  ❌ Failed to create repository: ${repo_name}"
        return 1
    fi
}

# Function to upload repository content
upload_content() {
    local repo_name=$1
    
    if [ -d "${BASE_DIR}/${repo_name}" ]; then
        echo "📤 Uploading content for: ${repo_name}"
        
        # Clone the repository locally
        temp_dir=$(mktemp -d)
        cd "${temp_dir}"
        
        gh repo clone "${ORG}/${repo_name}"
        cd "${repo_name}"
        
        # Copy content from our prepared structure
        cp -r "${BASE_DIR}/${repo_name}"/* .
        
        # Add, commit, and push
        git add .
        git commit -m "🧠 Initial cognitive architecture implementation

- Foundational patterns and principles
- Custom instructions for enhanced cognition  
- Implementation guides and examples
- Neural transport protocol foundations

Implements 'ordo ab chao' principle for living AI development ecosystem."
        
        git push origin main
        
        echo "  ✅ Content uploaded to: ${repo_name}"
        
        # Cleanup
        cd /
        rm -rf "${temp_dir}"
    else
        echo "  ℹ️ No prepared content found for: ${repo_name}"
    fi
}

# Main deployment process
echo "🚀 Beginning Repository Creation Process..."
echo ""

# Create repositories
for repo_name in "${!REPOSITORIES[@]}"; do
    description="${REPOSITORIES[$repo_name]}"
    
    # Check if repository already exists
    if gh repo view "${ORG}/${repo_name}" &> /dev/null; then
        echo "ℹ️ Repository already exists: ${repo_name}"
    else
        create_repository "${repo_name}" "${description}"
        sleep 2  # Rate limiting courtesy
    fi
    
    # Upload content if available
    upload_content "${repo_name}"
    
    echo ""
done

echo "📋 POST-CREATION SETUP CHECKLIST"
echo "================================"
echo ""
echo "Next steps to complete the cognitive architecture forge:"
echo ""
echo "1. 🧠 Configure Custom Instructions:"
echo "   https://github.com/organizations/${ORG}/settings/copilot/custom_instructions"
echo "   Copy content from: cognitive-architecture/custom-instructions/cogpilot-instructions.md"
echo ""
echo "2. 📚 Configure Knowledge Base:"
echo "   https://github.com/organizations/${ORG}/settings/copilot/chat_settings/new"
echo "   Follow: cognitive-architecture/implementation/implementation-checklist.md"
echo ""
echo "3. 🔄 Begin Self-Referential Enhancement:"
echo "   Add created repositories to knowledge base:"
for repo_name in "${!REPOSITORIES[@]}"; do
    echo "   - ${ORG}/${repo_name}"
done
echo ""
echo "4. 🌊 Establish Neural Transport Channels:"
echo "   Connect to cogcities and cosmo enterprise organizations"
echo "   Set up cross-org project coordination"
echo ""
echo "✨ COGNITIVE ARCHITECTURE FORGE COMPLETE!"
echo "Ready to begin development within the living AI ecosystem! 🚀"
