#!/usr/bin/env python3
"""
TiRex Weights Diagnostic - Check if weights are accessible
"""

import os
from pathlib import Path

def check_weights():
    print("=" * 60)
    print("TiRex Weights Diagnostic")
    print("=" * 60)
    
    # Check 1: Default location
    default_weights = Path.home() / ".cache" / "tirex" / "weights" / "model.ckpt"
    print(f"\n1. Default weights location:")
    print(f"   Path: {default_weights}")
    print(f"   Exists: {default_weights.exists()}")
    if default_weights.exists():
        size_gb = default_weights.stat().st_size / (1024**3)
        print(f"   Size: {size_gb:.2f} GB")
    
    # Check 2: Environment variable
    env_path = os.getenv("TIREX_WEIGHTS_PATH")
    print(f"\n2. Environment variable (TIREX_WEIGHTS_PATH):")
    print(f"   Set: {env_path is not None}")
    if env_path:
        env_path = Path(env_path)
        print(f"   Path: {env_path}")
        
        # Check if directory or file
        if env_path.is_dir():
            ckpt = env_path / "model.ckpt"
            print(f"   Type: Directory")
            print(f"   Contains model.ckpt: {ckpt.exists()}")
            if ckpt.exists():
                size_gb = ckpt.stat().st_size / (1024**3)
                print(f"   File size: {size_gb:.2f} GB")
        elif env_path.is_file():
            print(f"   Type: File")
            size_gb = env_path.stat().st_size / (1024**3)
            print(f"   File size: {size_gb:.2f} GB")
        else:
            print(f"   Status: Path does not exist!")
    
    # Check 3: Try importing TiRex
    print(f"\n3. TiRex import:")
    try:
        from tirex import load_model, setup_offline_env
        print(f"   Status: ✓ Successfully imported")
    except ImportError as e:
        print(f"   Status: ✗ Import failed: {e}")
        return False
    
    # Check 4: Try loading model
    print(f"\n4. Model loading:")
    try:
        if default_weights.exists() or env_path:
            model = load_model("NX-AI/TiRex")
            print(f"   Status: ✓ Model loaded successfully!")
            return True
        else:
            print(f"   Status: ⚠️  No weights found")
            print(f"   Action: Copy model.ckpt to ~/.cache/tirex/weights/")
            return False
    except Exception as e:
        print(f"   Status: ✗ Failed to load: {e}")
        return False

if __name__ == "__main__":
    success = check_weights()
    
    print("\n" + "=" * 60)
    if success:
        print("✓ All checks passed! TiRex is ready to use offline.")
    else:
        print("✗ Please follow the instructions above.")
        print("\nQuick setup:")
        print("  1. Get model.ckpt file")
        print("  2. mkdir -p ~/.cache/tirex/weights")
        print("  3. cp model.ckpt ~/.cache/tirex/weights/")
        print("  4. Run this script again to verify")
    print("=" * 60)
