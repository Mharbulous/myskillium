# Testing Workflow

```mermaid
flowchart TD
    START([Start Testing]) --> ENV_HEADER[Test Environments]

    ENV_HEADER -.-> ENV1[Local CLI<br/>VS Code]
    ENV_HEADER -.-> ENV2[Claude Code Web]
    ENV_HEADER -.-> ENV3[Windows]
    ENV_HEADER -.-> ENV4[Linux/Mac]

    ENV_HEADER --> T1[T1: Template Creation<br/>Use template on GitHub]
    T1 --> T2[T2: Skills Load<br/>Open in Claude Code]
    T2 --> T3[T3: Commands Available<br/>Check / commands]

    T3 --> T4[T4: Sync Script Bash<br/>./sync-myskillium.sh]
    T4 --> T5[T5: Sync Script Python<br/>python sync-myskillium.py]
    T5 --> T6[T6: Preserves Project Files<br/>*.db, local/, settings]
    T6 --> T7[T7: Sync Updates Version<br/>.myskillium-version]

    T7 --> T8[T8: GUI Runs Standalone<br/>python xstory.py]
    T8 --> T9[T9: Web Compatibility<br/>Claude Code web]
    T9 --> T10[T10: Windows Compatibility<br/>No symlink errors]

    T10 --> REGRESSION[Regression Tests<br/>T1, T4/T5, T6]
    REGRESSION --> ALL_PASS{All tests pass?}

    ALL_PASS -->|No| FIX[Fix issues]
    FIX -.->|Re-run| T1

    ALL_PASS -->|Yes| END([Testing Complete])

    style ENV_HEADER fill:#E0E0E0
    style T1 fill:#87CEEB
    style T2 fill:#87CEEB
    style T3 fill:#87CEEB
    style T4 fill:#98FB98
    style T5 fill:#98FB98
    style T6 fill:#98FB98
    style T7 fill:#98FB98
    style T8 fill:#FFD700
    style T9 fill:#FFD700
    style T10 fill:#FFD700
    style REGRESSION fill:#DDA0DD
    style FIX fill:#FF6B6B
    style END fill:#90EE90
```

## Test Groups

| Category | Tests | Description | Color |
|----------|-------|-------------|-------|
| Core Template Tests | T1, T2, T3 | Verify template creation and basic Claude Code integration | Sky Blue (#87CEEB) |
| Sync Tests | T4, T5, T6, T7 | Validate sync scripts and version management | Pale Green (#98FB98) |
| Compatibility Tests | T8, T9, T10 | Ensure cross-platform and environment compatibility | Gold (#FFD700) |
| Regression Tests | T1, T4/T5, T6 | Re-run critical tests to prevent breaking changes | Plum (#DDA0DD) |

## Known Limitations

- **Manual Sync**: Sync is manual (not automatic) - users must run sync scripts explicitly
- **GUI Dependencies**: GUI requires Python + PySide6 installation
- **Repository Size**: Large files may slow clone operations

## Test Flow Notes

The testing workflow follows a sequential progression through three main categories:

1. **Core Template Tests (Blue)**: Establish baseline functionality
2. **Sync Tests (Green)**: Verify update mechanism works correctly
3. **Compatibility Tests (Gold)**: Ensure cross-platform support

After all tests, regression tests validate that core functionality remains intact. If any test fails, issues must be fixed and testing resumes from T1.
