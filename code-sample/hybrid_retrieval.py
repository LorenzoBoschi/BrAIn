"""
BrAIn — hybrid retrieval, selected excerpt.

This is a single, self-contained excerpt from BrAIn's private codebase,
shared as a code sample. The rest of the system (ingestion, indexing,
generation, MCP server, UI, hardware-adaptive layer) remains private.

------------------------------------------------------------------------
The problem it solves
------------------------------------------------------------------------
Consumer-grade embedding models compress cosine similarities into a
narrow band (roughly 0.75-0.90). A single fixed similarity threshold
therefore fails in BOTH directions: it rejects genuinely relevant
passages, and it accepts "the least-bad of a set of irrelevant results".
That second failure is exactly what makes small, local RAG systems
hallucinate confident answers on empty context.

BrAIn combines three signals so it answers only when it defensibly
should, and fuses semantic search with keyword search so that both
paraphrases *and* exact terms (names, codes, acronyms) are retrieved --
the two techniques cover each other's blind spots.
"""

from __future__ import annotations

from dataclasses import dataclass
from statistics import median

RRF_K = 60  # Reciprocal Rank Fusion damping constant (standard value)


@dataclass
class Hit:
    id: str
    similarity: float | None  # cosine similarity, or None for lexical-only
    rank: int                 # 1-based rank within its own result list


def passes_relevance_gate(
    best_similarity: float,
    candidate_similarities: list[float],
    min_similarity: float,
    has_lexical_anchor: bool,
) -> bool:
    """Contrast-based relevance gate.

    Instead of a single hard threshold, the top hit is accepted only if
    it is defensibly relevant under at least one of three tests:

      (a) it is high in ABSOLUTE terms, or
      (b) it clears the threshold AND stands out from the median of the
          other candidates -- a real match "peaks" above the field, an
          off-topic query produces a flat, indistinct distribution, or
      (c) a document contains EVERY rare term of the query (an exact
          lexical anchor that an off-topic query can never fabricate).

    If none hold, the caller returns "no relevant results" and never
    invokes the language model -- no context, no hallucination.
    """
    if has_lexical_anchor:
        return True
    mid = median(candidate_similarities) if candidate_similarities else 0.0
    strong = best_similarity >= min_similarity + 0.06
    peaked = (
        best_similarity >= min_similarity + 0.02
        and best_similarity - mid >= 0.03
    )
    return strong or peaked


def reciprocal_rank_fusion(
    vector_hits: list[Hit],
    lexical_hits: list[Hit],
    boost_lexical: bool,
) -> list[str]:
    """Fuse the semantic and keyword rankings into one ordered list.

    Each hit contributes 1 / (K + rank) for every list it appears in, so
    a passage ranked highly by BOTH semantic and keyword search rises to
    the top without having to calibrate the two very different score
    scales against each other.

    When the query names a rare term, the lexical ranking is weighted
    more heavily -- BM25 is precisely what captures rare, exact terms
    that dense embeddings tend to dilute.
    """
    weight = 2.0 if boost_lexical else 1.0
    scores: dict[str, float] = {}

    for hit in vector_hits:
        scores[hit.id] = scores.get(hit.id, 0.0) + 1.0 / (RRF_K + hit.rank)

    for hit in lexical_hits:
        scores[hit.id] = scores.get(hit.id, 0.0) + weight / (RRF_K + hit.rank)

    return sorted(scores, key=scores.__getitem__, reverse=True)
