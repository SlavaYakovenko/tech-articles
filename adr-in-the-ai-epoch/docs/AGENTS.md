# AGENTS.md

1. When creating a brand new ADR, you must use `./adr/ADR-TEMPLATE.md` as a template.
2. Naming convention for ADR files: `ADR-XXXX-{subject}`
   1. `XXXX` is a four-digit number starting from `0001`.
   2. `{subject}` is a short description of the problem addressed.
3. Files matching `./adr/ADR-*.md` must be added to the context during the following operations:
   1. When `/plan` mode is activated.
   2. When working on redesigns, refactoring, or making high-impact architectural decisions.