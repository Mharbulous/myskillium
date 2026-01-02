#!/usr/bin/env python3
"""
Myskillium Conidium - Germination & Homeostasis Script

A portable, self-contained script that serves two purposes:
1. GERMINATION (--germinate): Bootstrap myskillium into a new repository
2. HOMEOSTASIS (SessionStart hook): Maintain process consistency

Embeds all 5 essential myskillium files and can recreate the full skill
structure from this single script.

Usage:
    python conidium.py --germinate    # First-time setup
    python conidium.py                # Hook mode (automatic)

Workflow (hook mode - optimized for minimal intrusion):
1. 24h fast path -> silent exit if <24h since last check (most common)
2. Source template check -> silent exit if git remote is Mharbulous/Myskillium
3. Hash comparison -> restore files if any difference
4. Remote check -> notify if upstream update available
"""

# Minimal imports for fast path
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Lazy imports - only loaded when needed
hashlib = None
subprocess = None
urllib_request = None
urllib_error = None
json_module = None


def _import_hashlib():
    global hashlib
    if hashlib is None:
        import hashlib as _hashlib
        hashlib = _hashlib
    return hashlib


def _import_subprocess():
    global subprocess
    if subprocess is None:
        import subprocess as _subprocess
        subprocess = _subprocess
    return subprocess


def _import_urllib():
    global urllib_request, urllib_error
    if urllib_request is None:
        import urllib.request as _urllib_request
        import urllib.error as _urllib_error
        urllib_request = _urllib_request
        urllib_error = _urllib_error
    return urllib_request, urllib_error


def _import_json():
    global json_module
    if json_module is None:
        import json as _json
        json_module = _json
    return json_module


# Source template identifier
_SOURCE_OWNER = "Mharbulous"
_SOURCE_REPO = "Myskillium"

# ============================================================================
# CONIDIUM SOURCE METADATA
# These values identify where this conidium.py was copied FROM.
# During germination, pedigree.json is generated using these as source info.
# When conidium.py is copied to a new repo and germinated, these values are
# updated to point to the NEW repo, creating a chain of custody.
# ============================================================================
_CONIDIUM_SOURCE = {
    "url": "https://github.com/Mharbulous/Myskillium.git",
    "path": ".claude/skills/myskillium",
    "commit": "TEMPLATE",  # Updated during germination
}

# Remote version.yml for update checks
REMOTE_VERSION_URL = f"https://raw.githubusercontent.com/{_SOURCE_OWNER}/{_SOURCE_REPO}/main/.claude/skills/myskillium/version.yml"

# Target directory structure
MYSKILLIUM_DIR = ".claude/skills/myskillium"
SUBSTRATE_DIR = ".claude/skills/myskillium/substrate"
SCRIPTS_DIR = ".claude/skills/myskillium/scripts"
VERSION_FILE = ".claude/skills/myskillium/version.yml"
SETTINGS_FILE = ".claude/settings.json"

# ============================================================================
# EMBEDDED FILES - These are the canonical versions
# ============================================================================

EMBEDDED_DOCS = {
    "README.md": """\
# Myskillium

Myskillium is a meta-skill within the Claude Code ecosystem that finds and improves skills using processes modelled after mycelium.  Through a process called conidiation it creates spores (conidium) that can be copied to other repos where they grow independently into hyphae (threads) and eventualy connect to create decentralized network of symbiotic cloned skills.

Examples of use:

   "Claude, find me a skill that can ....X....?"
   "Claude, find a better version of this skill:  ...X.."
   "Claude, create a hybrid skill that combines the best elements of these two skills:  ...Y and Z..."

This experiment in non-deterministic evolutionary programming is dedicated to John Horton Conway, Edward Lorenz, Stephen Wolfram, and Andrej Karpathy.

1. Install

   ```bash
   python conidium.py --germinate
   ```

2. Uninstall

   ```bash
   python conidium.py --apoptose
   ```

""",

    "substrate/conidiation.md": """\
# Conidiation

## Skill Analogy

In the myskillium context, conidiation refers to the process of spreading via the portable installation script (`myskillium-conidium.py`). Just as mycelium use conidia to grow, conidiation is the process of myskillium to spread across repositories.

## Purpose

The conidium tool (`myskillium-conidium.py`) is a standalone script that can be copied into any repository to perform skill extraction without requiring the full myskillium skill to be present.

## Process

> **Status**: Not yet implemented

### Planned Workflow

1. **Package extraction logic** into portable Python script
2. **Include pedigree schema** for genealogy documentation
3. **Minimize dependencies** for maximum portability
4. **Version the spore** with its parent myskillium commit

### Output

```
myskillium-spore.py  # Portable extraction tool
```

## Relationship to Other Processes

| Process | Relationship |
|---------|-------------|
| Fragmentation | Uses the spore tool to perform extraction |
| Plasmogamy | Uses the spore tool to perform fusion |

The spore is the **mechanism**; fragmentation and plasmogamy are the **operations** that use it.
""",

    "substrate/fragmentation.md": """\
# Fragmentation

## Skill Analogy

In the myskillium context, fragmentation refers to **extracting a skill from one repository to another**. The skill is a "fragment" of the source repo's functionality that becomes independent in its new home.

Key parallels:
- The skill (fragment) is viable on its own
- It adapts to the new environment (project-specific references cleaned up)
- It grows independently (maintained separately from source)
- Genetic identity is preserved (pedigree documents lineage)

## Purpose

Migrate a skill from a source repository to Myskillium while:
1. Cleaning up project-specific references
2. Documenting skill pedigree
3. Preserving the skill's core functionality

## Process

### Prerequisites

- Source repository accessible (local clone or remote URL)
- Destination path in Myskillium identified
- Cleanup patterns defined for project-specific references

### Phase 1: Configure

Create or update migration config specifying:
- Source repository URL and skill path
- Destination path
- Cleanup replacements (project names → generic terms)

See `genealogy/templates/migration-config.json` for structure.

### Phase 2: Copy

Transfer skill files from source to destination:

```bash
cp -r "<source-repo>/<skill-path>/" "<dest-repo>/<skill-path>/"
```

### Phase 3: Cleanup

**Scan** for project-specific references:
```bash
grep -r -i "pattern1\\|pattern2\\|pattern3" "<destination>/" || echo "Clean"
```

**Replace** according to config:

| Type | Example Find | Example Replace |
|------|--------------|-----------------|
| Project name | `SyncoPaid` | `myapp` |
| Domain term | `story` → `task` | (whole word only) |
| Package name | `syncopaid.module` | `myapp.module` |
| Specific path | `tests/test_project.py` | "your test file" |
| Historical ref | "In the ProjectX case" | "In one case" |

**Verify** - remaining matches should be false positives only.

### Phase 4: Genealogy

Create pedigree file at `genealogy/<skill-name>.json`:

```json
{
  "name": "<from-frontmatter>",
  "description": "<from-frontmatter>",
  "pedigree": [
    {
      "date": "YYYY-MM-DD",
      "sourceURL": "https://github.com/org/source-repo.git",
      "sourcePath": ".claude/skills/skill-name",
      "sourceCommitID": "<40-char-hash>",
      "destURL": "https://github.com/org/dest-repo.git",
      "destPath": ".claude/skills/skill-name",
      "destCommitID": "<recorded-after-commit>",
      "destOperator": ".claude/skills/myskillium/SKILL.md",
      "destModel": "<model-id>"
    }
  ]
}
```

### Phase 5: Commit

```
feat: migrate <skill-name> from <source-repo>

Project-specific references cleaned up.
Pedigree documented in genealogy/<skill-name>.json
```

After commit, update the pedigree file with `destCommitID`.

## Experimental Control Requirements

To enable reproducibility research, this process MUST:

1. **Spawn isolated subagent** - Use Task tool, not main conversation
2. **Provide structured data only** - No conversation history passed
3. **Record all variables** - Operator, model, commits in pedigree

This ensures Claude's non-determinism is the only uncontrolled variable.

## Checklist

- [ ] Source skill identified and accessible
- [ ] Cleanup patterns defined
- [ ] Skill files copied to destination
- [ ] Project names generalized
- [ ] Domain terms universalized
- [ ] Example paths made generic
- [ ] Pedigree file created with all fields
- [ ] Commit created with descriptive message
- [ ] destCommitID recorded in pedigree
- [ ] Process used isolated subagent (experimental control)
""",

    "substrate/plasmogamy.md": """\
# Plasmogamy

## Skill Analogy

In the myskillium context, plasmogamy refers to **fusing two or more skills into a single hybrid skill**. Just as fungal plasmogamy combines genetic material from two parents, skill plasmogamy combines functionality, patterns, and approaches from two source skills into a single new hybrid skill.

Key parallels:
- Two (or more) parent skills contribute to the hybrid
- The hybrid has characteristics of both parents
- The combination creates something neither parent had alone
- Lineage from all parents is preserved in pedigree

## Purpose

Create a new skill by combining elements from multiple existing skills:
- Merge complementary functionality
- Combine different approaches to the same problem
- Synthesize best practices from multiple sources
- Create specialized variants by crossing general skills

## Process

> **Status**: Not yet implemented

### Planned Workflow

#### Phase 1: Select Parents

Identify two or more skills to combine:
- Define what each parent contributes
- Identify complementary vs conflicting elements
- Plan how conflicts will be resolved

#### Phase 2: Extract Parent Material

For each parent skill:
- Record source commit and path
- Extract the elements to be combined
- Document what is being taken from each

#### Phase 3: Fusion

Combine parent elements into hybrid:
- Merge non-conflicting sections
- Resolve conflicts according to plan
- Synthesize new sections that bridge parents
- Ensure coherent whole

#### Phase 4: Genealogy

Create pedigree with **multiple entries** in the array:

```json
{
  "name": "hybrid-skill-name",
  "description": "Hybrid combining parent-a and parent-b",
  "pedigree": [
    {
      "date": "YYYY-MM-DD",
      "sourceURL": "https://github.com/org/repo-a.git",
      "sourcePath": ".claude/skills/parent-a",
      "sourceCommitID": "<parent-a-commit>",
      "destURL": "https://github.com/org/myskillium.git",
      "destPath": ".claude/skills/hybrid-skill",
      "destCommitID": "<recorded-after-commit>",
      "destOperator": ".claude/skills/myskillium/SKILL.md",
      "destModel": "<model-id>"
    },
    {
      "date": "YYYY-MM-DD",
      "sourceURL": "https://github.com/org/repo-b.git",
      "sourcePath": ".claude/skills/parent-b",
      "sourceCommitID": "<parent-b-commit>",
      "destURL": "https://github.com/org/myskillium.git",
      "destPath": ".claude/skills/hybrid-skill",
      "destCommitID": "<recorded-after-commit>",
      "destOperator": ".claude/skills/myskillium/SKILL.md",
      "destModel": "<model-id>"
    }
  ]
}
```

#### Phase 5: Commit

```
feat: create <hybrid-name> by fusing <parent-a> and <parent-b>

Combined: [list of elements from each parent]
Pedigree documents both parent lineages.
```

## Experimental Control Requirements

To enable reproducibility research, this process MUST:

1. **Spawn isolated subagent** - Use Task tool, not main conversation
2. **Provide structured data only** - All parent content via parameters
3. **Record all variables** - Operator, model, all parent commits in pedigree

## Variance as the Primary Observable

### Why Plasmogamy Produces Higher Variance

Fragmentation is essentially a **transformation task**: take existing content, clean it up, move it. The input-output relationship is relatively deterministic - given the same source skill and cleanup rules, the output should be similar across runs.

Plasmogamy is fundamentally different. It requires **creative synthesis**:

| Fragmentation (Low Variance) | Plasmogamy (High Variance) |
|------------------------------|---------------------------|
| Copy and transform | Create and synthesize |
| Rules-based cleanup | Judgment-based integration |
| Single source of truth | Multiple sources to reconcile |
| Preserve original structure | Invent new structure |
| Obvious "correct" answer | Multiple valid solutions |

When Claude fuses two skills, it must make decisions that have no objectively correct answer:
- How to order sections from different parents?
- Which parent's phrasing to prefer when both address the same concept?
- How to bridge gaps where parents have different assumptions?
- What new connecting tissue to synthesize?

These decisions exist in a **high-dimensional solution space**. Even with identical inputs, Claude's inherent non-determinism will navigate this space differently each time.

### The Experimental Opportunity

By controlling all external variables (source content, operator, model, human input), we isolate Claude's non-determinism as the **sole source of variance**. This creates a natural experiment:

```
Run plasmogamy N times with identical inputs
    ↓
Measure variance in outputs
    ↓
Compare to fragmentation variance baseline
    ↓
Quantify the "creativity tax" - additional variance introduced by synthesis tasks
```

### What We Can Learn

1. **Variance spectrum**: How does output variance correlate with task type (transformation vs synthesis)?

2. **Consistency boundaries**: At what complexity threshold does Claude's output become unpredictably variable?

3. **Operator design**: Can operator instructions reduce synthesis variance without eliminating beneficial creativity?

4. **Model comparison**: Do different Claude models (Haiku vs Sonnet vs Opus) show different variance profiles on the same fusion task?

5. **Determinism ceiling**: Is there a theoretical minimum variance for synthesis tasks, or does creative work have inherent irreducible variance?

### Pedigree as Experimental Record

The pedigree file isn't just genealogy - it's **experimental documentation**. By recording:

- Exact source commits (inputs)
- Operator version (transformation function)
- Model ID (processing engine)
- Output commit (results)

We create an auditable record that proves: *"All controllable variables were held constant. Any variance observed is attributable to model non-determinism."*

This transforms skill management into **empirical AI research**.

## Checklist

- [ ] Parent skills identified
- [ ] Contribution from each parent defined
- [ ] Conflict resolution planned
- [ ] Parent material extracted
- [ ] Fusion performed by isolated subagent
- [ ] Hybrid skill coherent and functional
- [ ] Pedigree file created with entries for ALL parents
- [ ] Commit created with descriptive message
- [ ] destCommitID recorded in pedigree
""",

    "substrate/homeostasis.md": """\
# Homeostasis

## Definition

In the myskillium context, homeostasis refers to **protecting core processes from accidental modification through regular checking and automatic restoration**. Just as biological homeostasis maintains cellular integrity, skill homeostasis maintains process integrity across distributed repositories.

Key parallels:
- Sensing = hash comparison of core process files
- Regulatory response = detecting drift from canonical versions
- Restoration = overwriting modified files with canonical content
- Continuous monitoring = periodic checks (24h cycle)

## Purpose

Ensure consistency of core myskillium processes across all repositories:

1. **Detect drift** - Identify when core process files have been modified
2. **Restore canonical state** - Overwrite modified files with embedded versions
3. **Prevent fragmentation** - Keep all repos aligned with source-of-truth
4. **Enable safe experimentation** - Users can modify knowing restoration is automatic

## The Conidium Script

`conidium.py` is a portable, self-contained script that serves two purposes:

1. **Germination** - Bootstrap myskillium into a new repository
2. **Homeostasis** - Maintain consistency on each Claude Code session

### Embedded Content

The script embeds all essential myskillium files:

| File | Purpose |
|------|---------|
| `README.md` | Installation and overview |
| `SKILL.md` | Skill definition and process index |
| `substrate/conidiation.md` | Spore creation process |
| `substrate/fragmentation.md` | Skill extraction process |
| `substrate/plasmogamy.md` | Skill fusion process |
| `substrate/homeostasis.md` | This file - consistency maintenance |
| `substrate/apoptosis.md` | Controlled removal process |
| `substrate/tropism.md` | Skill discovery process |
| `substrate/pedigree.json` | Template for genealogy records |

### Relationship to myskillium-spore.py

| Aspect | myskillium-spore.py | conidium.py |
|--------|---------------------|-------------|
| **Primary role** | Bootstrap planning docs | Bootstrap + maintain myskillium skill |
| **Embedded content** | 7 planning docs (01-07) | 9 embedded files |
| **Target directory** | `.claude/skills/bootstrap/` | `.claude/skills/myskillium/` |
| **Germination** | Writes docs on first run | `--germinate` flag creates full skill |
| **Hook behavior** | Checks for updates | Restores drifted processes |

## Conidium Workflow

```mermaid
flowchart TD
    START([python conidium.py]) --> CHECK_FLAG{--germinate<br/>flag?}

    %% === GERMINATION PATH ===
    CHECK_FLAG -->|Yes| CHECK_EXISTS{.claude/skills/myskillium<br/>exists?}
    CHECK_EXISTS -->|Yes| WARN_EXISTS["Warning: skill already exists"]
    WARN_EXISTS --> ASK_OVERWRITE{Overwrite?}
    ASK_OVERWRITE -->|No| EXIT_ABORT([Exit - Aborted])
    ASK_OVERWRITE -->|Yes| GERMINATE
    CHECK_EXISTS -->|No| GERMINATE[Create directory structure]

    GERMINATE --> WRITE_FILES[Write all embedded files<br/>to substrate/]
    WRITE_FILES --> WRITE_SKILL[Write SKILL.md]
    WRITE_SKILL --> UPDATE_SETTINGS[Update .claude/settings.json<br/>Add SessionStart hook]
    UPDATE_SETTINGS --> WRITE_VERSION_G[Write version.yml]
    WRITE_VERSION_G --> MSG_GERMINATED["Myskillium Germinated<br/>Hook installed"]
    MSG_GERMINATED --> EXIT_GERMINATED([Exit])

    %% === HOMEOSTASIS PATH ===
    CHECK_FLAG -->|No| READ_VERSION[Read version.yml]
    READ_VERSION --> CHECK_24H{< 24h since<br/>last check?}

    CHECK_24H -->|Yes| EXIT_FAST([Silent Exit<br/>FAST PATH ~99%])
    CHECK_24H -->|No / Never| CHECK_SOURCE[Check git remote]

    CHECK_SOURCE --> IS_SOURCE{Remote contains<br/>Mharbulous/Myskillium?}
    IS_SOURCE -->|Yes| EXIT_SOURCE([Silent Exit<br/>Source Template])
    IS_SOURCE -->|No| CALC_HASHES[Calculate hashes for<br/>all 5 process files]

    CALC_HASHES --> COMPARE_PROCS{All hashes<br/>match embedded?}

    COMPARE_PROCS -->|No| RESTORE[Restore modified files<br/>+ update version.yml]
    RESTORE --> MSG_RESTORE["Myskillium Processes Restored"]
    MSG_RESTORE --> LIST_RESTORED["Lists which files were restored"]
    LIST_RESTORED --> EXIT_RESTORE([Exit])

    COMPARE_PROCS -->|Yes| FETCH_REMOTE[Fetch remote version.yml<br/>from GitHub<br/>5s timeout]

    FETCH_REMOTE --> NETWORK{Network<br/>success?}
    NETWORK -->|No| WRITE_VERSION_NET[Write version.yml<br/>★ resets 24h timer]
    WRITE_VERSION_NET --> EXIT_NET([Silent Exit<br/>Retry in 24h])

    NETWORK -->|Yes| REMOTE_MATCH{Remote hash ==<br/>Embedded hash?}
    REMOTE_MATCH -->|No| MSG_UPDATE["Myskillium Update Available"]
    MSG_UPDATE --> EXIT_UPDATE([Exit<br/>Timer NOT reset])

    REMOTE_MATCH -->|Yes| WRITE_VERSION[Write version.yml<br/>★ resets 24h timer]
    WRITE_VERSION --> EXIT_OK([Silent Exit<br/>Processes Intact])

    %% === SEMANTIC CLASS DEFINITIONS ===
    classDef successExit fill:#90EE90,stroke:#333,stroke-width:2px
    classDef infoMessage fill:#87CEEB,stroke:#333,stroke-width:2px
    classDef warningMessage fill:#FFA500,stroke:#333,stroke-width:2px
    classDef abortExit fill:#FFB6C1,stroke:#333,stroke-width:2px
    classDef germinateProcess fill:#E6E6FA,stroke:#333,stroke-width:2px
    classDef neutralExit fill:#E0E0E0,stroke:#333,stroke-width:2px

    %% === APPLY CLASSES ===
    class EXIT_FAST,EXIT_OK,EXIT_NET successExit
    class MSG_GERMINATED,MSG_RESTORE,LIST_RESTORED infoMessage
    class MSG_UPDATE,WARN_EXISTS warningMessage
    class EXIT_ABORT abortExit
    class WRITE_FILES,WRITE_SKILL,UPDATE_SETTINGS germinateProcess
    class EXIT_SOURCE neutralExit
```

## Germination Mode

When a user copies `conidium.py` to their repository and runs:

```bash
python .claude/skills/myskillium/scripts/conidium.py --germinate
```

The script:

1. **Creates directory structure**
   ```
   .claude/skills/myskillium/
   ├── SKILL.md
   ├── version.yml
   ├── substrate/
   │   ├── conidiation.md
   │   ├── fragmentation.md
   │   ├── homeostasis.md
   │   ├── plasmogamy.md
   │   └── pedigree.json
   └── scripts/
       └── conidium.py
   ```

2. **Installs SessionStart hook** in `.claude/settings.json`:
   ```json
   {
     "hooks": {
       "SessionStart": [
         {
           "matcher": {},
           "hooks": [
             {
               "type": "command",
               "command": "python .claude/skills/myskillium/scripts/conidium.py"
             }
           ]
         }
       ]
     }
   }
   ```

3. **Writes version.yml** with current timestamp and embedded hash

## Homeostasis Mode

After germination, `conidium.py` runs automatically on each Claude Code session start via the installed hook.

### Phase 1: Fast Path Check (24h cooldown)

```
if version.yml exists AND last_check < 24h ago:
    exit silently (most common path)
```

This prevents unnecessary overhead on every session.

### Phase 2: Source Template Detection

```
if git remote contains "Mharbulous/Myskillium":
    exit silently (source never self-restores)
```

The canonical source template must be freely editable.

### Phase 3: Process Hash Comparison

For each of the 5 embedded files:
1. Calculate SHA-256 hash of local file content
2. Compare against embedded canonical hash
3. Track which files have drifted

### Phase 4: Restoration (if needed)

If any file has drifted:
1. Overwrite modified files with embedded canonical content
2. Update `version.yml` with new timestamp
3. Report which files were restored

### Phase 5: Remote Update Check

If all files match:
1. Fetch remote `version.yml` from GitHub
2. Compare remote hash against embedded hash
3. Notify if newer version available upstream

## 24h Cooldown Behavior

| Outcome | Writes version.yml? | Next session behavior |
|---------|---------------------|----------------------|
| Fast path (<24h) | No | Fast exit again |
| Source template | No | Fast exit (no version.yml needed) |
| Processes restored | **Yes** | Fast exit for 24h |
| Network error | **Yes** | Fast exit for 24h |
| Update available | No | Check again (intentional reminder) |
| All intact | **Yes** | Fast exit for 24h |

## Relationship to Other Processes

| Process | Homeostasis Role |
|---------|-----------------|
| **Conidiation** | Protects the spore-creation process definition |
| **Fragmentation** | Ensures extraction rules remain consistent across repos |
| **Plasmogamy** | Ensures fusion rules remain consistent across repos |

Homeostasis is the **guardian** of the other three processes. Without homeostasis:
- Process drift across repos would corrupt skill genealogy
- Incompatible extraction/fusion rules would produce broken skills
- The myskillium network would fragment into incompatible variants

## Self-Protection Paradox

Homeostasis protects itself (`homeostasis.md`). This creates a bootstrapping consideration:

- The embedded hash of `homeostasis.md` must be updated whenever this file changes
- Changes to homeostasis require updating `conidium.py` to embed the new canonical content
- This is intentional: modifying the protection mechanism requires deliberate action in the source template

## Checklist

- [ ] `conidium.py` embeds all 5 process files as strings
- [ ] `--germinate` flag creates full directory structure
- [ ] `--germinate` installs SessionStart hook in settings.json
- [ ] Hash calculation matches algorithm in `myskillium-spore.py`
- [ ] 24h cooldown prevents excessive checking
- [ ] Source template detection prevents self-restoration
- [ ] Restoration overwrites only modified files
- [ ] User is notified which files were restored
- [ ] Remote update check occurs after local verification
- [ ] `version.yml` tracks last check timestamp and hash
""",

    "substrate/apoptosis.md": """\
# Apoptosis

## Definition

In the myskillium context, apoptosis refers to **the controlled, orderly removal of myskillium from a repository**. Just as biological apoptosis is programmed cell death that cleanly removes cells without damaging surrounding tissue, skill apoptosis cleanly removes myskillium without corrupting the host repository.

Key parallels:
- Programmed = deliberate user decision, not accidental deletion
- Orderly = follows specific sequence to avoid orphaned artifacts
- Clean removal = no residual hooks, settings, or broken references
- Non-destructive = host repository continues functioning normally

## Purpose

Provide a safe, complete method to remove myskillium from a repository:

1. **Disable monitoring** - Remove the SessionStart hook first to prevent resurrection
2. **Remove artifacts** - Delete all myskillium files and directories
3. **Preserve integrity** - Leave no orphaned references in settings
4. **Document removal** - Optional: record removal in git history

## Process

### Prerequisites

- Repository has myskillium installed (`.claude/skills/myskillium/` exists)
- User has write access to `.claude/` directory
- User understands removal is permanent (no homeostasis to restore)

### Phase 1: Disable Hook

**Critical**: The hook must be removed FIRST. If the directory is deleted while the hook remains, Claude Code sessions will fail with missing script errors.

Edit `.claude/settings.json` and remove the myskillium SessionStart hook entry:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python .claude/skills/myskillium/scripts/conidium.py"
          }
        ]
      }
    ]
  }
}
```

If this is the only SessionStart hook, the entire `SessionStart` array can be removed.

### Phase 2: Remove Script

Delete the conidium script:

```bash
rm .claude/skills/myskillium/scripts/conidium.py
```

Or on Windows:

```powershell
Remove-Item .claude\\skills\\myskillium\\scripts\\conidium.py
```

This prevents any possibility of accidental re-execution.

### Phase 3: Remove Directory

Delete the entire myskillium skill directory:

```bash
rm -rf .claude/skills/myskillium/
```

Or on Windows:

```powershell
Remove-Item -Recurse -Force .claude\\skills\\myskillium\\
```

This removes:
- `SKILL.md` - The skill definition
- `README.md` - Documentation
- `version.yml` - Version tracking
- `substrate/` - All process documentation
- `scripts/` - The scripts directory (now empty)

### Phase 4: Commit (Optional)

If tracking the removal in git history:

```bash
git add .claude/
git commit -m "chore: remove myskillium skill"
```

## Apoptosis vs Necrosis

| Aspect | Apoptosis (Controlled) | Necrosis (Uncontrolled) |
|--------|------------------------|------------------------|
| **Hook removal** | First step | Forgotten |
| **Sequence** | Hook → Script → Directory | Random deletion |
| **Result** | Clean removal | Orphaned hooks, errors |
| **Recovery** | Re-germinate if needed | Debug broken settings |

**Warning**: Simply deleting `.claude/skills/myskillium/` without removing the hook causes "necrosis" - the SessionStart hook will attempt to run a non-existent script, producing errors on every Claude Code session.

## Resurrection

Apoptosis is reversible. To restore myskillium after removal:

1. Obtain a fresh `conidium.py` from upstream or another repository
2. Place it anywhere in your repository
3. Run `python conidium.py --germinate`

The germination process will recreate the full skill structure and reinstall the hook.

## Relationship to Other Processes

| Process | Apoptosis Relationship |
|---------|----------------------|
| **Conidiation** | Apoptosis undoes germination |
| **Homeostasis** | Must be disabled (hook removal) before apoptosis succeeds |
| **Fragmentation** | Can extract skills before apoptosis if preservation needed |
| **Plasmogamy** | Can fuse skills before apoptosis if combining with another |

Apoptosis is the **inverse of germination**. Where germination creates and installs, apoptosis removes and uninstalls. The hook removal step is critical because homeostasis would otherwise attempt to restore removed files.

## Quick Reference

```bash
# Complete apoptosis sequence (Unix/Mac)
# 1. Edit .claude/settings.json - remove the SessionStart hook entry
# 2. Then run:
rm .claude/skills/myskillium/scripts/conidium.py
rm -rf .claude/skills/myskillium/
git add .claude/ && git commit -m "chore: remove myskillium"
```

```powershell
# Complete apoptosis sequence (Windows PowerShell)
# 1. Edit .claude/settings.json - remove the SessionStart hook entry
# 2. Then run:
Remove-Item .claude\\skills\\myskillium\\scripts\\conidium.py
Remove-Item -Recurse -Force .claude\\skills\\myskillium\\
git add .claude/ ; git commit -m "chore: remove myskillium"
```

## Checklist

- [ ] User confirms intent to remove myskillium
- [ ] SessionStart hook entry removed from `.claude/settings.json`
- [ ] `conidium.py` script deleted
- [ ] `.claude/skills/myskillium/` directory deleted
- [ ] No orphaned references in settings.json
- [ ] Changes committed to git (optional)
- [ ] User informed how to re-germinate if needed
""",

    "substrate/tropism.md": """\
# Tropism

## Definition

In the myskillium context, tropism refers to **the process of discovering and locating skills from external sources**. Just as biological tropism is directional growth toward stimuli (light, nutrients, water), skill tropism is directional search toward valuable skill sources across the ecosystem.

Key parallels:
- Stimulus = need for new capability or improvement
- Directional response = targeted search toward likely sources
- Growth toward = progressive refinement of search results
- Sensitivity = ability to detect skill-like patterns in repositories

## Purpose

Discover and evaluate external skills before acquisition:

1. **Identify sources** - Find repositories likely to contain useful skills
2. **Detect skills** - Recognize Claude Code skill patterns in codebases
3. **Evaluate fitness** - Assess whether a skill meets current needs
4. **Prepare for extraction** - Gather information needed for fragmentation

## Tropism Types

| Type | Stimulus | Response |
|------|----------|----------|
| **Chemotropism** | Keyword/concept need | Search for skills by functionality |
| **Phototropism** | Popular/trending sources | Grow toward well-maintained repositories |
| **Thigmotropism** | Direct reference/link | Follow explicit skill recommendations |
| **Hydrotropism** | Resource availability | Seek skills with good documentation |

## Process

### Prerequisites

- Clear understanding of capability gap or need
- Access to potential source repositories (GitHub, local clones)
- Criteria for evaluating skill fitness

### Phase 1: Stimulus Recognition

Define what capability is needed:

```markdown
## Skill Need Assessment
- What problem does this solve?
- What existing solutions have been tried?
- What would an ideal skill provide?
- What constraints must it satisfy?
```

### Phase 2: Source Discovery

Identify repositories likely to contain relevant skills:

**GitHub Search Patterns:**
```
# Find Claude Code skills by structure
path:.claude/skills filename:SKILL.md

# Find skills by keyword
path:.claude/skills "description:" <keyword>

# Find skills in specific org
org:<organization> path:.claude/skills
```

**Known Skill Sources:**
- `Mharbulous/Myskillium` - Skill management and genealogy
- `anthropics/claude-code` - Official Claude Code examples
- Project-specific repositories with `.claude/skills/` directories

### Phase 3: Skill Detection

Identify skill patterns in discovered repositories:

**Skill Indicators:**
| Pattern | Confidence | Notes |
|---------|------------|-------|
| `.claude/skills/<name>/SKILL.md` | High | Standard skill structure |
| YAML frontmatter with `name:` and `description:` | High | Skill metadata |
| `.claude/commands/<name>.md` | Medium | Slash command (simpler) |
| Process/workflow documentation | Low | May be convertible |

**Scan Command:**
```bash
# Check if repository has skills
ls -la <repo>/.claude/skills/ 2>/dev/null || echo "No skills directory"

# List all skills
find <repo>/.claude/skills -name "SKILL.md" -exec dirname {} \\;
```

### Phase 4: Fitness Evaluation

Assess whether discovered skill meets needs:

| Criterion | Question | Weight |
|-----------|----------|--------|
| **Functionality** | Does it solve the problem? | Critical |
| **Compatibility** | Works with current Claude Code version? | Critical |
| **Maintainability** | Is it actively maintained? | High |
| **Documentation** | Is usage well-documented? | Medium |
| **Dependencies** | Does it require external tools? | Medium |
| **Portability** | Can it be adapted to our context? | Medium |

**Fitness Score:**
- 3+ Critical criteria met → Proceed to fragmentation
- 1-2 Critical criteria met → Investigate further
- 0 Critical criteria met → Continue search

### Phase 5: Extraction Preparation

Gather information needed for fragmentation:

```json
{
  "candidate": {
    "sourceURL": "https://github.com/org/repo.git",
    "sourcePath": ".claude/skills/skill-name",
    "sourceCommit": "<current-HEAD>",
    "skillName": "<from-frontmatter>",
    "description": "<from-frontmatter>"
  },
  "evaluation": {
    "fitnessScore": "high|medium|low",
    "adaptationNeeded": ["list", "of", "changes"],
    "dependencies": ["external", "requirements"],
    "risks": ["potential", "issues"]
  },
  "decision": "proceed|defer|reject",
  "rationale": "Why this decision was made"
}
```

## Tropism Signals

### Positive Signals (Grow Toward)
- Active commit history
- Clear skill documentation
- Established pedigree/lineage
- Community adoption
- Test coverage

### Negative Signals (Grow Away)
- Abandoned repository
- Missing or unclear documentation
- Heavy project-specific dependencies
- No visible maintenance
- Incompatible license

## Relationship to Other Processes

| Process | Tropism Relationship |
|---------|---------------------|
| **Fragmentation** | Tropism discovers; fragmentation extracts |
| **Plasmogamy** | Tropism may find multiple skills suitable for fusion |
| **Homeostasis** | Tropism may detect upstream updates for existing skills |
| **Conidiation** | Tropism spreads awareness of available conidia |
| **Apoptosis** | Tropism may find replacement before removal |

Tropism is the **sensory process** that precedes action. It answers "where are useful skills?" before fragmentation answers "how do we acquire them?"

## Autonomous Tropism

In future iterations, tropism could become automated:

```python
# Conceptual: Automated skill discovery
def autonomous_tropism(need: str) -> list[SkillCandidate]:
    \"\"\"
    Periodically scan known sources for skills matching needs.
    Alert when high-fitness candidates discovered.
    \"\"\"
    sources = load_known_sources()
    candidates = []
    for source in sources:
        skills = scan_for_skills(source)
        for skill in skills:
            if evaluate_fitness(skill, need) > THRESHOLD:
                candidates.append(skill)
    return candidates
```

This would enable myskillium to proactively suggest skill acquisitions.

## Checklist

- [ ] Capability need clearly defined
- [ ] Source repositories identified
- [ ] Skill detection scan completed
- [ ] Candidate skills evaluated for fitness
- [ ] High-fitness candidates documented
- [ ] Extraction preparation info gathered
- [ ] Decision made: proceed, defer, or reject
- [ ] Rationale documented for future reference
- [ ] Handoff to fragmentation process (if proceeding)
""",

    "substrate/pedigree.json": """\
{
  "name": "{{skill.name}}",
  "description": "{{skill.description}}",
  "pedigree": [
    {
      "date": "YYYY-MM-DD",
      "sourceURL": "https://github.com/org/repo.git",
      "sourcePath": ".claude/skills/skill-name",
      "sourceCommitID": "abcdef1234567890abcdef1234567890abcdef12",
      "destURL": "https://github.com/org/repo.git",
      "destPath": ".claude/skills/skill-name",
      "destCommitID": "1234567890abcdef1234567890abcdef12345678",
      "destOperator": ".claude/skills/myskillium/SKILL.md",
      "destModel": "claude-opus-4-5-20251101"
    }
  ]
}
""",

    "SKILL.md": """\
---
name: myskillium
description: Use when migrating skills between repositories or extracting skills from a project into a reusable form. Handles copying, cleanup of project-specific references, and genealogy documentation.
---

# Mysk Extractor

Migrate and crossbreed skills between repositories while documenting provenance for reproducibility research.

## Processes

This skill defines six processes, named after mycological and cellular biology:

| Process | File | Description |
|---------|------|-------------|
| **Conidiation** | `substrate/conidiation.md` | Spore production - create/update the portable extraction tool |
| **Fragmentation** | `substrate/fragmentation.md` | Asexual reproduction - extract a skill from a single source repo |
| **Plasmogamy** | `substrate/plasmogamy.md` | Sexual reproduction - fuse two skills into a hybrid |
| **Homeostasis** | `substrate/homeostasis.md` | Self-regulation - maintain process consistency across repositories |
| **Apoptosis** | `substrate/apoptosis.md` | Programmed death - controlled removal/uninstallation |
| **Tropism** | `substrate/tropism.md` | Sensory process - discover and locate skills from external sources |

## Pedigree Schema

Every extracted skill gets a genealogy file documenting its lineage.

### Schema Structure

See `genealogy/templates/pedigree.json` for the schema template.

### Field Reference

| Field | Purpose |
|-------|---------|
| `date` | When the extraction occurred |
| `sourceURL` | Git URL of the source repository |
| `sourcePath` | Path to skill within source repo |
| `sourceCommitID` | Exact commit hash at extraction time |
| `destURL` | Git URL of the destination repository |
| `destPath` | Path to skill within destination repo |
| `destCommitID` | Commit hash after extraction was committed |
| `destOperator` | The skill file that performed the extraction |
| `destModel` | Claude model ID that executed the operator |

### Crossbreeding Support

The `pedigree` array supports multiple entries for hybrid skills:
- Single entry = conidiation (one parent)
- Multiple entries = plasmogamy (multiple parents fused)

## Experimental Design: Isolated Agents

### Why Exclude Human Input

The pedigree schema captures all variables needed to theoretically reproduce a skill extraction:
- Source content (via `sourceCommitID`)
- Transformation logic (via `destOperator` at `destCommitID`)
- Model version (via `destModel`)

However, if human prompts influence the extraction, they become an uncontrolled variable that breaks reproducibility.

### Isolating Claude's Non-Determinism

By designing extraction processes to:
1. **Spawn subagents** rather than work in the main conversation
2. **Feed structured data** rather than conversation history
3. **Exclude human prompt context** from the transformation

We control for all external variables, leaving **Claude's inherent non-determinism as the only remaining variable**.

This enables experiments like:
- Run identical extractions N times → measure output variance
- Compare variance across different operator designs
- Correlate variance with task complexity

The pedigree file serves dual purposes:
1. **Genealogy record** - trace skill ancestry
2. **Experimental control log** - prove all controllable variables were fixed

### Implications for Process Design

Both `fragmentation.md` and `plasmogamy.md` processes MUST:
- Use the Task tool to spawn isolated subagents
- Provide all context via structured parameters, not conversation history
- Record the exact operator and model in the pedigree

## Templates

| File | Purpose |
|------|---------|
| `genealogy/templates/migration-config.json` | Migration configuration structure |
| `genealogy/templates/pedigree.json` | Pedigree file template |

## Workflow (Fragmentation)

See `substrate/fragmentation.md` for the full single-source extraction workflow.

High-level phases:
1. **Configure** - Define source/destination and cleanup rules
2. **Copy** - Transfer skill files
3. **Cleanup** - Generalize project-specific references
4. **Genealogy** - Create pedigree record
5. **Commit** - Finalize with descriptive message

## Checklist

- [ ] Process spawns isolated subagent (no conversation context)
- [ ] Subagent receives structured data only
- [ ] Skills copied to destination
- [ ] Project names generalized
- [ ] Domain terms universalized
- [ ] Pedigree file created with all fields populated
- [ ] destCommitID recorded after commit
""",
}


# ============================================================================
# HASH CALCULATION
# ============================================================================

_EMBEDDED_HASH = None


def calculate_hash(content: str) -> str:
    """Calculate SHA-256 hash of content."""
    _hashlib = _import_hashlib()
    return _hashlib.sha256(content.encode("utf-8")).hexdigest()


def calculate_embedded_hash() -> str:
    """Calculate combined hash of all embedded docs (cached)."""
    global _EMBEDDED_HASH
    if _EMBEDDED_HASH is not None:
        return _EMBEDDED_HASH

    combined = "".join(
        f"{name}:{calculate_hash(content)}"
        for name, content in sorted(EMBEDDED_DOCS.items())
    )
    _EMBEDDED_HASH = calculate_hash(combined)
    return _EMBEDDED_HASH


def calculate_local_hash(project_root: Path) -> str:
    """Calculate combined hash of all local process files."""
    combined_parts = []
    for name in sorted(EMBEDDED_DOCS.keys()):
        filepath = project_root / MYSKILLIUM_DIR / name
        if filepath.exists():
            content = filepath.read_text(encoding="utf-8")
            combined_parts.append(f"{name}:{calculate_hash(content)}")
        else:
            combined_parts.append(f"{name}:{calculate_hash('')}")
    return calculate_hash("".join(combined_parts))


def find_drifted_files(project_root: Path) -> list[str]:
    """Return list of files that differ from embedded versions."""
    drifted = []
    for name, embedded_content in EMBEDDED_DOCS.items():
        filepath = project_root / MYSKILLIUM_DIR / name
        if not filepath.exists():
            drifted.append(name)
        else:
            local_content = filepath.read_text(encoding="utf-8")
            if calculate_hash(local_content) != calculate_hash(embedded_content):
                drifted.append(name)
    return drifted


# ============================================================================
# VERSION FILE HANDLING
# ============================================================================

def _extract_hash_from_yml(content: str) -> str | None:
    """Extract hash value from version.yml content."""
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("hash:"):
            return line.split(":", 1)[1].strip().strip('"\'')
    return None


def read_version_yml(project_root: Path) -> dict:
    """Read version.yml and return parsed data."""
    version_path = project_root / VERSION_FILE
    result = {"last_check": None, "hash": None}

    if not version_path.exists():
        return result

    try:
        content = version_path.read_text(encoding="utf-8")
        result["hash"] = _extract_hash_from_yml(content)
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("last_check:"):
                ts_str = line.split(":", 1)[1].strip().strip('"\'')
                try:
                    dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)
                    result["last_check"] = dt
                except ValueError:
                    pass
                break
    except (OSError, IOError):
        pass

    return result


def write_version_yml(project_root: Path, embedded_hash: str) -> None:
    """Write version.yml with current timestamp and hash."""
    version_path = project_root / VERSION_FILE
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    content = f"""# Myskillium Version Tracking
# Auto-generated - do not edit manually
last_check: "{timestamp}"
hash: "{embedded_hash}"
"""
    try:
        version_path.parent.mkdir(parents=True, exist_ok=True)
        version_path.write_text(content, encoding="utf-8")
    except (OSError, IOError):
        pass


def hours_since_last_check(project_root: Path) -> float:
    """Calculate hours since the last check."""
    version_data = read_version_yml(project_root)
    last_check = version_data.get("last_check")

    if last_check is None:
        return float("inf")

    now = datetime.now(timezone.utc)
    delta = now - last_check
    return delta.total_seconds() / 3600


# ============================================================================
# SOURCE TEMPLATE DETECTION
# ============================================================================

def is_source_template(project_root: Path) -> bool:
    """Check if this is the Myskillium source template."""
    _subprocess = _import_subprocess()
    source_pattern = f"{_SOURCE_OWNER}/{_SOURCE_REPO}"
    try:
        result = _subprocess.run(
            ["git", "remote", "-v"],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=2.0,
        )
        if result.returncode == 0:
            return source_pattern in result.stdout
    except (_subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
    return False


# ============================================================================
# GIT REPOSITORY DETECTION
# ============================================================================

def get_git_remote_url(project_root: Path) -> str | None:
    """Get the git remote URL for origin."""
    _subprocess = _import_subprocess()
    try:
        result = _subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=2.0,
        )
        if result.returncode == 0:
            url = result.stdout.strip()
            # Normalize SSH URLs to HTTPS format for consistency
            if url.startswith("git@github.com:"):
                url = url.replace("git@github.com:", "https://github.com/")
            if not url.endswith(".git"):
                url = url + ".git"
            return url
    except (_subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
    return None


def get_git_head_commit(project_root: Path) -> str | None:
    """Get the current HEAD commit hash."""
    _subprocess = _import_subprocess()
    try:
        result = _subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=2.0,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (_subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
    return None


# ============================================================================
# PEDIGREE GENERATION
# ============================================================================

def generate_pedigree_json(project_root: Path) -> str:
    """Generate pedigree.json content with source and destination info.

    Source info comes from _CONIDIUM_SOURCE (embedded in this script).
    Destination info is detected from the current repository.
    """
    _json = _import_json()

    # Get destination repo info
    dest_url = get_git_remote_url(project_root) or "UNKNOWN"
    dest_commit = get_git_head_commit(project_root) or "PENDING"

    # Get current date
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    pedigree_data = {
        "name": "myskillium",
        "description": "Skill migration and genealogy tracking tool",
        "pedigree": [
            {
                "date": date_str,
                "sourceURL": _CONIDIUM_SOURCE["url"],
                "sourcePath": _CONIDIUM_SOURCE["path"],
                "sourceCommitID": _CONIDIUM_SOURCE["commit"],
                "destURL": dest_url,
                "destPath": MYSKILLIUM_DIR,
                "destCommitID": dest_commit,
                "destOperator": "conidium.py --germinate",
                "destModel": "N/A (script execution)"
            }
        ]
    }

    return _json.dumps(pedigree_data, indent=2)


def update_conidium_source_metadata(script_content: str, new_url: str, new_path: str, new_commit: str) -> str:
    """Update the _CONIDIUM_SOURCE metadata in the script content.

    This modifies the script so that when it's copied to another repo,
    it will have the correct source information for the chain of custody.
    """
    import re

    # Pattern to match the _CONIDIUM_SOURCE dictionary block at module level only
    # Uses ^ with MULTILINE to only match unindented (top-level) definitions
    # This prevents matching the template inside the update function itself
    pattern = r'^_CONIDIUM_SOURCE = \{[^}]+\}'

    replacement = f'''_CONIDIUM_SOURCE = {{
    "url": "{new_url}",
    "path": "{new_path}",
    "commit": "{new_commit}",
}}'''

    # Use MULTILINE so ^ matches start of lines, and DOTALL for newlines in content
    updated = re.sub(pattern, replacement, script_content, flags=re.MULTILINE)

    return updated


# ============================================================================
# REMOTE UPDATE CHECK
# ============================================================================

def fetch_remote_hash(timeout: float = 5.0) -> str | None:
    """Fetch remote hash from version.yml on GitHub."""
    _urllib_request, _urllib_error = _import_urllib()
    try:
        req = _urllib_request.Request(
            REMOTE_VERSION_URL,
            headers={"User-Agent": "Myskillium-Conidium/1.0"}
        )
        with _urllib_request.urlopen(req, timeout=timeout) as response:
            content = response.read().decode("utf-8")
            return _extract_hash_from_yml(content)
    except (_urllib_error.URLError, _urllib_error.HTTPError, TimeoutError, OSError):
        return None


# ============================================================================
# PROJECT ROOT DETECTION
# ============================================================================

def get_project_root() -> Path:
    """Get the project root directory."""
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR")
    if project_dir:
        return Path(project_dir)
    return Path.cwd()


# ============================================================================
# GERMINATION MODE
# ============================================================================

def germinate(project_root: Path, force: bool = False) -> None:
    """Bootstrap myskillium into the repository."""
    myskillium_dir = project_root / MYSKILLIUM_DIR

    # Check if already exists
    if myskillium_dir.exists() and not force:
        print("## Warning: Myskillium Already Exists")
        print()
        print(f"Directory `{MYSKILLIUM_DIR}` already exists.")
        print()
        response = input("Overwrite? [y/N]: ").strip().lower()
        if response != "y":
            print("Aborted.")
            sys.exit(1)

    # Create directory structure
    substrate_dir = project_root / SUBSTRATE_DIR
    scripts_dir = project_root / SCRIPTS_DIR
    substrate_dir.mkdir(parents=True, exist_ok=True)
    scripts_dir.mkdir(parents=True, exist_ok=True)

    # Write embedded files EXCEPT pedigree.json (which is generated dynamically)
    for name, content in EMBEDDED_DOCS.items():
        if name == "substrate/pedigree.json":
            continue  # Skip - will be generated dynamically
        filepath = project_root / MYSKILLIUM_DIR / name
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content, encoding="utf-8")

    # Generate pedigree.json dynamically with source/destination info
    pedigree_path = project_root / SUBSTRATE_DIR / "pedigree.json"
    pedigree_content = generate_pedigree_json(project_root)
    pedigree_path.write_text(pedigree_content, encoding="utf-8")

    # Get destination repo info for updating the script's source metadata
    dest_url = get_git_remote_url(project_root) or "UNKNOWN"
    dest_commit = get_git_head_commit(project_root) or "PENDING"

    # Copy this script to scripts directory, updating source metadata
    # so future copies from THIS repo have correct lineage
    this_script = Path(__file__).resolve()
    target_script = project_root / SCRIPTS_DIR / "conidium.py"
    if this_script != target_script:
        script_content = this_script.read_text(encoding="utf-8")
        # Update source metadata to point to THIS repo (destination becomes new source)
        updated_content = update_conidium_source_metadata(
            script_content,
            new_url=dest_url,
            new_path=MYSKILLIUM_DIR,
            new_commit=dest_commit
        )
        target_script.write_text(updated_content, encoding="utf-8")

    # Update settings.json with hook
    update_settings_hook(project_root)

    # Write version.yml
    write_version_yml(project_root, calculate_embedded_hash())

    print("## Myskillium Germinated")
    print()
    print(f"Created skill structure at `{MYSKILLIUM_DIR}/`")
    print()
    print("Files created:")
    for name in sorted(EMBEDDED_DOCS.keys()):
        if name == "substrate/pedigree.json":
            print(f"  - {name} (generated with lineage)")
        else:
            print(f"  - {name}")
    print(f"  - scripts/conidium.py")
    print()
    print("Pedigree lineage:")
    print(f"  Source: {_CONIDIUM_SOURCE['url']}")
    print(f"  Dest:   {dest_url}")
    print()
    print("SessionStart hook installed in `.claude/settings.json`")
    print()
    print("Next steps:")
    print("```")
    print("git add .claude/")
    print('git commit -m "feat: add myskillium skill"')
    print("```")


def update_settings_hook(project_root: Path) -> None:
    """Add SessionStart hook to settings.json using the new matcher format."""
    _json = _import_json()
    settings_path = project_root / SETTINGS_FILE

    # Read existing settings or create new
    if settings_path.exists():
        try:
            settings = _json.loads(settings_path.read_text(encoding="utf-8"))
        except _json.JSONDecodeError:
            settings = {}
    else:
        settings = {}
        settings_path.parent.mkdir(parents=True, exist_ok=True)

    # Ensure hooks structure exists
    if "hooks" not in settings:
        settings["hooks"] = {}
    if "SessionStart" not in settings["hooks"]:
        settings["hooks"]["SessionStart"] = []

    # Check if hook already exists (new format with matcher/hooks structure)
    hook_command = "python .claude/skills/myskillium/scripts/conidium.py"

    def hook_exists_in_entry(entry):
        """Check if our hook command exists in a hook entry."""
        if not isinstance(entry, dict):
            return False
        hooks_list = entry.get("hooks", [])
        return any(
            h.get("command") == hook_command
            for h in hooks_list
            if isinstance(h, dict)
        )

    hook_exists = any(
        hook_exists_in_entry(entry)
        for entry in settings["hooks"]["SessionStart"]
    )

    if not hook_exists:
        # SessionStart hooks don't require matcher - omit it to run on all session starts
        settings["hooks"]["SessionStart"].append({
            "hooks": [
                {
                    "type": "command",
                    "command": hook_command
                }
            ]
        })

    # Write updated settings
    settings_path.write_text(
        _json.dumps(settings, indent=2) + "\n",
        encoding="utf-8"
    )


# ============================================================================
# HOMEOSTASIS MODE
# ============================================================================

def homeostasis(project_root: Path) -> None:
    """Run homeostasis check and restoration."""

    # ==== STEP 1: 24-Hour Fast Path ====
    if hours_since_last_check(project_root) < 24:
        sys.exit(0)

    # ==== STEP 2: Source Template Detection ====
    if is_source_template(project_root):
        sys.exit(0)

    # ==== STEP 3: Hash Comparison ====
    embedded_hash = calculate_embedded_hash()
    local_hash = calculate_local_hash(project_root)

    if local_hash != embedded_hash:
        # Find which files drifted
        drifted = find_drifted_files(project_root)

        # Restore drifted files
        for name in drifted:
            filepath = project_root / MYSKILLIUM_DIR / name
            filepath.parent.mkdir(parents=True, exist_ok=True)
            filepath.write_text(EMBEDDED_DOCS[name], encoding="utf-8")

        write_version_yml(project_root, embedded_hash)

        print("## Myskillium Processes Restored")
        print()
        print("The following files were restored to canonical versions:")
        for name in drifted:
            print(f"  - {name}")
        print()
        print("This ensures consistency across all repositories using myskillium.")
        sys.exit(0)

    # ==== STEP 4: Remote Update Check ====
    remote_hash = fetch_remote_hash()

    if remote_hash is None:
        # Network error - update timestamp to avoid retry storm
        write_version_yml(project_root, embedded_hash)
        sys.exit(0)

    if remote_hash != embedded_hash:
        # Update available - don't update timestamp (reminder on next session)
        print("## Myskillium Update Available")
        print()
        print("A new version of myskillium is available upstream.")
        print()
        print("To update, run:")
        print("```")
        print("python sync-myskillium.py")
        print("```")
        print()
        print("Or copy the latest `conidium.py` from Myskillium and run:")
        print("```")
        print("python conidium.py --germinate")
        print("```")
        sys.exit(0)

    # ==== Everything up to date ====
    write_version_yml(project_root, embedded_hash)
    sys.exit(0)


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point."""
    project_root = get_project_root()

    # Check for --germinate flag
    if "--germinate" in sys.argv:
        force = "--force" in sys.argv
        germinate(project_root, force=force)
    else:
        homeostasis(project_root)


if __name__ == "__main__":
    main()
