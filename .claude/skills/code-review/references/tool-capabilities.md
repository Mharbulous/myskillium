# AI Code Review Tool Capabilities

*Research Date: December 2025*

## CodeRabbit

**Type:** Specialized AI Code Review Platform
**Pricing:** Free tier, Lite ($12/mo), Pro ($24/mo per developer)
**Scale:** 2M+ repositories, 13M+ PRs processed

### What It Checks

| Category | Capabilities |
|----------|-------------|
| **Bugs** | Off-by-ones, edge cases, logic errors |
| **Security** | Vulnerabilities, secrets, race conditions, security holes |
| **Performance** | Not optimal implementations |
| **Architecture** | Architectural drift, pattern violations |
| **Style** | Coding style consistency across modules |
| **Testing** | Missing tests detection |

### Key Features

- **40+ industry tools** - linters, security analyzers, performance checkers
- **AST Analysis** - understands code structure and semantics, not just patterns
- **Full codebase context** - considers entire codebase, not just changed files
- **5-second reviews** - much faster than competitors
- **Interactive chat** - @coderabbitai in PR for follow-up
- **Agentic actions** - generate tests, draft docs, open Jira/Linear issues
- **Learning** - applies preferences to future reviews
- **SOC 2 Type II certified** - ephemeral containers, no code retention

### Integrations

- GitHub, GitLab, Azure DevOps, Bitbucket
- VS Code, Cursor, Windsurf extensions
- Jira, Linear (Pro plan)

---

## GitHub Copilot Code Review

**Type:** Integrated GitHub Feature
**Pricing:** Pro, Pro+, Business, Enterprise plans
**Availability:** GA April 2025

### What It Checks

| Category | Capabilities |
|----------|-------------|
| **Bugs** | Code issues, potential bugs |
| **Performance** | Performance problems |
| **Security** | Via CodeQL integration, security vulnerabilities |
| **Quality** | Via ESLint, PMD integration |
| **Context** | Full project architecture understanding |

### Key Features

- **Static analysis fusion** - combines LLM with CodeQL, ESLint, PMD
- **Agentic context gathering** - reads directory structure, references
- **Actionable suggestions** - click to apply fixes
- **Coding agent handoff** - @copilot applies fixes in stacked PR
- **Custom instructions** - copilot-instructions.md for team standards

### Integrations

- VS Code, Visual Studio, JetBrains, Xcode
- Native github.com integration

### Limitations

- Risk of hallucination - may flag non-existent problems
- Large/complex changes may miss issues
- Must supplement with human review

---

## Semgrep

**Type:** SAST Platform
**Pricing:** Free tier, Team, Enterprise
**Registry:** 2,000+ community rules

### What It Detects

| Category | Capabilities |
|----------|-------------|
| **Security** | Injection, deserialization, XXE, OWASP Top 10 |
| **Secrets** | Credentials, API keys, auth tokens |
| **Correctness** | Bug patterns, logic issues |
| **Style** | Best practice violations |

### Key Features

- **Pattern matching** - rules look like code, easy to write/read
- **Data flow analysis** - tracks tainted data through code
- **Cross-file analysis** (Pro) - understands function calls across files
- **Reachability analysis** - reduces false positives by 98% for dependencies
- **AI-powered filtering** - contextual noise reduction
- **19+ languages** - broad framework support

### Frameworks Supported

Express, Spring, Java Servlets, Laravel, Go net/http, React, Next.js, Angular

### Rule Writing

```yaml
rules:
  - id: hardcoded-password
    pattern: password = "..."
    message: Hardcoded password detected
    severity: ERROR
```

---

## SonarQube

**Type:** Continuous Code Quality Platform
**Pricing:** Community (free), Developer, Enterprise, Data Center
**Scale:** 7M+ developers, 400K+ organizations

### What It Detects

| Category | Description |
|----------|-------------|
| **Bugs** | Something wrong that will break |
| **Code Smells** | Maintainability issues, confusing code |
| **Vulnerabilities** | Security issues |
| **Security Hotspots** | Security-sensitive code needing review |
| **Duplications** | Repeated code blocks |

### Code Smell Examples

- Large classes / long methods
- Duplicated code
- Complex methods (cyclomatic complexity)
- Poor naming conventions
- Missing documentation
- Unused variables/imports

### Key Features

- **6,500+ rules** - including taint analysis for security
- **35+ languages** - broad coverage
- **Real-time IDE plugin** - SonarQube for IDE
- **Quality Gates** - pass/fail criteria for CI/CD
- **Technical debt tracking** - time estimates to fix
- **SBOM generation** - software bill of materials
- **AI CodeFix** - LLM-suggested one-click corrections

### Metrics Tracked

- Code coverage
- Duplications
- Maintainability rating
- Reliability rating
- Security rating
- Technical debt ratio

---

## Tool Comparison Matrix

| Feature | CodeRabbit | Copilot | Semgrep | SonarQube |
|---------|------------|---------|---------|-----------|
| AI-Powered | Yes | Yes | Partial | Partial |
| Real-time IDE | Yes | Yes | Yes | Yes |
| PR Review | Yes | Yes | CI/CD | CI/CD |
| Custom Rules | Limited | Instructions | Yes | Yes |
| Security Focus | Medium | Medium | High | High |
| Free Tier | Yes | No | Yes | Yes |
| Self-hosted | No | No | Yes | Yes |
| Speed | 5 sec | Varies | Fast | Varies |

## Recommended Stack (Example)

For a typical Python application:

1. **Primary:** SonarQube Community (free, Python support, comprehensive)
2. **Security:** Semgrep (excellent Python rules, secrets detection)
3. **Optional PR Review:** CodeRabbit Free (if using GitHub PRs)

## Sources

- [CodeRabbit Documentation](https://docs.coderabbit.ai/)
- [CodeRabbit on Massive Codebases](https://www.coderabbit.ai/blog/how-coderabbit-delivers-accurate-ai-code-reviews-on-massive-codebases)
- [GitHub Copilot Code Review Docs](https://docs.github.com/en/copilot/concepts/agents/code-review)
- [Semgrep Documentation](https://semgrep.dev/docs/running-rules)
- [SonarQube](https://www.sonarsource.com/products/sonarqube/)
- [Understanding Code Smells](https://www.sonarsource.com/resources/library/code-smells/)
