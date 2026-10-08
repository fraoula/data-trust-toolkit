import importlib.util
from pathlib import Path
import unittest
MODULE_PATH=Path(__file__).resolve().parents[1]/"drift_guard.py"
SPEC=importlib.util.spec_from_file_location("drift_guard",MODULE_PATH)
drift_guard=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(drift_guard)
class DriftGuardTests(unittest.TestCase):
    def test_removed(self):
        b,w,s=drift_guard.compare_schemas({'id':'integer','status':'string'},{'id':'integer'})
        self.assertIn('Required field removed: status',b)
    def test_type_change(self):
        b,_,_=drift_guard.compare_schemas({'customer_id':'integer'},{'customer_id':'string'})
        self.assertIn('customer_id: integer → string',b)
    def test_sensitive_warning(self):
        b,w,s=drift_guard.compare_schemas({'id':'integer'},{'id':'integer','ssn':'string'})
        self.assertFalse(b); self.assertIn('New sensitive field detected: ssn',w)
    def test_safe_add(self):
        b,w,s=drift_guard.compare_schemas({'id':'integer'},{'id':'integer','nickname':'string'})
        self.assertFalse(b); self.assertFalse(w); self.assertIn('Optional field added: nickname',s)
    def test_risk_cap(self):
        self.assertEqual(drift_guard.calculate_risk(['x']*10,['y']*10),100)
    def test_status(self):
        self.assertEqual(drift_guard.determine_status(['x'],['y']),'FAIL')
        self.assertEqual(drift_guard.determine_status([],['y']),'WARN')
        self.assertEqual(drift_guard.determine_status([],[]),'PASS')
if __name__=='__main__': unittest.main()
