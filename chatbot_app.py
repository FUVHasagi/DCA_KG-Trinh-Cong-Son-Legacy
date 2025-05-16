"""
Streamlit GraphRAG Chatbot (Local‑only Skeleton)
================================================
A minimal Streamlit UI that chats with your **GraphRAG** pipeline and renders answers in full Markdown.
Conversation histories are stored as JSON files under *chat_history/*.  

Run locally:
```
streamlit run chatbot_app.py
```
(First time may take a moment while GraphRAG loads.)
"""

from __future__ import annotations

import json
import os
import sys
import importlib.util
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import streamlit as st

# -----------------------------------------------------------------------------
# 🔧 Configuration — edit these paths to fit your project folder structure
# -----------------------------------------------------------------------------
WORKING_DIR = "./KGs/all_song_version1"          # location of your NetworkX graphs
CRED_FILE   = "./creds.py"                 # must expose OPAI_api = "<key>"
CHAT_FOLDER = Path("chat_history")               # where JSON logs live

# -----------------------------------------------------------------------------
# 🗝️  Load OpenAI key at runtime (local‑only, never sent to Streamlit Cloud)
# -----------------------------------------------------------------------------

def _load_api_key(path: str) -> None:
    spec = importlib.util.spec_from_file_location("OPAI_api", path)
    if spec is None or spec.loader is None:
        raise FileNotFoundError(f"Cannot locate creds file: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["OPAI_api"] = module  # so `import OPAI_api` works elsewhere
    spec.loader.exec_module(module)    # type: ignore[attr-defined]
    os.environ["OPENAI_API_KEY"] = module.OPAI_api  # pyright: ignore


# -----------------------------------------------------------------------------
# 🧠  Lazy‑load GraphRAG + QueryParam (cached so it only builds once per run)
# -----------------------------------------------------------------------------

@st.cache_resource(show_spinner="Loading GraphRAG …")
def _init_graphrag():
    """Return a cached GraphRAG instance and default query param."""
    sys.path.append("./nano-graphrag")
    from nano_graphrag import GraphRAG, QueryParam  # local import after sys.path tweak

    gr = GraphRAG(working_dir=WORKING_DIR)
    qp = QueryParam(mode="local")  # local vector search only; switch if needed
    return gr, qp


# -----------------------------------------------------------------------------
# 💬  Chat helpers: save / load history as JSON  -------------------------------
# -----------------------------------------------------------------------------

CHAT_FOLDER.mkdir(exist_ok=True)


def _save_history(messages: List[Dict[str, str]]) -> None:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    file = CHAT_FOLDER / f"chat_{ts}.json"
    file.write_text(json.dumps(messages, ensure_ascii=False, indent=2))


def _list_histories() -> List[Path]:
    return sorted(CHAT_FOLDER.glob("chat_*.json"), reverse=True)


def _load_history(path: Path) -> List[Dict[str, str]]:
    try:
        return json.loads(path.read_text())
    except Exception:
        st.sidebar.error("Failed to load chat log.")
        return []


# -----------------------------------------------------------------------------
# 🤖  Core response generator  --------------------------------------------------
# -----------------------------------------------------------------------------

def _generate_response(prompt: str) -> str:
    graphrag, qparam = _init_graphrag()
    return graphrag.query(prompt, qparam)


# -----------------------------------------------------------------------------
# 🖼️  Streamlit Page Setup  -----------------------------------------------------
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="GraphRAG Chatbot (Local)", page_icon="💬", layout="centered"
)

st.title("💬  GraphRAG Chatbot")

# one‑time key load (safe because local)
try:
    _load_api_key(CRED_FILE)
except FileNotFoundError as e:
    st.warning(f"API key file not found: {e}")

# Session state bootstrap
if "messages" not in st.session_state:
    st.session_state.messages: List[Dict[str, str]] = []

# -----------------------------------------------------------------------------
# 📁 Sidebar — history load/save  ----------------------------------------------
# -----------------------------------------------------------------------------

with st.sidebar:
    st.header("📂 Chat History")

    # Save current conversation
    if st.button("💾 Save current chat", use_container_width=True):
        _save_history(st.session_state.messages)
        st.success("Chat saved.")

    # Load a previous conversation
    history_files = _list_histories()
    if history_files:
        choices = ["🆕  New chat"] + [p.name for p in history_files]
        selection = st.selectbox("Load previous:", choices, index=0)
        if selection != choices[0]:
            st.session_state.messages = _load_history(CHAT_FOLDER / selection)
            st.experimental_rerun()
    else:
        st.caption("No saved chats yet.")

# -----------------------------------------------------------------------------
# 📝  Show existing messages (Markdown rendered)  ------------------------------
# -----------------------------------------------------------------------------

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"], unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# ⌨️  Chat input & response loop  ----------------------------------------------
# -----------------------------------------------------------------------------

prompt = st.chat_input("Ask me anything about Trịnh Công Sơn …")
if prompt:
    # Echo user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant reply
    with st.chat_message("assistant"):
        with st.spinner("Thinking …"):
            reply = _generate_response(prompt)
            st.markdown(reply, unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": reply})