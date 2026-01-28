#!/usr/bin/env python3
"""
Setup script to download and prepare TiRex weights for offline use.

This script downloads weights from HuggingFace Hub and stores them locally
for offline inference. After running this, models can be loaded without internet.

Usage:
    python setup_offline_weights.py
    
    Optional arguments:
    --model-id: HuggingFace model ID (default: NX-AI/TiRex)
    --cache-dir: Directory to store weights (default: ~/.cache/tirex/weights/)
    --env-file: Create .env file with TIREX_WEIGHTS_PATH (default: .env)

Examples:
    # Download to default location
    python setup_offline_weights.py
    
    # Download to custom location
    python setup_offline_weights.py --cache-dir /path/to/weights
    
    # Create .env file
    python setup_offline_weights.py --env-file
"""

import argparse
import os
import sys
from pathlib import Path

try:
    from huggingface_hub import hf_hub_download
except ImportError:
    print("Error: huggingface_hub is not installed.")
    print("Install it with: pip install huggingface-hub")
    sys.exit(1)


def setup_offline_weights(
    model_id: str = "NX-AI/TiRex",
    cache_dir: str | None = None,
    create_env_file: bool = False,
):
    """Download and setup offline weights."""
    
    if cache_dir is None:
        cache_dir = os.path.expanduser("~/.cache/tirex/weights")
    else:
        cache_dir = os.path.expanduser(cache_dir)
    
    # Create cache directory
    Path(cache_dir).mkdir(parents=True, exist_ok=True)
    
    print(f"Downloading {model_id} weights...")
    print(f"Cache directory: {cache_dir}")
    
    try:
        # Download the model checkpoint
        checkpoint_path = hf_hub_download(
            repo_id=model_id,
            filename="model.ckpt",
            cache_dir=cache_dir,
        )
        print(f"✓ Downloaded successfully to: {checkpoint_path}")
        
        # Copy to standard location if needed
        standard_path = os.path.join(cache_dir, "model.ckpt")
        if checkpoint_path != standard_path:
            import shutil
            shutil.copy2(checkpoint_path, standard_path)
            print(f"✓ Copied to standard location: {standard_path}")
        
        # Create .env file if requested
        if create_env_file:
            env_content = f"TIREX_WEIGHTS_PATH={cache_dir}\n"
            with open(".env", "w") as f:
                f.write(env_content)
            print(f"✓ Created .env file with TIREX_WEIGHTS_PATH={cache_dir}")
            print("  Add to your notebook with: from dotenv import load_dotenv; load_dotenv()")
        else:
            print(f"\nTo use offline, set environment variable:")
            print(f"  export TIREX_WEIGHTS_PATH={cache_dir}")
            print(f"\nOr in Python:")
            print(f"  import os")
            print(f"  os.environ['TIREX_WEIGHTS_PATH'] = '{cache_dir}'")
            print(f"  from tirex import load_model")
            print(f"  model = load_model('NX-AI/TiRex')")
        
        return True
        
    except Exception as e:
        print(f"✗ Error downloading weights: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Setup TiRex weights for offline use",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--model-id",
        type=str,
        default="NX-AI/TiRex",
        help="HuggingFace model ID (default: NX-AI/TiRex)",
    )
    parser.add_argument(
        "--cache-dir",
        type=str,
        default=None,
        help="Directory to store weights (default: ~/.cache/tirex/weights/)",
    )
    parser.add_argument(
        "--env-file",
        action="store_true",
        help="Create .env file with TIREX_WEIGHTS_PATH",
    )
    
    args = parser.parse_args()
    
    success = setup_offline_weights(
        model_id=args.model_id,
        cache_dir=args.cache_dir,
        create_env_file=args.env_file,
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
