# Validation note

This note summarises the evidence available for the public showcase.

## Historical development result

The development record for **BrAIn v0.6.13, dated 10 September 2026**, reports **1,241 passing automated tests**. The preceding development entries describe checks around retrieval behaviour, citations, conversation follow-ups, document access and the chat/canvas interfaces.

This is a historical result from the private development record, not a new run for this showcase. Later interface changes are not included in that full-suite result. The application and test suite remain private.

## Showcase checks — 13 September 2026

The application was run in an isolated local demo with a fresh index, separate history and five fictional Markdown documents. Indexing completed for all five files without errors. Web search was disabled.

- Direct document listings with source references and document cards.
- A searchable 2D document map.
- Two connected document-list requests on the canvas.
- A targeted clarification for an ambiguous firewall-port question.

The chat and canvas screenshots show direct document-list responses, not free-form model summaries. Screenshots illustrate these workflows; they are not a benchmark of retrieval or model quality.

Additional questions using the local `llama3.2:3b` model exposed missing citations and inaccurate interpretation of a retrieved passage. Opening an original Markdown document also required a Windows file association that was unavailable in the demo environment. These observations are consistent with the limitations below; no full automated test suite was run for this showcase update.

## Limits of the evidence

Automated regression tests check expected behaviours in defined cases. They do not establish how often an arbitrary document collection will yield a complete or correct answer.

In particular:

- Citations can refer to real retrieved sources without proving that every generated statement follows from them.
- Refusal and clarification paths cover defined cases; they do not prevent all unsupported answers or detect every ambiguity.
- Search can omit relevant material, and OCR or document structure can affect what is indexed.
- Model comparisons display different responses for the user to assess; they do not automatically select a winner.
- Runtime depends on hardware, model size, document content and cache state.

A broader benchmark would need a defined set of questions, expected sources and model configurations. No answer-accuracy percentage is claimed here.
