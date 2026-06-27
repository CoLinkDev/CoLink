# CoLink Agent Notes

- If `AGENTS.local.md` exists, read it for machine-local instructions. It is ignored by git.
- All commits must use Conventional Commits.
- This directory is a top-level workspace repository containing multiple projects, each maintained as an independent nested Git repository. Except for changes owned by the top-level workspace repository, perform all Git operations from within the affected nested repository.
- When working in a project, strictly follow the instructions in that project's `AGENTS.md`.
- When changing fixed UI strings, update all i18n entries; first check how many locales the target app carries.

## Protocol Compatibility

- Version management has been implemented for nearly all fixed fields, APIs and Actions within the protocol. Any changes made within the same protocol version must be both backward and forward compatible. Under the same protocol version, the meaning, mandatory status, data type and lifecycle semantics of existing fields shall not be modified.
- All protocol consumers shall abide by the following rules when processing protocol data: only read fields required for current logic and ignore unrecognized fields. No deserialization shall reject messages due to unknown fields.
- If a change cannot meet compatibility requirements, a new protocol version must be released.
