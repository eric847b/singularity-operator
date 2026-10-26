# Documentation Policy

## Archive Candidate Conditions

A document becomes an archive candidate when:

- Not updated in 90+ days
- Not linked from README
- Not referenced by active documentation
- Not referenced by active code

Archived content remains preserved but is removed from active navigation.

## Active Documentation Requirements

Active documentation must describe:

- Existing functionality
- Current architecture
- Current roadmap
- Supported workflows

## Structure

```
docs/
├── architecture/
│   ├── system-overview.md
│   ├── component-map.md
│   └── integration-model.md
│
├── memory-model/
│   ├── storage.md
│   ├── indexing.md
│   └── provenance.md
│
├── validation-pipeline/
│   ├── validators.md
│   ├── trust-model.md
│   └── scoring.md
│
├── integrations/
│   ├── ai-collaboration-hub.md
│   ├── nexus.md
│   └── third-door.md
│
├── roadmap/
│   ├── active-roadmap.md
│   └── release-plan.md
│
└── archive/
```

Historical architectural drafts, deprecated singularity milestone documents, obsolete future-intelligence projections, and superseded design proposals belong in `/docs/archive`.
