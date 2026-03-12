# Cleanup Checklist

Use this checklist before pushing a release repo.

## Always review

- `.env`, `.env.local`, `.env.*`
- Cookies, API keys, tokens, private URLs, SSH keys
- Database files, WAL/SHM files, local caches
- Logs, screenshots, Playwright reports, temporary exports
- `node_modules/`, `.venv/`, `dist/`, `build/`, `coverage/`
- `__pycache__/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`
- `tmp/`, `.tmp/`, `output/`, `test-results/`, `playwright-report/`

## Keep by default when they are intentional

- `.env.example`
- `.env.sample`
- `.env.template`
- `.gitignore`
- `.gitattributes`
- Source code, tests, lockfiles, README, LICENSE

## Review questions

1. Does the release need current uncommitted changes?
2. Does the release need committed history, or only a clean snapshot?
3. Is force push acceptable for the target branch?
4. Should any generated examples or fixtures stay in the open-source version?
5. Does the release directory contain files that only exist on the local machine?

## Recommended execution pattern

1. Run the publish script with `--dry-run`.
2. Run once with `--push skip`.
3. Inspect the isolated release directory manually.
4. Push only after the release directory looks clean.
