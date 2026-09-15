#!/usr/bin/env python3

# Copyright (c) 2026 Vrahad Analytics LLP, all rights reserved.
"""Generate docs for all public modules in PyDataRheo and save them to docs/generated.

Usage:
    poetry run python docs/generate.py

"""

from __future__ import annotations

import importlib.util
import pathlib
import re
import shutil
from urllib.parse import quote

import pdoc
import pdoc.render_helpers


def _regenerate_mcp_markdown() -> None:
    """Regenerate `docs/mcp-generated/` before pdoc runs.

    The `datarheo.mcp.{agents,cloud,local,interactive,registry,prompts}` modules pull the
    per-module Markdown files from `docs/mcp-generated/` via pdoc's
    `.. include::` directive. That directory is git-ignored, so on a clean
    checkout pdoc would fail to resolve the include unless we regenerate it
    here. Running the generator from inside `docs-generate` makes the full
    docs build reproducible from a fresh clone (and matches the standalone
    `poe mcp-docs-md` task).

    We load the generator via `importlib.util` from its on-disk path rather
    than a plain `from generate_mcp_markdown import ...`: the generator
    lives under `scripts/` (not on `sys.path`), and a static import would
    also trip `deptry` into flagging `generate_mcp_markdown` as a missing
    external dependency.
    """
    script = pathlib.Path(__file__).parent.parent / "scripts" / "generate_mcp_markdown.py"
    if not script.exists():
        raise RuntimeError(f"MCP markdown generator not found at {script}")
    spec = importlib.util.spec_from_file_location("_mcp_markdown_gen", script)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load spec for {script}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    print("[docs-generate] Regenerating docs/mcp-generated/ ...")
    module.generate(
        server_spec=module.DEFAULT_SERVER_SPEC,
        output=module.DEFAULT_OUTPUT,
    )


# --------------------------------------------------------------------------- brand

_LOGO_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 56" width="260" height="56" role="img" aria-label="PyDataRheo">
  <defs>
    <linearGradient id="dr" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#14A0AC"/>
      <stop offset="1" stop-color="#0B646D"/>
    </linearGradient>
  </defs>
  <rect x="2" y="8" width="40" height="40" rx="11" fill="url(#dr)"/>
  <g fill="none" stroke="#ffffff" stroke-width="3.2" stroke-linecap="round">
    <path d="M10 21c4-4.2 8-4.2 12 0s8 4.2 12 0"/>
    <path d="M10 28c4-4.2 8-4.2 12 0s8 4.2 12 0"/>
    <path d="M10 35c4-4.2 8-4.2 12 0s8 4.2 12 0"/>
  </g>
  <text x="54" y="36" font-family="Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="23" letter-spacing="-0.4">
    <tspan fill="#45BEC8" font-weight="500">Py</tspan><tspan fill="#14A0AC" font-weight="700">DataRheo</tspan>
  </text>
</svg>"""

_FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 44 44" width="44" height="44">
  <defs>
    <linearGradient id="dr" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#14A0AC"/>
      <stop offset="1" stop-color="#0B646D"/>
    </linearGradient>
  </defs>
  <rect width="44" height="44" rx="11" fill="url(#dr)"/>
  <g fill="none" stroke="#ffffff" stroke-width="3.4" stroke-linecap="round">
    <path d="M8 15c4-4.4 8-4.4 12 0s8 4.4 12 0"/>
    <path d="M8 22c4-4.4 8-4.4 12 0s8 4.4 12 0"/>
    <path d="M8 29c4-4.4 8-4.4 12 0s8 4.4 12 0"/>
  </g>
</svg>"""


def _data_uri(svg: str) -> str:
    """Return `svg` as an inline `data:` URL.

    pdoc renders the logo and favicon as plain `<img>` / `<link>` URLs on pages at
    several directory depths, so a relative path would break on nested pages and an
    external URL would make the docs depend on a host we do not control. An inline
    data URL avoids both problems.
    """
    return "data:image/svg+xml;charset=utf-8," + quote(" ".join(svg.split()), safe="")


_INCLUDE_DIRECTIVE = re.compile(r"^\s*\.\.\s+include::\s+(\S+)\s*$", re.MULTILINE)


def _display_path(path: pathlib.Path, root: pathlib.Path) -> str:
    """Return `path` relative to `root`, or absolute if it falls outside `root`."""
    if path.is_relative_to(root):
        return str(path.relative_to(root))
    return str(path)


def _validate_includes(root: pathlib.Path) -> None:
    """Raise if a reStructuredText include in a DataRheo source is missing."""
    resolved_root = root.resolve()
    missing: list[str] = []
    for source in sorted((resolved_root / "datarheo").rglob("*.py")):
        for match in _INCLUDE_DIRECTIVE.finditer(source.read_text(encoding="utf-8")):
            target = (source.parent / match.group(1)).resolve()
            if not target.exists():
                missing.append(
                    f"{_display_path(source, resolved_root)} includes missing "
                    f"{_display_path(target, resolved_root)}"
                )
    if missing:
        raise RuntimeError("Unresolved documentation includes:\n" + "\n".join(missing))


def run() -> None:
    """Generate docs for all public modules in PyDataRheo and save them to docs/generated."""
    public_modules = ["datarheo", "datarheo/cli/pydr.py"]

    # Regenerate MCP Markdown first so the `.. include::` directives in the
    # MCP module docstrings resolve on a clean checkout (docs/mcp-generated/
    # is git-ignored).
    _regenerate_mcp_markdown()
    _validate_includes(pathlib.Path(__file__).parent.parent)

    # recursively delete the docs/generated folder if it exists
    if pathlib.Path("docs/generated").exists():
        shutil.rmtree("docs/generated")

    # pdoc's default sidebar TOC depth is 2 (H1 + H2 only), which hides the
    # per-tool H3 anchors produced by our MCP Markdown generator. Bump to 3 so
    # individual tools / prompts / resources show up in the left nav. This
    # monkey-patches the module-level `markdown_extensions` dict because pdoc
    # 16's `configure()` does not expose markdown extension options.
    # pyrefly: ignore[unsupported-operation]
    pdoc.render_helpers.markdown_extensions["toc"] = {"depth": 3}

    pdoc.render.configure(
        template_directory=pathlib.Path("docs/templates"),
        show_source=True,
        search=True,
        logo=_data_uri(_LOGO_SVG),
        favicon=_data_uri(_FAVICON_SVG),
        mermaid=True,
        docformat="google",
    )
    pdoc.pdoc(
        *public_modules,
        output_directory=pathlib.Path("docs/generated"),
    )


if __name__ == "__main__":
    run()
