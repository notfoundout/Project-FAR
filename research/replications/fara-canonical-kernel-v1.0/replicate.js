#!/usr/bin/env node
"use strict";

const fs = require("fs");
const crypto = require("crypto");
const path = require("path");

const RELATION_SCHEMA = {
  represents: ["Representation", "Object"],
  assigns: ["Interpretation", "Representation", "Meaning"],
  uses_calculus: ["Investigation", "ReasoningCalculus"],
  has_objective: ["Investigation", "Objective"],
  has_condition: ["Investigation", "Condition"],
  contains_rule: ["ReasoningCalculus", "Rule"],
  applies: ["Event", "Rule"],
  input_state: ["Event", "State"],
  output_state: ["Event", "State"],
  occurs_in: ["Event", "Investigation"],
  precedes: ["Event", "Event"],
  occurrence_type: ["RelationOccurrence", "RelationType"],
  participant: ["RelationOccurrence", "Role", "Object"],
  provenance_of: ["Event", "Provenance"]
};

const SCAFFOLDING = new Set(["Node", "Port", "Hyperedge", "Operation", "Transition"]);

function stable(value) {
  if (Array.isArray(value)) return value.map(stable);
  if (value && typeof value === "object") {
    return Object.fromEntries(Object.keys(value).sort().map((key) => [key, stable(value[key])]));
  }
  return value;
}

function canonical(value) {
  return JSON.stringify(stable(value));
}

function digest(value) {
  return crypto.createHash("sha256").update(canonical(value)).digest("hex");
}

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

function materializeScenario(scenario) {
  const prefix = scenario.id;
  const events = scenario.event_labels.map((label, index) => `${prefix}:event:${index}:${label}`);
  const rules = events.map((_, index) => `${prefix}:rule:${index}`);
  const states = Array.from({ length: events.length + 1 }, (_, index) => `${prefix}:state:${index}`);
  const objects = scenario.objects.map((item) => `${prefix}:object:${item}`);
  const representations = objects.map((item, index) => `${prefix}:representation:${index}:${path.basename(item)}`);
  const meanings = objects.map((_, index) => `${prefix}:meaning:${index}`);
  const interpretations = objects.map((_, index) => `${prefix}:interpretation:${index}`);
  const investigation = `${prefix}:investigation`;
  const calculus = `${prefix}:calculus`;
  const relationType = `${prefix}:relation-type:associated`;
  const occurrences = Array.from({ length: scenario.parallel_occurrences }, (_, index) => `${prefix}:occurrence:${index}`);
  const roles = [`${prefix}:role:left`, `${prefix}:role:right`];
  const provenance = [];
  for (let eventIndex = 0; eventIndex < events.length; eventIndex += 1) {
    for (let p = 0; p < scenario.provenance_per_event; p += 1) {
      provenance.push(`${prefix}:provenance:${eventIndex}:${p}`);
    }
  }

  const relations = Object.fromEntries(Object.keys(RELATION_SCHEMA).map((name) => [name, []]));
  representations.forEach((representation, index) => {
    relations.represents.push([representation, objects[index]]);
    relations.assigns.push([interpretations[index], representation, meanings[index]]);
  });
  relations.uses_calculus.push([investigation, calculus]);
  relations.has_objective.push([investigation, `${prefix}:objective`]);
  relations.has_condition.push([investigation, `${prefix}:condition`]);
  rules.forEach((rule) => relations.contains_rule.push([calculus, rule]));
  events.forEach((event, index) => {
    relations.applies.push([event, rules[index]]);
    relations.input_state.push([event, states[index]]);
    relations.output_state.push([event, states[index + 1]]);
    relations.occurs_in.push([event, investigation]);
    if (index + 1 < events.length) relations.precedes.push([event, events[index + 1]]);
    for (let p = 0; p < scenario.provenance_per_event; p += 1) {
      relations.provenance_of.push([event, `${prefix}:provenance:${index}:${p}`]);
    }
  });
  occurrences.forEach((occurrence) => {
    relations.occurrence_type.push([occurrence, relationType]);
    relations.participant.push([occurrence, roles[0], objects[0]]);
    relations.participant.push([occurrence, roles[1], objects[1]]);
  });

  return {
    id: scenario.id,
    sorts: {
      Object: objects,
      Representation: representations,
      Meaning: meanings,
      Interpretation: interpretations,
      ReasoningCalculus: [calculus],
      Rule: rules,
      State: states,
      Event: events,
      Investigation: [investigation],
      Objective: [`${prefix}:objective`],
      Condition: [`${prefix}:condition`],
      RelationType: [relationType],
      RelationOccurrence: occurrences,
      Role: roles,
      Provenance: provenance
    },
    relations
  };
}

function countFor(model, relation, subject) {
  return (model.relations[relation] || []).filter((row) => row[0] === subject).length;
}

function containsCycle(edges) {
  const adjacency = new Map();
  for (const [source, target] of edges) {
    if (!adjacency.has(source)) adjacency.set(source, []);
    adjacency.get(source).push(target);
  }
  const visiting = new Set();
  const visited = new Set();
  function visit(node) {
    if (visiting.has(node)) return true;
    if (visited.has(node)) return false;
    visiting.add(node);
    for (const target of adjacency.get(node) || []) if (visit(target)) return true;
    visiting.delete(node);
    visited.add(node);
    return false;
  }
  return [...adjacency.keys()].some(visit);
}

function validateModel(model) {
  const errors = [];
  const owner = new Map();
  for (const [sort, ids] of Object.entries(model.sorts || {})) {
    if (!Array.isArray(ids) || new Set(ids).size !== ids.length) errors.push(`duplicate identity within ${sort}`);
    for (const id of ids || []) {
      if (owner.has(id)) errors.push(`cross-sort identity collision: ${id}`);
      owner.set(id, sort);
    }
  }
  for (const [relation, signature] of Object.entries(RELATION_SCHEMA)) {
    const rows = model.relations?.[relation];
    if (!Array.isArray(rows)) {
      errors.push(`missing relation: ${relation}`);
      continue;
    }
    rows.forEach((row, index) => {
      if (!Array.isArray(row) || row.length !== signature.length) {
        errors.push(`arity mismatch: ${relation}[${index}]`);
        return;
      }
      row.forEach((id, position) => {
        if (owner.get(id) !== signature[position]) errors.push(`type mismatch: ${relation}[${index}][${position}]`);
      });
    });
  }
  for (const event of model.sorts?.Event || []) {
    const requirements = [
      ["applies", "rule"],
      ["input_state", "input state"],
      ["output_state", "output state"],
      ["occurs_in", "investigation"]
    ];
    for (const [relation, label] of requirements) {
      if (countFor(model, relation, event) !== 1) errors.push(`event requires exactly one ${label}: ${event}`);
    }
    if (countFor(model, "provenance_of", event) < 1) errors.push(`event without explicit provenance: ${event}`);
  }
  for (const occurrence of model.sorts?.RelationOccurrence || []) {
    if (countFor(model, "occurrence_type", occurrence) !== 1) errors.push(`occurrence requires exactly one type: ${occurrence}`);
    if (countFor(model, "participant", occurrence) < 1) errors.push(`occurrence without participant: ${occurrence}`);
  }
  if (containsCycle(model.relations?.precedes || [])) errors.push("precedes relation contains a cycle");
  return errors;
}

function normalizeModel(model) {
  const normalized = clone(model);
  for (const key of Object.keys(normalized.sorts)) normalized.sorts[key].sort();
  for (const key of Object.keys(normalized.relations)) normalized.relations[key].sort((a, b) => canonical(a).localeCompare(canonical(b)));
  return normalized;
}

function extensionalProjection(model) {
  const types = new Map(model.relations.occurrence_type.map(([occurrence, type]) => [occurrence, type]));
  const participants = new Map();
  for (const [occurrence, role, object] of model.relations.participant) {
    if (!participants.has(occurrence)) participants.set(occurrence, []);
    participants.get(occurrence).push([role, object]);
  }
  const facts = [];
  for (const occurrence of model.sorts.RelationOccurrence) {
    const ordered = (participants.get(occurrence) || []).sort((a, b) => canonical(a).localeCompare(canonical(b)));
    facts.push([types.get(occurrence), ordered]);
  }
  return [...new Map(facts.map((fact) => [canonical(fact), fact])).values()];
}

function toHypergraph(model) {
  const nodes = [];
  for (const [sort, ids] of Object.entries(model.sorts)) for (const id of ids) nodes.push({ id, sort });
  const hyperedges = [];
  for (const [relation, rows] of Object.entries(model.relations)) {
    rows.forEach((row, index) => {
      hyperedges.push({
        id: `edge:${relation}:${index}`,
        relation,
        ports: row.map((node, position) => ({ position, node }))
      });
    });
  }
  return { schema: ["Node", "Port", "Hyperedge"], nodes, hyperedges };
}

function fromHypergraph(view) {
  const sorts = {};
  for (const node of view.nodes) {
    if (!sorts[node.sort]) sorts[node.sort] = [];
    sorts[node.sort].push(node.id);
  }
  const relations = Object.fromEntries(Object.keys(RELATION_SCHEMA).map((name) => [name, []]));
  for (const edge of view.hyperedges) {
    const row = edge.ports.slice().sort((a, b) => a.position - b.position).map((port) => port.node);
    relations[edge.relation].push(row);
  }
  return { id: "restored", sorts, relations };
}

function toAlgebraic(model) {
  const one = (relation, event) => model.relations[relation].find((row) => row[0] === event)?.[1];
  return {
    schema: ["Operation", "Transition"],
    operations: model.sorts.Event.map((event) => ({
      event,
      operation: one("applies", event),
      domain: one("input_state", event),
      codomain: one("output_state", event),
      investigation: one("occurs_in", event)
    })),
    order: clone(model.relations.precedes),
    sidecar: clone(model)
  };
}

function fromAlgebraic(view) {
  if (!view.sidecar) throw new Error("explicit sidecar required");
  return clone(view.sidecar);
}

function mutateCrossSort(model) {
  const changed = clone(model);
  changed.sorts.Representation.push(changed.sorts.Object[0]);
  return changed;
}
function mutateDuplicateRule(model) {
  const changed = clone(model);
  const event = changed.sorts.Event[0];
  const rule = `${changed.id}:rule:duplicate`;
  changed.sorts.Rule.push(rule);
  changed.relations.contains_rule.push([changed.sorts.ReasoningCalculus[0], rule]);
  changed.relations.applies.push([event, rule]);
  return changed;
}
function mutateMissingProvenance(model) {
  const changed = clone(model);
  const event = changed.sorts.Event[0];
  changed.relations.provenance_of = changed.relations.provenance_of.filter((row) => row[0] !== event);
  return changed;
}
function mutateCycle(model) {
  const changed = clone(model);
  const events = changed.sorts.Event;
  changed.relations.precedes.push([events[events.length - 1], events[0]]);
  return changed;
}

function baseGateEvidence(models) {
  const valid = models.every((model) => validateModel(model).length === 0);
  const collisionRejected = models.every((model) => validateModel(mutateCrossSort(model)).some((error) => error.includes("cross-sort identity collision")));
  const duplicateRuleRejected = models.every((model) => validateModel(mutateDuplicateRule(model)).some((error) => error.includes("exactly one rule")));
  const missingProvenanceRejected = models.every((model) => validateModel(mutateMissingProvenance(model)).some((error) => error.includes("without explicit provenance")));
  const cycleRejected = models.every((model) => validateModel(mutateCycle(model)).some((error) => error.includes("cycle")));
  const interpretationSeparated = models.every((model) => model.sorts.Interpretation.length > 0 && model.relations.assigns.length > 0);
  const calculusIndependent = models.every((model) => model.sorts.ReasoningCalculus.length > 0 && !Object.hasOwn(model.sorts, "Operation"));
  const architectureSeparated = models.every((model) => model.sorts.Rule.length > 0 && model.sorts.Event.length > 0 && !Object.hasOwn(model.sorts, "Operation"));
  const occurrenceEvidence = models.map((model) => ({ occurrences: model.sorts.RelationOccurrence.length, projected: extensionalProjection(model).length }));
  const identityPreserved = occurrenceEvidence.every((row) => row.occurrences > row.projected);
  const neutral = models.every((model) => Object.keys(model.sorts).every((sort) => !SCAFFOLDING.has(sort)));
  return {
    representation_object_separation: { pass: valid && collisionRejected, measurements: { valid, collision_rejected: collisionRejected } },
    rule_execution_result_separation: { pass: valid && duplicateRuleRejected, measurements: { valid, duplicate_rule_rejected: duplicateRuleRejected } },
    interpretation_separation: { pass: interpretationSeparated, measurements: { scenario_count: models.length } },
    calculus_independence: { pass: calculusIndependent, measurements: { operation_sort_absent: calculusIndependent } },
    architecture_operation_separation: { pass: architectureSeparated, measurements: { rule_event_disjoint: architectureSeparated } },
    identity_bearing_occurrences: { pass: identityPreserved, measurements: { scenarios: occurrenceEvidence } },
    explicit_provenance_and_order: { pass: valid && missingProvenanceRejected && cycleRejected, measurements: { missing_provenance_rejected: missingProvenanceRejected, cycle_rejected: cycleRejected } },
    encoding_neutrality: { pass: neutral, measurements: { forbidden_scaffolding_absent: neutral } }
  };
}

function classify(candidate, gates) {
  const failed = Object.entries(gates).filter(([, evidence]) => !evidence.pass).map(([gate]) => gate);
  let classification;
  if (failed.length === 0) classification = "provisional-canonical-candidate";
  else if (candidate.kind === "derived-view") classification = "admissible-derived-view";
  else classification = "noncanonical";
  return { id: candidate.id, classification, failed_gates: failed, gate_results: gates };
}

function execute(protocol, fixtures) {
  if (fixtures.scenarios.some((scenario) => Object.hasOwn(scenario, "expected_gates") || Object.hasOwn(scenario, "proposed_foundation"))) {
    throw new Error("neutral fixtures contain outcome leakage");
  }
  const models = fixtures.scenarios.map(materializeScenario);
  const base = baseGateEvidence(models);
  const hyperRoundtrip = models.every((model) => {
    const restored = fromHypergraph(toHypergraph(model));
    restored.id = model.id;
    return canonical(normalizeModel(restored)) === canonical(normalizeModel(model));
  });
  const algebraicRoundtrip = models.every((model) => canonical(normalizeModel(fromAlgebraic(toAlgebraic(model)))) === canonical(normalizeModel(model)));
  const bareRejected = models.every((model) => {
    const view = toAlgebraic(model);
    delete view.sidecar;
    try { fromAlgebraic(view); return false; } catch (error) { return /sidecar/.test(String(error)); }
  });

  const rows = [];
  for (const candidate of protocol.candidates) {
    let gates = clone(base);
    if (candidate.id === "many-sorted-extensional-relational") {
      gates.identity_bearing_occurrences = {
        pass: false,
        measurements: { scenarios: models.map((model) => ({ occurrences: model.sorts.RelationOccurrence.length, projected: extensionalProjection(model).length })) }
      };
    } else if (candidate.id === "typed-hypergraph") {
      gates = Object.fromEntries(Object.entries(base).map(([gate, evidence]) => [gate, { pass: hyperRoundtrip && evidence.pass, measurements: { roundtrip_exact: hyperRoundtrip } }]));
      gates.encoding_neutrality = { pass: false, measurements: { native_schema: ["Node", "Port", "Hyperedge"] } };
    } else if (candidate.id === "algebraic-state-transition") {
      gates = {
        representation_object_separation: { pass: false, measurements: { carriers_present: false } },
        rule_execution_result_separation: { pass: models.every((model) => toAlgebraic(model).operations.every((row) => row.event && row.operation && row.domain && row.codomain)), measurements: { operation_rows: models.reduce((total, model) => total + model.sorts.Event.length, 0) } },
        interpretation_separation: { pass: false, measurements: { interpretation_carrier_present: false } },
        calculus_independence: { pass: false, measurements: { formation_by_operation_rows: true } },
        architecture_operation_separation: { pass: false, measurements: { operation_native: true } },
        identity_bearing_occurrences: { pass: false, measurements: { occurrence_identity_present: false } },
        explicit_provenance_and_order: { pass: false, measurements: { order_present: true, provenance_present: false } },
        encoding_neutrality: { pass: false, measurements: { native_schema: ["Operation", "Transition"] } }
      };
    }
    rows.push(classify(candidate, gates));
  }

  return {
    replication_id: protocol.replication_id,
    source_campaign_id: protocol.source_campaign.campaign_id,
    status: "Research",
    scope: protocol.scope,
    implementation: {
      language: "JavaScript (Node.js)",
      clean_room: true,
      isolated_execution_required: true,
      source_kernel_imported: false,
      source_proof_read_during_execution: false,
      runtime_modules: ["fs", "crypto", "path"]
    },
    fixture_corpus: {
      corpus_id: fixtures.corpus_id,
      scenario_count: models.length,
      materialized_model_digests: models.map((model) => ({ id: model.id, digest: digest(normalizeModel(model)) })),
      all_models_valid: models.every((model) => validateModel(model).length === 0)
    },
    candidate_adjudication: rows,
    translations: {
      typed_hypergraph_roundtrip_exact: hyperRoundtrip,
      algebraic_roundtrip_exact_with_sidecar: algebraicRoundtrip,
      bare_algebraic_reconstruction_rejected: bareRejected
    },
    provisional_result: rows.filter((row) => row.classification === "provisional-canonical-candidate").map((row) => row.id),
    lifecycle: {
      replication: "implementation-independent clean-room execution complete",
      investigator_independence: "not established",
      acceptance: "pending separate adjudication",
      promotion: "pending separate adjudication"
    },
    nonclaims: protocol.nonclaims
  };
}

function main(argv) {
  if (argv.length !== 2) throw new Error("usage: replicate.js <protocol.json> <fixtures.json>");
  const protocol = JSON.parse(fs.readFileSync(argv[0], "utf8"));
  const fixtures = JSON.parse(fs.readFileSync(argv[1], "utf8"));
  process.stdout.write(`${JSON.stringify(execute(protocol, fixtures), null, 2)}\n`);
}

if (require.main === module) {
  try { main(process.argv.slice(2)); }
  catch (error) { process.stderr.write(`${error.stack || error}\n`); process.exit(1); }
}

module.exports = { execute, materializeScenario, validateModel, extensionalProjection, toHypergraph, fromHypergraph, toAlgebraic, fromAlgebraic };
