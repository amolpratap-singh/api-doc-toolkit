import os
import json
import yaml

from pathlib import Path

CONFIG_DIR = Path(__file__).parent.parent.parent / "config"

def load_env():
    """
    Load environment variables from config/env.json or config/env.yaml,
    merged with OS env.
    """
    env_vars = {}

    json_path = CONFIG_DIR / "env.json"
    yaml_path = CONFIG_DIR / "env.yaml"

    if json_path.exists():
        with open(json_path) as f:
            env_vars.update(json.load(f, encoding='utf-8'))
    elif yaml_path.exists():
        env_vars.update(yaml.safe_load(yaml_path.read_text(encoding='utf-8')) or {})

    # OS environment variables override config file variables
    for key in env_vars:
        os_val = os.environ.get(key)
        if os_val:
            env_vars[key] = os_val

    return env_vars
    