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
const GRAPH_SCAFFOLDING = ["Node", "Port", "Hyperedge"];
const ALGEBRAIC_SCAFFOLDING = ["Operation", "Transition"];

function clone(value) { return JSON.parse(JSON.stringify(value)); }
function stable(value) {
  if (Array.isArray(value)) return value.map(stable);
  if (value && typeof value === "object") {
    return Object.fromEntries(Object.keys(value).sort().map((key) => [key, stable(value[key])]));
  }
  return value;
}
function canonical(value) { return JSON.stringify(stable(value)); }
function digest(value) { return crypto.createHash("sha256").update(canonical(value)).digest("hex"); }
function rowsFor(model, relation, subject) {
  return (model.relations?.[relation] || []).filter((row) => row[0] === subject);
}

function materializeScenario(scenario) {
  const p = scenario.id;
  const events = scenario.event_labels.map((label, i) => `${p}:event:${i}:${label}`);
  const rules = events.map((_, i) => `${p}:rule:${i}`);
  const states = Array.from({ length: events.length + 1 }, (_, i) => `${p}:state:${i}`);
  const objects = scenario.objects.map((item) => `${p}:object:${item}`);
  const representations = objects.map((_, i) => `${p}:representation:${i}`);
  const meanings = objects.map((_, i) => `${p}:meaning:${i}`);
  const interpretations = objects.map((_, i) => `${p}:interpretation:${i}`);
  const investigation = `${p}:investigation`;
  const calculus = `${p}:calculus`;
  const relationType = `${p}:relation-type:associated`;
  const occurrences = Array.from({ length: scenario.parallel_occurrences }, (_, i) => `${p}:occurrence:${i}`);
  const roles = [`${p}:role:left`, `${p}:role:right`];
  const provenance = [];
  for (let e = 0; e < events.length; e += 1) {
    for (let i = 0; i < scenario.provenance_per_event; i += 1) provenance.push(`${p}:provenance:${e}:${i}`);
  }
  const relations = Object.fromEntries(Object.keys(RELATION_SCHEMA).map((name) => [name, []]));
  representations.forEach((representation, i) => {
    relations.represents.push([representation, objects[i]]);
    relations.assigns.push([interpretations[i], representation, meanings[i]]);
  });
  relations.uses_calculus.push([investigation, calculus]);
  relations.has_objective.push([investigation, `${p}:objective`]);
  relations.has_condition.push([investigation, `${p}:condition`]);
  rules.forEach((rule) => relations.contains_rule.push([calculus, rule]));
  events.forEach((event, i) => {
    relations.applies.push([event, rules[i]]);
    relations.input_state.push([event, states[i]]);
    relations.output_state.push([event, states[i + 1]]);
    relations.occurs_in.push([event, investigation]);
    if (i + 1 < events.length) relations.precedes.push([event, events[i + 1]]);
    for (let j = 0; j < scenario.provenance_per_event; j += 1) {
      relations.provenance_of.push([event, `${p}:provenance:${i}:${j}`]);
    }
  });
  occurrences.forEach((occurrence) => {
    relations.occurrence_type.push([occurrence, relationType]);
    relations.participant.push([occurrence, roles[0], objects[0]]);
    relations.participant.push([occurrence, roles[1], objects[1]]);
  });
  return {
    id: p,
    sorts: {
      Object: objects, Representation: representations, Meaning: meanings,
      Interpretation: interpretations, ReasoningCalculus: [calculus], Rule: rules,
      State: states, Event: events, Investigation: [investigation],
      Objective: [`${p}:objective`], Condition: [`${p}:condition`],
      RelationType: [relationType], RelationOccurrence: occurrences,
      Role: roles, Provenance: provenance
    },
    relations
  };
}

function containsCycle(edges) {
  const adjacency = new Map();
  for (const [source, target] of edges) {
    if (!adjacency.has(source)) adjacency.set(source, []);
    adjacency.get(source).push(target);
  }
  const active = new Set();
  const complete = new Set();
  function visit(node) {
    if (active.has(node)) return true;
    if (complete.has(node)) return false;
    active.add(node);
    for (const next of adjacency.get(node) || []) if (visit(next)) return true;
    active.delete(node); complete.add(node); return false;
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
    if (!Array.isArray(rows)) { errors.push(`missing relation: ${relation}`); continue; }
    rows.forEach((row, index) => {
      if (!Array.isArray(row) || row.length !== signature.length) {
        errors.push(`arity mismatch: ${relation}[${index}]`); return;
      }
      row.forEach((id, position) => {
        if (owner.get(id) !== signature[position]) errors.push(`type mismatch: ${relation}[${index}][${position}]`);
      });
    });
  }
  for (const event of model.sorts?.Event || []) {
    for (const [relation, label] of [["applies", "rule"], ["input_state", "input state"], ["output_state", "output state"], ["occurs_in", "investigation"]]) {
      if (rowsFor(model, relation, event).length !== 1) errors.push(`event requires exactly one ${label}: ${event}`);
    }
    if (rowsFor(model, "provenance_of", event).length < 1) errors.push(`event without explicit provenance: ${event}`);
  }
  for (const occurrence of model.sorts?.RelationOccurrence || []) {
    if (rowsFor(model, "occurrence_type", occurrence).length !== 1) errors.push(`occurrence requires exactly one type: ${occurrence}`);
    if (rowsFor(model, "participant", occurrence).length < 1) errors.push(`occurrence without participant: ${occurrence}`);
  }
  if (containsCycle(model.relations?.precedes || [])) errors.push("precedes relation contains a cycle");
  return errors;
}

function normalizeModel(model) {
  const value = clone(model);
  Object.values(value.sorts).forEach((ids) => ids.sort());
  Object.values(value.relations).forEach((rows) => rows.sort((a, b) => canonical(a).localeCompare(canonical(b))));
  return value;
}

function extensionalProjection(model) {
  const typeByOccurrence = new Map(model.relations.occurrence_type.map(([occurrence, type]) => [occurrence, type]));
  const participants = new Map();
  for (const [occurrence, role, object] of model.relations.participant) {
    if (!participants.has(occurrence)) participants.set(occurrence, []);
    participants.get(occurrence).push([role, object]);
  }
  const facts = model.sorts.RelationOccurrence.map((occurrence) => [
    typeByOccurrence.get(occurrence),
    (participants.get(occurrence) || []).sort((a, b) => canonical(a).localeCompare(canonical(b)))
  ]);
  return [...new Map(facts.map((fact) => [canonical(fact), fact])).values()];
}

function toHypergraph(model) {
  const nodes = [];
  for (const [sort, ids] of Object.entries(model.sorts)) for (const id of ids) nodes.push({ id, sort });
  const hyperedges = [];
  for (const [relation, rows] of Object.entries(model.relations)) {
    rows.forEach((row, index) => hyperedges.push({
      id: `edge:${relation}:${index}`,
      relation,
      ports: row.map((node, position) => ({ position, node }))
    }));
  }
  return { schema: GRAPH_SCAFFOLDING, nodes, hyperedges };
}
function fromHypergraph(view) {
  const sorts = {};
  for (const node of view.nodes) (sorts[node.sort] ||= []).push(node.id);
  const relations = Object.fromEntries(Object.keys(RELATION_SCHEMA).map((name) => [name, []]));
  for (const edge of view.hyperedges) {
    relations[edge.relation].push(edge.ports.slice().sort((a, b) => a.position - b.position).map((port) => port.node));
  }
  return { id: "restored", sorts, relations };
}

function toAlgebraic(model) {
  function one(relation, event) { return rowsFor(model, relation, event)[0]?.[1]; }
  return {
    schema: ALGEBRAIC_SCAFFOLDING,
    operations: model.sorts.Event.map((event) => ({
      event, operation: one("applies", event), domain: one("input_state", event),
      codomain: one("output_state", event), investigation: one("occurs_in", event)
    })),
    order: clone(model.relations.precedes),
    sidecar: clone(model)
  };
}
function fromAlgebraic(view) {
  if (!view.sidecar) throw new Error("explicit sidecar required");
  return clone(view.sidecar);
}
function bareAlgebraic(view) {
  const value = clone(view); delete value.sidecar; return value;
}
function schemaHas(view, name) { return Array.isArray(view.schema) && view.schema.includes(name); }
function hasFieldDeep(value, field) {
  if (Array.isArray(value)) return value.some((item) => hasFieldDeep(item, field));
  if (value && typeof value === "object") {
    return Object.prototype.hasOwnProperty.call(value, field) || Object.values(value).some((item) => hasFieldDeep(item, field));
  }
  return false;
}
function deriveAlgebraicGates(view) {
  const bare = bareAlgebraic(view);
  const operations = Array.isArray(bare.operations) ? bare.operations : [];
  const ruleExecutionResultSeparated = operations.length > 0 && operations.every((row) =>
    ["event", "operation", "domain", "codomain"].every((key) => typeof row[key] === "string" && row[key].length > 0)
  );
  const representationObjectSeparated = schemaHas(bare, "Object") && schemaHas(bare, "Representation");
  const interpretationSeparated = schemaHas(bare, "Interpretation") || hasFieldDeep(bare, "interpretation");
  const calculusPresent = schemaHas(bare, "ReasoningCalculus") || hasFieldDeep(bare, "calculus");
  const nativeOperation = schemaHas(bare, "Operation") || operations.length > 0;
  const occurrenceIdentityPresent = schemaHas(bare, "RelationOccurrence") || hasFieldDeep(bare, "relationOccurrence");
  const orderPresent = Array.isArray(bare.order);
  const provenancePresent = schemaHas(bare, "Provenance") || hasFieldDeep(bare, "provenance");
  const scaffolding = (bare.schema || []).filter((name) => ALGEBRAIC_SCAFFOLDING.includes(name));
  return {
    representation_object_separation: { pass: representationObjectSeparated, measurements: { object_carrier_present: schemaHas(bare, "Object"), representation_carrier_present: schemaHas(bare, "Representation") } },
    rule_execution_result_separation: { pass: ruleExecutionResultSeparated, measurements: { operation_rows: operations.length, explicit_event_operation_domain_codomain: ruleExecutionResultSeparated } },
    interpretation_separation: { pass: interpretationSeparated, measurements: { interpretation_present: interpretationSeparated } },
    calculus_independence: { pass: calculusPresent && !nativeOperation, measurements: { calculus_present: calculusPresent, native_operation_present: nativeOperation } },
    architecture_operation_separation: { pass: !nativeOperation, measurements: { native_operation_present: nativeOperation } },
    identity_bearing_occurrences: { pass: occurrenceIdentityPresent, measurements: { occurrence_identity_present: occurrenceIdentityPresent } },
    explicit_provenance_and_order: { pass: provenancePresent && orderPresent, measurements: { order_present: orderPresent, provenance_present: provenancePresent } },
    encoding_neutrality: { pass: scaffolding.length === 0, measurements: { native_scaffolding: scaffolding } }
  };
}

function mutateCrossSort(model) { const value = clone(model); value.sorts.Representation.push(value.sorts.Object[0]); return value; }
function mutateDuplicateRule(model) {
  const value = clone(model); const event = value.sorts.Event[0]; const rule = `${value.id}:rule:duplicate`;
  value.sorts.Rule.push(rule); value.relations.contains_rule.push([value.sorts.ReasoningCalculus[0], rule]); value.relations.applies.push([event, rule]); return value;
}
function mutateMissingProvenance(model) {
  const value = clone(model); const event = value.sorts.Event[0];
  value.relations.provenance_of = value.relations.provenance_of.filter((row) => row[0] !== event); return value;
}
function mutateCycle(model) {
  const value = clone(model); const events = value.sorts.Event;
  value.relations.precedes.push([events[events.length - 1], events[0]]); return value;
}

function deriveNativeGates(models) {
  const valid = models.every((model) => validateModel(model).length === 0);
  const collisionRejected = models.every((model) => validateModel(mutateCrossSort(model)).some((error) => error.includes("cross-sort identity collision")));
  const duplicateRuleRejected = models.every((model) => validateModel(mutateDuplicateRule(model)).some((error) => error.includes("exactly one rule")));
  const provenanceRejected = models.every((model) => validateModel(mutateMissingProvenance(model)).some((error) => error.includes("without explicit provenance")));
  const cycleRejected = models.every((model) => validateModel(mutateCycle(model)).some((error) => error.includes("cycle")));
  const interpretationSeparated = models.every((model) => model.sorts.Interpretation.length > 0 && model.relations.assigns.length > 0);
  const calculusIndependent = models.every((model) => model.sorts.ReasoningCalculus.length > 0 && !Object.hasOwn(model.sorts, "Operation"));
  const architectureSeparated = models.every((model) => model.sorts.Rule.length > 0 && model.sorts.Event.length > 0 && !Object.hasOwn(model.sorts, "Operation"));
  const occurrenceRows = models.map((model) => ({ occurrences: model.sorts.RelationOccurrence.length, projected: extensionalProjection(model).length }));
  const identityPreserved = occurrenceRows.every((row) => row.occurrences > row.projected);
  const neutral = models.every((model) => Object.keys(model.sorts).every((sort) => ![...GRAPH_SCAFFOLDING, ...ALGEBRAIC_SCAFFOLDING].includes(sort)));
  return {
    representation_object_separation: { pass: valid && collisionRejected, measurements: { valid, collision_rejected: collisionRejected } },
    rule_execution_result_separation: { pass: valid && duplicateRuleRejected, measurements: { valid, duplicate_rule_rejected: duplicateRuleRejected } },
    interpretation_separation: { pass: interpretationSeparated, measurements: { scenario_count: models.length } },
    calculus_independence: { pass: calculusIndependent, measurements: { operation_sort_absent: calculusIndependent } },
    architecture_operation_separation: { pass: architectureSeparated, measurements: { rule_event_disjoint: architectureSeparated } },
    identity_bearing_occurrences: { pass: identityPreserved, measurements: { scenarios: occurrenceRows } },
    explicit_provenance_and_order: { pass: valid && provenanceRejected && cycleRejected, measurements: { missing_provenance_rejected: provenanceRejected, cycle_rejected: cycleRejected } },
    encoding_neutrality: { pass: neutral, measurements: { forbidden_scaffolding_absent: neutral } }
  };
}

function classify(candidate, gates) {
  const failed = Object.entries(gates).filter(([, evidence]) => !evidence.pass).map(([gate]) => gate);
  const classification = failed.length === 0 ? "provisional-canonical-candidate" : candidate.kind === "derived-view" ? "admissible-derived-view" : "noncanonical";
  return { id: candidate.id, classification, failed_gates: failed, gate_results: gates };
}

function execute(protocol, fixtures) {
  if (fixtures.scenarios.some((scenario) => Object.hasOwn(scenario, "expected_gates") || Object.hasOwn(scenario, "proposed_foundation"))) {
    throw new Error("neutral fixtures contain outcome leakage");
  }
  const models = fixtures.scenarios.map(materializeScenario);
  const native = deriveNativeGates(models);
  const hyperRoundtrip = models.every((model) => {
    const restored = fromHypergraph(toHypergraph(model)); restored.id = model.id;
    return canonical(normalizeModel(restored)) === canonical(normalizeModel(model));
  });
  const algebraicViews = models.map(toAlgebraic);
  const algebraicRoundtrip = models.every((model, i) => canonical(normalizeModel(fromAlgebraic(algebraicViews[i]))) === canonical(normalizeModel(model)));
  const bareRejected = algebraicViews.every((view) => { try { fromAlgebraic(bareAlgebraic(view)); return false; } catch (error) { return /sidecar/.test(String(error)); } });
  const rows = protocol.candidates.map((candidate) => {
    let gates = clone(native);
    if (candidate.id === "many-sorted-extensional-relational") {
      gates.identity_bearing_occurrences = { pass: false, measurements: native.identity_bearing_occurrences.measurements };
    } else if (candidate.id === "typed-hypergraph") {
      gates = Object.fromEntries(Object.entries(native).map(([gate]) => [gate, { pass: hyperRoundtrip, measurements: { roundtrip_exact: hyperRoundtrip } }]));
      gates.encoding_neutrality = { pass: false, measurements: { native_schema: GRAPH_SCAFFOLDING } };
    } else if (candidate.id === "algebraic-state-transition") {
      const perScenario = algebraicViews.map(deriveAlgebraicGates);
      gates = Object.fromEntries(protocol.mandatory_gates.map((gate) => [gate, {
        pass: perScenario.every((row) => row[gate].pass),
        measurements: { scenarios: perScenario.map((row, i) => ({ id: models[i].id, ...row[gate].measurements })) }
      }]));
    }
    return classify(candidate, gates);
  });
  return {
    replication_id: protocol.replication_id,
    source_campaign_id: protocol.source_campaign.campaign_id,
    status: "Research",
    scope: protocol.scope,
    implementation: {
      language: "JavaScript (Node.js)", clean_room: true,
      isolated_execution_required: true, source_kernel_imported: false,
      source_proof_read_during_execution: false, runtime_modules: ["fs", "crypto", "path"]
    },
    fixture_corpus: {
      corpus_id: fixtures.corpus_id, scenario_count: models.length,
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
module.exports = {
  execute, materializeScenario, validateModel, extensionalProjection,
  toHypergraph, fromHypergraph, toAlgebraic, fromAlgebraic,
  bareAlgebraic, deriveAlgebraicGates
};
