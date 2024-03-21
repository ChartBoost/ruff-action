# ruff-action
A GitHub Action for Ruff


Ruff can now be used as a [GitHub Action](https://github.com/features/actions).

This action is commonly used as a pass/fail test to ensure your repository stays clean, abiding the [Rules](https://docs.astral.sh/ruff/rules/) specified in your configuration.  Though it runs `ruff`, the action can do anything `ruff` can (ex, fix).

### Compatibility
This action is known to support all GitHub-hosted runner OSes. In addition, only published versions of Ruff are supported (i.e. whatever is available on PyPI).

### Usage
Create a file (ex: `.github/workflows/ruff.yml`) inside your repository with:

```yaml
name: Ruff
on: [push, pull_request]
jobs:
  ruff:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: chartboost/ruff-action@v1
```

Alternatively,
```
      - uses: chartboost/ruff-action@v1
```
can be included as a step in any other workflow file.

The Ruff action can be customized via optional configuration parameters passed to Ruff (using `with:`):

- version: Must be a Ruff release available on PyPI. By default, latest release of Ruff. You can pin a version, or use any valid version specifier.
- args: default, `check`
- src: default, '.'

```yaml
- uses: chartboost/ruff-action@v1
  with:
    src: "./src"
    version: 0.2.2
    args: --select B
```

See [Configuring Ruff](https://github.com/astral-sh/ruff/blob/main/docs/configuration.md) for details
