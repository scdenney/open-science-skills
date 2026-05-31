# Codex-native skills

Skills in this directory run inside **OpenAI Codex** (the `codex` CLI), not the Claude Code `oss` plugin. They are kept here as repo assets so the Codex-native variants stay versioned alongside their Claude siblings. The Claude plugin loader and `plugin/scripts/check.sh` do not touch this directory.

## diverge

Codex-native version of the [`diverge`](../plugin/skills/diverge/SKILL.md) skill: generate 3–5 conceptually distinct approaches before implementing, each labeled by creativity dimension (Novel, Surprising, Diverse, Conventional), holding for selection. Based on Creative Preference Optimization (Ismayilzada et al., 2025; see [`../plugin/skills/diverge/reference/creative-preference-optimization.md`](../plugin/skills/diverge/reference/creative-preference-optimization.md)).

Install into Codex:

```bash
ln -sfn "$(pwd)/codex/diverge" ~/.codex/skills/diverge
```

Then invoke `$diverge <task>` inside Codex.

For the Claude Code equivalents, install the `oss` plugin and use `/oss:diverge` (Claude-only) or `/oss:diverge-codex` (Claude delegates the brainstorm to Codex).
