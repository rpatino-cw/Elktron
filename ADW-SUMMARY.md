# Agentic Developer Workflows (ADW) — CoreWeave IDP Platform

> **Team:** Internal Developer Platforms (IDP)
> **Authors:** Ankur Manga, Jack Yin, Vince Liang, Arzoo Singh, Devi Sridharan
> **Status:** Approved | **Jira:** IDPLAT-85
> **Slack:** #wg-agentic-dev-workflows-platform

---

## TL;DR

CoreWeave's IDP team is building a platform that lets AI agents safely do developer work — reviewing PRs, generating tests, deploying code, and handling incidents. It uses a 4-layer stack (Knowledge, Tools, MCP Servers, Agentic Experiences), runs agents in isolated Coder workspaces, connects tools via MCP (Model Context Protocol), and enforces strict safety guardrails (human-in-the-loop, RBAC, audit logging, autonomy levels 0-3). The first two MVPs are a **Code Review Agent** and a **Test Generation Agent**, both targeting Go repos.

---

## The 4-Layer Stack

### Layer 1 — Knowledge & Context
- Unified index over code, docs, specs, runbooks, incidents
- Sourcegraph for cross-repo semantic code search (500+ repos, sub-second)
- RAG pipelines for developer queries
- Context engineering: instructions + requirements + validation

### Layer 2 — Developer Tools & Services
- CW-CLI, remote dev (CoreEnv), CI/CD APIs, scaffolding tools
- Modeled as high-level "verbs" agents can call: `run_test_suite`, `promote_release`, `create_remote_dev_env`
- Idempotent, observable, with dry-run modes

### Layer 3 — MCP Servers & Registry
- MCP (Model Context Protocol) = "USB-C for AI agents"
- Wraps tools/data sources into standardized servers agents can discover and call
- IDP-owned central registry with: ownership, permissions, env scope, versioning, stability, safety level
- Core servers: sourcegraph-mcp, github-mcp, cw-cli-mcp, ci-cd-mcp, coder-mcp, glean-mcp, atlassian-mcp

### Layer 4 — Agentic Experiences
- **Inner Loop:** Coding assistants (extend Cursor/Claude Code with CW MCP servers)
- **Integration Loop:** PR review agents, test generation agents
- **Deployment Loop:** Release agents, incident copilots

---

## Safety & Governance (Non-Negotiable)

- **Human-in-the-loop by default** for high-risk actions (code, infra, deployments)
- **Autonomy Levels:**
  - Level 0: Suggest Only (default for all new workflows)
  - Level 1: Low-Risk Auto (non-prod, sandboxed)
  - Level 2: Semi-Autonomous (human approval for risky steps)
  - Level 3: Fully Autonomous (only validated, reversible workflows)
- **Hard prohibitions:** No direct commits, infra changes, prod mutations, or dependency additions without human approval
- **Full observability:** Every MCP/tool call logged, attributable, reviewable
- **Policy gates:** Security scanners, linting, vulnerability checks apply to AI and human changes equally
- **Continuous monitoring:** Drift detection, misbehavior detection, auto-disable

---

## MVP 1 — Code Review Agent (Integration Loop)

- Triggered on PR open (`pull_request.opened`, `pull_request.synchronize`)
- Assembles context via MCP: diff + symbols + callers + tests + review guidelines
- 5 specialized agents: Correctness, Security, Performance, Standards, Test Coverage
- Coordinator merges findings into single structured PR comment
- Severity levels: must-fix, should-fix, nice-to-have
- Autonomy Level 0 (suggest only)
- Target: <5 min from PR open to review posted, >70% helpful rating

## MVP 2 — Test Generation Agent

- Triggered by `/generate-tests` PR comment
- Analyzes diff, cross-references Codecov coverage data
- Generates unit tests for uncovered new functions
- **Validation loop:** compile + run each test before suggesting (max 3 retries)
- Go-first (standardized testing, majority of CW codebase)
- Target: >50% test acceptance rate, <8 min generation time

---

## Technical Architecture

### Execution Environment
- **Coder Tasks** (CoreEnv) — isolated, ephemeral Kata VM workspaces per agent
- KataWeave isolation + CrowdStrike Falcon + BlastShield egress control
- Agent Boundaries: network domain allowlists, method restrictions, audit logging

### Platform Services
- **API Gateway** (Kynes/ConnectRPC): REST + gRPC, JWT/API Key/Console Token auth, RBAC, rate limiting
- **Control Plane:** Workflow orchestration, execution state machine, Coder provisioning
- **MCP Gateway:** Tool routing, agent status reporting, org-scoped registry
- **Database:** PostgreSQL (CWDB) with JSONB workflow definitions, execution state, audit logs
- **Redis:** Leader election, distributed locks, rate limiting

### CW-Agent-SDK (Go)
```
cw-agent-sdk/
  workflowkit/   — Workflow orchestration (parse YAML, execute steps, checkpoints)
  agentkit/      — Provider adapters (Claude Agent SDK, OpenAI Agents SDK via subprocess)
  skillskit/     — Load & inject skills as context
  knowledgekit/  — Code context (Sourcegraph), PR context (GitHub), docs (Confluence/Glean)
  auth/          — OIDC/JWT, agent tokens
  observability/ — Metrics, cost tracking, audit trail
```

### Agent Definition (cw-ai-agents repo)
```yaml
name: code-review-agent
backend: claude           # or openai
boundary:
  allow:
    - domain: api.github.com
      methods: [GET, POST, PATCH]
  block:
    - domain: "*.external-service.com"
inputs:
  - name: pr_url
    required: true
prompts:
  default: prompts/default.md
skills:
  - skills/code-review/SKILL.md
mcp:
  config: mcp/.mcp.json
runners:
  claude: runners/claude.sh
  openai: runners/openai.py
```

### Workflow Definition
```yaml
apiVersion: agentic.coreweave.com/v1
kind: Workflow
metadata:
  name: code-review-workflow
spec:
  triggers:
    - type: github
      event: pull_request
      actions: [opened, synchronize]
  governance:
    autonomyLevel: 0
    auditLogging: true
  steps:
    - name: fetch-context
      agent: context-assembler
      inputs:
        pr: "{{ trigger.pull_request }}"
    - name: review-code
      agent: code-review-agent
      inputs:
        context: "{{ steps.fetch-context.outputs.context }}"
    - name: post-review
      agent: github-commenter
      inputs:
        review: "{{ steps.review-code.outputs.review }}"
```

---

## Roadmap

| Phase | What Ships | Timeline |
|-------|-----------|----------|
| 0 — Foundations | CoreEnv GA, Sourcegraph eval, MCP hosting design | Current |
| 1 — MCP Enablement | Core MCP servers, registry v1, CW-Agent-SDK v0.1 | Q1 2026 |
| 2 — First Agents | Code Review Agent, Test Gen Agent, IDE integration | Q1-Q2 2026 |
| 3 — Expansion | Deployment agents, team MCP servers, self-service registry | Q2-Q3 2026 |
| 4 — Maturity | Usage analytics, cost management, drift detection, enterprise-wide | Q3-Q4 2026 |

---

## Security Summary

- **Auth chain:** JWT (OIDC) → API Key (`cwak_` prefix, SHA-256 hashed) → Console Token (WhoAmI) → Agent Token (execution-scoped, 24h TTL) → Webhook HMAC (SHA-256)
- **RBAC roles:** Viewer → Member → Admin → Owner
- **Production safeguards:** Force RBAC on, force JWT validation on in prod
- **Network policies:** K8s NetworkPolicy per service; agent boundaries per workspace
- **Encryption:** AES-256-GCM for MCP server env vars and workflow secrets at rest
- **Audit:** All requests logged (including unauthenticated), 90-day retention
- **Container security:** Chainguard static base, runAsNonRoot, readOnlyRootFilesystem, drop ALL capabilities

---

## Key People

| Role | Person |
|------|--------|
| Engineering Manager, IDP | Ankur Manga |
| Platform Lead | Jack Yin |
| Contributors | Vince Liang, Arzoo Singh, Devi Sridharan |

---

## Related Links

- Jira: IDPLAT-85
- Slack: #wg-agentic-dev-workflows-platform
- Coder Tasks: https://coder.com/docs/ai-coder/tasks
- MCP Spec: https://modelcontextprotocol.io
- Sourcegraph: https://sourcegraph.com
