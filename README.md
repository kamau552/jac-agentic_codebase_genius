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

cd BE

# Test cloning
python -m py_helpers.clone_repo

# Test parsing
python -m py_helpers.parse_code

# Test diagrams
python -m py_helpers.make_diagram
3. Run the Jac System


# Start Jac server
jac serve main.jac
4. Generate Documentation
Option A: Use the test walker (easiest)

jac run main.jac -w test_system
Option B: Use the API

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

🛠️ TODOs
✅ repo_mapper.jac: Create dedicated walker for file mapping

✅ code_analyzer.jac: Build CCG as Jac nodes/edges

✅ docgenie.jac: Separate documentation generation logic

✅ Jac parsing: Add Jac language support (currently Python only)

✅ LLM integration: Better README summarization

✅ Error handling: Graceful failures for private repos

🐛 Troubleshooting
"jac: command not found"


📚 Resources
Jac Language: Jac Documentation

Jac Tutorial: Beginner's Guide

## Task Manager Example: Agentic-AI

🎓 Assignment Deliverables Checklist
✅ All Jac files (main.jac, repo_mapper.jac, code_analyzer.jac, docgenie.jac)

✅ Python helpers (clone_repo.py, parse_code.py, make_diagram.py)

✅ requirements.txt with all dependencies

✅ This README.md with setup instructions

✅ Sample output (docs.md + diagrams) in outputs/

✅ Optional: Streamlit UI


📝 License
Educational project for assignment purposes.

Built using Jac Language
