---
description: "Scaffold a new wp-theme-base block (PHP template + PostCSS + optional JS). Usage: /project:wp-block <block-name> [description]"
argument-hint: <block-name> [description of the block]
---

Generate a new block component for wp-theme-base from $ARGUMENTS. A block has up to 3 files that follow strict conventions.

## Step 1: Parse arguments

Extract from $ARGUMENTS:
- **block-name** (kebab-case, e.g. `team-grid`, `cta-banner`)
- **description** (optional — what the block displays)

If no description is given, infer from the name.

## Step 2: Determine if JS is needed

Blocks that need JS:
- Sliders/carousels → Swiper
- Accordions/tabs → toggle logic
- Forms → validation
- Anything with user interaction

Static display blocks (grids, cards, heroes, content areas) do NOT need JS.

## Step 3: Detect theme location

Look for the wp-theme-base theme in these locations (check in order):
1. Current working directory (if it has `templates/blocks/`)
2. `/Users/khoipro/Workspaces/wp-theme-base/`
3. Any WordPress theme in the current project

Set `$THEME_DIR` to the found path.

## Step 4: Generate files

### 4a. PHP Template — `$THEME_DIR/templates/blocks/{block-name}.php`

Follow this exact pattern (derived from existing blocks like faq.php, statistics.php):

```php
<?php
/**
 * Block: {Block Title}
 *
 * @package codetot
 * @author codetot
 */

$data = wp_parse_args(
	$args, [
		'class' => '',
		'title' => '',
		// Add appropriate default fields based on block type
	]
);

$_class = '{block-name}';
$_class .= ! empty($data['class']) ? ' ' . esc_attr($data['class']) : '';

// Add data-block attribute ONLY if JS is needed
?>
<div class="<?php echo esc_attr($_class); ?>"<?php if (NEEDS_JS) : ?> data-block="{block-name}"<?php endif; ?>>
	<div class="container">
		<!-- Block content using BEM: {block-name}__{element} -->
	</div>
</div>
```

**Conventions to follow:**
- `wp_parse_args($args, [...])` for data with sensible defaults
- `$_class` pattern for CSS class building
- BEM naming: `{block-name}__title`, `{block-name}__content`, `{block-name}__item`
- Use Bootstrap 5 utilities for layout: `row`, `col-*`, `d-flex`, `py-*`, `container`
- Use `esc_html()` for text, `wp_kses_post(wpautop())` for rich content, `esc_attr()` for attributes
- Use `esc_url()` for URLs
- `get_template_part('templates/core-blocks/image', null, [...])` for images
- `codetot_get_svg_icon('name')` for icons
- Section spacing: `py-2 py-lg-4 section--lg` for standard sections
- Wrap in conditional: `if (!empty($data['key'])) :`

### 4b. PostCSS — `$THEME_DIR/src/postcss/blocks/{block-name}.css`

```css
.{block-name} {
	/* Section-level styles */
}

.{block-name}__title {
	margin-bottom: 1.5rem;
}

/* Use PostCSS nesting with & */
.{block-name}__item {
	& .icon {
		transition: all 0.3s ease;
	}
}

/* Responsive with custom media */
@media (--md) {
	.{block-name} {
		/* tablet+ styles */
	}
}
```

**CSS conventions:**
- BEM naming matching the PHP
- Use CSS custom properties from `variables.css`: `var(--primary)`, `var(--bs-primary)`
- Custom media queries: `--s`, `--sm`, `--md`, `--lg`, `--xl`, `--xxl`
- PostCSS nesting with `&`
- Transitions on interactive elements: `transition: all 0.3s ease`

### 4c. JS Module (only if interactive) — `$THEME_DIR/src/js/modules/{block-name}.js`

```js
export function init{BlockName}() {
	const elements = document.querySelectorAll('[data-block="{block-name}"]');
	if (!elements.length) return;

	elements.forEach((el) => {
		// Block initialization logic
	});
}
```

**JS conventions:**
- Export a named `init{PascalCase}()` function
- Query by `[data-block="{block-name}"]`
- Guard with `if (!elements.length) return`
- Use vanilla JS (no jQuery)
- For sliders: import Swiper

## Step 5: Register the new files

After creating files, update these registries:

1. **Add CSS import** to `$THEME_DIR/src/postcss/blocks/index.css`:
   ```css
   @import url('{block-name}.css');
   ```

2. **If JS was created**, add to `$THEME_DIR/src/js/main.js`:
   ```js
   import { init{BlockName} } from './modules/{block-name}';
   // Add init{BlockName}() call inside DOMContentLoaded
   ```

## Step 6: Delegate CSS to local agent (optional)

If the block is complex (grid layout, responsive behavior), delegate the PostCSS to a local agent for faster generation:

```bash
curl -s --max-time 120 http://localhost:11434/api/generate \
  -d '{"model":"qwen2.5-coder:7b","prompt":"Write PostCSS for a {block-name} component using BEM naming. Use & for nesting. Custom media: --md (782px), --lg (960px). Keep it minimal.","stream":false}' \
  | jq -r '.response'
```

## Step 7: Validate generated code

**IMPORTANT: Always validate before reporting success.**

Run these checks on the generated files (use Bash tool with `timeout: 30000`):

```bash
# Lint PHP
cd $THEME_DIR && composer lint -- templates/blocks/{block-name}.php

# Lint CSS
./node_modules/.bin/stylelint src/postcss/blocks/{block-name}.css

# Lint JS (if created)
npx eslint src/js/modules/{block-name}.js

# Format check
npx prettier --check src/postcss/blocks/{block-name}.css src/js/modules/{block-name}.js

# Build check
npm run build
```

If any lint errors are found, fix them before reporting. Common fixes:
- PHP: missing escaping → add `esc_html()`, `esc_attr()`, `wp_kses_post()`
- CSS: duplicate selectors → merge them
- JS: unused vars → remove or prefix with `_`

## Step 8: Report

Tell the user:
- Files created (with paths)
- Whether JS was included and why
- Validation results (all linters passed / issues found and fixed)
- How to use: `get_template_part('templates/blocks/{block-name}', null, ['title' => '...', ...])`
- Remind to run `npm run dev` to rebuild
