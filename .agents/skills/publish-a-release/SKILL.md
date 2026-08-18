---
name: publish-a-release
description: Cut a release end-to-end: verify the working tree is clean and pushed, create and push an annotated version tag, wait for the CI-created GitHub Release, then write and publish multilingual Release Notes.
---

# Publish a Release

Use this skill to release a new version of the application: Create and push an annotated version tag, wait for the remote CI to create the GitHub Release, then write and publish user-facing Release Notes for the new tag. If the user specifies a version, use it; otherwise infer it from the changes.

## Scope and safety requirements

- Update the body of the GitHub Release for the target tag only after the version differences have been fully reviewed.
- Do not modify the title, draft or prerelease status, assets, or target commit.
- If the user does not specify which project needs a release, stop and ask.
- The workspace root is a multi-project repository. Perform all Git operations from within the affected nested repository, except for changes owned by the top-level workspace repository.

## Workflow

**IMPORTANT: AFTER COMPLETING EACH OF THE FOLLOWING STEPS, YOU MUST RE‑READ THIS SKILL FILE TO ENSURE OPERATIONAL ACCURACY.**

### 1. Ensure the working tree is clean and pushed

Before tagging, the repository MUST be in a releasable state.

1. Confirm the working tree is clean — no uncommitted changes to tracked files. If there are any, stop and report.
2. Confirm the current branch has no unpushed commits. If there are unpushed commits, push them first.

### 2. Create and push the annotated tag

1. Determine the new version. If the user specified a version or a bump policy, use it. Otherwise infer it from the latest tag and the changes being released, following semantic versioning.
2. Create an annotated tag (not a lightweight one):
   ```
   git tag -a v<version> -m "Release v<version>"
   ```
3. Push the tag.

### 3. Write the Release Notes

Right after pushing the tag, draft the notes first — the CI runs in the background while you write.

1. Synchronize remote tags, then determine the comparison range: the target tag is the new `v<version>`; the baseline is the tag created immediately before it. Confirm both resolve.
2. Fully inspect the commits and file differences between the two tags, and deeply think about the relevant implementation. Do not rely solely on commit titles. For every potentially user-facing change, focus on UI text, user workflows, configuration behavior, documentation for supported behavior, and user-visible error handling.
3. Write the Release Notes draft to a temporary Markdown file, following the [template](references/release-notes-template.md) and [example](references/release-notes-example.md) and the content rules below.

- Organize the content according to the actual changes in this release, using the [Release Note template](references/release-notes-template.md) and [Release Note example](references/release-notes-example.md) as references. The notes MUST include every language in order.
- Include only externally observable changes and describe specific capabilities or outcomes from the user's perspective: new capabilities, improvements to the user experience, and fixes for user-visible issues. Exclude refactoring, tests, CI, packaging, dependencies, internal architecture, and other engineering changes unless they directly affect the user experience. Keep each item concise and specific. Do not include commit IDs, PR numbers, file names, module names, or implementation details.
- **When the same feature undergoes multiple iterations or follow-up corrections within the version, merge all related commits into a single entry describing only the final net effect — do not expose intermediate development steps or superseded states.**
- The meaning MUST be equivalent in every language and expressed naturally in each one. Product names, established UI labels, file extensions, keyboard shortcuts, and technical terms that aid understanding may remain untranslated.
- Include only categories with qualifying content. If a category has no relevant changes, omit both its heading and content in every language. Do not use placeholder text or add internal changes merely to populate a category.

### 4. Wait for the CI-created Release

1. Poll the remote CI for the Release with `gh release view v<version>` until it exists. Stop polling as soon as the Release appears — publishing notes only needs the Release, not the completed build.

### 5. Publish and verify

1. Inspect the draft you wrote in step 3 before publishing.
2. Use `gh release edit v<version> --notes-file <draft>` to update only the body of the Release.
3. Read the target Release to confirm that its published body matches the expected content, then delete the temporary Markdown file.
4. Report the comparison range, Release link, and a brief summary of the published user-facing changes.
