# Exercise 2 · Put a clock on it

**15 minutes · ring 2, `/loop` · branch: `./workshop reset ex2`**

`/loop` repeats a prompt: on a fixed interval (`/loop 2m …`) or at a pace Claude picks
after each iteration (`/loop …`, one minute to one hour). A loop on a fixed interval
never ends by itself. A self-paced loop ends when Claude decides the job is done, **if
your prompt says what done means.** Claude's documentation calls each repetition an
**iteration**, and one iteration holds the many turns you counted in exercise 1.

You run two loops **at the same time**, each in its own terminal. Each one spends
most of its life waiting.

> **Commands** go in your terminal; on Windows type `py workshop` wherever this page
> says `./workshop`. **Prompts** go inside Claude Code and are the same everywhere.

**Keep a note**, outside this folder, of anything that breaks or surprises you:
exercise 5 starts from that list.

## Loop A · watch a pipeline until it is green

This branch has a bug that makes CI fail. The pipeline takes about two minutes.

**Terminal 1:**

```bash
./workshop reset ex2
git push -u origin ex2-work
claude
```

The push starts CI. Paste this in Claude Code:

```text
/loop Watch the CI run of branch ex2-work. Each iteration, run:
gh run list --branch ex2-work --workflow CI --limit 1
- Still queued or in progress: say "waiting", nothing else, and check again in about
  two minutes.
- Failed: read why with gh run view <run id> --log-failed, fix the cause in the code,
  run the tests, then commit and push. The push starts a new CI run.
- Succeeded, on the commit that is at the tip of ex2-work: tell me how many iterations
  this loop took and what you fixed, then stop the loop. Do not check again.
```

**Expect:** a few `waiting` iterations, one fix and push, more `waiting`, then a
summary and the loop ends. Count the iterations.

### Variant · forget the stop

Once Loop A has ended, try the same watch with a fixed interval and **no stop rule**:

```text
/loop 1m Run gh run list --branch ex2-work --workflow CI --limit 1 and tell me the
status of the latest run.
```

Let it fire three times after the run is green. Every iteration costs tokens and tells
you the same thing. Then stop it. A fixed-interval loop does not stop itself, and
`Esc` only stops self-paced ones:

```text
What scheduled tasks do I have? Cancel the CI status one.
```

## Loop B · a fix going to production

**Terminal 2:** start the fake production log. It writes four lines a minute, and a
regression comes after a few minutes. Leave this terminal running.

```bash
./workshop deploy
```

**Terminal 3:**

```bash
claude
```

```text
/loop Watch deploy.log: a fix just went to production, and the log gets four lines
per minute. Each iteration, read only the lines added since the previous one.
- Every new line says status=ok: say "quiet", then wait longer than last time before
  the next check: 1 minute, then 2, then 3, then stay at 3.
- Any new line says status=degraded: tell me the minute and the error_rate, and go
  back to checking every minute.
- Once the log has reached minute=8: summarise what you saw and stop the loop.
```

In the room, minutes stand in for hours.

**Expect:** the waits get longer while the log is quiet, drop back to one minute
soon after `minute=3`, and get longer again once the regression is over.

### Variant · let the log tell you

Loop B goes back to the log to ask whether anything changed. The Monitor tool turns
that around: Claude writes a small script, runs it in the background, and each line
the script prints reaches the session as it is written. You keep working, and Claude
interjects when one arrives. On Windows, Monitor needs Git Bash.

Once Loop B has stopped, start a second log, three times faster: twelve minutes of log
in four.

**Terminal 2:**

```bash
./workshop deploy --out monitor.log --interval 5
```

**Terminal 3**, straight away:

```text
Use the Monitor tool, not /loop, to watch monitor.log. Tell me each time a new line
says status=degraded, with its minute and error_rate. When the log reaches
minute=11.75, summarise what you saw and stop watching.
```

**Expect:** ten notifications, `minute=3` to `minute=5.25`, each a few seconds after
its line was written, and nothing in between: no prompt runs while the log is quiet.
Loop B found the same regression up to a minute late.

Then look at what Claude wrote:

```text
Show me the exact command your monitor runs.
```

If it matches only `status=degraded`, the line `minute=11.75` never reaches Claude:
the log ends and the monitor stays silent until its deadline (5 minutes unless Claude
set a longer one), exactly as it would while waiting for more.

**Break it.** Ask Claude to start the same watch again, then run the deploy command
again and press `Ctrl-C` in terminal 2 at about `minute=4`. The log stops in the
middle of the regression. What does the monitor say? Then:

```text
Re-arm the monitor so it also tells me when monitor.log has not grown for 30 seconds.
```

## Watch for

- The forgotten stop: the loop keeps firing after the pipeline is green, and every
  iteration is paid for.
- The interval: one minute feels responsive and mostly buys identical answers.
- Silence is not success: a monitor that matches only the line you hope for stays quiet
  through a crash, and quiet looks exactly like still running.
- Monitor may have shown up in Loop B already: when you give `/loop` no interval,
  Claude may use Monitor instead of re-running the prompt.
- These loops die with your session. Which of these watches should have been a
  routine (`/schedule`), which keeps running with the laptop closed?
