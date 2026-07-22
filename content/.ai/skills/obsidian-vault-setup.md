# Obsidian Vault Setup Skill

## Context
You are setting up an Obsidian vault for academic research. All file and folder operations happen in the current working directory (the vault root).

## Folder Structure to Create
Create the following directories:
- 01 Sources/Articles/
- 01 Sources/Books/
- 01 Sources/Papers/
- 01 Sources/Web/
- 02 Literature Notes/
- 03 Permanent Notes/
- 04 Projects/
- 05 Outputs/Drafts/
- 05 Outputs/Published/
- 99 Templates/

## Template Files to Create
In 99 Templates/, create these files with exact frontmatter schemas:

### Source Template.md
---
type: source
author: 
year: 
tags: [source, literature]
status: unread
rating: 
doi: 
url: 
---

# {{title}}

## Metadata
- **Author(s):** 
- **Year:** 
- **URL/DOI:** 

## Summary

## Key Arguments
- 

## Key Quotes
> 

## My Notes
- 

## Connections
- [[ ]]
- [[ ]]

## Questions/Follow-ups
- 

### Literature Note Template.md
---
type: literature-note
source: 
tags: []
created: {{date:YYYY-MM-DD}}
---

# {{title}}

## Context

## Key Ideas
- 

## Critical Analysis

## Relevance to My Research

## Related Notes
- [[ ]]

### Permanent Note Template.md
---
type: permanent-note
tags: []
created: {{date:YYYY-MM-DD}}
---

# {{title}}

## Idea

## Evidence

## Implications

## Connections
- [[ ]]
- [[ ]]

## Rules
- Create directories with mkdir
- Create files with exact content
- Do not overwrite existing files
