import tempfile
import unittest
from pathlib import Path

from imei_validation_claim_audit.audit import audit, claims, evidence, main
from imei_validation_claim_audit.phrases import IMEIVALIDATION, NOIMEIVALIDATION, GENERIC_NAMES


class AuditTests(unittest.TestCase):
    def test_phrases(self):
        for phrase in IMEIVALIDATION:
            with self.subTest(phrase=phrase):
                self.assertTrue(claims(phrase)[0])
        for phrase in NOIMEIVALIDATION:
            with self.subTest(phrase=phrase):
                yes, no = claims(phrase)
                self.assertFalse(yes)
                self.assertTrue(no)
        self.assertEqual(claims('```\nvalidate imei\n```'), (set(), set()))
        self.assertTrue(claims('`validate-imei`')[0])

    def test_library_routes(self):
        for name in ('validate', 'is_valid', 'imei_type'):
            for source in ('from stdnum.imei import {0}\n{0}(x)',
                           'from stdnum.imei import {0} as v\nv(x)',
                           'import stdnum.imei\nstdnum.imei.{0}(x)',
                           'import stdnum.imei as im\nim.{0}(x)',
                           'from stdnum import imei\nimei.{0}(x)',
                           'import stdnum\nstdnum.imei.{0}(x)'):
                with self.subTest(name=name, source=source):
                    self.assertTrue(evidence(source.format(name)))

    def test_generic_routes(self):
        for name in GENERIC_NAMES:
            for source in ('obj.{0}(x)', 'from lib import {0}\n{0}(x)',
                           'from lib import {0} as f\nf(x)', 'obj = thing()\nobj.{0}(x)'):
                with self.subTest(name=name, source=source):
                    self.assertTrue(evidence(source.format(name)))

    def test_not_evidence(self):
        sources = ['import stdnum.imei', 'validate(x)', 'is_valid(x)', 'imei_type(x)',
                   'imei(x)', 'compact(x)', 'format(x)', 'split(x)', 'validate_imei(x)',
                   'obj.validate(x)', 'obj.is_valid(x)', 'obj.imei_type(x)',
                   'obj.imei(x)', 'obj.compact(x)', 'obj.format(x)', 'obj.split(x)',
                   'import stdnum.imei\nstdnum.imei.compact(x)',
                   'import stdnum.imei\nstdnum.imei.format(x)',
                   'import stdnum.imei\nstdnum.imei.split(x)',
                   'from stdnum import luhn\nluhn.validate(x)',
                   'from stdnum import luhn\nluhn.calc_check_digit(x)',
                   'import re\nre.match("[0-9]+", x)', 'import re\nre.search("x", x)',
                   'import re\nre.fullmatch("x", x)', 'len(x) == 15', 'x[:8] in tac',
                   'obj.validate_meid(x)', 'obj.validate_esn(x)', 'obj.lookup_imei(x)',
                   'import validators\nvalidators.imei(x)', '"validate imei"',
                   '# imei validation', 'obj.validate_imei', 'def broken(:',
                   'import subprocess\nsubprocess.run(["imei-checker"])',
                   'from stdnum.imei import validate\ndef validate(x): pass\nvalidate(x)',
                   'import stdnum.imei as im\nim = other\nim.validate(x)',
                   'from lib import validate_imei as v\nwith obj as v: pass\nv(x)',
                   'def validate_imei(x): pass\nobj.validate_imei(x)']
        for source in sources:
            with self.subTest(source=source):
                self.assertFalse(evidence(source))

    def test_findings_and_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'README.md').write_text('validate imei')
            self.assertEqual(audit(root)[0]['severity'], 'HIGH')
            (root / 'tests').mkdir()
            (root / 'tests/test_x.py').write_text('obj.validate_imei(x)')
            self.assertEqual(audit(root)[0]['severity'], 'MEDIUM')
            self.assertEqual(main(['audit', tmp]), 0)
            self.assertEqual(main(['audit', tmp, '--fail-on', 'medium']), 2)
            (root / 'app.py').write_text('obj.validate_imei(x)')
            self.assertFalse(audit(root))
            (root / 'README.md').write_text('does not validate imei')
            self.assertEqual(audit(root)[0]['id'], 'documented-no-imei-validation-claim-false')
            self.assertFalse(audit(root, ['app.py']))
            self.assertEqual(main(['audit', str(root / 'missing')]), 1)

    def test_exclusions_and_self_audit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'README.md').write_text('validate imei')
            for folder in ('docs', 'fixtures', 'examples'):
                (root / folder).mkdir()
                (root / folder / 'x.py').write_text('obj.validate_imei(x)')
            self.assertEqual(audit(root)[0]['severity'], 'HIGH')
        self.assertFalse(audit(Path(__file__).resolve().parents[1]))


if __name__ == '__main__':
    unittest.main()
