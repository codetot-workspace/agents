---
description: "Estimate FE/BE days from a project brief. Usage: /project:estimate <brief-file-or-paste>"
argument-hint: <brief file path or pasted brief>
---

Create a structured estimation from a website project brief. The brief is in $ARGUMENTS (file path or inline text).

## Step 1: Parse the brief into a sitemap

Read the brief and extract:
- **Page list** with hierarchy (1, 1.1, 1.1.1, etc.)
- **Page name** (Vietnamese or English)
- **Reference URLs** (if provided)
- **Notes** (e.g. "text + ảnh", "thêm cập nhật bài viết")

Output a numbered list of unique page templates. Group pages that share the same template (e.g. "4.1.1 through 4.1.4 are all the same text+image template").

## Step 2: Identify sections per page template

For each unique page template that has a reference URL, delegate to gemma4 to name the sections.

**IMPORTANT: Use Ollama REST API, never interactive `ollama run`.**

For each reference URL, ask gemma4 to identify visible sections:

```bash
curl -s --max-time 120 http://localhost:11434/api/generate \
  -d '{"model":"gemma4","prompt":"List sections for PAGE_NAME (PAGE_TYPE). For each give: English name (kebab-case) | static or dynamic | 1-line description. Max 12 sections.","stream":false}' \
  | jq -r '.response'
```

**Keep the prompt short and structured** — gemma4 produces better output with concise instructions and pipe-delimited format.

Use Bash tool with `timeout: 120000`.

**If Ollama is unavailable**, fall back to DeepSeek:
```bash
opencode run -m deepseek/deepseek-chat "SAME_PROMPT"
```

**If reference URL exists and you need to see the actual page**, use the `/browse` skill to screenshot and analyze real sections. This is optional but improves accuracy.

## Step 3: Classify and estimate each section

For each section identified, classify using this reference table:

### FE Estimation Reference

| Section Type | Examples | Days |
|-------------|----------|------|
| Static block | Text + image, about section, simple CTA | 0.25 |
| Static block (complex layout) | Multi-column, responsive grid, icon grid | 0.5 |
| Hero/banner | Full-width hero with text overlay, parallax | 0.5 |
| Slider/carousel | Image slider, testimonials carousel | 0.5 |
| List/grid (static) | Service cards, feature grid, team members | 0.5 |
| List/grid (dynamic + filter) | Portfolio grid with category filter, search | 1.0 |
| Form | Contact form, inquiry form | 0.5 |
| Form (complex) | Multi-step form, file upload, validation | 1.0 |
| Map section | Google Maps embed + info | 0.25 |
| Tabs/accordion | Tabbed content, FAQ accordion | 0.5 |
| Detail page template | Blog post, project detail, service detail | 1.0 |
| Archive/listing page | Blog listing, project archive with pagination | 1.0 |
| Navigation | Header + mega menu + mobile menu | 1.0 |
| Footer | Footer with columns + newsletter | 0.5 |
| Breadcrumb + sidebar | Secondary nav elements | 0.25 |
| Animation/interaction | Scroll animations, hover effects, transitions | 0.5 |
| Responsive QA | Testing all breakpoints for a page | 0.25 |

### BE Estimation Reference (WordPress/CMS assumed unless stated)

| Task Type | Examples | Days |
|-----------|----------|------|
| Static page (no custom fields) | Simple text page | 0 |
| Custom fields setup | ACF/meta boxes for a page template | 0.25 |
| Custom post type | Portfolio, services, team members | 0.5 |
| Custom taxonomy | Categories, tags, filters for CPT | 0.25 |
| Archive query | Custom WP_Query for listing pages | 0.25 |
| Detail template | Single post/CPT template with custom fields | 0.5 |
| Contact form backend | Form handler, email notification, spam protection | 0.5 |
| API integration | Third-party API, external data source | 1.0 |
| Search functionality | Custom search with filters | 1.0 |
| Performance optimization | Caching, lazy load, image optimization | 0.5 |

## Step 4: Produce the estimation table

Output the final estimation in this exact format:

```markdown
# Project Estimation: [PROJECT_NAME]

Generated: [DATE]
Brief: [FILE_OR_SOURCE]

## Summary

| | Pages | FE Days | BE Days | Total |
|---|-------|---------|---------|-------|
| Total | X | X.XX | X.XX | X.XX |

## Page Templates

### [PAGE_NUMBER] — [PAGE_NAME]
Reference: [URL or "from PDF/brief"]

| # | Section | Type | FE | BE | Notes |
|---|---------|------|----|----|-------|
| 1 | hero-banner | Hero/banner | 0.5 | 0 | Full-width with text overlay |
| 2 | service-grid | List/grid (static) | 0.5 | 0.25 | 4-column card layout |
| ... | ... | ... | ... | ... | ... |
| | **Subtotal** | | **X.X** | **X.X** | |

[Repeat for each unique page template]

## Shared Components (counted once)

| # | Component | FE | BE | Notes |
|---|-----------|----|----|-------|
| 1 | header-navigation | 1.0 | 0 | Mega menu + mobile |
| 2 | footer | 0.5 | 0.25 | Multi-column + newsletter |
| 3 | responsive-qa | 0.5 | 0 | Cross-device testing |
| | **Subtotal** | **X.X** | **X.X** | |

## Notes
- Pages sharing a template are counted once (e.g. all service sub-pages = 1 template)
- Estimates assume [CMS platform] with standard tooling
- Does not include: hosting setup, domain config, content entry, SEO audit
```

## Rules

1. **Group duplicate templates** — If 4.1.1 through 4.1.4 share the same layout, count as ONE template with a note "×4 pages, same template"
2. **Shared components once** — Header, footer, global elements are estimated once, not per page
3. **Vietnamese page names OK** — Keep original names, add English section names
4. **Round to 0.25** — All estimates in 0.25-day increments
5. **Conservative by default** — When unsure, estimate higher. A missing half-day is worse than an extra one
6. **Flag unknowns** — If a page has no URL and no description, flag it as "needs clarification" with a placeholder estimate
