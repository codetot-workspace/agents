---
description: "Scaffold a WordPress page template from a brief or section list. Usage: /project:wp-page <page-name> [sections...]"
argument-hint: <page-name> [section1, section2, ...]
---

Generate a WordPress page template for wp-theme-base from $ARGUMENTS. Composes existing blocks into a complete page.

## Step 1: Parse arguments

Extract from $ARGUMENTS:
- **page-name** (e.g. `about`, `services`, `homepage`)
- **sections** (optional list of block names or descriptions)

If sections are not specified, delegate to gemma4 to suggest them:

```bash
curl -s --max-time 120 http://localhost:11434/api/generate \
  -d '{"model":"gemma4","prompt":"List sections for a PAGE_TYPE page for a Vietnamese web agency client. For each: kebab-case name | static or dynamic | 1-line description. Max 10 sections.","stream":false}' \
  | jq -r '.response'
```

Use Bash tool with `timeout: 120000`.

## Step 2: Map sections to existing blocks

Check which blocks already exist in `templates/blocks/`:

```
hero-image, hero-title, hero-post, breadcrumb, content-area,
faq, feature-grid, feature-item, feature-list-two-up, footer, header,
highlight-section, listing-section, logo-grid, post-card, post-grid,
post-grid-loop, pricing-table, review-item, reviews-slider,
statistics, step-section, two-up-image
```

For each section:
- If it matches an existing block → use it directly
- If it's close but not exact → note the closest match and what needs customizing
- If it's new → flag it for creation with `/project:wp-block`

## Step 3: Generate the page template

Create `$THEME_DIR/page-{page-name}.php`:

```php
<?php
/**
 * Template Name: {Page Title}
 *
 * @package codetot
 */

get_header();
?>

<main class="main" role="main">
	<?php
	// Section 1: Hero
	get_template_part('templates/blocks/hero-image', null, [
		'title' => get_the_title(),
		'description' => get_field('hero_description'),
		'image' => get_field('hero_image'),
	]);

	// Section 2: ... (repeat for each section)
	?>
</main>

<?php
get_footer();
```

**Conventions:**
- Template name comment at top: `Template Name: {Page Title}`
- Wrap in `<main class="main" role="main">`
- Use `get_template_part()` for each block
- Use `get_field()` for ACF fields (assume ACF Pro is installed)
- Comment each section with its purpose

## Step 4: Generate ACF field group

Create the ACF field group PHP registration (or JSON for `acf-json/`).

For each section that needs CMS data, define fields:

```php
// In inc/acf/{page-name}.php or output as ACF JSON
acf_add_local_field_group([
    'key' => 'group_{page_name}',
    'title' => '{Page Title} Fields',
    'fields' => [
        // Hero section
        [
            'key' => 'field_{page_name}_hero_title',
            'label' => 'Hero Title',
            'name' => 'hero_title',
            'type' => 'text',
        ],
        // Repeater for items-based blocks
        [
            'key' => 'field_{page_name}_stats',
            'label' => 'Statistics',
            'name' => 'statistics',
            'type' => 'repeater',
            'sub_fields' => [
                ['key' => 'field_stat_number', 'label' => 'Number', 'name' => 'number', 'type' => 'text'],
                ['key' => 'field_stat_unit', 'label' => 'Unit', 'name' => 'unit', 'type' => 'text'],
                ['key' => 'field_stat_title', 'label' => 'Title', 'name' => 'title', 'type' => 'text'],
            ],
        ],
    ],
    'location' => [
        [['param' => 'page_template', 'operator' => '==', 'value' => 'page-{page-name}.php']],
    ],
]);
```

**ACF field type mapping:**
- Text content → `text`
- Rich text / description → `wysiwyg` or `textarea`
- Image → `image` (return format: ID)
- Link/URL → `link`
- Repeater items (FAQ, stats, features) → `repeater`
- True/false toggle → `true_false`
- Select/choice → `select`

## Step 5: Validate generated code

**IMPORTANT: Always validate before reporting success.**

```bash
# Lint the page template PHP
cd $THEME_DIR && composer lint -- page-{page-name}.php

# If ACF PHP was created
composer lint -- inc/acf/{page-name}.php

# Build check (ensures no import errors)
npm run build
```

Fix any lint errors before reporting.

## Step 6: Report

Output:
1. **Page template file** created
2. **Blocks used** — which existing blocks, which need creating
3. **ACF fields** — the field group with all fields
4. **Validation** — all linters passed / issues found and fixed
5. **Missing blocks** — suggest running `/project:wp-block {name}` for each
6. **Usage** — how to assign the template in WP admin
