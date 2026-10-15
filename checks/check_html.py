#!/usr/bin/env python3
"""Validate the demo HTML structure with Python's standard library."""
from html.parser import HTMLParser
from pathlib import Path
import sys

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


class Structure(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []
        self.seen = set()

    def handle_starttag(self, tag, attrs):
        self.seen.add(tag)
        if tag not in VOID:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.seen.add(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack or self.stack[-1] != tag:
            self.errors.append(f"unexpected closing tag </{tag}>")
        else:
            self.stack.pop()


def main(filename):
    path = Path(filename)
    try:
        source = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"FAIL {filename}: {exc}")
        return 1
    parser = Structure()
    parser.feed(source)
    parser.close()
    if parser.stack:
        parser.errors.append("unclosed tags: " + ", ".join(parser.stack))
    for required in ("html", "head", "title", "body", "main"):
        if required not in parser.seen:
            parser.errors.append(f"required element <{required}> is missing")
    if "<!doctype html>" not in source.lower():
        parser.errors.append("missing HTML doctype")
    if parser.errors:
        print(f"FAIL {filename}")
        for error in parser.errors:
            print(f"  - {error}")
        return 1
    print(f"OK {filename}: HTML structure is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else "app/index.html"))
