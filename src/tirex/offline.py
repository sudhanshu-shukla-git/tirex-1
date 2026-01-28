"""
Offline utilities for TiRex - easy setup for offline weight loading.

Usage:
    from tirex.offline import setup_offline_env
    setup_offline_env()  # Uses ~/.cache/tirex/weights/ by default
    
Or:
    from tirex.offline import setup_offline_env
    setup_offline_env(weights_path="/custom/path/to/weights")
"""

import os
from pathlib import Path


def setup_offline_env(
    weights_path: str | None = None,
    create_if_missing: bool = False,
) -> bool:
    """
    Setup environment for offline TiRex weight loading.
    
    Args:
        weights_path: Path to weights directory or model.ckpt file.
                     Defaults to ~/.cache/tirex/weights/
        create_if_missing: If True, creates directory if it doesn't exist.
        
    Returns:
        True if setup successful, False otherwise.
        
    Examples:
        >>> from tirex.offline import setup_offline_env
        >>> setup_offline_env()  # Use default cache directory
        >>> from tirex import load_model
        >>> model = load_model("NX-AI/TiRex")
        
        >>> # Or use custom path
        >>> setup_offline_env("/path/to/my/weights")
    """
    
    if weights_path is None:
        weights_path = os.path.expanduser("~/.cache/tirex/weights")
    else:
        weights_path = os.path.expanduser(weights_path)
    
    # Verify path exists
    if not os.path.exists(weights_path):
        if create_if_missing:
            Path(weights_path).mkdir(parents=True, exist_ok=True)
            print(f"Created weights directory: {weights_path}")
        else:
            print(f"Warning: Weights path does not exist: {weights_path}")
            print(f"Run: python setup_offline_weights.py --cache-dir {weights_path}")
            return False
    
    # Set environment variable
    os.environ["TIREX_WEIGHTS_PATH"] = weights_path
    print(f"✓ Offline mode enabled with weights from: {weights_path}")
    
    return True


def get_weights_path() -> str | None:
    """
    Get the current offline weights path.
    
    Returns:
        Path to weights directory or None if not configured.
    """
    return os.getenv("TIREX_WEIGHTS_PATH")


def is_offline_mode() -> bool:
    """Check if offline mode is enabled."""
    weights_path = get_weights_path()
    if weights_path and os.path.exists(weights_path):
        return True
    return False
