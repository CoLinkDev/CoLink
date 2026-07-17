---
name: publish-release-notes
description: Compare a specified Git tag (or the latest tag by default) with its baseline, then create and publish multilingual GitHub Release Notes for users.
---

# Publish Release Notes

Use this skill when writing or updating the GitHub Release Notes for a version of this application. If the user specifies a tag, use it as the release version; otherwise, use the latest tag by default. Include only user-facing changes: new capabilities, improvements to the user experience, and fixes for user-visible issues. Exclude refactoring, tests, CI, packaging, dependencies, internal architecture, and other engineering changes unless they directly affect the user experience.

## Terminology

- **All languages**: Every supported language listed at the top of the `README.md` in the current working root (not the project directory), in that exact order.

## Scope and safety requirements

- Update the body of the GitHub Release for the target tag only after the version differences have been fully reviewed.
- Do not modify the title, draft or prerelease status, assets, or target commit.
- If the user does not specify which project needs Release Notes, stop and ask.

## Determine the comparison range

1. Synchronize remote tags, then determine the target tag. If the user explicitly specifies a tag, use it. If the user provides a version without the `v` prefix, first attempt to resolve `v<version>`. Otherwise, use the most recently created tag. Confirm that the target tag resolves.
2. Determine the baseline tag. If the user explicitly specifies a comparison tag, use it. Otherwise, find the tag created immediately before the target tag. Confirm that the baseline tag resolves.
3. Before drafting, use the `gh` CLI to confirm that a GitHub Release exists for the target tag.
4. Fully inspect the commits, file differences, and relevant implementation between the two tags. Do not rely solely on commit titles. For every potentially user-facing change, focus on UI text, user workflows, configuration behavior, documentation for supported behavior, and user-visible error handling.

## Write the Release Notes

Use the [Release Note template](references/release-notes-template.md) and [Release Note example](references/release-notes-example.md) as references, and organize the content according to the actual changes in this release. The notes must include every language in order.

Content rules:

- Include only externally observable changes and describe specific capabilities or outcomes from the user's perspective. Combine related commits, and keep each item concise and specific. Do not include commit IDs, PR numbers, file names, module names, or implementation details. Do not present isolated refactors or translation changes as user-facing changes.
- Put new capabilities under **What's New**, user-visible optimizations under **Improvements**, and issue fixes under **Fixes**.
- The meaning must be equivalent in every language and expressed naturally in each one. Product names, established UI labels, file extensions, keyboard shortcuts, and technical terms that aid understanding may remain untranslated.
- Include only categories with qualifying content. If a category has no relevant changes, omit both its heading and content in every language. Do not use placeholder text or add internal changes merely to populate a category.
- Avoid promises, speculation, and marketing language.

## Publish and verify

1. Write the completed notes to a temporary Markdown file and inspect its contents before publishing.
2. Use `gh release edit` to update only the body of the Release.
3. Read the target Release to confirm that its published body matches the expected content, then delete the temporary Markdown file.
4. Report the comparison range, Release link, and a brief summary of the published user-facing changes.
