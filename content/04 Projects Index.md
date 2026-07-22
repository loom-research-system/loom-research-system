
**`04 Projects/Index.md`:**
```markdown
---
type: dashboard
---

# Projects Index

```dataview
TABLE id, created, file.mtime as "Updated"
FROM "04 Projects"
WHERE type = "project-note"
SORT id ASC