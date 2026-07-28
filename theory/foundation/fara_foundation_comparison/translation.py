"""Explicit source-to-candidate translations; execution remains candidate-local."""
from __future__ import annotations
FOUNDATIONS=("many-sorted-relational","typed-hypergraph","algebraic-state-transition")
def translate(source,foundation):
    if foundation not in FOUNDATIONS: raise ValueError("undeclared foundation")
    elements=[x["id"] for x in source["elements"]]
    correspondence={x:f"{foundation}:{x}" for x in elements}
    external=source.get("required_capability")=="external-semantics"
    native=source.get("required_capability")==foundation
    omitted=list(source["commitments"] if external else ([] if native else ["history"]))
    return {"source_elements":elements,"generated_target_elements":list(correspondence.values()),"correspondence_map":correspondence,"omitted_commitments":omitted,"introduced_commitments":[],"derived_vs_native":{"native":source["name"] if native else "encoded","derived":[] if native else list(omitted)},"external_assumptions":list(source.get("external",[])),"opaque_content":[],"failure_or_unknown_reason":source.get("unknown_reason")}
