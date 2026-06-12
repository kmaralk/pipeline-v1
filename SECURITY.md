# Security

Do not publish local active-copy state, raw transcripts, browser session data,
auth state, environment dumps, or generated evidence logs in this repository.

Before publishing a release, run:

```bash
gitleaks detect --redact --no-banner
rg -n -i 'secret|token|password|cookie|sessionStorage|localStorage|auth header|/home/<user>|internal host|agent worktree'
```

Report security concerns privately through the repository owner.
