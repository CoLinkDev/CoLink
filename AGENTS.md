# CoLink Agent Notes

- If `AGENTS.local.md` exists, read it for machine-local instructions. It is ignored by git.
- All commits must use Conventional Commits.
- This directory is a top-level workspace repository containing multiple projects, each maintained as an independent nested Git repository. Except for changes owned by the top-level workspace repository, perform all Git operations from within the affected nested repository.
- When working in a project, strictly follow the instructions in that project's `AGENTS.md`.
- When changing fixed UI strings, update all i18n entries; first check how many locales the target app carries.
