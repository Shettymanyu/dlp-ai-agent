<!--
  Drop this file in: github.com/Shettymanyu/dlp-ai-agent/README.md
  Adjust any TODO markers (model name, exact run command, etc.) to match your actual code.
-->

<h1 align="center">DLP AI Agent</h1>

<p align="center">
  <em>A retrieval-augmented agent for Data Loss Prevention &mdash; scans content against a vector store of policy rules and flags sensitive material with reasoning.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square"/>
  <img src="https://img.shields.io/badge/ChromaDB-FF6F00?style=flat-square"/>
  <img src="https://img.shields.io/badge/RAG-0A0A0A?style=flat-square"/>
  <img src="https://img.shields.io/badge/Status-Active%20development-blue?style=flat-square"/>
</p>

---

## Why I built this

Traditional DLP tools rely on regex and keyword lists, which leak context. I wanted to see how far you can push **retrieval-augmented reasoning** instead: index policy documents, contract clauses, and PII definitions in a vector store, then have an LLM agent decide whether a given snippet violates them &mdash; and explain why.

## What it does

- **Ingests** policy documents and sensitive-data examples from `data/` into a Chroma vector store (`chroma_db/`)
- **Embeds and indexes** chunks so similar policy text is retrievable in milliseconds
- **Answers questions** like *"Does this email leak PII?"* by retrieving the most relevant policy passages and asking an LLM to classify with citations
- **CLI and app entrypoints** &mdash; `main.py` for batch runs, `app.py` for the interactive surface

## Architecture

```
                          +-------------------+
   policy docs  --------> | Loader / chunker  |
   (data/)                +---------+---------+
                                    |
                                    v
                          +-------------------+
                          | Embeddings model  |
                          +---------+---------+
                                    |
                                    v
                          +-------------------+
   user query  ---------> | Chroma retriever  |
                          +---------+---------+
                                    |
                                    v
                          +-------------------+
                          |   LLM reasoner    |  --->  verdict + citation
                          +-------------------+
```

## Tech stack

- **Python** for the agent and CLI
- **LangChain** style orchestration for retrieval + generation
- **ChromaDB** as the local vector store (`chroma_db/`)
- **OpenAI / compatible LLM** for the reasoning step <!-- TODO: confirm the exact provider you used -->
- `requirement.txt` pins dependencies

## Getting started

```bash
git clone https://github.com/Shettymanyu/dlp-ai-agent.git
cd dlp-ai-agent

python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate

pip install -r requirement.txt
```

Create a `.env` file in the project root with your API key:

```env
OPENAI_API_KEY=sk-...
# any other vars main.py / app.py expect
```

Run the agent:

```bash
# one-shot CLI
python main.py

# or the interactive app
python app.py
```

## Repo layout

```
.
|-- src/             Agent code (retrieval, prompting, classification)
|-- data/            Source policy docs / sample sensitive content
|-- chroma_db/       Persisted Chroma vector store
|-- app.py           Interactive entrypoint
|-- main.py          Batch / CLI entrypoint
|-- requirement.txt  Python dependencies
`-- .env             API keys (gitignored)
```

> Heads-up: there are a couple of stray placeholder files in the repo (`-r`, `26.0.1`, `[21`, `python`). They look like accidental commits from terminal copy-paste &mdash; safe to delete in a future cleanup.

## Roadmap

- [ ] Swap in an evaluation harness (precision / recall on a labeled set)
- [ ] Add a small web UI for ad-hoc document scanning
- [ ] Support pluggable LLM backends (Anthropic, local Llama)
- [ ] Streaming + redaction output mode for production use

## Author

Built by **Manyu Shetty** &mdash; <a href="https://github.com/Shettymanyu">@Shettymanyu</a> &middot; <a href="mailto:shettymanyu@gmail.com">shettymanyu@gmail.com</a>
