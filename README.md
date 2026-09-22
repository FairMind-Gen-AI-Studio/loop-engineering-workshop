# Loop engineering workshop

The exercises for **Loop Engineering with Claude Code**, a half-day FairMind Academy
workshop. Five loops, each built on the one inside it:

| Ring | Loop | Exercise |
|---|---|---|
| 1 | the agentic loop: model, tool, result | [Watch the loop you already run](kit/ex1.md) |
| 2 | `/loop`: repetition on a clock | [Put a clock on it](kit/ex2.md) |
| 3 | `/goal` and `/fairmind-loop`: an exit the maker does not judge | [Same task, two evaluators](kit/ex3.md) |
| 4 | the pull request review loop | [Write your own review loop](kit/ex4.md) |
| 5 | dogfooding: defects → nightly repair → merge | [Close the loop on today](kit/ex5.md) |

Everything runs on `shop/`, a checkout small enough to read in five minutes.
Amounts are integer cents; `python3 -m shop` prints a receipt.

## What you need

- A **GitHub account**, and the rights to create a public repository in it.
- A **Claude subscription** (Pro, Max, Team or Enterprise): the review runs on it
  through `claude setup-token`, and routines (exercise 5) need it too.
- macOS or Linux. On Windows, use WSL; the commands below assume a POSIX shell.

## Before the workshop · 20 minutes

Do this the day before. Every step is checked by `./workshop doctor` at the end.

1. **Make your own copy.** On GitHub, **Use this template → Create a new repository**,
   in your own account. Make it **public**: branch rulesets, which exercise 5 uses,
   need a public repository or a paid plan. Your exercise work will be visible.
   Then clone your copy and `cd` into it.
2. **Install the tools:** [Claude Code](https://claude.com/claude-code) (logged in),
   [GitHub CLI](https://cli.github.com) then `gh auth login`, `jq`, Python 3.10 or
   later, and `python3 -m pip install pytest`.
3. **Install the plugin** (exercise 3). Inside Claude Code:

   ```
   /plugin marketplace add FairMind-Gen-AI-Studio/fairmind-plugins-public
   /plugin install fairmind-coding@fairmind-plugins
   ```

4. **Let Claude review your pull requests** (exercises 4 and 5). Two things, both on
   your copy:
   - install the [Claude GitHub App](https://github.com/apps/claude) and give it
     access to your copy: the review posts through it;
   - give the review its credential, generated on your own subscription:

     ```bash
     claude setup-token                          # prints a long-lived token
     gh secret set CLAUDE_CODE_OAUTH_TOKEN       # paste it when asked
     ```

5. **Check, then set up:**

   ```bash
   ./workshop doctor      # every line should be ✓
   ./workshop setup       # labels, CODEOWNERS, the main ruleset
   ```

   `setup` commits one change to your `main` (it puts your username in
   `.github/CODEOWNERS`) and pushes it, then turns on the ruleset. Run it once.

## During the workshop

Each exercise starts from a clean branch:

```bash
./workshop reset ex2        # ex1, ex2, ex3-goal, ex3-loop, ex4, ex5
```

It asks before discarding uncommitted changes, and builds the exercise on top of
your own `main`, so the pull requests you open go to your copy.

## What is in here

| Path | What |
|---|---|
| `shop/`, `tests/` | the application and its tests (`python3 -m pytest`) |
| `kit/` | one handout per exercise, plus `kit/ex5/` for the dogfooding exercise |
| `.github/workflows/ci.yml` | tests plus a clearly labelled simulated slow stage, about two minutes |
| `.github/workflows/review.yml` | Claude reviews every pull request, then labels it `reviewed` |
| `.github/ISSUE_TEMPLATE/defect.yml` | a defect with a stable key and a Reproduce block |
| `.github/CODEOWNERS`, `.github/rulesets/main.json` | the paths that stay human, and what GitHub enforces |
| `.claude/skills/review-loop/` | the skill you write in exercise 4 |
| `scripts/fake_deploy.py` | the fake production log for exercise 2 |
| `workshop` | `doctor`, `setup`, `reset`, `deploy` |

## If something goes wrong

| Symptom | Cause and fix |
|---|---|
| `./workshop doctor` shows ✗ | the line after the arrow says what to install or run |
| `reset` says it could not start an exercise | your `main` has diverged from the template's; ask the facilitator |
| the review check is green and nothing was posted | it ran for ~15 s: the workflow file differs from `main`'s, or the app is not installed on your copy |
| the review check is red: credential not set | `gh secret set CLAUDE_CODE_OAUTH_TOKEN` on your copy |
| `/fairmind-loop` asks about a Fairmind workspace | answer **no**: the loop runs without one |
| `setup`: ruleset not created | your copy is private on a free plan; make it public |

## Two things that will bite

- **Edit `.github/workflows/review.yml` on `main` only.** The review action refuses to
  run when its workflow file differs from the default branch, and then exits green
  having reviewed nothing.
- **The routines act as you.** Anything a routine commits, opens or merges carries
  your GitHub identity. Exercise 5 is about what that means for a merge policy.
