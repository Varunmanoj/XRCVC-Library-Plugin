import importlib.util
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ReleaseHelpersTest(unittest.TestCase):
    def test_cachebuster_uses_canonical_version_utc_and_preserves_identity(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            (root / ".codex-plugin").mkdir()
            (root / "plugin.json").write_text(json.dumps({"version": "1.0.4"}))
            path = root / ".codex-plugin/plugin.json"
            original = {"name": "registered-identity", "version": "1.0.3+codex.20260924150222", "apps": "./.app.json", "interface": {"displayName": "XRCVC Library"}}
            path.write_text(json.dumps(original))
            now = datetime(2026, 10, 6, 16, 28, 2, tzinfo=timezone(timedelta(hours=5, minutes=30)))
            version = load("refresh_codex_cachebuster").refresh(root, now)
            self.assertEqual(version, "1.0.4+codex.20261006105802")
            self.assertEqual(json.loads(path.read_text()), {**original, "version": version})

    def test_invalid_release_version_does_not_modify_host_manifest(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            (root / ".codex-plugin").mkdir()
            (root / "plugin.json").write_text(json.dumps({"version": "1.0.4+wrong"}))
            path = root / ".codex-plugin/plugin.json"
            path.write_text('{"name":"preserve-me"}')
            with self.assertRaises(ValueError):
                load("refresh_codex_cachebuster").refresh(root)
            self.assertEqual(path.read_text(), '{"name":"preserve-me"}')

    def test_live_contract_detects_missing_tools_and_changed_mutation_hints(self):
        validator = load("validate_live_contract").validate
        annotations = {"readOnlyHint": False, "openWorldHint": False, "destructiveHint": True}
        submission = {"tools": {"update_member_profile": {"annotations": annotations}}}
        response = {"result": {"tools": [{"name": "update_member_profile", "annotations": annotations.copy()}]}}
        self.assertEqual(validator(submission, response), {"tools": 1, "mutations": 1})
        response["result"]["tools"][0]["annotations"]["destructiveHint"] = False
        with self.assertRaises(ValueError):
            validator(submission, response)
        with self.assertRaises(ValueError):
            validator(submission, {"result": {"tools": []}})


if __name__ == "__main__":
    unittest.main()
