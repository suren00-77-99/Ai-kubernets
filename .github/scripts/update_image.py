#!/usr/bin/env python3
"""Update the Helm image pin on the GitOps branch."""
import os
from pathlib import Path
import re
import sys
import yaml

VALUES = Path("helm/app/values.yaml")


def main():
    if len(sys.argv) != 2 or not re.fullmatch(r"[0-9a-f]{7,40}", sys.argv[1]):
        raise SystemExit("Usage: update_image.py <git-commit-sha>")
    repository = os.environ.get("IMAGE_REPOSITORY", "")
    if not re.fullmatch(r"[0-9]{12}\.dkr\.ecr\.[a-z0-9-]+\.amazonaws\.com/[a-z0-9._/-]+", repository):
        raise SystemExit("IMAGE_REPOSITORY must be a valid ECR image repository URI")
    values = yaml.safe_load(VALUES.read_text(encoding="utf-8"))
    values["image"]["repository"] = repository
    values["image"]["tag"] = sys.argv[1]
    VALUES.write_text(yaml.safe_dump(values, sort_keys=False), encoding="utf-8")
    print(f"Updated {VALUES}: {repository}:{sys.argv[1]}")


if __name__ == "__main__":
    main()
