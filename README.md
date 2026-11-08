# Loop engineering workshop

The exercises for **Loop Engineering with Claude Code**, a FairMind Academy workshop
with a two-hour run. Five loops, each built on the one inside it, and one exercise on
what a run carries over to the next:

| Exercise | Loop | Where |
|---|---|---|
| 1 · [Watch the loop you already run](kit/ex1.md) | the agentic loop: model, tool, result | room |
| 2 · [Put a clock on it](kit/ex2.md) | `/loop`: repetition on a clock | room |
| 3, run 1 · [Same task, two evaluators](kit/ex3.md) | `/goal`: an exit the maker does not judge | room |
| [What the next run knows](kit/memory.md) | memory: what a new run starts with | room |
| 3, run 2 and Compare · [Same task, two evaluators](kit/ex3.md) | `/fairmind-loop`: an exit that runs checks | advanced, optional |
| 4 · [Write your own review loop](kit/ex4.md) | the pull request review loop | home |
| 5 · [Close the loop on today](kit/ex5.md) | dogfooding: defects → nightly repair → merge | home |

Everything runs on `shop/`, a checkout small enough to read in five minutes.
Amounts are integer cents; `python3 -m shop` prints a receipt.

## What you need

- A **GitHub account**.
- **Access to Claude**, one of:
  - an **Anthropic API key**, from the credits your facilitator gives you; or
  - a **Claude subscription** (Pro, Max, Team or Enterprise).

  Routines (`/schedule`, the optional part of exercise 5) need a subscription login;
  with an API key only, you run the same prompts by hand, which the exercise expects.
- macOS or Linux. On Windows, use WSL; the commands below assume a POSIX shell.

## For the room · 15 minutes

Do this the day before.

1. **Make your own copy.** On GitHub, **Use this template → Create a new repository**,
   in your own account. Then clone your copy and `cd` into it.
2. **Install the tools:** [Claude Code](https://claude.com/claude-code), logged in
   with your subscription or started with `export ANTHROPIC_API_KEY=<your key>`;
   git, Python 3.10 or later, and `python3 -m pip install pytest`.
3. **Check:**

   ```bash
   ./workshop doctor      # every line under "tools" should be ✓
   ```

   Lines marked `·` belong to the sections below; they are not needed yet.

## Only for exercises 4 and 5, at home

Make the copy **public**: branch rulesets, which exercise 5 uses, need a public
repository or a paid plan. Your exercise work will be visible.

1. [GitHub CLI](https://cli.github.com) then `gh auth login`, and `jq`.
2. **Let Claude review your pull requests.** Two things, both on your copy:
   - install the [Claude GitHub App](https://github.com/apps/claude) and give it
     access to your copy: the review posts through it;
   - give the review its credential, **one** of:

     ```bash
     gh secret set ANTHROPIC_API_KEY             # the API key; paste it when asked
     # or, on a subscription:
     claude setup-token                          # prints a long-lived token
     gh secret set CLAUDE_CODE_OAUTH_TOKEN       # paste it when asked
     ```

3. **Set up:**

   ```bash
   ./workshop doctor      # the "at home" lines should be ✓
   ./workshop setup       # labels, CODEOWNERS, the main ruleset
   ```

   `setup` commits one change to your `main` (it puts your username in
   `.github/CODEOWNERS`) and pushes it, then turns on the ruleset. Run it once. The
   GitHub App `doctor` cannot see, so check that one by hand.

## Only for the advanced track, exercise 3 run 2

Install the plugin. Inside Claude Code:

```
/plugin marketplace add FairMind-Gen-AI-Studio/fairmind-plugins-public
/plugin install fairmind-coding@fairmind-plugins
```

## During the workshop

Each exercise starts from a clean branch:

```bash
./workshop reset ex2        # ex1, ex2, ex3-goal, ex3-loop, memory, ex4, ex5
```

It asks before discarding uncommitted changes, and builds the exercise on top of
your own `main`, so the pull requests you open go to your copy.

## What is in here

| Path | What |
|---|---|
| `shop/`, `tests/` | the application and its tests (`python3 -m pytest`) |
| `kit/` | one handout per exercise, `kit/memory.md` for the memory exercise, and `kit/ex5/` for the dogfooding exercise |
| `.github/workflows/ci.yml` | tests plus a clearly labelled simulated slow stage, about two minutes |
| `.github/workflows/review.yml` | Claude reviews every pull request, then labels it `reviewed` |
| `.github/ISSUE_TEMPLATE/defect.yml` | a defect with a stable key and a Reproduce block |
| `.github/CODEOWNERS`, `.github/rulesets/main.json` | the paths that stay human, and what GitHub enforces |
| `.claude/settings.json` | the commands the exercises may run without asking: tests, `git`, and the `gh` verbs that read or comment. Merging and raw API calls still ask |
| `.claude/skills/review-loop/` | the skill you write in exercise 4 |
| `scripts/fake_deploy.py` | the fake production log for exercise 2 |
| `scripts/check_percent.py` | the check the Stop hook runs in the memory exercise |
| `workshop` | `doctor`, `setup`, `reset`, `events`, `hook`, `deploy` |

## If something goes wrong

| Symptom | Cause and fix |
|---|---|
| `./workshop doctor` shows ✗ | the line after the arrow says what to install or run; `·` lines are for later |
| Claude asks permission for every test or `git` command | the folder is not trusted: run `claude` there once and answer yes |
| `./workshop` does nothing on Windows | type `py workshop …` instead |
| `claude` says Git Bash was not found (Windows) | install Git for Windows, then open a new terminal |
| `reset` says it could not start an exercise | your `main` has diverged from the template's; ask the facilitator |
| the review check is green and nothing was posted | it ran for ~15 s: the workflow file differs from `main`'s, or the app is not installed on your copy |
| the review check is red: no review credential | `gh secret set ANTHROPIC_API_KEY` on your copy (or the subscription token) |
| `/fairmind-loop` asks about a Fairmind workspace | answer **no**: the loop runs without one |
| `setup`: ruleset not created | your copy is private on a free plan; make it public |

## Two things that will bite

- **Edit `.github/workflows/review.yml` on `main` only.** The review action refuses to
  run when its workflow file differs from the default branch, and then exits green
  having reviewed nothing.
- **The routines act as you.** Anything a routine commits, opens or merges carries
  your GitHub identity. Exercise 5 is about what that means for a merge policy.
