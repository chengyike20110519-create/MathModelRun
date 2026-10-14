"""Long-lived CLI contract tests; fake files are not scientific/visual reviews.

Every artifact and review below is an isolated schema fixture. Passing these
tests verifies gate behavior only, not an actual figure's truth or aesthetics.
Run with: python -m unittest discover -s tests -p test_figure_gate.py -v
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "my-mathmodel-agent" / "scripts" / "figure_gate.py"
BASE_ROLES = ["spec", "caption", "image", "final_size_preview", "grayscale_preview"]
SCIENTIFIC_CHECKS = {
    "data": ["sources_values", "units_estimators", "encoding_fit",
             "uncertainty_sampling", "transforms_missingness"],
    "workflow": ["labels_exact", "nodes_edges_exact", "sequence_feedback",
                 "claims_match_model"],
}
VISUAL_CHECKS = ["final_size_grayscale", "hierarchy_alignment", "labels_overlap"]


class FigureGateContractTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="figure-gate-unittest-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}

    def read(self, path):
        return json.loads(path.read_text(encoding="utf-8"))

    def write(self, path, value):
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

    def fixture(self, name="case", *, kind="data", scope="standalone", omit=()):
        directory = self.root / name
        directory.mkdir()
        roles = BASE_ROLES + (["data", "code", "vector"] if kind == "data" else ["model"])
        if scope == "paper":
            roles += ["paper_source", "paper_pdf", "rendered_page"]
        files = []
        for role in roles:
            if role in omit:
                continue
            artifact = directory / (role + ".fixture")
            artifact.write_text("Nonempty schema fixture: " + role + "\n", encoding="utf-8")
            files.append({"role": role, "path": artifact.name, "sha256": "old-fixture-hash"})
        reviews = {}
        for category, keys in (("scientific", SCIENTIFIC_CHECKS[kind]),
                               ("visual", VISUAL_CHECKS)):
            reviews[category] = {
                "status": "pass", "reviewer": "independent-fixture-reviewer",
                "fingerprint": "old-fixture-fingerprint",
                "checks": {key: {"status": "pass", "evidence": "Synthetic contract-test evidence only."}
                           for key in keys},
            }
        reviews["visual"]["scores"] = {key: 4 for key in
                                             ("hierarchy", "readability", "comparison", "finish")}
        case = {"kind": kind, "scope": scope, "builder": "fixture-builder",
                "files": files, "mechanical_warnings": [], "warning_resolutions": {},
                "reviews": reviews}
        path = directory / "CASE.json"
        self.write(path, case)
        return path

    def cli(self, action, path):
        process = subprocess.run([sys.executable, str(SCRIPT), action, str(path)],
                                 cwd=self.root, env=self.environment,
                                 capture_output=True, text=True, timeout=30)
        self.assertEqual(process.stderr, "", "CLI should return friendly JSON, not a traceback")
        result = json.loads(process.stdout)
        self.assertEqual(process.returncode, 1 if result["verdict"] == "fail" else 0)
        return result

    def record_fixture_reviews(self, path):
        """Declare synthetic pass metadata to test the validator, not an actual review."""
        case = self.read(path)
        for review in case["reviews"].values():
            review["status"] = "pass"
            review["fingerprint"] = case["fingerprint"]
            for check in review["checks"].values():
                check["status"] = "pass"
        self.write(path, case)

    def completed_fixture(self, name="complete", **kwargs):
        path = self.fixture(name, **kwargs)
        self.assertEqual(self.cli("seal", path)["verdict"], "sealed")
        self.record_fixture_reviews(path)
        return path

    def assert_error(self, result, text):
        self.assertEqual(result["verdict"], "fail")
        self.assertTrue(any(text in error for error in result["errors"]), result)

    def test_seal_resets_reviews_and_pending_blocks(self):
        path = self.fixture()
        self.assertEqual(self.cli("seal", path)["verdict"], "sealed")
        case = self.read(path)
        for review in case["reviews"].values():
            self.assertEqual(review["status"], "pending")
            self.assertEqual(review["fingerprint"], "")
            for check in review["checks"].values():
                self.assertEqual(check["status"], "pending")
                self.assertEqual(check["evidence"], "Synthetic contract-test evidence only.")
        self.assertEqual(case["reviews"]["visual"]["scores"]["finish"], 4)
        self.assert_error(self.cli("check", path), "status is not pass")
        # Even sealing unchanged, previously reviewed files requires fresh review.
        self.record_fixture_reviews(path)
        self.assertEqual(self.cli("check", path)["verdict"], "pass")
        self.cli("seal", path)
        self.assert_error(self.cli("check", path), "status is not pass")

    def test_complete_independent_data_and_workflow_records_pass(self):
        for kind, scope in (("data", "standalone"), ("workflow", "paper")):
            with self.subTest(kind=kind, scope=scope):
                path = self.completed_fixture(kind, kind=kind, scope=scope)
                result = self.cli("check", path)
                self.assertEqual(result["verdict"], "pass")
                self.assertEqual(result["errors"], [])

    def test_changed_image_invalidates_hash_and_reviews(self):
        path = self.completed_fixture()
        (path.parent / "image.fixture").write_text("Changed after fixture review\n", encoding="utf-8")
        result = self.cli("check", path)
        self.assert_error(result, "stale or missing sha256")
        self.assert_error(result, "fingerprint is missing or stale")
        self.assert_error(result, "reviews.visual.fingerprint is missing or stale")

    def test_builder_cannot_review_own_artifact(self):
        for category in ("scientific", "visual"):
            with self.subTest(category=category):
                path = self.completed_fixture(category)
                case = self.read(path)
                case["reviews"][category]["reviewer"] = " FIXTURE-BUILDER "
                self.write(path, case)
                self.assert_error(self.cli("check", path), category + ".reviewer must differ from builder")

    def test_missing_vector_and_paper_page_block(self):
        for scope, role in (("standalone", "vector"), ("paper", "rendered_page")):
            with self.subTest(scope=scope, role=role):
                path = self.completed_fixture(scope, scope=scope, omit=[role])
                self.assert_error(self.cli("check", path), "Missing required file role: " + role)

    def test_unresolved_hard_defect_cannot_be_accepted(self):
        path = self.completed_fixture()
        case = self.read(path)
        for status in ("pending", "accepted"):
            with self.subTest(status=status):
                case["issues"] = [{"severity": "hard", "status": status,
                                   "rationale": "Acceptance must not bypass a hard defect."}]
                self.write(path, case)
                self.assert_error(self.cli("check", path), "hard issue must be resolved")
        case["issues"][0]["status"] = "resolved"
        self.write(path, case)
        self.assertEqual(self.cli("check", path)["verdict"], "pass")

    def test_same_resolved_file_cannot_fill_multiple_evidence_roles(self):
        for alias_type in ("relative", "absolute", "symlink"):
            with self.subTest(alias=alias_type):
                path = self.completed_fixture(alias_type)
                case = self.read(path)
                image = path.parent / "image.fixture"
                if alias_type == "relative":
                    alias = "./image.fixture"
                elif alias_type == "absolute":
                    alias = str(image.resolve())
                else:
                    link = path.parent / "image-alias.fixture"
                    link.symlink_to(image.name)
                    alias = link.name
                vector = next(record for record in case["files"] if record["role"] == "vector")
                vector["path"] = alias
                self.write(path, case)
                before = path.read_bytes()
                self.assert_error(self.cli("seal", path), "duplicate physical file")
                self.assertEqual(path.read_bytes(), before)
                self.assert_error(self.cli("check", path), "duplicate physical file")

    def test_empty_file_seal_fails_without_modifying_case(self):
        path = self.fixture()
        (path.parent / "vector.fixture").write_text("", encoding="utf-8")
        before = path.read_bytes()
        self.assert_error(self.cli("seal", path), "file is empty")
        self.assertEqual(path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
