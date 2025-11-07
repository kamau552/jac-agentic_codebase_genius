"""
Parse Python source code to extract structure (functions, classes, calls).
Uses Python's built-in AST (Abstract Syntax Tree) module.
"""

import ast
import os
from pathlib import Path
from typing import Dict, List, Any


def parse_python_file(path: str) -> dict:
    """
    Parse a single Python file to extract its structure.
    
    Args:
        path: Path to Python file
    
    Returns:
        dict with functions, classes, calls, imports, or error
    """
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            source = f.read()
        
        tree = ast.parse(source, filename=path)
        
        functions = []
        classes = []
        calls = []
        imports = []
        
        # Walk the AST
        for node in ast.walk(tree):
            # Extract function definitions
            if isinstance(node, ast.FunctionDef):
                functions.append({
                    "name": node.name,
                    "lineno": node.lineno,
                    "args": [arg.arg for arg in node.args.args],
                    "decorators": [get_decorator_name(d) for d in node.decorator_list],
                    "returns": get_annotation_name(node.returns) if node.returns else None,
                    "docstring": ast.get_docstring(node)
                })
            
            # Extract class definitions
            elif isinstance(node, ast.ClassDef):
                # Get base class names
                bases = []
                for base in node.bases:
                    base_name = get_name_from_node(base)
                    if base_name:
                        bases.append(base_name)
                
                # Get methods
                methods = []
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        methods.append(item.name)
                
                classes.append({
                    "name": node.name,
                    "lineno": node.lineno,
                    "bases": bases,
                    "methods": methods,
                    "docstring": ast.get_docstring(node)
                })
            
            # Extract function calls
            elif isinstance(node, ast.Call):
                func_name = get_name_from_node(node.func)
                if func_name:
                    calls.append({
                        "func": func_name,
                        "lineno": node.lineno
                    })
            
            # Extract imports
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({
                        "module": alias.name,
                        "alias": alias.asname,
                        "lineno": node.lineno
                    })
            
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    imports.append({
                        "module": f"{module}.{alias.name}",
                        "alias": alias.asname,
                        "lineno": node.lineno
                    })
        
        return {
            "success": True,
            "functions": functions,
            "classes": classes,
            "calls": calls,
            "imports": imports
        }
    
    except SyntaxError as e:
        return {
            "success": False,
            "error": f"Syntax error: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Parse error: {str(e)}"
        }


def get_name_from_node(node) -> str:
    """Extract name from various AST node types."""
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Attribute):
        # Handle things like os.path.join
        value = get_name_from_node(node.value)
        return f"{value}.{node.attr}" if value else node.attr
    elif isinstance(node, ast.Call):
        return get_name_from_node(node.func)
    return ""


def get_decorator_name(node) -> str:
    """Extract decorator name."""
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Call):
        return get_name_from_node(node.func)
    return str(node)


def get_annotation_name(node) -> str:
    """Extract type annotation name."""
    return get_name_from_node(node)


def scan_repo_for_python(root: str) -> dict:
    """
    Scan entire repository for Python files and parse them.
    
    Args:
        root: Repository root directory
    
    Returns:
        dict mapping file paths to parse results
    """
    results = {}
    
    ignore_dirs = {".git", "node_modules", "__pycache__", 
                   "venv", ".venv", "dist", "build"}
    
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip ignored directories
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs]
        
        for filename in filenames:
            if filename.endswith(".py"):
                full_path = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(full_path, root)
                
                parse_result = parse_python_file(full_path)
                results[rel_path] = parse_result
    
    return results


def build_call_graph(parse_results: dict) -> list:
    """
    Build a call graph from parse results.
    
    Args:
        parse_results: Output from scan_repo_for_python
    
    Returns:
        List of (caller, callee) tuples
    """
    edges = []
    
    # Create a mapping of function names to files
    function_locations = {}
    for file_path, data in parse_results.items():
        if data.get("success"):
            for func in data.get("functions", []):
                func_name = func["name"]
                function_locations[func_name] = file_path
    
    # Build edges based on calls
    for file_path, data in parse_results.items():
        if not data.get("success"):
            continue
        
        # For each function in this file
        for func in data.get("functions", []):
            caller = func["name"]
            
            # Check all calls in the file
            for call in data.get("calls", []):
                callee = call["func"]
                
                # Only add edge if both functions exist in our codebase
                if caller and callee in function_locations:
                    edges.append((caller, callee))
    
    return edges


if __name__ == "__main__":
    # Test on this file itself
    print("Testing parse_python_file on this file...")
    result = parse_python_file(__file__)
    
    if result.get("success"):
        print(f"✓ Functions: {[f['name'] for f in result['functions']]}")
        print(f"✓ Classes: {[c['name'] for c in result['classes']]}")
        print(f"✓ Imports: {len(result['imports'])} imports found")
    else:
        print(f"✗ Error: {result.get('error')}")