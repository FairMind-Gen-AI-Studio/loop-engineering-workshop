# Exercise 3 · Same task, two evaluators

**25 minutes · ring 3, `/goal` and `/fairmind-loop`**

One task, run twice. First the exit condition is judged by a model reading the
session (`/goal`). Then it is judged by checks that run (`/fairmind-loop`). Compare
what each one accepted as done.

## Run 1 · `/goal`

```bash
./workshop reset ex3-goal
claude
```

Read `TICKET.md`, then write one `/goal` condition taken from the ticket, for example:

```
/goal discount codes work as TICKET.md describes and python3 -m pytest passes
```

Note what it accepted as done. Keep the branch: `git log -1` shows its commit.

## Run 2 · `/fairmind-loop`

```bash
./workshop reset ex3-loop        # same code, same ticket, plus a prepared contract
claude
```

```
/fairmind-loop DISC-1
```

The brief (`.fairmind/design/DISC-1.md`) and the checks (`.fairmind/gate/`) are
prepared. Tell it to use them, not to write new ones. When it asks whether you have a
Fairmind workspace, answer **no**: the loop runs on git, python3 and bash alone.

1. **Read the brief before the checks.** The brief says what to build; the checks
   only say what is measured.
2. **Watch admission quarantine a check.** One is badly written on purpose. Do not
   fix it: read why it was refused.
3. **Confirm a small budget: six iterations.**
4. **Let the gate refuse at least once**, then stop at the first green evaluation.
   Reaching `passed_pending_human` takes three greens and a completeness review:
   that is the overflow, not the exercise.

## Compare

What did the goal accept that the gate refused? The ticket hides one edge case.
Which run caught it?

## Watch for

- The reset between the runs is not optional: on code `/goal` already changed, every
  check passes before the loop starts, admission quarantines all of them, and the
  loop refuses to arm.
- Editing a check instead of the code: admission refuses that too.
