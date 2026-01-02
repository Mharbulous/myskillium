# Migration Phases

```mermaid
flowchart TD
    START([Begin Migration])
    PRE[PRE-MIGRATION]
    PRE_ITEMS[- Repo created<br/>- Structure established<br/>- Sync scripts ready<br/>- StoryTree accessible]
    SKILLS[SKILLS MIGRATION]
    SKILLS_ITEMS[- story-tree/<br/>- story-execution/<br/>- streamline/<br/>- SKILL.md updates]
    COMMANDS[COMMANDS MIGRATION]
    COMMANDS_ITEMS[- ci-create-plan.md<br/>- ci-implement-plan.md<br/>- design-story.md]
    SCRIPTS[SCRIPTS MIGRATION]
    WORKFLOWS[WORKFLOWS MIGRATION]
    SCHEMA[SCHEMA MIGRATION]
    GUI[GUI MIGRATION]
    DOCS[DOCUMENTATION]
    DOCS_ITEMS[- CLAUDE.md<br/>- README.md<br/>- No StoryTree refs]
    CONFIG[CONFIGURATION]
    CONFIG_ITEMS[- .gitignore<br/>- .myskillium-version<br/>- Template enabled]
    VALIDATE[VALIDATION]
    VALIDATE_ITEMS[- Test from template<br/>- Skills load<br/>- Commands work<br/>- Sync works]
    POST[POST-MIGRATION]
    POST_ITEMS[- Update StoryTree README<br/>- Archive StoryTree<br/>- Migrate dependents]
    END([Complete])

    START --> PRE
    PRE -.-> PRE_ITEMS
    PRE --> SKILLS
    SKILLS -.-> SKILLS_ITEMS
    SKILLS --> COMMANDS
    COMMANDS -.-> COMMANDS_ITEMS
    COMMANDS --> SCRIPTS
    SCRIPTS --> WORKFLOWS
    WORKFLOWS --> SCHEMA
    SCHEMA --> GUI
    GUI --> DOCS
    DOCS -.-> DOCS_ITEMS
    DOCS --> CONFIG
    CONFIG -.-> CONFIG_ITEMS
    CONFIG --> VALIDATE
    VALIDATE -.-> VALIDATE_ITEMS
    VALIDATE --> POST
    POST -.-> POST_ITEMS
    POST --> END

    style PRE fill:#FFB6C1
    style SKILLS fill:#87CEEB
    style COMMANDS fill:#87CEEB
    style SCRIPTS fill:#87CEEB
    style WORKFLOWS fill:#87CEEB
    style SCHEMA fill:#87CEEB
    style GUI fill:#87CEEB
    style DOCS fill:#98FB98
    style CONFIG fill:#98FB98
    style VALIDATE fill:#FFD700
    style POST fill:#DDA0DD
    style END fill:#90EE90
```

## Phase Summary

| Phase | Category | Key Items |
|-------|----------|-----------|
| **Pre-Migration** | Setup (Pink) | Repo created, Structure established, Sync scripts ready, StoryTree accessible |
| **Skills Migration** | Core (Blue) | story-tree/, story-execution/, streamline/, SKILL.md updates |
| **Commands Migration** | Core (Blue) | ci-create-plan.md, ci-implement-plan.md, design-story.md |
| **Scripts Migration** | Core (Blue) | Migration of script files |
| **Workflows Migration** | Core (Blue) | Migration of workflow files |
| **Schema Migration** | Core (Blue) | Migration of schema definitions |
| **GUI Migration** | Core (Blue) | Migration of GUI components |
| **Documentation** | Docs/Config (Green) | CLAUDE.md, README.md, No StoryTree refs |
| **Configuration** | Docs/Config (Green) | .gitignore, .myskillium-version, Template enabled |
| **Validation** | Testing (Gold) | Test from template, Skills load, Commands work, Sync works |
| **Post-Migration** | Cleanup (Purple) | Update StoryTree README, Archive StoryTree, Migrate dependents |

## Migration Flow

The migration follows a linear progression from setup through core migrations, documentation, validation, and cleanup:

1. **Setup Phase**: Establish repository structure and sync mechanisms
2. **Core Migrations**: Migrate skills, commands, scripts, workflows, schema, and GUI in sequence
3. **Documentation & Configuration**: Update all documentation and configuration files
4. **Validation**: Comprehensive testing of all migrated components
5. **Cleanup**: Archive old system and migrate dependent projects

Dotted lines in the diagram indicate detailed checklist items for each major phase.
