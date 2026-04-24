# GStack Skills Guide for Web Agency Workflow

> Last updated: 2026-04-24
> Context: WordPress/PHP web agency, daily development + client delivery

## Quick Reference

```
Daily:     /browse  /qa  /investigate  /review  /ship
Weekly:    /design-review  /health  /plan-eng-review  /checkpoint
Per-project: /design-html  /qa-only  /cso  /setup-browser-cookies
```

## Tier 1 — Daily Use

### /browse
Fast headless browser for QA testing and site dogfooding.

**When:** Test client sites, verify forms, check responsive layouts, take screenshots for bug reports.

```
/browse https://client-site.com
```

- ~100ms per command
- Navigate, click, fill forms, take annotated screenshots
- Diff before/after actions
- Test responsive layouts at different breakpoints

**Tip:** Always use `/browse` instead of `mcp__claude-in-chrome__*` tools.

### /qa
Systematically QA test a web application and fix bugs found.

**When:** Before client delivery. Finds bugs, fixes them in source code, commits each fix atomically, re-verifies.

```
/qa https://staging.client-site.com
```

- Three tiers: Quick (critical/high), Standard (+ medium), Exhaustive (+ cosmetic)
- Produces before/after health scores and ship-readiness summary
- For report-only (no fixes): use `/qa-only` instead

### /investigate
Systematic debugging with root cause investigation.

**When:** Client reports "it's broken", 500 errors, unexpected behavior, "it was working yesterday".

```
/investigate why the contact form returns 500 on submit
```

- Four phases: investigate → analyze → hypothesize → implement
- Iron Law: no fixes without root cause
- Prevents the "try random things" debugging anti-pattern

### /review
Pre-landing PR review.

**When:** Before merging code. Analyzes diff against base branch.

```
/review
```

- Checks: SQL safety, LLM trust boundaries, conditional side effects
- Structural issue detection in the diff
- Complements `/project:review-with` (which gets a second opinion from another AI)

### /ship
Ship workflow: test → review → changelog → commit → push → PR.

**When:** Code is ready to deploy.

```
/ship
```

- Detects + merges base branch
- Runs tests
- Reviews diff
- Bumps VERSION, updates CHANGELOG
- Creates PR

**Follow-up:** Use `/land-and-deploy` after PR is approved to merge + verify production.

## Tier 2 — Weekly / Per-Project

### /design-review
Designer's eye QA for live sites.

**When:** After building a page template, before showing to client.

```
/design-review https://staging.client-site.com/about
```

- Finds: spacing issues, visual inconsistency, hierarchy problems, AI slop patterns
- Iteratively fixes issues in source code with before/after screenshots
- For plan-mode design review (before implementation): use `/plan-design-review`

### /health
Code quality dashboard.

**When:** Before project delivery, or weekly to track trends.

```
/health
```

- Runs: type checker, linter, test runner, dead code detector
- Weighted composite 0–10 score
- Tracks trends over time

### /plan-eng-review
Engineering plan review.

**When:** Before starting a new project or major feature — lock in architecture.

```
/plan-eng-review
```

- Reviews: architecture, data flow, edge cases, test coverage, performance
- Interactive walkthrough with opinionated recommendations
- Use after writing a plan (in plan mode)

### /design-html
Generate production-quality HTML/CSS from design descriptions.

**When:** Turning approved designs into code, building page templates.

```
/design-html
```

- Works with approved mockups or descriptions
- Text reflows, dynamic layouts, computed heights
- 30KB overhead, zero deps
- Good starting point before integrating into WordPress theme

### /checkpoint
Save and resume working state.

**When:** End of day, switching between projects, before a long break.

```
/checkpoint
```

- Captures: git state, decisions made, remaining work
- Resume exactly where you left off, even across branches
- Useful for multi-project agency work

## Tier 3 — Situational

### /qa-only
Report-only QA testing — finds bugs but doesn't fix them.

**When:** Client wants a bug report, or you need to hand off QA findings to another developer.

```
/qa-only https://client-site.com
```

- Structured report with health score, screenshots, repro steps
- No code changes made

### /cso
Security audit.

**When:** Before launch, especially for sites handling user data, payments, or forms.

```
/cso
```

- Secrets archaeology, dependency supply chain, OWASP Top 10
- Two modes: daily (zero-noise) and comprehensive (monthly deep scan)
- STRIDE threat modeling

### /setup-browser-cookies
Import cookies from your real browser into the headless browse session.

**When:** Before QA testing authenticated pages (WP admin, member areas).

```
/setup-browser-cookies
```

- Opens interactive picker UI
- Select which cookie domains to import
- Required for testing behind-login pages

### /codex
Get a second opinion from OpenAI Codex CLI.

**When:** Tricky code, want independent verification.

```
/codex review
/codex challenge    # adversarial mode — tries to break your code
/codex consult      # ask anything
```

### /document-release
Update documentation after shipping.

**When:** After a PR is merged or feature is shipped.

```
/document-release
```

- Cross-references the diff with project docs
- Updates README, ARCHITECTURE, CONTRIBUTING, CLAUDE.md
- Polishes CHANGELOG voice

### /land-and-deploy
Merge PR and verify production health.

**When:** After PR is approved, ready to deploy.

```
/land-and-deploy
```

- Merges PR, waits for CI
- Verifies production health via canary checks
- Requires `/setup-deploy` first for deploy config

### /setup-deploy
Configure deployment settings (one-time setup).

**When:** First time setting up deploy for a project.

```
/setup-deploy
```

- Detects platform (Fly.io, Render, Vercel, Netlify, etc.)
- Writes config to CLAUDE.md for automatic future deploys

## Skills to Skip (Not for Agency Work)

| Skill | Why Skip |
|-------|----------|
| /plan-ceo-review | Startup founder mode — rethinks the whole product |
| /office-hours | YC-style brainstorming for new product ideas |
| /retro | Weekly engineering retrospective for product teams |
| /design-shotgun | Multiple AI design variants — too exploratory for fixed-scope client work |
| /design-consultation | Creates DESIGN.md from scratch — clients provide their brand |
| /canary | Post-deploy monitoring for SaaS, not typical WordPress |
| /benchmark | Performance regression tracking — overkill for most agency sites |
| /pair-agent | Pair remote AI with browser — niche use case |
| /plan-tune | Meta: tunes gstack's own question behavior |
| /learn | Manages gstack learnings — not actionable for daily work |

## Integration with Custom Commands

GStack skills and custom `/project:*` commands serve different purposes:

| Layer | Tools | Purpose |
|-------|-------|---------|
| Cost optimization | `/project:delegate`, `/project:route` | Route work to cheapest capable agent |
| Estimation | `/project:estimate` | FE/BE day estimation from briefs |
| Second opinions | `/project:review-with`, `/project:consensus` | Multi-agent agreement |
| Specialized capabilities | `/browse`, `/qa`, `/investigate`, `/design-review` | Things only gstack can do (browser, visual QA) |
| Workflow automation | `/ship`, `/review`, `/land-and-deploy` | Git + PR + deploy pipeline |

**Typical flow for a new project:**

```
1. /project:estimate brief.md          → FE/BE day estimates
2. /plan-eng-review                     → Lock architecture
3. Code (delegate mechanical work)      → /project:delegate
4. /browse + /design-review             → Visual QA
5. /qa https://staging-url              → Find + fix bugs
6. /health                              → Quality score check
7. /review                              → PR review
8. /ship                                → Create PR
9. /land-and-deploy                     → Merge + verify prod
10. /document-release                   → Update docs
```
