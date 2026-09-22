# Facilitator guide

This branch (`solutions`) is main plus what participants should not start from: the
overlays that make each starting branch, the solutions, and the scripts that build and
verify them. The deck, its speaker notes and the timing live with the deck, not here.

## The branches

| Branch | Built from | For |
|---|---|---|
| `main` | by hand | exercises 1 and 5, and the base of every other branch |
| `ex2-start` | main + `overlays/ex2-start` | a VAT rounding bug that turns CI red |
| `ex3-goal-start` | main + `overlays/ex3-goal-start` | `TICKET.md` only, for the `/goal` run |
| `ex3-loop-start` | main + both ex3 overlays | the ticket plus the prepared `.fairmind/` contract |
| `ex4-start` | main + `overlays/ex4-start` | free shipping, with two flaws for the reviewer |
| `solutions` | main + `tools/` | you |

Never edit a starting branch by hand. Change `main` or an overlay, then:

```bash
git checkout solutions && git merge main
python3 tools/build_branches.py
FM_SCRIPTS=<path to the public plugin>/plugins/fairmind-coding/scripts bash tools/verify.sh
git push origin main solutions
git push --force origin ex2-start ex3-goal-start ex3-loop-start ex4-start
```

Overlays store `.fairmind/` as `_fairmind/`; the build renames it.

**Rebuild and force-push the starting branches in the same sitting as every change to
`main`.** `reset` replays the template's `main`→starting-branch diff on the
participant's copy, so a starting branch built from an older `main` carries the
inverse of every newer change: `reset ex2` would bring back the old handouts and the
old `workshop`. `verify.sh` fails on exactly that ("rolls main's files back").

## What each exercise is built to show

- **Ex 1.** The receipt prints `24.5 EUR`. Any fix works; the point is the event log.
  `workshop events` reads it (UTF-16 too, for a PowerShell 5.1 redirect), and `workshop
  hook` writes the `PostToolUse` hook into the gitignored `.claude/settings.local.json`,
  calling `workshop log-tool` through the absolute interpreter path, with no jq. The
  headless run needs the committed `.claude/settings.json` allow-list: without it
  every test command is denied, and Claude Code ignores that file until the folder is
  trusted, which README's setup and `doctor` cover.
- **Ex 2.** `shop/tax.py` truncates instead of rounding half up: `test_vat_rounds_half_up`
  fails. CI waits 100 s in a step that says it checks nothing, so a `/loop` has
  something to wait for. `./workshop deploy` regresses at minute 7 for 3 minutes.
- **Ex 3.** The ticket never says what `FREE100` takes 100% off. The brief does: items
  only, shipping still charged. `ac4-free-keeps-shipping` is the check `/goal` usually
  has no reason to satisfy. `module-exists` passes before any work and is quarantined
  by admission; no criterion points at it, so arming still succeeds. The exercise ends
  at the first green evaluation (`confirmation 1/3`).
- **Ex 4.** `shipping_for` uses `>` where the docstring says "50.00 EUR or more", and
  the receipt still prints the full shipping fee on a free order. The shipped tests
  cover neither; `solutions/ex4/tests/test_shipping.py` catches both.
- **Ex 5.** No code. The discussion is the merge policy, and the solo-copy trap in
  `kit/ex5/merge-policy.md`: GitHub cannot tell a routine from its owner.

## Windows

Participants on Windows run natively: `py workshop …`, and Git for Windows, whose Git
Bash Claude Code uses for its shell. Nothing here has been run on Windows yet. The
known risk is exercise 3 run 2: the plugin's loop gate calls `python3` from Git Bash,
and a python.org or `winget` Python answers only to `python` and `py`. `doctor`
checks it on Windows. Before a room with Windows laptops, run the whole kit on one.

## API credits

Participants on API credits need one key each, for two uses: Claude Code in their
terminal (`export ANTHROPIC_API_KEY=…`) and the review in their copy (the repository
secret `ANTHROPIC_API_KEY`). Issue one key per participant from a Console workspace
with a spend limit, so one runaway loop cannot drain the room, and revoke the keys
after the workshop: they sit in repository secrets you do not control. Routines do
not run on an API key; those participants do exercise 5's routines by hand.

## Before each delivery

1. Run `tools/verify.sh` against the **public** plugin participants will install.
2. Re-check the dated facts in the deck's delivery notes (`/loop`, `/goal`, routines).
3. Make a copy from the template in a scratch account and run README's setup end to end:
   the steps that touch GitHub (app, secret, ruleset, label event) are the ones
   `verify.sh` cannot see.
