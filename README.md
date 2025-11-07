Codebase Genius 🚀
An AI-powered, multi-agent system that automatically generates high-quality documentation for any software repository.
📋 What This Does

Accepts a GitHub repository URL
Clones the repository
Maps the file structure and reads README
Analyzes Python code (functions, classes, relationships)
Generates markdown documentation with diagrams

🏗️ Architecture
Multi-Agent System (Jac Walkers)

CodebaseGenius (Supervisor): Orchestrates the entire pipeline
Repo Mapper: Clones repo, lists files, summarizes README
Code Analyzer: Parses Python files, builds Code Context Graph (CCG)
DocGenie: Generates final markdown documentation

Technology Stack

Jac Language: Multi-agent orchestration
Python: Helper modules for git, parsing, diagrams
Graphviz: Diagram generation
GitPython: Repository cloning
AST: Python code parsing

🚀 Quick Start
1. Setup Environment
bash# Navigate to project directory
cd ~/projects/agentic_codebase_genius

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r BE/requirements.txt
2. Test Python Helpers (Optional)
bashcd BE

# Test cloning
python -m py_helpers.clone_repo

# Test parsing
python -m py_helpers.parse_code

# Test diagrams
python -m py_helpers.make_diagram
3. Run the Jac System
bash# From BE/ directory
cd BE

# Start Jac server
jac serve main.jac
4. Generate Documentation
Option A: Use the test walker (easiest)
bash# In another terminal (while server is running)
cd BE
jac run main.jac -w test_system
Option B: Use the API
bashcurl -X POST http://127.0.0.1:8000/walkers/serve_documentation \
  -H "Content-Type: application/json" \
  -d '{"github_url": "https://github.com/psf/requests"}'
Option C: Use Streamlit UI (if you build it)
bashcd FE
streamlit run streamlit_app.py
📂 Project Structure
agentic_codebase_genius/
├── BE/                          # Backend Jac code
│   ├── main.jac                 # Main orchestrator
│   ├── repo_mapper.jac          # File mapping agent
│   ├── code_analyzer.jac        # Code analysis agent
│   ├── docgenie.jac             # Documentation generator
│   ├── py_helpers/              # Python helper modules
│   │   ├── clone_repo.py        # Git operations
│   │   ├── parse_code.py        # AST parsing
│   │   └── make_diagram.py      # Graphviz diagrams
│   └── requirements.txt
├── FE/                          # Frontend (optional)
│   └── streamlit_app.py
├── outputs/                     # Generated documentation
│   └── <repo_name>/
│       ├── docs.md              # Main documentation
│       └── call_graph.png       # Call graph diagram
└── README.md
📖 Understanding the Jac Code
Key Concepts
1. Nodes - Data containers in a graph
jacnode Repository {
    has url: str;
    has path: str;
}
2. Walkers - Agents that traverse and act
jacwalker CodebaseGenius {
    can start_documentation with `root entry {
        # Your code here
    }
}
3. Python Integration
jacimport:py from py_helpers.clone_repo {clone_repo}
4. Spawning Nodes
jacrepo_node = Repository(url="...") spawn root;
5. Visiting Nodes
jacvisit repo_node;  # Walker moves to this node
🧪 Testing
Test with a Small Repo
bash# Use the built-in test walker
jac run main.jac -w test_system
Check Outputs
bash# View generated documentation
cat outputs/<repo-name>/docs.md

# View diagram (if xdg-open available in WSL)
xdg-open outputs/<repo-name>/call_graph.png
📊 Example Output
The system generates:

docs.md with:

Repository overview
Statistics (files, functions, classes)
File structure tree
Code structure (functions & classes per file)
Call graph diagram


call_graph.png:

Visual representation of function relationships



🎯 Learning Path
Phase 1: Understand the Starter (You Are Here!)

✅ Setup environment
✅ Run Python helpers standalone
✅ Run the Jac server
✅ Generate docs for a sample repo

Phase 2: Customize & Extend

Add support for Jac language parsing
Improve README summarization with LLMs
Add more diagram types
Build Streamlit UI

Phase 3: Advanced Features

Support for JavaScript/TypeScript
Cyclomatic complexity analysis
Interactive diagrams
API documentation extraction

🛠️ TODOs for You

repo_mapper.jac: Create dedicated walker for file mapping
code_analyzer.jac: Build CCG as Jac nodes/edges
docgenie.jac: Separate documentation generation logic
Jac parsing: Add Jac language support (currently Python only)
LLM integration: Better README summarization
Error handling: Graceful failures for private repos

🐛 Troubleshooting
"jac: command not found"
bashpip install jaclang
# or
pip install --upgrade jaclang
"No module named 'git'"
bashpip install gitpython
"Graphviz executables not found"
bash# Ubuntu/Debian (WSL)
sudo apt-get install graphviz

# macOS
brew install graphviz
WSL Specific Issues
bash# If you can't see images, copy to Windows filesystem
cp outputs/*/call_graph.png /mnt/c/Users/<YourName>/Desktop/
📚 Resources

Jac Language: Jac Documentation
Jac Tutorial: Beginner's Guide
Task Manager Example: Agentic-AI

🎓 Assignment Deliverables Checklist

 All Jac files (main, repo_mapper, code_analyzer, docgenie)
 Python helpers (clone, parse, diagram)
 Requirements.txt with all dependencies
 This README with setup instructions
 Sample output (docs.md + diagrams) in outputs/
 Optional: Streamlit UI
 Optional: Report on design decisions

📝 License
Educational project for assignment purposes.

Built with ❤️ using Jac Language