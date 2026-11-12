#!/usr/bin/env node
// Exercise the released packages and exact hooks.json commands with throwaway keys.
import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync, writeFileSync, chmodSync, mkdirSync, existsSync, rmSync, statSync, readdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, resolve, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const repo = resolve(dirname(fileURLToPath(import.meta.url)), '../../..');
const work = mkdtempSync(join(tmpdir(), 'protect-hook-migration-'));
let passed = 0;
function run(command, args, options = {}) {
  return spawnSync(command, args, { cwd: work, encoding: 'utf8', input: '', timeout: 60000, maxBuffer: 4 * 1024 * 1024, ...options });
}
function npm(pkg, args, options) { return run('npx', ['--yes', pkg, ...args], options); }
function check(name, fn) { fn(); passed++; console.log(`PASS: ${name}`); }
function ok(result) { assert.equal(result.status, 0, result.stderr || result.error?.message || result.stdout); }
function quiet(result, status = 0) {
  assert.equal(result.status, status, result.stderr || result.error?.message || result.stdout);
  assert.equal(result.stdout, '', 'PostToolUse must never emit a CLI summary');
}
try {
  ok(npm('protect-mcp@0.32.4', ['init', '--dir', work]));
  const key = join(work, 'keys/gateway.json');
  check('0.32.4 init creates an owner-only key', () => assert.equal(statSync(key).mode & 0o777, 0o600));
  const originalKey = readFileSync(key, 'utf8');
  const publicKey = JSON.parse(originalKey).publicKey;
  const verify = file => npm('@veritasacta/verify@0.11.1', ['--replay-chain', file, '--key', publicKey, '--json']);
  const event = { tool_name: 'Read', tool_input: { secret: 'PRIVATE-INPUT' }, tool_response: { secret: 'PRIVATE-OUTPUT' }, transcript_path: 'PRIVATE-TRANSCRIPT' };

  for (const [plugin, prefix] of [['protect-mcp', 'PROTECT_MCP'], ['review-agent-governance', 'REVIEW_GOVERNANCE']]) {
    const root = join(repo, 'plugins', plugin);
    const command = JSON.parse(readFileSync(join(root, 'hooks/hooks.json'), 'utf8')).hooks.PostToolUse[0].hooks[0].command;
    const receiptDir = join(work, plugin);
    const env = { ...process.env, CLAUDE_PLUGIN_ROOT: root, [`${prefix}_KEY`]: key, [`${prefix}_RECEIPTS`]: receiptDir };
    const hook = (payload = event, extra = {}) => run('bash', ['-c', command], { env: { ...env, ...extra }, input: typeof payload === 'string' ? payload : JSON.stringify(payload) });
    for (let i = 0; i < 3; i++) check(`${plugin}: real stdin event signs with empty stdout (${i + 1})`, () => quiet(hook()));
    const log = join(receiptDir, 'receipts.jsonl');
    const lines = readFileSync(log, 'utf8').trim().split('\n');
    check(`${plugin}: all calls append tool-only modern receipts`, () => {
      assert.equal(lines.length, 3);
      for (const line of lines) {
        const receipt = JSON.parse(line);
        assert.equal(receipt.payload.tool_name, 'Read');
        assert.equal(receipt.signature.alg, 'EdDSA');
        assert.equal(receipt.payload.payload_digest, undefined);
        assert.doesNotMatch(line, /PRIVATE-|tool_input|tool_response|transcript_path/);
      }
      assert.equal(JSON.parse(lines[0]).payload.previousReceiptHash, undefined);
      assert.match(JSON.parse(lines[1]).payload.previousReceiptHash, /^sha256:[0-9a-f]{64}$/);
    });
    check(`${plugin}: complete linked log verifies`, () => ok(verify(log)));
    const altered = join(work, `${plugin}-altered.jsonl`);
    const replay = entries => { writeFileSync(altered, entries.join('\n') + '\n'); return verify(altered); };
    check(`${plugin}: interior deletion breaks the chain`, () => assert.equal(replay([lines[0], lines[2]]).status, 1));
    check(`${plugin}: reordering breaks the chain`, () => assert.equal(replay([lines[0], lines[2], lines[1]]).status, 1));
    check(`${plugin}: a truncated tail remains unverifiable for completeness`, () => ok(replay(lines.slice(0, 2))));
    const tampered = JSON.parse(lines[1]); tampered.payload.decision = 'deny';
    check(`${plugin}: changing signed content fails verification`, () => assert.equal(replay([lines[0], JSON.stringify(tampered), lines[2]]).status, 1));
    check(`${plugin}: malformed JSON fails verification`, () => assert.equal(replay([lines[0], '{', lines[2]]).status, 1));
    check(`${plugin}: invalid stdin creates no invented receipt`, () => {
      const badDir = join(work, `${plugin}-invalid`);
      quiet(hook('{', { [`${prefix}_RECEIPTS`]: badDir }), 1);
      assert.equal(existsSync(join(badDir, 'receipts.jsonl')), false);
    });
    check(`${plugin}: missing key fails with empty stdout and a diagnostic`, () => {
      const result = hook(event, { [`${prefix}_KEY`]: join(work, 'missing-key'), [`${prefix}_RECEIPTS`]: join(work, `${plugin}-unsigned`) });
      quiet(result, 1); assert.match(result.stderr, /no persisted signed receipt confirmed/);
    });
    check(`${plugin}: receipts path file fails without changing existing data`, () => {
      const blocked = join(work, `${plugin}-blocked`);
      writeFileSync(blocked, 'sentinel');
      const result = hook(event, { [`${prefix}_RECEIPTS`]: blocked });
      quiet(result, 1); assert.match(result.stderr, /no persisted signed receipt confirmed/);
      assert.equal(readFileSync(blocked, 'utf8'), 'sentinel');
    });
    check(`${plugin}: unreadable log is archived before starting a fresh chain`, () => {
      const recovered = join(work, `${plugin}-recovered`);
      mkdirSync(recovered); mkdirSync(join(recovered, 'receipts.jsonl'));
      writeFileSync(join(recovered, 'receipts.jsonl', 'sentinel'), 'preserve me');
      const result = hook(event, { [`${prefix}_RECEIPTS`]: recovered });
      quiet(result); assert.match(result.stderr, /moved to .*corrupt-.*new chain/);
      const archive = readdirSync(recovered).find(name => name.startsWith('receipts.jsonl.corrupt-'));
      assert.ok(archive); assert.equal(readFileSync(join(recovered, archive, 'sentinel'), 'utf8'), 'preserve me');
      ok(verify(join(recovered, 'receipts.jsonl')));
    });
    const fake = join(work, `${plugin}-fakebin`); mkdirSync(fake);
    for (const [label, script, status] of [
      ['signer failure', 'echo signer-failed >&2\nexit 42', 42],
      ['empty summary', 'exit 0', 1],
      ['malformed summary', 'printf "not-json"', 1],
      ['unsigned summary', 'printf \'{"signed":false}\'', 1],
      ['unpersisted signed summary', 'printf \'{"signed":true,"request_id":"missing-receipt"}\'', 1]
    ]) {
      writeFileSync(join(fake, 'npx'), `#!/bin/sh\n${script}\n`); chmodSync(join(fake, 'npx'), 0o755);
      check(`${plugin}: ${label} propagates without stdout`, () => {
        const result = hook(event, { PATH: `${fake}:${process.env.PATH}` });
        quiet(result, status);
        assert.match(result.stderr, status === 42 ? /signer-failed/ : /no persisted signed receipt confirmed/);
      });
    }
    // A real second append can finish before the first signer returns its summary.
    writeFileSync(join(fake, 'npx'), `#!/usr/bin/env node
const { spawnSync } = require('node:child_process');
const args = process.argv.slice(2);
const env = { ...process.env, PATH: process.env.HOOK_TEST_REAL_PATH };
const first = spawnSync('npx', args, { encoding: 'utf8', env, input: '', timeout: 30000 });
if (first.status !== 0) { process.stderr.write(first.stderr || 'first signer failed'); process.exit(first.status || 1); }
const second = spawnSync('npx', args, { encoding: 'utf8', env, input: '', timeout: 30000 });
if (second.status !== 0) { process.stderr.write(second.stderr || 'second signer failed'); process.exit(second.status || 1); }
process.stdout.write(first.stdout);
`);
    check(`${plugin}: correlated readback accepts a receipt before a later real append`, () => {
      const concurrent = join(work, `${plugin}-concurrent`);
      quiet(hook(event, { PATH: `${fake}:${process.env.PATH}`, HOOK_TEST_REAL_PATH: process.env.PATH, [`${prefix}_RECEIPTS`]: concurrent }));
      assert.equal(readFileSync(join(concurrent, 'receipts.jsonl'), 'utf8').trim().split('\n').length, 2);
    });
    check(`${plugin}: signing preserves the existing key`, () => assert.equal(readFileSync(key, 'utf8'), originalKey));
  }

  // Migration uses the old released signer with the same key; no synthetic signatures.
  const mixedDir = join(work, 'mixed');
  for (let i = 0; i < 3; i++) ok(npm('protect-mcp@0.7.4', ['sign', '--tool', 'Read', '--key', key, '--receipts', mixedDir]));
  const mixedLog = join(mixedDir, 'receipts.jsonl');
  check('0.11.1 verifies legacy 0.7.4 receipts with the independent key', () => ok(verify(mixedLog)));
  ok(npm('protect-mcp@0.32.4', ['sign', '--tool', 'Read', '--key', key, '--receipts', mixedDir]));
  check('0.11.1 verifies the mixed legacy and modern log', () => ok(verify(mixedLog)));
  const mixed = readFileSync(mixedLog, 'utf8').trim().split('\n');
  check('first modern receipt links to the last legacy receipt', () => assert.match(JSON.parse(mixed[3]).payload.previousReceiptHash, /^sha256:[0-9a-f]{64}$/));
  writeFileSync(mixedLog, [mixed[0], mixed[2], mixed[3]].join('\n') + '\n');
  check('interior legacy deletion remains undetected by chain replay', () => ok(verify(mixedLog)));
  writeFileSync(mixedLog, [mixed[1], mixed[0], mixed[2], mixed[3]].join('\n') + '\n');
  check('legacy reordering remains undetected by chain replay', () => ok(verify(mixedLog)));
  console.log(`${passed} passed, 0 failed`);
} finally { rmSync(work, { recursive: true, force: true }); }
