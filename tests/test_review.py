import importlib.util
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("review", Path(__file__).parents[1] / "scripts/review.py")
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)

class ReviewTests(unittest.TestCase):
    def test_changed_number_and_link(self):
        self.assertEqual(len(r.audit("Cena 900 Kč https://a.example", "Cena 90 Kč https://b.example")), 2)
    def test_duplicate_number_removed(self):
        self.assertTrue(r.audit("2 kusy, 2 barvy", "2 kusy, barvy"))
    def test_unchanged_facts(self):
        self.assertEqual(r.audit("Cena je 900 Kč.", "Zaplatíte 900 Kč."), [])
    def test_empty_or_wrong_response(self):
        for value in [{}, {"revised_text": "", "changes": [], "questions": []}, {"revised_text":"X", "changes":"X", "questions":[]}]:
            with self.assertRaises(ValueError): r.validate(value)
    def test_transport_and_no_thought_in_output(self):
        reply = {"revised_text":"Cena je 900 Kč.", "changes":[], "questions":[]}
        response = {"candidates":[{"finishReason":"STOP", "content":{"parts":[{"thought":True,"text":"internal"},{"text":json.dumps(reply)}]}}]}
        with patch.object(r, "urlopen", return_value=io.BytesIO(json.dumps(response).encode())) as call:
            self.assertEqual(r.fetch("Cena 900 Kč", "vykání", "example-model", "synthetic-key"), reply)
            req = call.call_args.args[0]
            self.assertNotIn("synthetic-key", req.full_url)
            self.assertEqual(req.get_header("X-goog-api-key"), "synthetic-key")
    def test_truncated_response_rejected(self):
        with patch.object(r, "urlopen", return_value=io.BytesIO(b'{"candidates":[{"finishReason":"MAX_TOKENS"}]}')):
            with self.assertRaises(ValueError): r.fetch("X", "zachovat", "example-model", "synthetic-key")

if __name__ == "__main__": unittest.main()
