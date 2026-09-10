// Execute the real page script against a minimal DOM and inspect Blob bytes.
// Run from the repository root with Node; no browser or external service.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

async function main() {
  const source = fs.readFileSync('commercial/far-demo/src/far_demo/app.py', 'utf8');
  const script = source.match(/<script>([\s\S]*?)<\/script>/)[1];
  const elements = new Map();
  const blobs = [];
  const revoked = [];
  const context = {
    Blob,
    URL: {
      createObjectURL(blob) { blobs.push(blob); return `blob:test-${blobs.length}`; },
      revokeObjectURL(url) { revoked.push(url); },
    },
    document: { getElementById(id) {
      if (!elements.has(id)) elements.set(id, {
        style: {}, classList: { add() {} }, addEventListener() {}, scrollIntoView() {},
      });
      return elements.get(id);
    } },
  };
  vm.createContext(context);
  vm.runInContext(script, context);
  for (const version of [1, 2]) {
    const artifact = { schema: 'test-upload', version, sha256: 'a'.repeat(64) };
    context.render({ artifact, release_decision: 'REVIEW_REQUIRED', headline: 'test',
      plain_summary: 'test', why_it_matters: 'test', status_transition: ['justified', 'justified'],
      structural_changes: [], trace_completeness: 1, unknowns: [], rule_findings: [],
    });
    assert.equal(elements.get('downloadReport').href, `blob:test-${version}`);
    assert.deepEqual(JSON.parse(await blobs[version - 1].text()), artifact);
  }
  assert.deepEqual(revoked, ['blob:test-1']);
  console.log('PASS: render downloads the current artifact and revokes the previous Blob URL');
}
main().catch(error => { console.error(error); process.exitCode = 1; });
