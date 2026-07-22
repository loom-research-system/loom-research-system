---
type: documentation
id: PL-DOC05
created: 2026-07-19
tags: [plugins, guide]
---

# Plugin Guide

## Installed Plugins

| Plugin | What It Does | When You Need It |
|--------|--------------|------------------|
| **Dataview** | Creates automatic tables and lists from your notes | Dashboards, indexes, finding untagged notes |
| **Templater** | Fills in dates, IDs, and other variables when you create notes | Every time you create a note from a template |
| **Copilot** | AI assistant inside Obsidian | Summarizing, finding connections, suggesting tags |
| **Tasks** | Tracks research tasks and deadlines | Managing active projects |
| **Omnisearch** | Better search across your entire vault | Finding anything quickly |

## Dataview

### What It Is

Dataview reads the metadata (frontmatter) in your notes and displays it as tables or lists.

### How to Use It

1. Create a note
2. Switch to Source mode (Ctrl+E)
3. Type a code block starting with `dataview`:

```dataview
TABLE type, id, created
FROM "03 Permanent Notes"
WHERE type = "permanent-note"
SORT id ASC
4. Switch to Reading view (Ctrl+E) to see the table
    

### Common Queries

**All notes by type:**

TABLE type, id, created
FROM ""
WHERE type
SORT type, id

```dataview
SORT type, id
```

**Recently modified:**

TABLE file.mtime as "Modified", type
FROM ""
WHERE type
SORT file.mtime DESC
LIMIT 10

**Untagged notes:**

TABLE id, type, created
FROM ""
WHERE type AND tags = []
SORT created DESC

## Templater

### What It Does

When you create a note from a template, Templater automatically fills in:

- Today's date
    
- A unique ID
    
- The note title
    

### How to Use It

1. Create a new note
    
2. Press Ctrl+P
    
3. Type "Templater: Insert Template"
    
4. Select your template
    
5. Type the note title
    
6. Templater fills in the rest
    

### Template Variables

| Variable                                      | What It Becomes       | Example     |
| --------------------------------------------- | --------------------- | ----------- |
| `<% tp.date.now("YYYY-MM-DD") %>`             | Today's date          | 2026-07-19  |
| `<% tp.date.now("YY") %>`                     | Current year (short)  | 26          |
| `<% tp.file.title %>`                         | The note's title      | My New Note |
| `<% Math.floor(Math.random() * 900 + 100) %>` | Random 3-digit number | 473         |

## Copilot

### What It Does

AI assistant that can read your notes and help with research tasks.

### How to Access It

1. Open the Copilot sidebar (icon in left ribbon)
    
2. Or press your configured hotkey
    
3. Select a custom prompt or type freely
    

### Custom Prompts

| Prompt               | What It Does                                     |
| -------------------- | ------------------------------------------------ |
| **Summarize Note**   | 2-sentence summary + gaps in reasoning           |
| **Find Connections** | Suggests 3 related notes as \[\[PL-XXX]] links   |
| **Suggest Tags**     | Recommends 5 tags from standard categories       |
| **Analyze Source**   | Evaluates argument, evidence, methods, relevance |

### Good Uses

- Summarizing an article
    
- Identifying assumptions
    
- Suggesting related notes
    
- Explaining difficult concepts
    
- Brainstorming questions
    

### Avoid

- Writing your conclusions
    
- Generating evidence
    
- Replacing critical reading
    

## Troubleshooting

| Problem                 | Fix                                           |
| ----------------------- | --------------------------------------------- |
| Dataview shows raw code | Switch to Reading view (Ctrl+E)               |
| Templater shows `<% %>` | Template is corrupted, rebuild in Source mode |
| Copilot not responding  | Check API key in settings                     |
| Plugin not working      | Check if it's enabled in Community Plugins    |
