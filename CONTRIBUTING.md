# Contributing to Frontend Frameworks Comparison

Thank you for helping keep this 2026 frontend frameworks benchmark, guide, and starter collection accurate and free of dead links!

## How You Can Help

1. **Report outdated versions or broken ecosystem links** by opening an issue.
2. **Add or improve framework examples** under `examples/same-app-task-tracker/` following the shared Sprint Task Tracker specification.
3. **Improve starter templates** under `starters/` while keeping dependencies minimal and MIT-compatible.
4. **Update verified stats** in `frameworks.json` and run `cp frameworks.json docs/frameworks.json`.

## Verification Before Opening a PR

```bash
python3 -m unittest discover -s tests -v
python3 framework_advisor.py --verify-sync
```
