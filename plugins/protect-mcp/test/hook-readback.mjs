#!/usr/bin/env node
// Focused receipt-confirmation I/O tests. These fixtures test shape/correlation,
// not signatures; hook-migration.mjs covers the real released signers/verifier.
import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync, writeFileSync, mkdirSync, chmodSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, resolve, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const repo = resolve(dirname(fileURLToPath(import.meta.url)), '../../..');
const work = mkdtempSync(join(tmpdir(), 'protect-hook-readback-'));
const chunkSize = 64 * 1024;
const requestId = 'readback-test-request';
let passed = 0;
function receipt(tool = 'Read', padding = '') {
  return Buffer.from(JSON.stringify({
    payload: { request_id: requestId, padding, tool_name: tool },
    signature: { alg: 'EdDSA', sig: 'a'.repeat(128) }
  }) + '\n');
}
function laterLine(length) {
  const empty = JSON.stringify({ later: '' }) + '\n';
  return Buffer.from(JSON.stringify({ later: 'x'.repeat(length - Buffer.byteLength(empty)) }) + '\n');
}

try {
  const fake = join(work, 'bin'); mkdirSync(fake);
  writeFileSync(join(fake, 'npx'), `#!/bin/sh\nprintf '%s' '{"signed":true,"request_id":"${requestId}"}'\n`);
  chmodSync(join(fake, 'npx'), 0o755);
  // Observe only the readback log descriptor, and inject filesystem races/errors.
  // The parser process never opens this path, so it cannot overwrite the metrics.
  const preload = join(work, 'observe.cjs');
  writeFileSync(preload, `
const fs = require('node:fs');
const path = require('node:path');
const original = { open: fs.openSync, stat: fs.fstatSync, read: fs.readSync, close: fs.closeSync };
let target;
const metrics = { reads: [], stats: 0, closes: 0 };
fs.openSync = function(file, ...args) {
  const fd = original.open.call(this, file, ...args);
  if (typeof file === 'string' && path.resolve(file) === process.env.READBACK_LOG) target = fd;
  return fd;
};
fs.fstatSync = function(fd, ...args) {
  if (fd !== target) return original.stat.call(this, fd, ...args);
  metrics.stats++;
  if (process.env.READBACK_FAULT === 'stat') throw new Error('injected stat error');
  const stat = original.stat.call(this, fd, ...args);
  metrics.snapshot = stat.size;
  if (process.env.READBACK_APPEND) fs.appendFileSync(process.env.READBACK_LOG, Buffer.from(process.env.READBACK_APPEND, 'base64'));
  return stat;
};
fs.readSync = function(fd, buffer, offset, length, position) {
  if (fd !== target) return original.read.call(this, fd, buffer, offset, length, position);
  if (process.env.READBACK_FAULT === 'read') throw new Error('injected read error');
  const requested = process.env.READBACK_FAULT === 'short' ? Math.max(0, length - 1) : length;
  const bytes = original.read.call(this, fd, buffer, offset, requested, position);
  metrics.reads.push({ length, position, bytes });
  return bytes;
};
fs.closeSync = function(fd, ...args) {
  if (fd === target) metrics.closes++;
  return original.close.call(this, fd, ...args);
};
process.on('exit', () => {
  if (target !== undefined) fs.writeFileSync(process.env.READBACK_METRICS, JSON.stringify(metrics));
});
`);

  for (const [plugin, prefix] of [['protect-mcp', 'PROTECT_MCP'], ['review-agent-governance', 'REVIEW_GOVERNANCE']]) {
    const root = join(repo, 'plugins', plugin);
    const command = JSON.parse(readFileSync(join(root, 'hooks/hooks.json'), 'utf8')).hooks.PostToolUse[0].hooks[0].command;
    let sequence = 0;
    function check(label, bytes, { status = 0, tool = 'Read', fault = '', append, inspect = () => {} } = {}) {
      const directory = join(work, `${plugin}-${sequence++}`); mkdirSync(directory);
      const log = join(directory, 'receipts.jsonl'); writeFileSync(log, bytes);
      const metricsFile = join(directory, 'metrics.json');
      const result = spawnSync('bash', ['-c', command], {
        cwd: work, encoding: 'utf8', timeout: 10000,
        input: JSON.stringify({ tool_name: tool, tool_input: {} }),
        env: {
          ...process.env, CLAUDE_PLUGIN_ROOT: root, PATH: `${fake}:${process.env.PATH}`,
          [`${prefix}_RECEIPTS`]: directory,
          NODE_OPTIONS: `${process.env.NODE_OPTIONS || ''} --require "${preload}"`,
          READBACK_LOG: log, READBACK_METRICS: metricsFile, READBACK_FAULT: fault,
          READBACK_APPEND: append ? append.toString('base64') : ''
        }
      });
      assert.equal(result.status, status, `${label}: ${result.stderr || result.error?.message}`);
      assert.equal(result.stdout, '', `${label}: stdout must remain empty`);
      if (status) assert.match(result.stderr, /no persisted signed receipt confirmed/);
      const metrics = JSON.parse(readFileSync(metricsFile, 'utf8'));
      assert.equal(metrics.stats, 1, 'take one size snapshot');
      assert.equal(metrics.closes, 1, 'close the log descriptor on every outcome');
      for (const read of metrics.reads) assert.ok(read.position + read.length <= metrics.snapshot, 'never read beyond the snapshot');
      inspect(metrics);
      passed++;
      console.log(`PASS: ${plugin}: ${label}`);
    }

    const own = receipt();
    const prefixBytes = Buffer.from('{"old":true}\n'.repeat(700000));
    check('recent match reads only one chunk despite a multi-megabyte prefix', Buffer.concat([prefixBytes, own]), {
      inspect: metrics => {
        assert.equal(metrics.reads.length, 1);
        assert.equal(metrics.reads[0].bytes, chunkSize);
      }
    });
    check('receipt beginning exactly at a chunk boundary is reconstructed', Buffer.concat([
      Buffer.from('{"old":true}\n'), own, laterLine(chunkSize - own.length)
    ]), { inspect: metrics => assert.equal(metrics.reads.length, 2) });

    const unicode = receipt('Read🚀', 'x'.repeat(chunkSize + 321));
    const split = unicode.indexOf(Buffer.from('🚀')) + 2;
    const suffix = laterLine(split + chunkSize - unicode.length);
    check('multi-chunk receipt preserves a UTF-8 character split between reads', Buffer.concat([unicode, suffix]), {
      tool: 'Read🚀', inspect: metrics => assert.ok(metrics.reads.length >= 3)
    });
    check('complete receipt before a partial concurrent line still matches', Buffer.concat([own, Buffer.from('{"payload":{"request_id":')]));
    check('unterminated matching JSON alone does not count as an appended line', own.subarray(0, own.length - 1), { status: 1 });
    check('later append after snapshot cannot hide an existing receipt', own, { append: laterLine(100) });
    check('matching receipt appended only after snapshot is ignored', Buffer.from('{"old":true}\n'), { append: own, status: 1 });
    check('unrelated receipts cannot satisfy the request id', Buffer.from(own.toString().replace(requestId, 'other-request')), { status: 1 });
    check('empty log fails and closes its descriptor', Buffer.alloc(0), { status: 1 });
    for (const fault of ['stat', 'read', 'short']) check(`${fault} failure closes the descriptor and stays silent`, own, { fault, status: 1 });
  }
  console.log(`${passed} passed, 0 failed`);
} finally { rmSync(work, { recursive: true, force: true }); }
