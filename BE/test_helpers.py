#!/usr/bin/env python3
"""
Quick test script to verify all Python helpers work correctly.
Run this before testing the Jac system.

Usage:
    python test_helpers.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from py_helpers.clone_repo import clone_repo, list_files, read_readme, summarize_readme
from py_helpers.parse_code import parse_python_file, scan_repo_for_python, build_call_graph
from py_helpers.make_diagram import make_function_call_graph, make_class_hierarchy


def test_clone_and_map():
    """Test cloning and file mapping."""
    print("\n" + "="*60)
    print("TEST 1: Clone Repository & Map Files")
    print("="*60)
    
    # Use a small test repo
    test_url = "https://github.com/pallets/click"
    
    print(f"\n📦 Cloning {test_url}...")
    result = clone_repo(test_url)
    
    if not result.get("success"):
        print(f"❌ FAILED: {result.get('error')}")
        return None
    
    print(f"✅ SUCCESS: Cloned to {result['path']}")
    repo_path = result['path']
    
    print(f"\n📂 Listing files...")
    tree = list_files(repo_path)
    print(f"✅ SUCCESS: Found {len(tree)} directories")
    
    # Show first few
    print("\nFirst 5 directories:")
    for item in tree[:5]:
        print(f"  {item['path']}: {len(item['files'])} files")
    
    print(f"\n📖 Reading README...")
    readme = read_readme(repo_path)
    
    if readme.get("success"):
        print(f"✅ SUCCESS: README found ({len(readme['content'])} chars)")
        
        print(f"\n📝 Summarizing README...")
        summary = summarize_readme(readme['content'])
        print(f"✅ SUCCESS: Summary created")
        print(f"\nSummary:\n{summary[:200]}...")
    else:
        print(f"⚠️  WARNING: {readme.get('error')}")
    
    return repo_path


def test_parse_code(repo_path):
    """Test code parsing."""
    print("\n" + "="*60)
    print("TEST 2: Parse Python Code")
    print("="*60)
    
    if not repo_path:
        print("⏭️  SKIPPED: No repo to parse")
        return None
    
    print(f"\n🔍 Scanning for Python files...")
    parse_results = scan_repo_for_python(repo_path)
    print(f"✅ SUCCESS: Parsed {len(parse_results)} Python files")
    
    # Count totals
    total_funcs = 0
    total_classes = 0
    success_count = 0
    error_count = 0
    
    for file_path, data in parse_results.items():
        if data.get("success"):
            success_count += 1
            total_funcs += len(data.get("functions", []))
            total_classes += len(data.get("classes", []))
        else:
            error_count += 1
    
    print(f"\n📊 Results:")
    print(f"  - Successfully parsed: {success_count} files")
    print(f"  - Parse errors: {error_count} files")
    print(f"  - Total functions: {total_funcs}")
    print(f"  - Total classes: {total_classes}")
    
    # Show sample
    print(f"\n📄 Sample file (first one):")
    for file_path, data in list(parse_results.items())[:1]:
        print(f"  File: {file_path}")
        if data.get("success"):
            funcs = data.get("functions", [])
            classes = data.get("classes", [])
            print(f"  Functions: {[f['name'] for f in funcs[:5]]}")
            print(f"  Classes: {[c['name'] for c in classes[:5]]}")
    
    print(f"\n🔗 Building call graph...")
    call_graph = build_call_graph(parse_results)
    print(f"✅ SUCCESS: Built call graph with {len(call_graph)} edges")
    
    if call_graph:
        print(f"\nSample edges:")
        for caller, callee in call_graph[:5]:
            print(f"  {caller} → {callee}")
    
    return parse_results, call_graph


def test_diagrams(parse_results, call_graph):
    """Test diagram generation."""
    print("\n" + "="*60)
    print("TEST 3: Generate Diagrams")
    print("="*60)
    
    if not call_graph:
        print("⏭️  SKIPPED: No call graph to visualize")
        return
    
    print(f"\n📊 Creating function call graph...")
    result = make_function_call_graph(
        call_graph[:20],  # Limit to first 20 edges
        "/tmp/test_call_graph",
        "Test Call Graph"
    )
    
    if result.get("success"):
        print(f"✅ SUCCESS: Diagram saved to {result['path']}")
        print(f"  - Nodes: {result['nodes']}")
        print(f"  - Edges: {result['edges']}")
    else:
        print(f"❌ FAILED: {result.get('error')}")
    
    # Test class hierarchy
    if parse_results:
        print(f"\n📊 Creating class hierarchy diagram...")
        
        # Collect all classes
        all_classes = []
        for data in parse_results.values():
            if data.get("success"):
                all_classes.extend(data.get("classes", []))
        
        if all_classes:
            result = make_class_hierarchy(
                all_classes[:10],  # Limit to first 10 classes
                "/tmp/test_class_hierarchy"
            )
            
            if result.get("success"):
                print(f"✅ SUCCESS: Diagram saved to {result['path']}")
            else:
                print(f"❌ FAILED: {result.get('error')}")
        else:
            print("⏭️  SKIPPED: No classes found")


def main():
    """Run all tests."""
    print("\n" + "🧪"*30)
    print("CODEBASE GENIUS - Python Helpers Test Suite")
    print("🧪"*30)
    
    try:
        # Test 1: Clone and map
        repo_path = test_clone_and_map()
        
        # Test 2: Parse code
        parse_results, call_graph = test_parse_code(repo_path)
        
        # Test 3: Generate diagrams
        test_diagrams(parse_results, call_graph)
        
        print("\n" + "="*60)
        print("✅ ALL TESTS COMPLETED!")
        print("="*60)
        print("\nYou're ready to run the Jac system!")
        print("Next steps:")
        print("  1. cd BE")
        print("  2. jac serve main.jac")
        print("  3. In another terminal: jac run main.jac -w test_system")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ UNEXPECTED ERROR: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()