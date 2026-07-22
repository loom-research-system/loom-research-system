---
type: dashboard
---

# Permanent Notes Index

```dataview
TABLE id, created, file.inlinks as "Linked By"
FROM "03 Permanent Notes"
WHERE type = "permanent-note"
SORT id ASC