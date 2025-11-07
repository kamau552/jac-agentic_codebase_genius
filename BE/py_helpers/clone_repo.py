"""
Clone and explore GitHub repositories.
This module handles downloading repos and listing their files.
"""

import os
import shutil
import tempfile
from pathlib import Path
from git import Repo
from git.exc import GitCommandError


def clone_repo(url: str, dest_base: str = None) -> dict:
    """
    Clone a GitHub repository to a temporary or specified directory.
    
    Args:
        url: GitHub repository URL
        dest_base: Optional destination directory (creates temp if None)
    
    Returns:
        dict with 'path' (str) and 'name' (str) or 'error' (str)
    """
    try:
        # Create destination
        if dest_base is None:
            dest_base = tempfile.mkdtemp(prefix="cbg_")
        
        # Extract repo name from URL
        repo_name = url.rstrip("/").split("/")[-1].replace(".git", "")
        dest = os.path.join(dest_base, repo_name)
        
        # Remove if exists
        if os.path.exists(dest):
            shutil.rmtree(dest)
        
        # Clone with depth=1 for speed
        print(f"Cloning {url} to {dest}...")
        Repo.clone_from(url, dest, depth=1)
        
        return {
            "path": dest,
            "name": repo_name,
            "success": True
        }
    
    except GitCommandError as e:
        return {
            "error": f"Git clone failed: {str(e)}",
            "success": False
        }
    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}",
            "success": False
        }


def list_files(root: str, ignore_dirs=None) -> list:
    """
    Create a file tree structure, ignoring common non-source directories.
    
    Args:
        root: Root directory path
        ignore_dirs: Set of directory names to skip
    
    Returns:
        List of dicts with path, files, and dirs info
    """
    if ignore_dirs is None:
        ignore_dirs = {".git", "node_modules", "__pycache__", 
                      "venv", ".venv", "dist", "build", ".pytest_cache"}
    
    tree = []
    
    for dirpath, dirnames, filenames in os.walk(root):
        # Filter out ignored directories IN PLACE (modifies the walk)
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs]
        
        # Get relative path
        rel = os.path.relpath(dirpath, root)
        
        tree.append({
            "path": rel if rel != "." else ".",
            "files": sorted(filenames),
            "dirs": sorted(dirnames)
        })
    
    return tree


def find_readme(root: str) -> str:
    """
    Find README file in repository root.
    
    Args:
        root: Repository root directory
    
    Returns:
        Path to README file or empty string if not found
    """
    readme_names = ["README.md", "README.MD", "readme.md", 
                   "README.txt", "README.rst", "README"]
    
    for name in readme_names:
        path = os.path.join(root, name)
        if os.path.exists(path):
            return path
    
    return ""


def read_readme(root: str) -> dict:
    """
    Read and return README content.
    
    Args:
        root: Repository root directory
    
    Returns:
        dict with 'content' (str) and 'path' (str) or 'error'
    """
    readme_path = find_readme(root)
    
    if not readme_path:
        return {"error": "No README found"}
    
    try:
        with open(readme_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        
        return {
            "content": content,
            "path": readme_path,
            "success": True
        }
    except Exception as e:
        return {"error": f"Failed to read README: {str(e)}"}


# Simple README summarizer (no LLM needed for starter)
def summarize_readme(content: str, max_chars: int = 600) -> str:
    """
    Create a simple summary of README content.
    
    Args:
        content: Full README text
        max_chars: Maximum characters for summary
    
    Returns:
        Summary string
    """
    # Get first few lines
    lines = content.split("\n")
    
    # Find title (usually first non-empty line with # or capital letters)
    title = ""
    for line in lines[:5]:
        clean = line.strip()
        if clean and (clean.startswith("#") or clean[0].isupper()):
            title = clean.replace("#", "").strip()
            break
    
    # Get first paragraph of content
    summary_lines = []
    for line in lines:
        clean = line.strip()
        if clean and not clean.startswith("#"):
            summary_lines.append(clean)
            if len(" ".join(summary_lines)) > max_chars:
                break
    
    summary = " ".join(summary_lines)[:max_chars]
    
    if title:
        return f"{title}\n\n{summary}..."
    return summary + "..."


if __name__ == "__main__":
    # Test the functions
    test_url = "https://github.com/jaseci-labs/jaclang-sample"
    
    print("Testing clone_repo...")
    result = clone_repo(test_url)
    
    if result.get("success"):
        print(f"✓ Cloned to: {result['path']}")
        
        print("\nTesting list_files...")
        tree = list_files(result['path'])
        print(f"✓ Found {len(tree)} directories")
        
        print("\nTesting read_readme...")
        readme = read_readme(result['path'])
        if readme.get("success"):
            print(f"✓ README found: {len(readme['content'])} characters")
            
            print("\nTesting summarize_readme...")
            summary = summarize_readme(readme['content'])
            print(f"✓ Summary:\n{summary}")
    else:
        print(f"✗ Error: {result.get('error')}")