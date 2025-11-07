"""
Generate diagrams from code relationships using Graphviz.
"""

import os
from graphviz import Digraph
from typing import List, Tuple, Dict


def make_function_call_graph(edges: List[Tuple[str, str]], 
                             output_path: str,
                             title: str = "Function Call Graph") -> dict:
    """
    Create a function call graph diagram.
    
    Args:
        edges: List of (caller, callee) tuples
        output_path: Path where to save the diagram (without extension)
        title: Graph title
    
    Returns:
        dict with 'path' to generated image or 'error'
    """
    try:
        # Create directed graph
        dot = Digraph(comment=title, format='png')
        dot.attr(rankdir='LR')  # Left to right layout
        dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightblue')
        
        # Add title
        dot.attr(label=title, fontsize='16', fontname='Arial Bold')
        
        # Collect all unique nodes
        nodes = set()
        for caller, callee in edges:
            nodes.add(caller)
            nodes.add(callee)
        
        # Add nodes
        for node in sorted(nodes):
            dot.node(node, node)
        
        # Add edges
        edge_counts = {}
        for caller, callee in edges:
            key = (caller, callee)
            edge_counts[key] = edge_counts.get(key, 0) + 1
        
        for (caller, callee), count in edge_counts.items():
            label = str(count) if count > 1 else ""
            dot.edge(caller, callee, label=label)
        
        # Render
        output_file = dot.render(output_path, cleanup=True)
        
        return {
            "success": True,
            "path": output_file,
            "nodes": len(nodes),
            "edges": len(edges)
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to create diagram: {str(e)}"
        }


def make_class_hierarchy(classes: List[Dict], 
                        output_path: str) -> dict:
    """
    Create a class inheritance diagram.
    
    Args:
        classes: List of class dicts with 'name' and 'bases'
        output_path: Path where to save the diagram (without extension)
    
    Returns:
        dict with 'path' to generated image or 'error'
    """
    try:
        dot = Digraph(comment="Class Hierarchy", format='png')
        dot.attr(rankdir='BT')  # Bottom to top (child -> parent)
        dot.attr('node', shape='box', style='filled', fillcolor='lightgreen')
        
        # Add title
        dot.attr(label="Class Inheritance Diagram", fontsize='16')
        
        # Add all classes as nodes
        for cls in classes:
            name = cls['name']
            methods = cls.get('methods', [])
            
            # Create label with methods
            if methods:
                label = f"{name}\\n---\\n" + "\\n".join(f"+ {m}()" for m in methods[:3])
                if len(methods) > 3:
                    label += f"\\n+ ... ({len(methods) - 3} more)"
            else:
                label = name
            
            dot.node(name, label)
        
        # Add inheritance edges
        for cls in classes:
            child = cls['name']
            for base in cls.get('bases', []):
                # Only add edge if parent class is in our diagram
                if any(c['name'] == base for c in classes):
                    dot.edge(child, base)
        
        # Render
        output_file = dot.render(output_path, cleanup=True)
        
        return {
            "success": True,
            "path": output_file,
            "classes": len(classes)
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to create class diagram: {str(e)}"
        }


def make_file_structure_diagram(file_tree: List[Dict], 
                               output_path: str,
                               max_depth: int = 3) -> dict:
    """
    Create a file/folder structure diagram.
    
    Args:
        file_tree: List of dicts with 'path', 'files', 'dirs'
        output_path: Path where to save diagram
        max_depth: Maximum depth to show
    
    Returns:
        dict with 'path' or 'error'
    """
    try:
        dot = Digraph(comment="File Structure", format='png')
        dot.attr(rankdir='LR')
        dot.attr('node', shape='folder', style='filled', fillcolor='wheat')
        
        dot.attr(label="Repository Structure", fontsize='16')
        
        # Add root
        dot.node("root", "Repository")
        
        # Track which nodes we've added
        added_nodes = {"root"}
        
        for item in file_tree:
            path = item['path']
            depth = path.count(os.sep) if path != "." else 0
            
            if depth > max_depth:
                continue
            
            # Create node ID from path
            node_id = path.replace(os.sep, "_").replace(".", "root")
            
            if node_id not in added_nodes:
                # Use just the folder name as label
                label = os.path.basename(path) if path != "." else "root"
                dot.node(node_id, label)
                added_nodes.add(node_id)
            
            # Connect to parent
            if path != ".":
                parent_path = os.path.dirname(path)
                parent_id = parent_path.replace(os.sep, "_").replace(".", "root")
                
                if parent_id in added_nodes:
                    dot.edge(parent_id, node_id)
            else:
                # Connect root
                dot.edge("root", node_id)
            
            # Add important files as leaves
            for file in item['files']:
                if file.endswith(('.py', '.jac', '.md', '.txt')):
                    file_id = f"{node_id}_{file.replace('.', '_')}"
                    dot.node(file_id, file, shape='note', fillcolor='lightyellow')
                    dot.edge(node_id, file_id)
        
        output_file = dot.render(output_path, cleanup=True)
        
        return {
            "success": True,
            "path": output_file
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to create structure diagram: {str(e)}"
        }


if __name__ == "__main__":
    # Test with sample data
    print("Testing diagram generation...")
    
    # Test call graph
    sample_edges = [
        ("main", "process_data"),
        ("main", "save_results"),
        ("process_data", "validate_input"),
        ("process_data", "transform_data"),
        ("save_results", "write_file")
    ]
    
    result = make_function_call_graph(sample_edges, "/tmp/test_call_graph", 
                                     "Sample Call Graph")
    if result.get("success"):
        print(f"✓ Call graph created: {result['path']}")
    else:
        print(f"✗ Error: {result.get('error')}")
    
    # Test class hierarchy
    sample_classes = [
        {"name": "Animal", "bases": [], "methods": ["eat", "sleep"]},
        {"name": "Dog", "bases": ["Animal"], "methods": ["bark", "fetch"]},
        {"name": "Cat", "bases": ["Animal"], "methods": ["meow", "purr"]}
    ]
    
    result = make_class_hierarchy(sample_classes, "/tmp/test_class_hierarchy")
    if result.get("success"):
        print(f"✓ Class diagram created: {result['path']}")
    else:
        print(f"✗ Error: {result.get('error')}")