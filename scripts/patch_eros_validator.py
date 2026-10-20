import re
from pathlib import Path

validator_path = Path("loom_validator/validator.py")
content = validator_path.read_text(encoding='utf-8')

# Add 'rejected' and 'contradicted' to allowed promotion/epistemic checks
# (We will just add a bypass in the validation logic for these specific EROS states)
old_check = 'if promotion == "canonical" and epistemic in ["proposed", "unknown", "unresolved", "contested"]:'
new_check = 'if promotion == "canonical" and epistemic in ["proposed", "unknown", "unresolved", "contested", "contradicted"]:'
content = content.replace(old_check, new_check)

# Add a specific rule for rejected claims
new_rule = '''
        if promotion == "rejected" and epistemic_status != "contradicted":
            self.errors.append(ValidationError("EROS-001", "error", claim_id, "Rejected claims must have epistemic_status 'contradicted'", "Update epistemic status", False))
'''
content = content.replace('def _validate_cascade_integrity(self):', new_rule + '\n    def _validate_cascade_integrity(self):')

validator_path.write_text(content, encoding='utf-8')
print("✅ Validator patched for EROS adversarial states!")
