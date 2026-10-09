import yaml
import subprocess
import sys
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
FLINT_DIR = BASE_DIR / "artifacts" / "flint"
OUTPUT_FILE = FLINT_DIR / "PUBLICATION_BUNDLE_QUARTZ.md"
GITHUB_REPO = "https://github.com/loom-research-system/loom-research-system/blob/main"

def load_yaml(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"🚨 VALIDATION FAILED: Missing required artifact '{filepath.name}'.")
        print("The audit trail is incomplete. Refusing to generate publication bundle.")
        sys.exit(1)

def main():
    print("🛡️ STEP 1: Running mechanical validation (Fail-Closed Gate)...")
    
    # 1. FAIL-CLOSED GATE: Run the validator before generating anything
    result = subprocess.run(
        [sys.executable, str(BASE_DIR / "loom_validator" / "validator.py"), str(BASE_DIR)],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("🚨 VALIDATION FAILED! Refusing to generate publication bundle.")
        print("The underlying YAML artifacts contain epistemic or schema violations.")
        print("Validator output:\n", result.stdout)
        sys.exit(1)
        
    print("✅ Validation passed. Proceeding to bundle generation...\n")
    
    # 2. Load all Flint artifacts (will fail-closed gracefully if any are missing)
    src1 = load_yaml(FLINT_DIR / "SRC-FLINT-001.yaml")
    src2 = load_yaml(FLINT_DIR / "SRC-FLINT-002.yaml")
    src3 = load_yaml(FLINT_DIR / "SRC-FLINT-003.yaml")
    
    evd1 = load_yaml(FLINT_DIR / "EVD-FLINT-001.yaml")
    evd2 = load_yaml(FLINT_DIR / "EVD-FLINT-002.yaml")
    evd3 = load_yaml(FLINT_DIR / "EVD-FLINT-003.yaml")
    
    claim = load_yaml(FLINT_DIR / "CLM-FLINT-001.yaml")
    diag = load_yaml(FLINT_DIR / "DIAG-FLINT-001.yaml")
    
    evt1 = load_yaml(FLINT_DIR / "EVT-FLINT-001.yaml")
    evt2 = load_yaml(FLINT_DIR / "EVT-FLINT-002.yaml")
    evt3 = load_yaml(FLINT_DIR / "EVT-FLINT-003.yaml")
    evt4 = load_yaml(FLINT_DIR / "EVT-FLINT-004.yaml")
    evt5 = load_yaml(FLINT_DIR / "EVT-FLINT-005.yaml")
    evt6 = load_yaml(FLINT_DIR / "EVT-FLINT-006.yaml")
    
    # 3. Generate Markdown with direct GitHub links and dynamic data
    epistemic_date = claim.get('current_as_of', datetime.now().strftime('%Y-%m-%d'))
    
    md = f"""---
title: "Flint Water Crisis: Corrosion Control Failure"
date: {epistemic_date}
tags: [flint, water-crisis, validated, phase-9]
loom_spec: "PL-307 v1.0"
validation_status: "PASSED (CI-Enforced)"
---

# Flint Water Crisis Analysis
> [!abstract] Executive Summary
> **Thesis:** {diag['thesis']}  
> **Epistemic Status:** `{diag['epistemic_status'].capitalize()}` | **Audit Status:** `{diag['status'].replace('_', ' ').title()}`

This artifact represents a fully audited, multi-source analysis of the Flint Water Crisis. Every claim below is mechanically validated and backed by a cryptographic audit trail.

---

## 1. The Core Claim
**Statement:** "{claim['statement']}"

> [!check] Validation Metrics
> - **Epistemic Status:** `{claim['epistemic_status'].capitalize()}`
> - **Verification Level:** `{claim['verification_level'].replace('_', ' ').title()}`
> - **Promotion Stage:** `{claim['promotion_stage'].capitalize()}`
> - **Contradiction Status:** `{claim['contradiction_status'].capitalize()}`

---

## 2. Evidence Chain & Source Registry

### 2.1 Primary Supporting Evidence

#### Source A: {src1['title']}
> "{evd1['extracted_content']}"  
> — *{src1['publisher']}, {src1['date']}*

<details>
<summary><strong>⚙️ View Provenance & Cryptographic Hash</strong></summary>

> [!info] Raw Metadata
> - **Object ID:** [`{evd1['id']}`]({GITHUB_REPO}/artifacts/flint/{evd1['id']}.yaml)
> - **Source ID:** [`{evd1['source_id']}`]({GITHUB_REPO}/artifacts/flint/{evd1['source_id']}.yaml)
> - **Location:** {evd1['location']}
> - **Document Hash:** `{evd1['document_hash']}`
> - **Extracted By:** `{evd1['extracted_by']}`
> - **Retrieved At:** {evd1['retrieved_at']}
</details>

#### Source B: {src2['title']}
> "{evd2['extracted_content']}"  
> — *{src2['publisher']}, {src2['date']}*

<details>
<summary><strong>⚙️ View Provenance & Cryptographic Hash</strong></summary>

> [!info] Raw Metadata
> - **Object ID:** [`{evd2['id']}`]({GITHUB_REPO}/artifacts/flint/{evd2['id']}.yaml)
> - **Source ID:** [`{evd2['source_id']}`]({GITHUB_REPO}/artifacts/flint/{evd2['source_id']}.yaml)
> - **Location:** {evd2['location']}
> - **Document Hash:** `{evd2['document_hash']}`
> - **Extracted By:** `{evd2['extracted_by']}`
> - **Retrieved At:** {evd2['retrieved_at']}
</details>

### 2.2 Contradictory Evidence & Resolution

#### Source C: {src3['title']}
> "{evd3['extracted_content']}"  
> — *{src3['publisher']}, {src3['date']}*

<details>
<summary><strong>⚙️ View Provenance & Cryptographic Hash</strong></summary>

> [!warning] Contradictory Source
> - **Object ID:** [`{evd3['id']}`]({GITHUB_REPO}/artifacts/flint/{evd3['id']}.yaml)
> - **Source ID:** [`{evd3['source_id']}`]({GITHUB_REPO}/artifacts/flint/{evd3['source_id']}.yaml)
> - **Location:** {evd3['location']}
> - **Document Hash:** `{evd3['document_hash']}`
> - **Resolution:** {claim.get('contradiction_resolution', 'N/A')}
</details>

---

## 3. Human Audit & Provenance Trail
This artifact was promoted to `{claim['promotion_stage']}` only after satisfying the PL-001 v1.1 Bootstrap Governance Rule (requiring ≥2 designated internal auditors).

> [!timeline] Audit Log
> 1. **Verification:** [`{evt1['actor']}`]({GITHUB_REPO}/artifacts/actors/{evt1['actor'].split(':')[1]}.yaml) confirmed excerpt at {evt1['timestamp'][:10]}.
> 2. **Verification:** [`{evt2['actor']}`]({GITHUB_REPO}/artifacts/actors/{evt2['actor'].split(':')[1]}.yaml) confirmed excerpt at {evt2['timestamp'][:10]}.
> 3. **Assessment:** [`{evt3['actor']}`]({GITHUB_REPO}/artifacts/actors/{evt3['actor'].split(':')[1]}.yaml) resolved contradiction.
> 4. **Promotion:** [`{evt4['actor']}`]({GITHUB_REPO}/artifacts/actors/{evt4['actor'].split(':')[1]}.yaml) promoted claim to `{evt4['new_stage']}`.
> 5. **Independent Audit:** [`{evt5['actor']}`]({GITHUB_REPO}/artifacts/actors/{evt5['actor'].split(':')[1]}.yaml) performed blind confirmation.
> 6. **Diagnostic Promotion:** [`{evt6['actor']}`]({GITHUB_REPO}/artifacts/actors/{evt6['actor'].split(':')[1]}.yaml) promoted diagnostic to `{evt6['new_stage']}`.

---

## 4. Reproducibility
You do not have to take our word for it. 

1. Clone the repository: `git clone https://github.com/loom-research-system/loom-research-system.git`
2. Install dependencies: `pip install pyyaml`
3. Run the validator: `python loom_validator/validator.py .`
4. Expected output: `✓ All validation rules passed`

> [!note] Generation Metadata
> This bundle was automatically generated on **{datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}**. 
> The epistemic validity of the claims is anchored to the `current_as_of` date: **{epistemic_date}**.

*Generated by Project Loom Publication Compiler v1.3 (Fail-Closed + Direct GitHub Linking)*
"""

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(md)
        
    print(f"✅ Fail-Closed Publication Bundle successfully generated!")
    print(f"📄 Location: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
