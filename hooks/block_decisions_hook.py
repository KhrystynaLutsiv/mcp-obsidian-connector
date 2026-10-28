#!/usr/bin/env python3
"""Pre-tool-use hook: блокує видалення та модифікацію файлів у Decisions/."""

from __future__ import annotations

import json
import re
import sys
from typing import Any

BLOCK_EXIT_CODE = 2
DECISIONS_MARKER = "decisions"

MUTATING_TOOL_NAMES = {
    "delete",
    "write",
    "strreplace",
    "editnotebook",
    "applypatch",
    "edit",
}

SHELL_TOOL_NAMES = {"shell", "bash"}

PATH_KEYS = (
    "path",
    "file_path",
    "filePath",
    "target_file",
    "targetFile",
    "working_directory",
)

MUTATING_COMMAND_PATTERN = re.compile(
    r"("
    r"\brm\b|\brmdir\b|\bdel\b|\berase\b|\bmove\b|\bmv\b|\bren\b|\brename\b|"
    r"\bgit\s+rm\b|\bremove-item\b|\bset-content\b|\badd-content\b|"
    r"\bout-file\b|\bnew-item\b|"
    r"\bwrite\b|\bdelete\b|>{1,2}"
    r")",
    re.IGNORECASE,
)


def _as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    try:
        return json.dumps(value, ensure_ascii=False)
    except TypeError:
        return str(value)


def _collect_paths_and_commands(payload: dict[str, Any]) -> str:
    tool_input = payload.get("tool_input") or payload.get("input") or {}
    fragments = [
        payload.get("command"),
        payload.get("path"),
        payload.get("file_path"),
    ]
    if isinstance(tool_input, dict):
        fragments.append(tool_input.get("command"))
        for key in PATH_KEYS:
            fragments.append(tool_input.get(key))
    elif tool_input:
        fragments.append(tool_input)
    return " ".join(_as_text(part) for part in fragments if part not in (None, ""))


def _mentions_decisions(text: str) -> bool:
    return DECISIONS_MARKER in text.lower()


def _is_mutating_tool(tool_name: str, combined_text: str) -> bool:
    normalized = tool_name.lower()
    if normalized in MUTATING_TOOL_NAMES:
        return True
    if normalized in SHELL_TOOL_NAMES:
        return bool(MUTATING_COMMAND_PATTERN.search(combined_text))
    return "delete" in normalized or "write" in normalized or "edit" in normalized


def _block(message: str) -> int:
    print(message, file=sys.stderr)
    print(
        json.dumps(
            {
                "permission": "deny",
                "user_message": message,
                "agent_message": message,
            },
            ensure_ascii=False,
        )
    )
    return BLOCK_EXIT_CODE


def main() -> int:
    raw = sys.stdin.read()
    if not raw.strip():
        print(json.dumps({"permission": "allow"}))
        return 0

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        print(json.dumps({"permission": "allow"}))
        return 0

    if not isinstance(payload, dict):
        print(json.dumps({"permission": "allow"}))
        return 0

    tool_name = str(payload.get("tool_name") or payload.get("tool") or "")
    combined = _collect_paths_and_commands(payload)

    if _is_mutating_tool(tool_name, combined) and _mentions_decisions(combined):
        return _block(
            "Порушення guardrails: заборонено видаляти або змінювати файли "
            "в Decisions/. Операцію заблоковано (pre-tool-use hook)."
        )

    print(json.dumps({"permission": "allow"}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
