"""
Codebase Genius - WORKING Python Version
No Jac syntax issues - runs immediately
"""

import os
import sys
import json

# Add current directory to path to import local modules
sys.path.insert(0, os.path.dirname(__file__))

try:
    from py_helpers.clone_repo import clone_repo, list_files, read_readme, summarize_readme
    from py_helpers.parse_code import scan_repo_for_python, build_call_graph
    from py_helpers.make_diagram import make_function_call_graph
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please make sure your py_helpers modules are available")
    sys.exit(1)


class CodebaseGenius:
    """Main orchestrator for codebase documentation generation"""
    
    def __init__(self, github_url, output_dir="./outputs"):
        self.github_url = github_url
        self.output_dir = output_dir
        self.repo_data = {}
    
    def run(self):
        """Main pipeline"""
        print(f"🚀 Starting Codebase Genius for: {self.github_url}")
        
        # Step 1: Clone repository
        if not self.clone_repository():
            return False
        
        # Step 2: Map file structure
        self.map_file_tree()
        
        # Step 3: Analyze README
        self.analyze_readme()
        
        # Step 4: Analyze code
        self.analyze_code()
        
        # Step 5: Generate documentation
        self.generate_documentation()
        
        print("✅ Complete!")
        return True
    
    def clone_repository(self):
        """Clone the repository"""
        print("📦 Cloning repository...")
        
        result = clone_repo(self.github_url)
        
        if not result.get("success"):
            print(f"❌ Clone failed: {result.get('error')}")
            return False
        
        self.repo_data['path'] = result['path']
        self.repo_data['name'] = result['name']
        print(f"✅ Cloned to: {result['path']}")
        return True
    
    def map_file_tree(self):
        """Create file tree structure"""
        print("📂 Mapping file structure...")
        
        tree = list_files(self.repo_data['path'])
        self.repo_data['file_tree'] = tree
        
        total_files = sum(len(item['files']) for item in tree)
        print(f"✅ Found {total_files} files")
    
    def analyze_readme(self):
        """Summarize README"""
        print("📖 Reading README...")
        
        readme_data = read_readme(self.repo_data['path'])
        
        if readme_data.get("success"):
            summary = summarize_readme(readme_data['content'])
            self.repo_data['readme_summary'] = summary
            print("✅ README summarized")
        else:
            self.repo_data['readme_summary'] = "No README found"
            print("⚠️  No README found")
    
    def analyze_code(self):
        """Parse code and build call graph"""
        print("🔍 Analyzing Python code...")
        
        # Parse all Python files
        parse_results = scan_repo_for_python(self.repo_data['path'])
        self.repo_data['parse_results'] = parse_results
        
        # Count totals
        total_funcs = 0
        total_classes = 0
        for file_data in parse_results.values():
            if file_data.get("success"):
                total_funcs += len(file_data.get("functions", []))
                total_classes += len(file_data.get("classes", []))
        
        # Build call graph
        call_graph = build_call_graph(parse_results)
        self.repo_data['call_graph'] = call_graph
        
        print(f"✅ Found {total_funcs} functions and {total_classes} classes")
        print(f"✅ Built call graph with {len(call_graph)} edges")
    
    def generate_documentation(self):
        """Generate markdown documentation"""
        print("📝 Generating documentation...")
        
        # Create output directory
        output_path = os.path.join(self.output_dir, self.repo_data['name'])
        os.makedirs(output_path, exist_ok=True)
        
        # Build markdown content
        markdown = self.build_markdown()
        
        # Generate diagram if call graph exists
        if self.repo_data.get('call_graph'):
            print("📊 Creating call graph diagram...")
            diagram_path = os.path.join(output_path, "call_graph")
            result = make_function_call_graph(
                self.repo_data['call_graph'],
                diagram_path,
                f"{self.repo_data['name']} - Function Calls"
            )
            if result.get("success"):
                print(f"✅ Diagram saved: {result['path']}")
        
        # Save markdown
        docs_path = os.path.join(output_path, "docs.md")
        with open(docs_path, "w", encoding="utf-8") as f:
            f.write(markdown)
        
        self.repo_data['docs_path'] = docs_path
        print(f"✅ Documentation generated: {docs_path}")
    
    def build_markdown(self):
        """Build the markdown content"""
        md = f"# {self.repo_data['name']} - Documentation\n\n"
        md += f"**Repository:** {self.github_url}\n\n"
        md += f"**Generated by:** Codebase Genius\n\n"
        md += "---\n\n"
        
        # Overview
        md += "## 📖 Overview\n\n"
        md += self.repo_data.get('readme_summary', 'No description') + "\n\n"
        
        # Statistics
        md += "## 📊 Repository Statistics\n\n"
        total_files = sum(len(item['files']) for item in self.repo_data.get('file_tree', []))
        md += f"- **Total Files:** {total_files}\n"
        
        total_funcs = 0
        total_classes = 0
        for file_data in self.repo_data.get('parse_results', {}).values():
            if file_data.get("success"):
                total_funcs += len(file_data.get("functions", []))
                total_classes += len(file_data.get("classes", []))
        
        md += f"- **Python Functions:** {total_funcs}\n"
        md += f"- **Python Classes:** {total_classes}\n"
        md += f"- **Call Relationships:** {len(self.repo_data.get('call_graph', []))}\n\n"
        
        # File Structure
        md += "## 📁 File Structure\n\n```\n"
        for item in self.repo_data.get('file_tree', [])[:10]:
            md += f"{item['path']}/\n"
            for f in item['files'][:5]:
                md += f"  ├── {f}\n"
        md += "```\n\n"
        
        # Code Structure
        md += "## 🔧 Code Structure\n\n"
        count = 0
        for file_path in sorted(self.repo_data.get('parse_results', {}).keys())[:10]:
            file_data = self.repo_data['parse_results'][file_path]
            if not file_data.get("success"):
                continue
            
            funcs = file_data.get("functions", [])
            classes = file_data.get("classes", [])
            
            if funcs or classes:
                md += f"### `{file_path}`\n\n"
                
                if classes:
                    md += "**Classes:**\n"
                    for cls in classes:
                        bases = ", ".join(cls["bases"]) if cls["bases"] else "object"
                        md += f"- `{cls['name']}({bases})`\n"
                    md += "\n"
                
                if funcs:
                    md += "**Functions:**\n"
                    for func in funcs[:5]:
                        args = ", ".join(func["args"])
                        md += f"- `{func['name']}({args})`\n"
                    md += "\n"
                
                count += 1
                if count >= 10:
                    break
        
        # Call Graph
        if self.repo_data.get('call_graph'):
            md += "## 🔗 Function Call Graph\n\n"
            md += "![Call Graph](call_graph.png)\n\n"
        
        return md


def main():
    """CLI interface"""
    if len(sys.argv) < 2:
        print("Usage: python main.py <github_url>")
        print("Example: python main.py https://github.com/psf/requests")
        sys.exit(1)
    
    github_url = sys.argv[1]
    genius = CodebaseGenius(github_url)
    
    if genius.run():
        print(f"\n📄 Documentation: {genius.repo_data['docs_path']}")
    else:
        print("\n❌ Failed to generate documentation")
        sys.exit(1)


if __name__ == "__main__":
    main()