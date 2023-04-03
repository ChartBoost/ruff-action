# ruff-action
A GitHub Action for Ruff


Ruff can now be used as a [GitHub Action](https://github.com/features/actions).

This action is commonly used as a pass/fail test to ensure your repository stays clean, abiding the [Rules](https://beta.ruff.rs/docs/rules/) specified in your configuration.  Though it runs `ruff` so the action can do anything `ruff` can (ex: fix).

Compatibility
This action is known to support all GitHub-hosted runner OSes. In addition, only published versions of Ruff are supported (i.e. whatever is available on PyPI).

Usage
Create a file (ex: `.github/workflows/ruff.yml`) inside your repository with:

```yaml
name: Ruff
on: [push, pull_request]
jobs:
  ruff:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: chartboost/ruff-action@v1
```

Alternatively,
```
      - uses: chartboost/ruff-action@v1
```
can be included as a step in any other workflow file.

The Ruff action can be customized via optional configuration parameters passed to Ruff (using `with:`):

- version: Must be release available on PyPI. default, latest release of ruff. You can pin a version, or use any valid version specifier.
- options: default,`check`
- src: default, '.'

```yaml
- uses: chartboost/ruff-action@v1
  with:
    src: "./src"
    version: 0.0.259
    options: --select B
```

See [Configuring Ruff](https://github.com/charliermarsh/ruff/blob/main/docs/configuration.md) for details
