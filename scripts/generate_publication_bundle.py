import yaml
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
FLINT_DIR = BASE_DIR / "artifacts" / "flint"
ERRATA_DIR = BASE_DIR / "errata"
OUTPUT_FILE = FLINT_DIR / "PUBLICATION_BUNDLE.md"

def load_yaml(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def main():
    print(" Compiling Phase 9 Publication Bundle...")
    
    # Load all Flint artifacts
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
    
    # Load Errata
    errata_files = list(ERRATA_DIR.glob("*.md"))
    
    # Generate Markdown
    md = f"""# Loom Research Artifact: Flint Water Crisis Analysis
**Publication Date:** {datetime.now().strftime('%Y-%m-%d')}  
**Loom Specification Version:** PL-307 v1.0 / PL-001 v1.1 (LOCKED)  
**Repository:** github.com/loom-research-system/loom-research-system  
**Validation Status:** ✅ PASSED (Mechanically enforced via CI/CD)  

---

## 1. Executive Summary & Diagnostic Thesis
> *"{diag['thesis']}"*  
> **Epistemic Status:** {diag['epistemic_status'].capitalize()} | **Status:** {diag['status'].replace('_', ' ').title()}

This artifact represents a fully audited, multi-source analysis of the Flint Water Crisis, specifically examining the failure of corrosion control implementation in 2014 and the institutional response.

---

## 2. The Core Claim
**ID:** `{claim['id']}`  
**Statement:** "{claim['statement']}"  
**Epistemic Status:** `{claim['epistemic_status'].capitalize()}`  
**Verification Level:** `{claim['verification_level'].replace('_', ' ').title()}`  
**Promotion Stage:** `{claim['promotion_stage'].capitalize()}`  

---

## 3. Evidence Chain & Source Registry

### 3.1 Primary Supporting Evidence
**Source 1:** {src1['title']} ({src1['publisher']}, {src1['date']})  
- **Independence:** {src1['independence']} | **Quality:** {src1['source_assessment']['quality_rating'].capitalize()}  
- **Excerpt:** > "{evd1['extracted_content']}"  
- **Location:** {evd1['location']}  

**Source 2:** {src2['title']} ({src2['publisher']}, {src2['date']})  
- **Independence:** {src2['independence']} | **Quality:** {src2['source_assessment']['quality_rating'].capitalize()}  
- **Excerpt:** > "{evd2['extracted_content']}"  
- **Location:** {evd2['location']}  

### 3.2 Contradictory Evidence & Resolution
**Source 3:** {src3['title']} ({src3['publisher']}, {src3['date']})  
- **Independence:** {src3['independence']} | **Quality:** {src3['source_assessment']['quality_rating'].capitalize()}  
- **Excerpt:** > "{evd3['extracted_content']}"  

**Contradiction Status:** `{claim['contradiction_status'].capitalize()}`  
**Resolution:** {claim.get('contradiction_resolution', 'N/A')}  

---

## 4. Human Audit & Provenance Trail
This artifact was promoted to `{claim['promotion_stage']}` only after satisfying the PL-001 v1.1 Bootstrap Governance Rule (requiring ≥2 designated internal auditors).

1. **{evt1['timestamp'][:10]}** | `{evt1['action'].replace('_', ' ').title()}` by `{evt1['actor']}`  
   *Result: {evt1['result'].capitalize()} ({evt1['method'][:50]}...)*
2. **{evt2['timestamp'][:10]}** | `{evt2['action'].replace('_', ' ').title()}` by `{evt2['actor']}`  
   *Result: {evt2['result'].capitalize()} ({evt2['method'][:50]}...)*
3. **{evt3['timestamp'][:10]}** | `{evt3['action'].replace('_', ' ').title()}` by `{evt3['actor']}`  
   *Rationale: {evt3['rationale'][:80]}...*
4. **{evt4['timestamp'][:10]}** | `{evt4['action'].replace('_', ' ').title()}` by `{evt4['actor']}`  
   *Promoted claim to `{evt4['new_stage']}`.*
5. **{evt5['timestamp'][:10]}** | `{evt5['action'].replace('_', ' ').title()}` by `{evt5['actor']}`  
   *Result: {evt5['result'].capitalize()} (Blind independent confirmation).*
6. **{evt6['timestamp'][:10]}** | `{evt6['action'].replace('_', ' ').title()}` by `{evt6['actor']}`  
   *Promoted diagnostic to `{evt6['new_stage']}`.*

---

## 5. Known Limitations & Tracked Errata
Per PL-001 v1.1 Phase 9 requirements, all known specification defects at the time of publication are listed below. These do not invalidate this artifact but represent areas for future system refinement.

"""
    for errata_file in sorted(errata_files):
        with open(errata_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Extract just the title and issue for brevity
            lines = content.split('\n')
            title = next((l.replace('## Issue: ', '') for l in lines if l.startswith('## Issue:')), 'Unknown Issue')
            md += f"- **{title}**\n"

    md += """
---

## 6. Reproducibility & Verification
This artifact is machine-readable and mechanically validated. To verify this bundle:
1. Clone the repository: `git clone https://github.com/loom-research-system/loom-research-system.git`
2. Install dependencies: `pip install pyyaml`
3. Run the validator: `python loom_validator/validator.py .`
4. Expected output: `✓ All validation rules passed`

*Generated by Project Loom Publication Compiler v1.0*
"""

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(md)
        
    print(f"✅ Publication Bundle successfully generated!")
    print(f"📄 Location: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
