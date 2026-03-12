# Research

This skill is based on existing Git primitives and established split tools rather than a custom one-off workflow.

## Primary references

- Git official documentation: `git archive`
  - https://git-scm.com/docs/git-archive
  - Relevant capability: create an archive from committed content, support `export-ignore`, and use `--worktree-attributes` when the checked-out `.gitattributes` must affect the exported archive.
- Git official documentation: `git worktree`
  - https://git-scm.com/docs/git-worktree.html
  - Relevant capability: create linked working trees without disturbing the main working tree. Useful for branch isolation, but still attached to the same repository metadata.
- Git Book: `export-ignore` via Git attributes
  - https://git-scm.com/book/ms/v2/Customizing-Git-Git-Attributes
  - Relevant capability: exclude tracked files from archives without deleting them from the repository.

## Existing tools reviewed

- `splitsh/lite`
  - https://github.com/splitsh/lite
  - Strength: fast read-only subdirectory split with history preservation.
  - Trade-off: optimized for long-term subdirectory history export, not for publishing a local dirty working tree snapshot.
- `git-subsplit`
  - https://github.com/dflydev/git-subsplit
  - Strength: automates one-way read-only subtree splits.
  - Trade-off: better suited to recurring history-based splits than to ad-hoc clean snapshot publishing.

## Design conclusion

- Default mode should be `copy-snapshot` because it can publish the exact current state, including uncommitted changes, without mutating the source directory.
- Strict mode should be `git-archive` because it uses committed Git content and can integrate with `export-ignore`.
- History-preserving split should stay optional and advanced because it solves a different problem from “publish a clean snapshot right now”.
