#!/bin/bash
# TiRex Offline Setup Script
# Downloads weights from HuggingFace for offline use

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Default values
CACHE_DIR="${HOME}/.cache/tirex/weights"
MODEL_ID="NX-AI/TiRex"
CREATE_ENV=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --cache-dir)
            CACHE_DIR="$2"
            shift 2
            ;;
        --model-id)
            MODEL_ID="$2"
            shift 2
            ;;
        --env-file)
            CREATE_ENV=true
            shift
            ;;
        --help)
            cat << 'EOF'
TiRex Offline Weights Setup

Usage: ./setup_offline_weights.sh [OPTIONS]

Options:
    --cache-dir DIR     Directory to store weights (default: ~/.cache/tirex/weights)
    --model-id ID       HuggingFace model ID (default: NX-AI/TiRex)
    --env-file          Create .env file with TIREX_WEIGHTS_PATH
    --help              Show this help message

Examples:
    # Download to default location
    ./setup_offline_weights.sh
    
    # Download to custom location
    ./setup_offline_weights.sh --cache-dir /path/to/weights
    
    # Create .env file
    ./setup_offline_weights.sh --env-file

EOF
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Expand home directory
CACHE_DIR="${CACHE_DIR/#\~/$HOME}"

echo -e "${BLUE}TiRex Offline Weights Setup${NC}"
echo -e "Model: ${YELLOW}${MODEL_ID}${NC}"
echo -e "Cache Dir: ${YELLOW}${CACHE_DIR}${NC}"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: python3 not found${NC}"
    exit 1
fi

echo -e "${BLUE}Checking dependencies...${NC}"
python3 -c "import huggingface_hub" 2>/dev/null || {
    echo -e "${RED}Error: huggingface_hub not installed${NC}"
    echo "Install with: pip install huggingface-hub"
    exit 1
}
echo -e "${GREEN}✓ Dependencies OK${NC}"
echo ""

# Create cache directory
mkdir -p "$CACHE_DIR"
echo -e "${BLUE}Downloading weights...${NC}"

# Run Python script to download
python3 << PYTHON_EOF
from huggingface_hub import hf_hub_download
import os

try:
    print(f"Downloading from {os.environ.get('MODEL_ID', '${MODEL_ID}')}...")
    checkpoint = hf_hub_download(
        repo_id="${MODEL_ID}",
        filename="model.ckpt",
        cache_dir="${CACHE_DIR}",
    )
    
    # Copy to standard location
    import shutil
    dest = os.path.join("${CACHE_DIR}", "model.ckpt")
    if os.path.abspath(checkpoint) != os.path.abspath(dest):
        shutil.copy2(checkpoint, dest)
    
    print(f"Downloaded to: {dest}")
    file_size = os.path.getsize(dest) / (1024**3)
    print(f"File size: {file_size:.2f} GB")
    
except Exception as e:
    print(f"Error: {e}")
    exit(1)
PYTHON_EOF

if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to download weights${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Download complete${NC}"
echo ""

# Create .env file if requested
if [ "$CREATE_ENV" = true ]; then
    echo -e "${BLUE}Creating .env file...${NC}"
    cat > .env << EOF
TIREX_WEIGHTS_PATH=${CACHE_DIR}
EOF
    echo -e "${GREEN}✓ Created .env${NC}"
    echo ""
fi

# Print usage instructions
echo -e "${GREEN}Setup complete!${NC}"
echo ""
echo -e "${BLUE}To use offline weights:${NC}"
echo ""
echo "Option 1: Environment Variable"
echo -e "  ${YELLOW}export TIREX_WEIGHTS_PATH=${CACHE_DIR}${NC}"
echo ""
echo "Option 2: In Python"
echo -e "  ${YELLOW}from tirex import setup_offline_env${NC}"
echo -e "  ${YELLOW}setup_offline_env()${NC}"
echo ""
echo "Then use normally:"
echo -e "  ${YELLOW}from tirex import load_model${NC}"
echo -e "  ${YELLOW}model = load_model('${MODEL_ID}')${NC}"
echo ""
