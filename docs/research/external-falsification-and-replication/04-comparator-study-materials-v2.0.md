# EFR-001 v2.0 comparator study materials

Status: **PREREGISTERED MATERIALS — NOT DEPLOYED**

Amendment: [`EFR-001-COMPARATOR-AMENDMENT-2.0`](../../governance/external-falsification-and-replication-comparator-amendment-v2.0.md)

These materials govern `EFR-HD2` and `EFR-U2`. They inherit the frozen [v1.0 human-study materials](01-human-study-materials.md) verbatim except for the deltas below. The v1.0 file is not edited. Where a v1.0 sentence names two arms (`far`, `standard`), read it as applying to all three arms (`far`, `checker`, `standard`) unless a delta below says otherwise.

## Arms

| Arm ID | HD2 task form (after the common native evidence and contract fields) | U2 audit form (after the common native evidence and sealed SOP) |
|---|---|---|
| `standard` | No report box. | Nothing further. |
| `checker` | A box titled “Automated report” containing the complete plain-text output of the [generic table-consistency checker](../../../tools/efr_generic_collision_checker.py), run on the record's `representation` and `required_behavior` tables. | The neutral case tables (one row per source case: case ID, representation value, required-behavior value, rendered with the v1.0 JSON rule), followed by the same “Automated report” box with the generic checker's plain-text output. No other contract field is shown. |
| `far` | A box titled “Automated report” containing the complete plain-text output of `python -m mechanization.far_mechanization.contract_v2_strict RECORD` on the prepared record. | The v1.0 U1 FAR-arm contract fields, followed by the same FAR report box. |

The box title, position, typography, and dimensions are identical in the `checker` and `far` arms. Neither report may be summarized, colored, reordered, or annotated. Both reveal the machine classification; neither reveals the custodian's label.

The comparator exists to separate FAR-specific benefit from access to any determinate collision check. For finite explicit tables both reports state the same preservation/loss classification. HD2 and U2 therefore test whether FAR's contract framing and report add anything beyond a generic check. A null or negative FAR-versus-checker result is a legitimate, registered outcome.

## Generic checker input

For each record, the custodian extracts `{"representation": [...], "required_behavior": [...]}` with rows `{"case_id", "value"}` copied byte-for-byte (as canonical JSON values) from the prepared record's `contract.representation.table` and `contract.required_behavior.table`. The checker is run with Python 3.12 as `python tools/efr_generic_collision_checker.py TABLES.json`; its stdout is the report text. The checker imports no Project FAR code and uses no Project FAR terminology.

## Training delta

The four-hour course keeps v1.0's timetable. In minutes 120–130 read both report lessons below. In minutes 130–170, for each practice record P01–P12, inspect the FAR report and the generic checker report side by side for 200 seconds. Every participant therefore receives identical exposure to both report types, and neither report is favored by training. Qualification (minutes 180–240) is unchanged: standard form only, no report.

Exact FAR-report lesson: the v1.0 “automated-report lesson” text, verbatim.

Exact generic-checker lesson:

> The table consistency check compares the supplied representation values with the supplied required-behavior values. If two cases share a representation value but require different behavior, it lists that pair. Otherwise it lists one required-behavior value for each representation value. A syntactically valid file alone does not show preservation. The check does not establish that the tables capture every relevant feature of a real domain. Treat the report as evidence to inspect, not as an instruction that you must agree with it. The independent custodian's label is never displayed during the study.

## HD2 session schedule

Training is day 0, as in v1.0. Each reviewer rates 12 tasks per arm in two six-task sessions per arm, each starting at 09:00 local time. Days 2–3 use the reviewer's first allocated arm, days 5–6 the second, and days 8–9 the third. Days 4 and 7 are fixed no-rating intervals. Each session is exactly v1.0's six-task session: fixed 22-minute slots, three pairs with ten-minute breaks, task start offsets 0, 22, 54, 76, 108, and 130 minutes, ending at minute 152. Late-start, absence, missing-workload, safety-stop, and no-makeup rules are v1.0's. Arm order is the allocation's `arm_order`; each of the six orders is used by exactly ten reviewers.

## HD2 allocation input and generator

Run the content-addressed [HD2 allocation script](../../../tools/efr_hd2_allocation.py) under Python 3.12 as `python tools/efr_hd2_allocation.py sealed-input.json EXPECTED_SHA256`. The sealed manifest contains `"test_id": "EFR-HD2"`, `reviewers` (60 distinct ASCII IDs), and `cases` (the 120 EFR-H1 cases with `id`, `domain`, `class`). A v1.0 HD1 manifest is rejected. Analysis is `python tools/efr_hd2_analysis.py INPUT INPUT_SHA256 RATINGS RATINGS_SHA256`, where the ratings object has exactly 2,160 rows naming `reviewer_id`, `case_id`, `arm` (`far`, `checker`, or `standard`), and `decision`.

## U2 allocation input and generator

The sealed site-roster manifest contains `"test_id": "EFR-U2"` and, for each of `S01`–`S03`, `workers` (sealed order, at most 40) and `assignments` mapping investigation IDs `Sxx-001`…`Sxx-060` to workers by the cyclic rule `(i-1) mod N`. Allocation and analysis run under Python 3.12 via the content-addressed [U2 script](../../../tools/efr_u2_analysis.py): `python tools/efr_u2_analysis.py ROSTER ROSTER_SHA256 OUTCOMES OUTCOMES_SHA256`. The outcomes object lists every allocated investigation with `escaped_defect` (`true`, `false`, or `null` for a missing output).

Custodians prepare, for every enrolled investigation before its arm is revealed, the v1.0 U1 projection, the FAR report, the neutral case tables, and the generic checker report, and seal all four. All three arms' preparation happens for every investigation, preserving blinding.

## Rendering equivalence delta

The v1.0 operator attestation additionally verifies that HD2's three arms differ only in the report box (absent, generic checker, or FAR), and that U2's `checker` form shows exactly the neutral tables and the checker box while its `far` form shows exactly the v1.0 FAR-arm sections.

## Current disposition

These are frozen planned materials, not a deployed study system or evidence of utility. No participant has been recruited and no response has been collected.
