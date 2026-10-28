import os
import datetime
from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ObsidianVaultConnector")
VAULT_PATH = os.path.abspath(r"C:\Users\luciv\obsidian-vaults\Практична робота №2")

@mcp.tool()
def ingest_note(title: str, category: str, content: str, tags: list[str] = None) -> str:
    category_folder = Path(VAULT_PATH) / category
    category_folder.mkdir(parents=True, exist_ok=True)
    
    file_path = category_folder / f"{title}.md"
    today = datetime.date.today().isoformat()
    tags_str = ", ".join(tags) if tags else category.lower()

    frontmatter = f"""---
type: {category.lower()}
created: {today}
tags: [{tags_str}]
---

# {title}

{content}
"""

    if file_path.exists():
        if file_path.read_text(encoding="utf-8").strip() == frontmatter.strip():
            return f"Нотатка '{title}' вже існує і зміст не змінився."

    file_path.write_text(frontmatter, encoding="utf-8")
    return f"Нотатку '{title}' успішно збережено у папку {category}/ у Vault!"

@mcp.tool()
def get_note(title: str) -> str:
    vault = Path(VAULT_PATH)
    matching_files = list(vault.rglob(f"{title}.md"))
    if not matching_files:
        return f"Нотатку з назвою '{title}' не знайдено у Vault."
    return matching_files[0].read_text(encoding="utf-8")

if __name__ == "__main__":
    mcp.run()