"""
Streamlit UI for Codebase Genius
Simple interface to generate documentation from GitHub repos.
"""

import streamlit as st
import requests
import os
import json
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Codebase Genius",
    page_icon="🧠",
    layout="wide"
)

# Title and description
st.title("🧠 Codebase Genius")
st.markdown("""
Generate beautiful documentation for any GitHub repository automatically!

**How it works:**
1. Enter a public GitHub repository URL
2. Our AI agents analyze the code
3. Get markdown documentation with diagrams
""")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    jac_server_url = st.text_input(
        "Jac Server URL",
        value="http://127.0.0.1:8000",
        help="URL where your Jac server is running"
    )
    
    output_dir = st.text_input(
        "Output Directory",
        value="./outputs",
        help="Where to save generated documentation"
    )
    
    st.markdown("---")
    st.markdown("### 📊 Stats")
    
    # Count generated docs
    if os.path.exists(output_dir):
        repos = [d for d in os.listdir(output_dir) 
                if os.path.isdir(os.path.join(output_dir, d))]
        st.metric("Repos Documented", len(repos))
    else:
        st.metric("Repos Documented", 0)

# Main input area
st.header("🔗 Repository Input")

col1, col2 = st.columns([3, 1])

with col1:
    github_url = st.text_input(
        "GitHub Repository URL",
        placeholder="https://github.com/owner/repository",
        help="Enter a public GitHub repository URL"
    )

with col2:
    st.write("")  # Spacing
    st.write("")  # Spacing
    generate_button = st.button("🚀 Generate Docs", type="primary", use_container_width=True)

# Sample repos
with st.expander("📚 Try these sample repositories"):
    sample_repos = [
        ("Flask", "https://github.com/pallets/flask"),
        ("Requests", "https://github.com/psf/requests"),
        ("Rich", "https://github.com/Textualize/rich"),
        ("Click", "https://github.com/pallets/click"),
    ]
    
    cols = st.columns(len(sample_repos))
    for i, (name, url) in enumerate(sample_repos):
        with cols[i]:
            if st.button(name, key=f"sample_{i}", use_container_width=True):
                github_url = url
                st.rerun()

# Generation logic
if generate_button and github_url:
    # Validate URL
    if not github_url.startswith("https://github.com/"):
        st.error("❌ Please enter a valid GitHub URL starting with https://github.com/")
    else:
        # Extract repo name
        repo_name = github_url.rstrip("/").split("/")[-1]
        
        # Progress indicators
        progress_container = st.container()
        with progress_container:
            st.info(f"🔄 Processing repository: **{repo_name}**")
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Step 1: Call Jac server
            status_text.text("📡 Connecting to Jac server...")
            progress_bar.progress(20)
            
            try:
                # Make API call
                api_url = f"{jac_server_url}/walkers/serve_documentation"
                payload = {"github_url": github_url}
                
                status_text.text("🤖 Agents working on documentation...")
                progress_bar.progress(40)
                
                response = requests.post(
                    api_url,
                    json=payload,
                    timeout=300  # 5 minutes timeout
                )
                
                if response.status_code == 200:
                    progress_bar.progress(80)
                    status_text.text("📝 Finalizing documentation...")
                    
                    # Check if output exists
                    docs_path = os.path.join(output_dir, repo_name, "docs.md")
                    diagram_path = os.path.join(output_dir, repo_name, "call_graph.png")
                    
                    progress_bar.progress(100)
                    status_text.empty()
                    progress_bar.empty()
                    
                    st.success(f"✅ Documentation generated successfully!")
                    
                    # Display results
                    st.header("📄 Generated Documentation")
                    
                    # Show markdown
                    if os.path.exists(docs_path):
                        with open(docs_path, "r", encoding="utf-8") as f:
                            docs_content = f.read()
                        
                        # Tabs for different views
                        tab1, tab2, tab3 = st.tabs(["📖 Preview", "📝 Raw Markdown", "📊 Diagram"])
                        
                        with tab1:
                            st.markdown(docs_content)
                        
                        with tab2:
                            st.code(docs_content, language="markdown")
                        
                        with tab3:
                            if os.path.exists(diagram_path):
                                st.image(diagram_path, caption="Function Call Graph")
                            else:
                                st.info("No diagram generated")
                        
                        # Download button
                        st.download_button(
                            label="💾 Download Documentation",
                            data=docs_content,
                            file_name=f"{repo_name}_docs.md",
                            mime="text/markdown"
                        )
                    else:
                        st.warning(f"Documentation file not found at: {docs_path}")
                        st.info("The Jac server may have saved it to a different location. Check the server logs.")
                
                else:
                    progress_bar.empty()
                    status_text.empty()
                    st.error(f"❌ Server error: {response.status_code}")
                    st.code(response.text)
            
            except requests.exceptions.ConnectionError:
                progress_bar.empty()
                status_text.empty()
                st.error("❌ Cannot connect to Jac server!")
                st.markdown("""
                **Is your Jac server running?**
                
                Start it with:
                ```bash
                cd BE
                jac serve main.jac
                ```
                """)
            
            except requests.exceptions.Timeout:
                progress_bar.empty()
                status_text.empty()
                st.error("❌ Request timed out. The repository might be too large.")
            
            except Exception as e:
                progress_bar.empty()
                status_text.empty()
                st.error(f"❌ Unexpected error: {str(e)}")

# Previous generations
st.header("📚 Previously Generated")

if os.path.exists(output_dir):
    repos = [d for d in os.listdir(output_dir) 
            if os.path.isdir(os.path.join(output_dir, d))]
    
    if repos:
        cols = st.columns(3)
        for i, repo in enumerate(sorted(repos)):
            with cols[i % 3]:
                docs_path = os.path.join(output_dir, repo, "docs.md")
                if os.path.exists(docs_path):
                    if st.button(f"📖 {repo}", key=f"prev_{i}", use_container_width=True):
                        with open(docs_path, "r", encoding="utf-8") as f:
                            st.markdown(f.read())
    else:
        st.info("No documentation generated yet. Try generating one above!")
else:
    st.info("Output directory doesn't exist yet.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Built with ❤️ using <strong>Jac Language</strong></p>
    <p><small>Codebase Genius - AI-Powered Documentation Generator</small></p>
</div>
""", unsafe_allow_html=True)