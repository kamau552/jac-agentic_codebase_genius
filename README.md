# Codebase Genius 🚀

An AI-powered, multi-agent system that automatically generates high-quality documentation for any software repository.

---

## 📋 What This Does

- Accepts a GitHub repository URL
- Clones the repository
- Maps the file structure and reads README
- Analyzes Python code (functions, classes, relationships)
- Generates markdown documentation with diagrams

---

## 🏗️ Architecture

**Multi-Agent System (Jac Walkers)**

- **CodebaseGenius (Supervisor):** Orchestrates the entire pipeline  
- **Repo Mapper:** Clones repo, lists files, summarizes README  
- **Code Analyzer:** Parses Python files, builds Code Context Graph (CCG)  
- **DocGenie:** Generates final markdown documentation  

---

## 🛠️ Technology Stack

- **Jac Language:** Multi-agent orchestration  
- **Python:** Helper modules for git, parsing, diagrams  
- **Graphviz:** Diagram generation  
- **GitPython:** Repository cloning  
- **AST:** Python code parsing  

---

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Navigate to project directory
cd ~/projects/agentic_codebase_genius

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r BE/requirements.txt
2. Test Python Helpers (Optional)
bash
Copy code
cd BE

# Test cloning
python -m py_helpers.clone_repo

# Test parsing
python -m py_helpers.parse_code

# Test diagrams
python -m py_helpers.make_diagram
3. Run the Jac System
bash
Copy code
cd BE

# Start Jac server
jac serve main.jac
4. Generate Documentation
Option A: Use the test walker (easiest)

bash
Copy code
cd BE
jac run main.jac -w test_system
Option B: Use the API

bash
Copy code
curl -X POST http://127.0.0.1:8000/walkers/serve_documentation \
  -H "Content-Type: application/json" \
  -d '{"github_url": "https://github.com/psf/requests"}'
Option C: Use Streamlit UI (if you build it)

bash
Copy code
cd FE
streamlit run streamlit_app.py
📂 Project Structure
bash
Copy code
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
│   ├── requirements.txt
│   └── .gitignore               # Git ignore file
├── FE/                          # Frontend (optional)
│   └── streamlit_app.py
├── outputs/                     # Generated documentation
│   └── <repo_name>/
│       ├── docs.md              # Main documentation
│       └── call_graph.png       # Call graph diagram
└── README.md
.gitignore
gitignore
Copy code
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
venv/
env/
*.env

# Jac Language / BE outputs
*.jac~
outputs/
*.log

# IDE / Editor
.vscode/
.idea/
*.swp
*.swo

# System files
.DS_Store
Thumbs.db

# Streamlit / Frontend
.streamlit/
node_modules/
*.html
*.js.map

# Misc
*.bak
*.tmp
📖 Understanding the Jac Code
Key Concepts
Nodes - Data containers in a graph

jac
Copy code
jacnode Repository {
    has url: str;
    has path: str;
}
Walkers - Agents that traverse and act

jac
Copy code
jacwalker CodebaseGenius {
    can start_documentation with `root entry {
        # Your code here
    }
}
Python Integration

jac
Copy code
jacimport:py from py_helpers.clone_repo {clone_repo}
Spawning Nodes

jac
Copy code
jacrepo_node = Repository(url="...") spawn root;
Visiting Nodes

jac
Copy code
jacvisit repo_node;  # Walker moves to this node
🧪 Testing
Test with a Small Repo

bash
Copy code
# Use the built-in test walker
jac run main.jac -w test_system
Check Outputs

bash
Copy code
# View generated documentation
cat outputs/<repo-name>/docs.md

# View diagram (if xdg-open available in WSL)
xdg-open outputs/<repo-name>/call_graph.png
📊 Example Output
docs.md includes:

Repository overview

Statistics (files, functions, classes)

File structure tree

Code structure (functions & classes per file)

Call graph diagram

call_graph.png: Visual representation of function relationships

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

bash
Copy code
pip install jaclang
# or
pip install --upgrade jaclang
"No module named 'git'"

bash
Copy code
pip install gitpython
"Graphviz executables not found"

bash
Copy code
# Ubuntu/Debian (WSL)
sudo apt-get install graphviz

# macOS
brew install graphviz
WSL Specific Issues

bash
Copy code
# If you can't see images, copy to Windows filesystem
cp outputs/*/call_graph.png /mnt/c/Users/<YourName>/Desktop/
📚 Resources
Jac Language: Jac Documentation

Jac Tutorial: Beginner's Guide

Task Manager Example: Agentic-AI

🎓 Assignment Deliverables Checklist
All Jac files (main.jac, repo_mapper.jac, code_analyzer.jac, docgenie.jac)

Python helpers (clone_repo.py, parse_code.py, make_diagram.py)

requirements.txt with all dependencies

This README.md with setup instructions

Sample output (docs.md + diagrams) in outputs/

Optional: Streamlit UI

Optional: Report on design decisions

📝 License
Educational project for assignment purposes.

Built using Jac Language
