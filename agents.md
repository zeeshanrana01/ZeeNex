# OpenChat

- Frontend: Next.js in frontend/ (port 3000)
- Backend: FastAPI in backend/ (port 8000)
- AI: Ollama at localhost:11434, model llama3.2:3b
- Run everything: ./start.sh
- Test: cd backend && pytest

# Rules

- I am a beginner: explain changes simply
- Never commit .env or API keys
- Run the tests after every change

# OpenClaw Operations Reference for AI Agents

This file is the brain. You (Claude Code, OpenCode, Codex, or any other coding agent) read it once at session start, then again whenever you need to do OpenClaw work. The human you're paired with is your supervisor; they decide _what_ to do, you handle _how_.

You'll be asked to install OpenClaw, debug it, fix it, extend it with skills and plugins and MCP servers, configure channels, customize the brain, manage memory, schedule heartbeats, spawn coding agents back, audit security, and recover when something breaks. The crash course page (`https://agentfactory.panaversity.org/docs/openclaw-with-general-agents`) walks the human through a tour. This file is what you reach for whenever the human asks for _any_ OpenClaw operation, in any order, including the ones the crash course never touches.

This folder is a "little skill": a block of text plus a `CLAUDE.md` import marker. Covers the whole platform, not just install.

---

## Versions this folder was built against

```
OpenClaw:     ≥ v2026.5.7   (do NOT proceed on v2026.5.5/v2026.5.6: see hotfix chain in Diagnose & Recover)
Node.js:      ≥ 22.16   (Node 24 recommended; 22.0–22.15 will fail the install despite passing a loose "22+" check)
LLM model:    google/gemini-3.5-flash   (free tier; previous recommendation was gemini-2.5-flash)
Docs index:   https://docs.openclaw.ai/llms.txt   (the master index, ~850 lines)
Built on:     2026-06-23
```

If `openclaw --version` reports below v2026.5.7, run `openclaw update --channel stable` and re-verify before doing anything else. v2026.5.10 and beyond are beta-only; stay on stable for predictable behavior.

OpenClaw ships fast. Flag names and CLI surfaces drift. Treat this brief as today's-known-good, not eternal. When something here disagrees with the live docs, the live docs win.

---

# PART 1: PRINCIPLES (apply everywhere)

## Source of truth, in order

1. **Live docs** at `https://docs.openclaw.ai/`: commands, flags, paths, schema. Always.
2. **This file** (`AGENTS.md`): patterns, gotchas, and durable choreography of operating OpenClaw with a coding agent in the loop.
3. **The crash course page** on the book site: what the human is trying to learn in the current scenario.
4. **The gateway log** (`/tmp/openclaw/openclaw-YYYY-MM-DD.log`): when something breaks, read it before guessing.

If 2/3 disagree with 1, trust 1. If 1 contradicts itself, surface that and ask the human.

## Critical: discover before you act

Do not run any OpenClaw command from memory. Before you run a command or change config, fetch the matching doc page. One HTTP round-trip beats an unrecoverable `openclaw.json`.

| You're about to...                                         | Read first                                                                                                                                                                                                 |
| ---------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Install or onboard                                         | `https://docs.openclaw.ai/cli/onboard.md`, `https://docs.openclaw.ai/start/wizard.md`, `https://docs.openclaw.ai/start/wizard-cli-automation.md`, `https://docs.openclaw.ai/start/wizard-cli-reference.md` |
| Set or read a config key                                   | `https://docs.openclaw.ai/cli/config.md`                                                                                                                                                                   |
| Configure a model provider                                 | `https://docs.openclaw.ai/providers/<name>.md` (e.g. `/providers/google.md`)                                                                                                                               |
| Configure a channel                                        | `https://docs.openclaw.ai/channels/<name>.md` (e.g. `/channels/whatsapp.md`)                                                                                                                               |
| Start, stop, or inspect the gateway                        | `https://docs.openclaw.ai/cli/gateway.md`, `https://docs.openclaw.ai/gateway/index.md`                                                                                                                     |
| Diagnose a problem                                         | `https://docs.openclaw.ai/cli/doctor.md`, `https://docs.openclaw.ai/help/debugging.md`                                                                                                                     |
| Verify the model actually answers                          | `https://docs.openclaw.ai/cli/infer.md`, plus tail `openclaw logs --follow`                                                                                                                                |
| Install or invoke a skill                                  | `https://docs.openclaw.ai/cli/skills.md`, `https://docs.openclaw.ai/clawhub`                                                                                                                               |
| Connect or inspect an MCP server                           | `https://docs.openclaw.ai/cli/mcp.md`, `https://docs.openclaw.ai/mcp/index.md`                                                                                                                             |
| Install a plugin (channel adapter, voice, etc.)            | `https://docs.openclaw.ai/cli/plugins.md`, `https://docs.openclaw.ai/plugins/index.md`                                                                                                                     |
| Configure heartbeats or cron                               | `https://docs.openclaw.ai/gateway/heartbeat.md`, `https://docs.openclaw.ai/cli/cron.md`                                                                                                                    |
| Register a hook (HTTP webhook, plugin hook, internal hook) | `https://docs.openclaw.ai/hooks/index.md`                                                                                                                                                                  |
| Spawn a coding agent via ACP                               | `https://docs.openclaw.ai/tools/acp-agents` _(canonical: `/acp` and `/agents` both 404)_                                                                                                                   |
| Run multiple agents on one gateway                         | `https://docs.openclaw.ai/agents/multi-agent.md`                                                                                                                                                           |
| Deploy to production / harden security                     | `https://docs.openclaw.ai/deploy/index.md`, `https://docs.openclaw.ai/gateway/security`                                                                                                                    |
| Sandbox configuration                                      | `https://docs.openclaw.ai/sandbox/index.md`                                                                                                                                                                |
| Anything else                                              | `https://docs.openclaw.ai/llms.txt` (master index; useful but not exhaustive)                                                                                                                              |

If a command errors and the message is unclear, fetch its doc page before retrying.

## Working pattern (every task, every time)

1. **Read** the human's intent and the relevant doc pages from the table above.
2. **Propose** a 4–8 bullet plan in plain words: commands in order, one sentence per bullet.
3. **Ask** for go-ahead before the first command.
4. **Execute one step.** Show output.
5. **Verify** with `openclaw config get`, `openclaw doctor`, `openclaw channels status --probe`, or `openclaw logs --follow`.
6. **If verification fails**: read the doc page for that command, then the gateway log. Show the human the relevant lines. Propose one fix. Ask before applying.
7. **Repeat** until the human's intent is satisfied.

Never chain destructive commands without verification between them. Never run a long sequence silently and dump output at the end. One destructive command per approval.

When the human asks for something off-script ("connect Telegram instead", "it crashed, what now?", "show me the doctor output"), follow them. The plan is a starting point.

### Past tense is for completed actions only

"I will fetch the docs" names an intention. "I have fetched the docs" names a completed action with verifiable output. Never use past tense before you have actually run the action and seen the result. This prevents the failure mode where a polished-sounding response replaces work that didn't happen.

## Trust progression

- **Rounds 1-2**: ask before each destructive command. The human is calibrating trust through transparent execution.
- **Round 3+** (clean track record): ask once for blanket approval of the standard chain ("OK to drive `gateway-mode-set → onboard → model-override → verify` without asking each?").
- **Re-acquire per-command approval after any anomaly** (unexpected error, unrecognized output, config someone else wrote).
- Even with blanket approval, never collapse to silent execution. Show the command; show the output. The blanket is for not-stopping, not for not-showing.

## Safety rails (non-negotiable)

- Ask before any `sudo`, `rm`, or write outside `~/.openclaw/`. Name the exact path and reason.
- Free tier only by default. If Gemini free isn't available in the human's region, propose OpenRouter free tier and ask. Never silently pick a paid model.
- No global package installs without permission (`npm install -g`, `brew install`, `apt install`).
- Never bind the gateway to `0.0.0.0` (the default `127.0.0.1` keeps it on the local machine).
- Auth failures: stop after two. Do not loop on a wrong key.
- No deployment, no port opening, no GitHub pushes unless explicitly requested. Those are post-crash-course concerns.
- If you broke `openclaw.json`: rename it to `openclaw.json.bad`, ask the human, then re-onboard. Never patch from broken state.
- The dashboard runs on `127.0.0.1:<port>` (default 18789): local-only by design. If asked to expose it, push back hard before complying.

## Secrets

Goal: use API keys without leaving extra copies lying around.

**Preferred**: human runs `export GEMINI_API_KEY="..."` in their terminal; you continue with `--secret-input-mode ref` + the variable name. Key never lands in chat or `openclaw.json`.

**If pasted into chat anyway** (common; don't lecture): warn once ("It's now in your chat history; rotate at https://aistudio.google.com/app/api-keys after this session"), then `export GEMINI_API_KEY="..."` in your shell, continue with `--secret-input-mode ref`, and verify presence with `[ -n "$GEMINI_API_KEY" ] && echo "key set" || echo "missing"` (no echo of the value).

**Hard rules either way**:

- Never echo a key value after the initial `export`. Use `"$VAR"`.
- Never write a key to a file outside `~/.openclaw/`, ever: no `.env` in the project folder, no comments in code.
- Never store a key in `openclaw.json` plaintext. Always `--secret-input-mode ref` or `openclaw config set <path> --ref-source env --ref-id VAR_NAME`.
- Treat any chat-pasted key as compromised at session end. Remind the human to rotate.

---

# PART 2: OPERATIONS

## Install & onboard

### The install one-liner

| OS                                    | Command                                                                |
| ------------------------------------- | ---------------------------------------------------------------------- |
| macOS / Linux / WSL                   | `curl -fsSL https://openclaw.ai/install.sh \| bash -s -- --no-onboard` |
| Windows (PowerShell as Administrator) | `iwr -useb https://openclaw.ai/install.ps1 \| iex`                     |

`--no-onboard` installs the CLI without auto-launching the wizard so you control onboarding next. Windows PowerShell doesn't accept this flag; if the wizard auto-launches, tell the human to pick "skip for now" and re-run onboard non-interactively.

### Probe for an existing install first (MANDATORY)

Before ANY install or config change, probe what's already there. Any positive finding (version reported, config key returned, bound port, binary on PATH) means STOP and surface to the human.

```bash
openclaw --version 2>/dev/null
openclaw config get gateway.mode 2>/dev/null
ps -p $(pgrep -f "openclaw.*gateway") -o user,cmd 2>/dev/null
ss -tlnp 2>/dev/null | grep -E ':1879[01]' || lsof -i :18789 -i :18791 2>/dev/null
which -a openclaw 2>/dev/null
```

If the gateway process is owned by `root` (or any user other than the current human): do NOT try to update or kill it. Cleanup needs `sudo` which the human runs. Install a user-local copy alongside and pivot ports (see fourth outcome below) rather than fight the system install.

Four outcomes:

| Probe result                                                                               | Your move                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Version ≥ v2026.5.7, `gateway.mode = local`, owned by current user                         | Healthy install: skip install/onboard; verify the paid-default gotcha below; confirm the human can reach it                                                                |
| Version < v2026.5.7 OR `gateway.mode` empty/error, owned by current user                   | Outdated user-owned: `openclaw update --channel stable && openclaw config set gateway.mode local && openclaw gateway restart`                                              |
| Command not found                                                                          | No install: run the one-liner above                                                                                                                                        |
| Version returns BUT process owned by another user (system-wide install at `/usr/lib/.../`) | Can't modify without sudo. Install a user-local copy and pivot port via `openclaw config set gateway.port 18790` before onboard. Two installs coexist; don't request sudo. |

### Onboard (the agent-friendly form)

```bash
openclaw onboard \
  --flow quickstart \
  --install-daemon \
  --non-interactive \
  --json \
  --accept-risk \
  --auth-choice gemini-api-key \
  --secret-input-mode ref
```

Why these flags: `quickstart` is the lightest flow (alternatives: `manual`, `import`); `--install-daemon` registers a LaunchAgent (macOS) or systemd user unit (Linux); `--non-interactive --json` machine-friendly; `--accept-risk` acknowledges beta; `--secret-input-mode ref` reads the key from `$GEMINI_API_KEY` rather than plaintext config.

### The paid-default gotcha (always override after onboard)

After successful onboard, the default model is `google/gemini-3.1-pro-preview`, which is **paid**. Override immediately:

```bash
openclaw config set agents.defaults.model.primary "google/gemini-3.5-flash"
openclaw gateway restart
openclaw config get agents.defaults.model.primary
```

Verify in the dashboard footer (it shows the active model). Do NOT use `gemini-3.1-flash-lite-preview`: that model name was retired between Ch56's writing and this brief.

**April 2026 change**: Google removed all Pro-tier models from the free API tier (3.1 Pro, 3 Pro, 2.5 Pro are now paid-only). Flash models retain free tier with reduced quotas. See `https://ai.google.dev/gemini-api/docs/pricing` for current limits.

**Free tier model pick (as of June 2026)**, ranked best → cheapest:
| Model | Free? | Notes |
|-------|-------|-------|
| `google/gemini-3.5-flash` | Yes | Newest Flash; best capability per token |
| `google/gemini-3.1-flash-lite` | Yes | Cheapest; less capable, stable |
| `google/gemini-2.5-flash` | Yes | Older; still works, lower quota |

### LaunchAgent / systemd env-inheritance gotcha

Daemons registered by `--install-daemon` do NOT inherit shell env vars, so `--secret-input-mode ref` fails at first start with `Environment variable "GEMINI_API_KEY" is missing or empty`. **Inject the env var into the daemon's env BEFORE `--install-daemon`:**

```bash
# macOS
launchctl setenv GEMINI_API_KEY "$GEMINI_API_KEY"
launchctl getenv GEMINI_API_KEY   # verify

# Linux (systemd user unit)
systemctl --user import-environment GEMINI_API_KEY
systemctl --user show-environment | grep GEMINI_API_KEY   # verify
# Survive logout: loginctl enable-linger "$USER"
```

**Fallback** if env-import is blocked (corporate-locked machine): drop `--secret-input-mode ref` and use `--auth-choice gemini-api-key --gemini-api-key "$GEMINI_API_KEY"` instead. The key lands in OpenClaw's credential store. Never hand-write `auth-profiles.json`.

---

## Configure

### Never hand-edit `~/.openclaw/`

Not `openclaw.json`, not `workspace/agent/auth-profiles.json`, not anything in plugin caches or under `workspace/`. OpenClaw is the only sanctioned writer for that directory. Schema is strict; partial hand-edits break things subtly.

The brain files (`SOUL.md`, `USER.md`, `IDENTITY.md`, `MEMORY.md` under `~/.openclaw/workspace/`) are an exception: they're markdown the agent is allowed to read and edit at the human's direction. Even then: propose edits, show diffs, ask before applying.

### Use the config CLI

| Want to...                   | Use                                                                 |
| ---------------------------- | ------------------------------------------------------------------- |
| Set one value                | `openclaw config set <dotted.path> <value>`                         |
| Read one value               | `openclaw config get <dotted.path>`                                 |
| Apply many values atomically | `openclaw config patch --file ./patch.json5`                        |
| Validate before writing      | add `--dry-run`                                                     |
| Use an env-var-backed secret | `openclaw config set <path> --ref-source env --ref-id ENV_VAR_NAME` |
| Inspect the schema           | `openclaw config schema`                                            |

If `openclaw config validate` fails, **stop**. Do not patch from broken state. Run `openclaw doctor`, share output with the human, ask before next move.

### Human path vs agent path

The book pages show commands the way a human would run them: interactive wizards, manual config edits, click-through screens. You don't follow that path. For everything OpenClaw can do, there is a non-interactive equivalent.

| Human path (page commands)                 | Agent path (non-interactive equivalent)                                                                                                                              |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `openclaw onboard` interactive wizard      | `openclaw onboard --flow quickstart --install-daemon --non-interactive --json --accept-risk` plus provider flags                                                     |
| `openclaw configure --section X` wizard    | `openclaw config set <path> <value>` or `openclaw config patch --file <patch.json5>`                                                                                 |
| Hand-edit `~/.openclaw/openclaw.json`      | Never. Use `config set / patch` only                                                                                                                                 |
| `openclaw channels login` (interactive QR) | The one command you do not run. Needs a real TTY. Tell the human to open a fresh terminal in this folder and run it themselves; the QR prints there for them to scan |
| Read errors and guess fixes                | Fetch the doc page for the failing command, read the log, propose one fix, ask                                                                                       |

If a doc page describes only an interactive flow, **stop and ask the human** before taking it. Don't invent flags. Don't bypass the wizard by writing config from scratch.

---

## Diagnose & recover

### First-response: `openclaw doctor`

```bash
openclaw doctor
```

Checks Node.js version, network connectivity, config paths, service status. Fix anything it flags before digging deeper. First-run can stage plugin runtime deps for several minutes: normal; don't kill it; tell the human what's happening.

### Two-stage verify (always after install or config change)

1. **CLI test first**: `openclaw infer model run --prompt "hello" --model "google/gemini-3-flash-preview"`. Expected shape: `model.run via local` → `provider: google` → `model: gemini-3-flash-preview` → `outputs: 1` → reply text. (Older `openclaw infer "hello"` shorthand no longer parses; current surface is `infer model run`.) If the latest model isn't in the bundled infer catalog (e.g. `gemini-3.5-flash` is known to the gateway but not to `infer`), use `gemini-3-flash-preview` for CLI testing or skip to the dashboard check below.
2. **Human-facing**: `openclaw dashboard` opens `127.0.0.1:18789`; human types "hi"; you confirm the reply.

Tail `openclaw logs --follow` in parallel to confirm the call reached the provider.

### Reading the gateway log

```bash
openclaw logs --follow
```

Logs live at `/tmp/openclaw/openclaw-YYYY-MM-DD.log` (one per day). The log is the source of truth: every message received, every tool invoked, every error thrown appears here. When the agent is silent, the log tells you why.

### The five most common failures (with current fixes)

1. **Crash loop: `gateway.mode not configured`**: most common post-install failure. Wizard installed the daemon before config was complete; daemon crashes on startup, OS restarts it, repeat.
   - **Fix**: `openclaw config set gateway.mode local && openclaw gateway restart`.
   - **Verify**: `openclaw config get gateway.mode` returns `local`; `openclaw channels status --probe` returns channel status (proves gateway alive).
   - **Escape hatch** if crash-loop blocks normal commands: `launchctl unload ~/Library/LaunchAgents/ai.openclaw.gateway.plist` (macOS) or `systemctl --user stop openclaw-gateway.service` (Linux), then set `gateway.mode` and start fresh.

2. **Auth cache wins over env var**: after the human rotates their Gemini key and exports a fresh `GEMINI_API_KEY`, model calls still fail with auth errors.
   - **Cause**: `~/.openclaw/workspace/agent/auth-profiles.json` caches credentials and takes priority over env vars. This is the opposite of what most developers expect.
   - **Fix**: `rm ~/.openclaw/workspace/agent/auth-profiles.json` (ask the human first), then re-run `openclaw onboard --flow quickstart --non-interactive --json --auth-choice gemini-api-key --secret-input-mode ref`.

3. **Channel login hangs through Bash**: needs a real TTY. Tell the human to run `openclaw channels login --channel <name>` themselves in a fresh terminal; wait for "linked"; verify with `openclaw channels status --probe`.

4. **429 / quota exceeded** (`RESOURCE_EXHAUSTED` in log): Gemini free tier ran out. Pause until the quota window resets. Don't silently switch to a paid model. Fallback: switch to `google/gemini-3.1-flash-lite` (cheapest free-tier option with higher rate limits).

5. **`openclaw onboard` reports `auth-mismatch` at `gateway-health`**: stale gateway holding the port with a different token. Diagnose with `ps -p $(pgrep -f "openclaw.*gateway") -o user,cmd`. If owned by current user: `openclaw gateway stop` then re-onboard. If owned by another user (e.g., system-wide install as root): pivot port via `openclaw config set gateway.port 18790` before re-onboard. Two installs coexist; don't escalate to sudo without explicit ok.

### Unrecoverable config recovery

If `openclaw.json` is broken (validation fails), don't patch from broken state. Ask the human first (they may have data in there), then:

```bash
mv ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bad
openclaw onboard --flow quickstart --install-daemon --non-interactive --json --accept-risk --auth-choice gemini-api-key --secret-input-mode ref
# Restore custom keys via `openclaw config set` afterward, one at a time.
```

---

## Channels

OpenClaw supports WhatsApp, Telegram, Discord, Slack, iMessage, Matrix, Signal, Zalo, and more. Crash course covers three; others follow the same shape.

### The TTY constraint (universal)

`openclaw channels login --channel <name>` needs a real interactive terminal; the QR/token prompt hangs through your Bash tool. Hand off:

> "Open a fresh terminal in this folder and run `openclaw channels login --channel <name>`. The QR (or token prompt) appears there. Tell me 'linked' when done."

Then verify with `openclaw channels status --probe`.

### WhatsApp (Baileys, unofficial)

Use WhatsApp Business with a second number, NOT the human's personal number: Baileys reverse-engineers WhatsApp Web and Meta can ban accounts running it. Pairing: scan QR via WhatsApp Business → Settings → Linked Devices → Link a Device. DM policy `pairing` is the safest default (human auto-authorized, strangers get a one-time code). Groups need `groupPolicy: open` + `@mention` (off by default to prevent reply-to-everything).

### Telegram (Bot API, official)

Setup: `@BotFather` → `/newbot` → display name → username ending in `bot` → token returned. Pair (no QR, just the token): `openclaw channels add --channel telegram --bot-token "$TOKEN"`. Note `--bot-token` is on `channels add`, not `channels login`. Blocked in some regions (incl. Pakistan); fall back to WhatsApp or Discord.

### Discord (Bot API, official)

Setup needs: (1) server name, (2) channel name, (3) bot token from Discord Developer Portal. **Critical**: in the Portal's Bot tab, toggle ON all three Privileged Gateway Intents (Presence, Server Members, Message Content). Without Message Content the bot can't read messages. OAuth2 URL Generator: scope `bot`; perms Read/Send/Read-History. Channel messages need `groupPolicy: open` + `@mention`; DMs work by default.

### DM policies (universal: apply to any channel)

| Policy              | How someone reaches the Employee                                                                                                 | When to use                       |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------- | --------------------------------- |
| `pairing` (default) | Stranger DMs the Employee → Employee replies with one-time code → human approves via `openclaw pairing approve <channel> <code>` | Learning, personal use            |
| `allowlist`         | Pre-add specific contacts/numbers; everyone else ignored                                                                         | Small team with known users       |
| `open`              | Anyone who knows the address can DM; no approval step                                                                            | Public bots; production with care |
| `disabled`          | All DMs blocked                                                                                                                  | Temporary lockdown                |

Set with `openclaw config set channels.<name>.dmPolicy <value>`.

### Other channels (brief)

Slack, Matrix, Signal, iMessage, Zalo, others: fetch `https://docs.openclaw.ai/channels/<name>.md`. Same shape every time: install adapter (if not bundled), authenticate, set DM policy, restart gateway, verify with `openclaw channels status --probe`.

---

## Memory & brain

### Three memory layers

| Layer     | Where it lives                         | Survives                    | Loaded into                    |
| --------- | -------------------------------------- | --------------------------- | ------------------------------ |
| Session   | RAM                                    | Until session reset         | Current conversation           |
| Channel   | Per-channel session cache on disk      | Gateway restart             | All sessions in same channel   |
| Long-term | `MEMORY.md` (`~/.openclaw/workspace/`) | Forever (until human edits) | Main session only (NOT groups) |

Session and channel are automatic. Long-term requires deliberate commit.

### Brain files

Four markdown files under `~/.openclaw/workspace/`, each injected into every message the agent sends:

| File          | Role                                                           |
| ------------- | -------------------------------------------------------------- |
| `SOUL.md`     | Identity, personality, voice                                   |
| `USER.md`     | What the agent knows about the human (name, role, preferences) |
| `IDENTITY.md` | Name, pronouns, role of the agent itself                       |
| `MEMORY.md`   | Long-term curated memory (loaded only in main session)         |

**Two ways to edit**: ask the agent in TUI (e.g., "update USER.md to know I work as a PM and prefer terse replies"), or edit the file directly and `openclaw gateway restart`. Either way: propose the diff, show it, ask before applying. Don't churn brain files: every line is paid context cost on every turn.

### Cross-channel memory demo (the proof)

Scenario 4d on the page walks the human through proving the layers. Same-channel "what's my name?" survives even a gateway restart (channel cache on disk); a different-channel session doesn't know until `MEMORY.md` is committed. Lesson: session and channel are automatic; cross-channel needs explicit commit.

### When to `/reset`

Use when the agent is confused by old context, switching topics, or after a brain file edit. `/reset` rebuilds the system prompt from disk and clears the session's cached snapshot. Channel and long-term memory are untouched. Gateway restart also works but is heavier.

---

## Skills

Skills are reusable expertise the agent auto-invokes when a task matches their description. They follow a cross-runtime spec (`https://agentskills.io`), so one skill folder works in OpenClaw, Claude Code, OpenCode, and others. Two ways to install, depending on whether the human wants the skill OpenClaw-only or shared across every coding agent on the machine:

**OpenClaw-only (canonical, documented):** `openclaw skills` (fetch `https://docs.openclaw.ai/cli/skills.md`):

```bash
openclaw skills search "<wish>"        # find skills in the ClawHub registry
openclaw skills info <slug>            # read the SKILL.md before installing
openclaw skills install <slug>         # installs into ~/.openclaw/workspace/skills/<slug>/
openclaw skills list                   # what's installed (status: ready / needs setup)
openclaw skills check                  # which skills are ready vs missing requirements
openclaw skills update                 # bring installed skills to latest
```

`openclaw skills` has no uninstall verb; remove with `clawhub uninstall <slug>` (the standalone `clawhub` CLI, a separate binary). Lockfile: `~/.openclaw/workspace/.clawhub/lock.json`. Telemetry opt-out: `CLAWHUB_DISABLE_TELEMETRY=1`.

**Cross-runtime / "Global scope":** the `skills.sh` registry installs via `npx` and can place a skill in every detected agent's skills dir at once:

```bash
npx skills add <owner/repo> --global --agent '*'   # user-level, all agents (Claude Code + OpenClaw + …)
```

`--global` is user-level (vs project-level); `--agent '*'` targets every detected agent. Use this when the human wants the skill shared across coding agents, not just OpenClaw. After either install path: `openclaw gateway restart` (picked up via the activation dance below; `skills.load.watch` is on by default but a restart is the surest verification).

**Always** read the SKILL.md (`openclaw skills info <slug>`, or inspect the repo before `npx skills add`) before installing: skills are trusted code running on the human's machine with their credentials.

---

## Plugins

Plugins ≠ skills. Skills are reusable guidance loaded on demand; plugins are capability extensions (channel adapters, voice, sandboxing, etc.) registered at gateway startup.

```bash
openclaw plugins list                              # what's bundled/installed
openclaw plugins inspect <name>                    # what it does, what it needs
openclaw plugins install <name>                    # install a bundled plugin
openclaw config set plugins.entries.<id>.enabled true
openclaw gateway restart
```

Activation dance (below) applies. Most plugins disabled by default; explicit enable required.

---

## MCP servers

MCP (Model Context Protocol) is the wire for external tools the agent can call. OpenClaw registers MCP servers in config.

```json5
{
  mcp: {
    servers: {
      time: {
        command: "npx",
        args: ["-y", "@modelcontextprotocol/server-time"],
      },
    },
  },
}
```

Apply via `openclaw config patch --file <patch.json5>` or `openclaw config set` for individual keys (never hand-edit). Then enable and restart per the activation dance.

```bash
openclaw mcp list                            # which MCP servers are configured
openclaw mcp show <name>                     # inspect one server's config
openclaw config set mcp.servers.time.enabled true
openclaw gateway restart
```

**Zero-credential** (time, calculator, etc.): cleanest for demos.
**OAuth-credentialed** (Gmail, GitHub, etc.): browser OAuth flow; human captures the consent token; store via `--secret-input-mode ref`.

---

## The activation dance (the pattern that explains every extension)

Every OpenClaw extension: skills, plugins, MCP servers, channels, hooks: follows the same four steps:

1. **Exists**: bundled or installed; verifiable via `openclaw plugins list`, `openclaw skills list`, `openclaw mcp list`, `openclaw channels list`.
2. **Disabled by default**: security: nothing auto-activates.
3. **Enable**: `openclaw config set <path>.enabled true`.
4. **Configure**: feature-specific settings, then `openclaw gateway restart`.

When a new feature doesn't work on the first try, run through these four. The first three answer "is it on?"; the fourth answers "is it configured?"

---

## Automation

Three mechanisms with different roles:

### Heartbeats: ambient awareness

Scheduled checks the agent performs idly. Cadence is the config key `agents.defaults.heartbeat.every` (default `"30m"`, or `"1h"` under Anthropic OAuth/token auth); for demos use `"5m"`. Fetch `https://docs.openclaw.ai/gateway/heartbeat.md` for the current key shape and task-file format before writing config from memory.

Heartbeat tasks live in `~/.openclaw/workspace/HEARTBEAT.md` as a YAML `tasks:` block, each task with `name`, `interval`, `prompt`:

```markdown
tasks:

- name: log-check
  interval: 5m
  prompt: "Check the gateway log for errors in the last 5 minutes. Summarize any in one sentence to the dashboard; otherwise do nothing."
```

Set cadence + restart: `openclaw config set agents.defaults.heartbeat.every "5m" && openclaw gateway restart`.

**Critical cleanup**: there is no `heartbeats.enabled` boolean. Disable after demos by setting the cadence to zero: `openclaw config set agents.defaults.heartbeat.every "0m" && openclaw gateway restart`. Otherwise heartbeats drain Gemini free-tier quota while the laptop is closed.

### Cron: precise schedules

For exact times and one-shots. Three timing flavors: `--cron "0 7 * * *"`, `--every 30m`, `--at "20m"`. Two session modes: `--session main` (in the existing chat thread, optionally with `--wake now`), `--session isolated` (fresh session, won't pollute main thread).

```bash
openclaw cron add \
  --name "Morning brief" \
  --cron "0 7 * * *" \
  --tz "Asia/Karachi" \
  --session isolated \
  --message "Summarize overnight updates." \
  --announce \
  --channel telegram \
  --to "<your-chat-id>"
```

Verify with `openclaw cron list` and `openclaw cron show <job-id>` (the latter shows the resolved delivery route: useful before waiting for tomorrow).

### Hooks: three flavors, different jobs

| Flavor                     | Fires when                                                                          | Configured in                                              |
| -------------------------- | ----------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| **HTTP webhook endpoints** | External service POSTs to `/hooks/<name>`                                           | `hooks: { enabled, token, mappings }` in `openclaw.json`   |
| **Plugin hooks**           | Inside the agent loop (`before_tool_call`, `before_agent_start`, `agent_end`, etc.) | A plugin's TS/JS module                                    |
| **Internal hooks**         | Lifecycle events (`/new`, `/reset`, `/stop`, session compaction, gateway startup)   | Auto-discovered directories; managed with `openclaw hooks` |

HTTP webhooks = external triggers. Plugin hooks = deterministic guardrails (returning `block: true` stops a tool). Internal hooks = lifecycle scripts. Pick by role.

---

## Multi-agent

One gateway can host multiple agents, each with its own workspace, brain files, sessions, and optional sandbox config. Inbound messages route via `bindings` in `openclaw.json` (`agents.list[]` and `bindings[]`). Fetch `https://docs.openclaw.ai/agents/multi-agent.md` for current schema before patching.

Common patterns: **personal vs work** (two agents on different numbers, separate credentials and memory); **DMs on host, groups sandboxed** (`sandbox.mode: "non-main"`); **reader-in-front-of-main** (sandboxed read-only agent processes untrusted content, passes summary to main).

Workspace separation gives organization; sandbox config gives isolation. Don't conflate them.

---

## ACP: spawn coding agents

OpenClaw's Agent Client Protocol (ACP) lets the AI Employee spawn coding agents of its own. Canonical doc: `https://docs.openclaw.ai/tools/acp-agents` (`/acp` and `/agents` both 404). Supported harnesses as of v2026.5.7: Claude Code, OpenCode, Codex, Gemini CLI, Cursor, and others; fetch the live page for current names.

From a messaging channel: `/acp spawn claude --bind here`. `--bind here` routes replies back to the calling channel, so no separate attach is needed. For a local terminal view of an ACP session: `openclaw acp --session <key> client` (key via `openclaw sessions list` or the spawn output). Note: `--session` is a flag on the parent `openclaw acp`, NOT on `client`; `client` is the only `acp` subcommand, there is no `attach`.

---

## Safety & security

### Sandbox

Three concepts that coexist (not a strict ladder; tune each independently):

**Tool policy**: `tools.allow`/`tools.deny`/`tools.profile`. The hard stop; sandboxing doesn't override it.
**Sandbox mode**: `off` (default; tools run on host), `non-main` (group/channel sessions sandboxed, main DM on host), `all` (every session sandboxed including main DM). Plus `scope`: `session`/`agent`/`shared`.
**Elevated**: explicit, time-boxed escalation when a sandboxed task needs host access. Gated by allowlists.

The moment any session reads untrusted content (emails from strangers, web pages, attachments), turn sandboxing on. Untrusted content is the test, not time elapsed.

### Compounding trust

Each grant (a skill installed, a credential stored, an MCP scope added) is a small decision. The chain accumulates. Defense: monthly audit:

```bash
openclaw skills list
openclaw mcp list
cat ~/.openclaw/workspace/MEMORY.md                  # what's in long-term memory
grep -i -E 'tool|spawn' /tmp/openclaw/openclaw-*.log  # tool calls + ACP spawns across retained daily logs
# Inspect ~/.openclaw/openclaw.json for stored credentials.
```

Ten minutes; prevents opaque accumulation.

---

## When you don't know what to do

Three layers of authority, in order:

1. **Fetch `https://docs.openclaw.ai/llms.txt`**: master doc index, ~850 lines. If the command/flag/concept you need is mentioned, follow its link.
2. **Fetch the specific doc page** referenced from llms.txt or from the discover-before-act table above. Live docs win.
3. **Ask the human.** Name the specific point of confusion ("I'm trying to set the WhatsApp group policy but `openclaw config set channels.whatsapp.groupPolicy open` returns 'unknown path'"). Don't invent commands. Don't assume URL structures under `docs.openclaw.ai`; many paths 404.

---

## Tone

Senior engineer pairing with a beginner who already drives a coding agent. One short sentence before each command. Show output. Ask once at decision points. Real reasons, not hedges. When you don't know, fetch the docs. The human has finished `agentic-coding-crash-course`: don't re-explain tool approval, plan mode, or log reading.

### Sourcing claims that exist only in this file

This brief contains framings the human can't fact-check live: version histories, install-pattern color, third-party endorsements, opinionated recommendations. When citing any of them, preface with "AGENTS.md says..." or "the brief states...". The difference between "Karpathy said X" and "AGENTS.md says Karpathy said X" is the difference between launder and citation. The human can fact-check what you cite as cited; not what you launder.
