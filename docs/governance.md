# Repository governance

Maintainer and owner: **[@afurm](https://github.com/afurm)**. This is a public, personally owned repository. Forks and pull requests are welcome; contribution is not permission to publish changes to the upstream repository.

## Main branch policy

The intended active GitHub rulesets are:

1. **Owner-only PR merges:** updates to `main` are restricted, with only the `afurm` user allowed to bypass that restriction through a pull request. Direct pushes remain blocked.
2. **Owner review:** a pull request and one code-owner approval are required. `.github/CODEOWNERS` assigns all files to `@afurm`. Only `afurm` has a PR-only bypass of this review rule, allowing the owner to merge an owner-authored PR (GitHub does not allow self-approval).
3. **Main integrity:** passing `Required checks` from GitHub Actions, an up-to-date branch, resolved review conversations, linear history, no force-pushes, and no deletion. No bypass actors are configured for these rules.

The review exception does not waive CI or the other integrity rules. Use squash merging. Auto-merge is disabled; branches are deleted after merge. Any change to maintainer access or rulesets requires deliberate owner review.

GitHub permits members of the public to leave advisory reviews. Such reviews do not confer write/merge authority, and do not replace the owner's required code-owner review. The owner can use their explicit review exception for a PR; record the reason in the PR when skipping an otherwise required review. GitHub's owner/admin account can edit rulesets, so this policy assumes the owner account remains secure.

## Fork workflow safety

External contributors require workflow-run approval. CI runs with read-only repository permissions, does not receive client/API secrets, does not persist checkout credentials, and uses pinned action commits. There is no `pull_request_target` workflow executing fork code and no automated merge/review bot. Dependency updates arrive as PRs and follow the same checks and owner merge control.

Approval to run a fork's CI is not approval to merge it. Inspect workflow and script changes before approving execution. Do not add privileged secrets to contribution validation workflows.

## Release and quality claims

Packaging checks, installation tests, and synthetic behavioral evaluation establish different things. Reports must record what actually ran, the revision/configuration tested, observed failures, and limitations. A passing synthetic suite does not certify a client's production deployment or all future model behavior.

For changes: open a branch/PR, run checks, inspect the diff and relevant behavioral cases, then have the owner merge. Keep client data out of issues, PRs, and examples. See [contribution guidance](../CONTRIBUTING.md).

References: [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository), [code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners), [fork workflow approvals](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/approve-runs-from-forks).
