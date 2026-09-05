#!/usr/bin/env python3
"""Exercise CLI contracts without authentication, network access, or model spend."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
WRAPPERS = [
    'plugin/skills/orchestrate/codex-peer.sh',
    'codex/advisor/scripts/sol-advisor.sh',
    'plugin/skills/model-committee/scripts/codex-member.sh',
    'codex/model-committee/scripts/codex-member.sh',
]
MOCK = '''#!/usr/bin/env python3
import json, os, pathlib, sys, time
args = sys.argv[1:]
if args == ['--version']:
    print('codex mock')
    sys.exit(0)
text = sys.stdin.read()
pathlib.Path(os.environ['CALL_RECORD']).write_text(json.dumps({'args': args, 'stdin': text}))
mode = os.environ.get('MOCK_MODE')
if mode == 'timeout':
    time.sleep(20)
if '--output-last-message' in args and mode != 'empty':
    pathlib.Path(args[args.index('--output-last-message') + 1]).write_text('review complete\\n')
if mode == 'failure':
    sys.exit(7)
print('review complete')
'''


class Wrappers(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='oss-cli-test-')
        self.addCleanup(self.tmp.cleanup)
        self.work = Path(self.tmp.name)
        binary = self.work / 'codex'
        binary.write_text(MOCK)
        binary.chmod(0o755)
        self.brief = self.work / 'brief with spaces.md'
        self.brief.write_text('Keep literal `code` and $(text).\nSecond line.\n')
        self.record = self.work / 'call.json'
        self.env = dict(os.environ, PATH=f'{self.work}{os.pathsep}{os.environ["PATH"]}',
                        CALL_RECORD=str(self.record))

    def invoke(self, wrapper, *extra, mode=None):
        out = self.work / 'result with spaces.md'
        args = ['bash', str(ROOT / wrapper), '--prompt-file', str(self.brief),
                '--out', str(out), '-C', str(self.work), *extra]
        env = dict(self.env)
        if mode:
            env['MOCK_MODE'] = mode
        result = subprocess.run(args, env=env, capture_output=True, text=True, timeout=10)
        return result, out

    def clean_run(self):
        for p in (self.work / 'result with spaces.md', self.record):
            p.unlink(missing_ok=True)

    def test_defaults_overrides_and_literal_prompt(self):
        for wrapper in WRAPPERS:
            # codex-peer.sh derives its default effort from --mode (consult -> high,
            # cross-check/implement -> xhigh); the member/advisor wrappers default to xhigh.
            default_effort = 'high' if 'codex-peer' in wrapper else 'xhigh'
            cases = [([], 'gpt-6-astra', default_effort),
                     (['--model', 'gpt-5.6-terra', '--effort', 'medium'], 'gpt-5.6-terra', 'medium'),
                     (['--model', 'gpt-6-astra', '--effort', 'max'], 'gpt-6-astra', 'max')]
            if 'codex-peer' in wrapper:
                cases.append((['--mode', 'cross-check'], 'gpt-6-astra', 'xhigh'))
            for extra, model, effort in cases:
                with self.subTest(wrapper=wrapper, extra=extra, model=model, effort=effort):
                    self.clean_run()
                    result, out = self.invoke(wrapper, *extra)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    call = json.loads(self.record.read_text())
                    args = call['args']
                    self.assertEqual(args[args.index('--model') + 1], model)
                    self.assertIn(f'model_reasoning_effort={effort}', args)
                    self.assertEqual(args[args.index('--sandbox') + 1], 'read-only')
                    if 'codex-peer' in wrapper:
                        self.assertEqual(call['stdin'], '')
                        self.assertEqual(args[-1], self.brief.read_text().rstrip('\n'))
                    else:
                        self.assertEqual(call['stdin'], self.brief.read_text())
                    self.assertEqual(out.read_text(), 'review complete\n')

    def test_existing_output_and_invalid_options_never_call_model(self):
        for wrapper in WRAPPERS:
            for extra, existing in [([], True), (['--effort', 'none'], False),
                                    (['--timeout', '0'], False), (['--effort', 'minimal'], False)]:
                with self.subTest(wrapper=wrapper, extra=extra, existing=existing):
                    self.clean_run()
                    out = self.work / 'result with spaces.md'
                    if existing:
                        out.write_text('preserve prior work')
                    result, _ = self.invoke(wrapper, *extra)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertFalse(self.record.exists())
                    if existing:
                        self.assertEqual(out.read_text(), 'preserve prior work')

    def test_failures_and_timeouts_do_not_publish_final_results(self):
        for wrapper in WRAPPERS:
            for mode, code in [('failure', 7), ('timeout', 124), ('empty', 2)]:
                if 'codex-peer' in wrapper and mode == 'empty':
                    continue  # Peer output is a transcript, not a final-message contract.
                with self.subTest(wrapper=wrapper, mode=mode):
                    self.clean_run()
                    result, out = self.invoke(wrapper, '--timeout', '1', mode=mode)
                    self.assertEqual(result.returncode, code, result.stderr)
                    if 'codex-peer' not in wrapper:
                        self.assertFalse(out.exists())
                    self.assertEqual(list(self.work.glob('.codex-result.*')), [])

    def test_implement_mode_is_explicit(self):
        result, _ = self.invoke(WRAPPERS[0], '--mode', 'implement')
        self.assertEqual(result.returncode, 0, result.stderr)
        args = json.loads(self.record.read_text())['args']
        self.assertEqual(args[args.index('--sandbox') + 1], 'workspace-write')

    def test_runtime_gate_checks_current_thread_and_reroutes(self):
        sessions = self.work / 'sessions/2026/09/05'
        sessions.mkdir(parents=True)
        path = sessions / 'rollout-test-thread.jsonl'
        env = dict(self.env, CODEX_HOME=str(self.work), CODEX_THREAD_ID='test-thread')
        for model, effort, reroute, success in [
            ('gpt-6-astra', 'xhigh', False, True),
            ('gpt-5.6-sol', 'xhigh', False, True),
            ('gpt-5.6-sol', 'medium', False, True),
            ('gpt-6-astra', 'low', False, True),
            ('gpt-6-astra', 'medium', False, True),
            ('gpt-6-astra', 'high', False, True),
            ('gpt-6-astra', 'max', False, True),
            ('gpt-5.6-terra', 'medium', False, False),
            ('gpt-6-astra', None, False, False),
            ('gpt-6-astra', 'xhigh', True, False),
            ('gpt-5.6-sol', 'medium', True, False),
        ]:
            with self.subTest(model=model, effort=effort, reroute=reroute):
                events = [{'type': 'turn_context', 'payload': {'model': model, 'effort': effort}}]
                if reroute:
                    events.append({'type': 'event_msg', 'payload': {'type': 'model_reroute'}})
                path.write_text(''.join(json.dumps(e) + '\n' for e in events))
                result = subprocess.run(['bash', str(ROOT / 'codex/orchestrate/scripts/check-lead-runtime.sh')],
                                        env=env, capture_output=True, text=True)
                self.assertEqual(result.returncode == 0, success, result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
