# Installation and updates

The canonical skill is `skills/ai-practitioner/`. It uses the [Agent Skills format](https://agentskills.io/specification) and has no required hooks, MCP servers, tool allowlists, or provider SDKs. Review it before installation.

## Installer

Run the commands from the repository root:

```sh
python scripts/install.py --tool codex --dry-run
python scripts/install.py --tool codex
```

Choose `codex`, `claude`, or `both`. With no `--project`, destinations are the current user's `~/.agents/skills` for Codex and `~/.claude/skills` for Claude Code. `--project` must name an existing directory and uses that directory's `.agents/skills` and `.claude/skills` instead.

The installer plans all destinations before copying. It refuses linked/reparse installation paths or source files, incomplete sources, installation inside its own source tree, and existing differing content. Identical installed content is a no-op. It stages and verifies each complete copy before publishing its destination; failed copy staging is cleaned up within a verified temporary directory. When installing both tools, an already completed tool installation can remain if a later tool fails. It does not delete existing skills, create credentials, make network requests, or change configuration. Use it in a trusted local filesystem without concurrent installers changing the same paths.

## Manual installation

Copy the **entire** `skills/ai-practitioner` folder, including `references` and `assets`, into the appropriate skill directory:

| Scope | Codex | Claude Code |
|---|---|---|
| Personal | `~/.agents/skills/ai-practitioner` | `~/.claude/skills/ai-practitioner` |
| Project | `<project>/.agents/skills/ai-practitioner` | `<project>/.claude/skills/ai-practitioner` |

These are local filesystem installations. They do not install a skill into Claude's web UI or a remote/cloud runtime. Check your host's official documentation for those environments and organization-managed settings. Avoid multiple same-named installations if you do not intend their precedence/duplication behavior.

Codex invocation: `$ai-practitioner discovery ...`

Claude Code invocation: `/ai-practitioner discovery ...`

The mode is ordinary request text, not a custom CLI parser. You can simply describe the desired task. Automatic selection is available when supported by the host. Reopen the session if discovery does not refresh.

## Updating

Pull the repository changes and review the diff. Run the installer with `--dry-run`. If an installed copy differs, the installer will refuse to overwrite it. Preserve any local customizations, compare the folders, then replace only the intended skill using your normal file workflow. There is deliberately no force-overwrite option.

Uninstall by removing only the installed `ai-practitioner` directory you selected. No background service, registry entry, or remote account needs cleanup. Removing a skill does not remove client deliverables or already-loaded conversational context.

Official references: [OpenAI skill locations](https://learn.chatgpt.com/docs/build-skills), [Claude Code skills](https://code.claude.com/docs/en/skills). Checked November 23, 2026.
