<div align="center">
  <img src="assets/logo.png" alt="BrAIn logo" width="130" />
  <h1>BrAIn</h1>
  <p><strong>A fully local, private RAG assistant that lets you ask questions across your own documents — with nothing ever leaving your machine.</strong></p>
</div>

---

Professionals who handle confidential material — lawyers, accountants, clinics, consultants — can't paste their documents into cloud AI tools without breaking client confidentiality or data-protection rules. **BrAIn** solves this: it runs entirely on the user's own computer, indexes their documents, and answers natural-language questions about them with verifiable source citations — no cloud, no external APIs, no data leaving the device.

<div align="center">
  <img src="assets/01-chat.png" alt="Chat with cited answers" width="49%" />
  <img src="assets/02-graph.png" alt="Interactive 3D document graph" width="49%" />
  <img src="assets/03-archive.png" alt="Document archive and source viewer" width="49%" />
  <img src="assets/04-privacy.png" alt="Privacy-first controls" width="49%" />
</div>

## Architecture

```mermaid
flowchart LR
    Docs["Your documents<br/>PDF · DOCX · MD · TXT · EML · images"] --> Ingest["Ingestion pipeline"]
    Ingest --> Index[("Search index<br/>semantic + keyword")]

    User(["User"]) <--> UI["Local web app"]
    UI <--> Core["Application core"]
    Core -->|retrieve| Index
    Core -->|generate| LLM["Local language model"]
    LLM -->|answer + citations| UI

    Agents(["External AI agents"]) <--> MCP["MCP interface"]
    MCP <--> Core

    classDef store fill:#1e2230,stroke:#7c6cf5,color:#e8eaf0;
    classDef box fill:#171a23,stroke:#2a2f40,color:#e8eaf0;
    class Docs,Ingest,UI,Core,LLM,MCP box;
    class Index store;
```

*Everything inside the diagram runs on the user's machine. The MCP interface lets external AI agents query the archive, receiving only the relevant passages for a given question.*

## Tech stack

**Backend:** Python · FastAPI · Uvicorn
**Retrieval & AI:** ChromaDB · SQLite FTS5 · sentence-transformers (multilingual-e5) · cross-encoder reranking · Ollama
**Document processing:** PyMuPDF · python-docx · RapidOCR · Tesseract
**Frontend:** vanilla JavaScript · HTML5 Canvas · Mermaid
**Integration:** Model Context Protocol (MCP)

## Key features

- **Ask questions across your own documents** — PDF, DOCX, Markdown, TXT, EML, and images.
- **100% local and private** — no cloud, no external APIs; fully offline after the initial model download.
- **Verifiable answers** — every response cites its sources (file and page), so nothing is taken on trust.
- **Hybrid search** — combines semantic understanding with exact keyword matching for names, codes, and acronyms.
- **Incremental indexing** — only new or changed files are re-processed, never the whole corpus.
- **Built-in OCR** — reads scanned PDFs and pasted screenshots locally.
- **Interactive 3D document graph** — an explorable map of the archive where links represent semantic similarity.
- **Persistent chat history** with an editable prompt and an archive/source viewer.
- **Hardware-adaptive** — automatically tunes itself to the machine's available RAM and GPU.
- **Optional MCP server** — lets external AI assistants query the private archive as a tool.
- **Optional web search** — off by default, behind an explicit privacy warning.

## Why it's technically interesting

- **Reliable retrieval with small local models.** Consumer hardware can only run modest language models, which are easily distracted. A large part of the design went into a retrieval layer that surfaces the right context and a relevance gate that makes the system say *"I didn't find anything"* instead of inventing an answer on empty context.
- **Hybrid retrieval with a contrast-based relevance gate.** Semantic vectors and keyword search are fused so that both paraphrases and exact terms are matched, with a threshold that distinguishes a genuine match from "the least-bad of irrelevant results."
- **Memory kept under control on ordinary machines.** Streaming ingestion, lazy model loading, batched embeddings and on-disk indexes let the system run on everyday laptops without exhausting RAM.
- **Hardware-adaptive configuration.** The same build detects the machine it runs on and selects models, batch sizes and options accordingly — no manual tuning when moving to a different computer.
- **Real-time 3D visualization from embeddings.** The document graph is a custom physics-and-projection renderer built directly on the canvas, with no external graphics libraries.
- **Privacy by design.** The architecture is built so that, by default, no data can leave the device — and any exception (such as optional web search) is an explicit, clearly-communicated user choice.

## Note

This repository is a demonstrative showcase. The source code and internal implementation details are private and available on request.

## Contact

**Name:** Lorenzo Boschi
**LinkedIn:** [your-linkedin-url](https://www.linkedin.com/in/your-profile)
**Email:** [lolloboss5@gmail.com](mailto:lolloboss5@gmail.com)
