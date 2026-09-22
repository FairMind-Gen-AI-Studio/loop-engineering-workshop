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

## Before the workshop · 20 minutes

1. **Make your own copy.** On GitHub, **Use this template → Create a new repository**,
   in your own account. Make it **public**: branch rulesets need a public repository
   or a paid plan. Then clone it.
2. **Install the tools:** [Claude Code](https://claude.com/claude-code),
   [GitHub CLI](https://cli.github.com) (`gh auth login`), `jq`, Python 3.10 or later,
   and `python3 -m pip install pytest`.
3. **Install the plugin** (exercise 3), inside Claude Code:

   ```
   /plugin marketplace add FairMind-Gen-AI-Studio/fairmind-plugins-public
   /plugin install fairmind-coding@fairmind-plugins
   ```

4. **Give the review its credential** (exercises 4 and 5). The review runs on your
   own Claude subscription:

   ```bash
   claude setup-token                          # prints a token
   gh secret set CLAUDE_CODE_OAUTH_TOKEN       # paste it
   ```

5. **For exercise 5**, if your plan includes routines (`/schedule`), install the
   [Claude GitHub App](https://github.com/apps/claude) on your copy. Without
   routines you run the same prompts by hand.
6. **Check and set up:**

   ```bash
   ./workshop doctor      # every line should be ✓
   ./workshop setup       # labels, CODEOWNERS, the main ruleset
   ```

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

## Two things that will bite

- **Edit `.github/workflows/review.yml` on `main` only.** The review action refuses to
  run when its workflow file differs from the default branch, and then exits green
  having reviewed nothing.
- **The routines act as you.** Anything a routine commits, opens or merges carries
  your GitHub identity. Exercise 5 is about what that means for a merge policy.
