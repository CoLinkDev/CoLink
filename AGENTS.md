# CoLink Agent Notes

- If `AGENTS.local.md` exists, read it for machine-local instructions. It is ignored by git.
- All commits must use Conventional Commits.
- This directory is a top-level workspace repository containing multiple projects, each maintained as an independent nested Git repository. Except for changes owned by the top-level workspace repository, perform all Git operations from within the affected nested repository.
- When working in a project, strictly follow the instructions in that project's `AGENTS.md`.
- When changing strings, update all i18n entries; first check how many locales the target app carries.

## Updating root READMEs

When changing the root README content:

1. Change structure, links, images, tables, or shared Markdown in `docs/readme/README.md.j2`.
2. Add or update the matching text in `docs/readme/locales/en.yml` and `docs/readme/locales/template.yml`, then update the same keys in every other locale package. `en.yml` is the canonical key structure; every locale must retain the same keys and list lengths.
3. Regenerate and verify the committed README artifacts:

   ```bash
   uv run docs/readme/generate.py
   uv run docs/readme/generate.py --check
   ```

4. Never edit root `README*.md` files directly; they are generated from the template and locale packages.

When adding a README language:

1. Copy `docs/readme/locales/template.yml` to a new locale package and replace every `TODO`.
2. Add the locale code, display name, package path, and generated README path to `docs/readme/config.yml`.
3. Run the generation and verification commands above.
