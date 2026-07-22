---
type: documentation
id: PL-DOC04
created: 2026-07-19
tags: [conventions, organization]
---

# Naming Conventions

## Folder Names

Always use two digits and a space:

- `00 Documentation`
- `01 Sources`
- `02 Literature Notes`

This keeps them sorted alphabetically in the correct order.

## Note IDs

| Type | Format | Example |
|------|--------|---------|
| Sources | PL-1## | PL-101, PL-102 |
| Literature Notes | PL-2## | PL-201, PL-202 |
| Permanent Notes | PL-3## | PL-301, PL-302 |
| Projects | PL-4## | PL-401, PL-402 |
| Outputs | PL-5## | PL-501, PL-502 |
| Documentation | PL-DOC## | PL-DOC01, PL-DOC02 |

## Note Titles

- **Be specific**: "Power Asymmetry in Bureaucracies" not "Notes on Power"
- **Use verbs for processes**: "How Policy Drift Occurs" not "Policy Drift"
- **Avoid generic titles**: Every title should be recognizable 6 months later

## File Names

- Use hyphens: `my-note-name.md` not `my note name.md`
- No special characters except `-` and `_`
- Keep under 80 characters for readability

## Tag Conventions

Use lowercase, hyphenated tags:

- `philosophy` not `Philosophy`
- `policy-implementation` not `policy implementation`
- `case-study` not `casestudy`

Standard tags for Project Loom:

| Tag | Used For |
|-----|----------|
| `philosophy` | Foundational principles |
| `methodology` | Research methods |
| `systems` | Technical systems (ATLAS, EROS) |
| `validation` | Case studies, evidence |
| `governance` | Decision-making, version control |
| `ontology` | Concept definitions |
| `epistemology` | Knowledge theory |
| `ethics` | Normative considerations |
| `policy` | Government/policy content |
| `technology` | Technical implementation |

## Link Format

Always use wiki links: `[[Note Title]]`

For aliases: `[[Note Title|Display Text]]`

## Quick Reference

| Element | Good Example | Bad Example |
|---------|--------------|-------------|
| Folder | `03 Permanent Notes` | `PermanentNotes` |
| Note ID | `PL-301` | `PL301` |
| Note title | `Bureaucratic Resistance Patterns` | `Notes` |
| Tag | `policy-implementation` | `Policy Implementation` |
| Link | `[[PL-301 Bureaucratic Resistance]]` | `see the note about resistance` |