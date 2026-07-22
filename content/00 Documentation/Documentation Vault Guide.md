---
type: documentation
id: PL-DOC02
created: 2026-07-19
tags: [guide, structure]
---

# Vault Structure Guide

## Folder Purposes

| Folder | What Goes Here | Don't Put Here |
|--------|--------------|----------------|
| `01 Sources` | Original material: PDFs, articles, reports, interviews | Your own thoughts |
| `02 Literature Notes` | Reading notes: one per source | Multiple sources in one note |
| `03 Permanent Notes` | Your own ideas: one idea per note | Long summaries of sources |
| `04 Projects` | Active work: charters, frameworks, case studies | Finished outputs |
| `05 Outputs` | Completed work: essays, papers, presentations | Drafts (keep in Projects until done) |
| `99 Templates` | Note templates only | Regular notes |
| `99 Archive` | Old versions, deprecated notes | Active work |
| `00 Documentation` | Guides and conventions | Research content |

## Note Types

| Type | Used In | Purpose |
|------|---------|---------|
| `source` | 01 Sources | Original material metadata |
| `literature-note` | 02 Literature Notes | Reading summary and analysis |
| `permanent-note` | 03 Permanent Notes | Your own original idea |
| `project-note` | 04 Projects | Active research work |
| `dashboard` | Any folder | Dataview overview tables |
| `documentation` | 00 Documentation | Guides and how-tos |

## Naming Conventions

- **Sources**: `Author Year - Title` or `PL-###` for internal sources
- **Literature Notes**: `PL-### Author Year - Title`
- **Permanent Notes**: Descriptive phrase in your own words
- **Projects**: `PL-### Project Name`
- **All notes**: Use `-` between words, not spaces if possible

## Metadata Standard

Every note begins with:

```yaml
---
type: [see table above]
id: [PL-### or leave blank for auto-generation]
created: YYYY-MM-DD
tags: []
status: [unread/reading/draft/review/done]
---