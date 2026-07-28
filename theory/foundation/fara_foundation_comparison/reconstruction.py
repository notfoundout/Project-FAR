"""Canonical reconstruction without benchmark answers or opaque decoders."""
from __future__ import annotations
def reconstruct(source,trace):
    reverse={target:key for key,target in trace["correspondence_map"].items()}
    recovered=[reverse[x] for x in trace["generated_target_elements"] if x in reverse]
    return {"reconstruction_steps":[{"target":x,"source":reverse[x]} for x in trace["generated_target_elements"] if x in reverse],"recovered_elements":recovered,"recovered_commitments":[c for c in source["commitments"] if c not in trace["omitted_commitments"]]}
def compare(source,reconstruction):
    missing=sorted(set(source["commitments"])-set(reconstruction["recovered_commitments"]))
    return {"commitment_equivalent":not missing,"missing":missing}
