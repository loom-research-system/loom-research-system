import re
from pathlib import Path

validator_path = Path("loom_validator/validator.py")
content = validator_path.read_text(encoding='utf-8')

# 1. Add dispatch logic to validate_all
old_dispatch = 'elif obj_type == "source": self._validate_source(obj)'
new_dispatch = old_dispatch + '\n        elif obj_type == "mechanism": self._validate_mechanism(obj)\n        elif obj_type == "dependency": self._validate_dependency(obj)\n        elif obj_type == "transition": self._validate_transition(obj)'
content = content.replace(old_dispatch, new_dispatch)

# 2. Add new validation methods
new_methods = '''
    def _validate_mechanism(self, mech: dict):
        mech_id = mech["id"]
        if mech.get("effective_from") and mech.get("effective_to"):
            if mech["effective_from"] > mech["effective_to"]:
                self.errors.append(ValidationError("MECH-001", "error", mech_id, "effective_from is after effective_to", "Correct the dates", False))

    def _validate_dependency(self, dep: dict):
        dep_id = dep["id"]
        if dep.get("source_node_id") and dep["source_node_id"] not in self.objects:
            self.errors.append(ValidationError("DEP-001", "error", dep_id, f"Dependency references non-existent source node '{dep.get('source_node_id')}'", "Create source node or correct ID", False))
        if dep.get("target_node_id") and dep["target_node_id"] not in self.objects:
            self.errors.append(ValidationError("DEP-002", "error", dep_id, f"Dependency references non-existent target node '{dep.get('target_node_id')}'", "Create target node or correct ID", False))

    def _validate_transition(self, trans: dict):
        trans_id = trans["id"]
        if trans.get("target_node_id") and trans["target_node_id"] not in self.objects:
            self.errors.append(ValidationError("TRANS-001", "error", trans_id, f"Transition references non-existent target node '{trans.get('target_node_id')}'", "Create target node or correct ID", False))
        if trans.get("sequence_order") is not None and trans["sequence_order"] < 1:
            self.errors.append(ValidationError("TRANS-002", "error", trans_id, "sequence_order must be >= 1", "Update sequence order", False))

'''
content = content.replace('if __name__ == "__main__":', new_methods + '\nif __name__ == "__main__":')

validator_path.write_text(content, encoding='utf-8')
print("✅ Validator successfully patched for EROS schemas!")
