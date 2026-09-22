# Exercise 2 · Put a clock on it

**15 minutes · ring 2, `/loop` · branch: `./workshop reset ex2`**

`/loop` repeats a prompt: on a fixed interval (`/loop 2m …`) or at a pace Claude picks
after each pass (`/loop …`, one minute to one hour). It has no exit condition of its
own. Run the two loops below **at the same time, in two terminals**: each one spends
most of its life waiting.

## Loop A · watch a pipeline until it is green

This branch has a bug that makes CI fail. The pipeline takes about two minutes.

```bash
git push -u origin ex2-work   # CI runs on every push
claude
```

Then, in Claude Code, write a `/loop` that watches the CI run of this branch, fixes
what fails, and **stops** when it is green. You choose the interval and the stop.
Count the passes it took.

## Loop B · a fix going to production

```bash
./workshop deploy            # one line a minute into deploy.log; a regression comes later
```

In a second Claude Code session, ask the agent to watch `deploy.log` and to **re-arm
its own loop** with longer waits after every quiet check, and to go back to the
shortest wait and tell you on any regression. In the room, minutes stand in for
hours: 1, 2, 5.

## Watch for

- The forgotten stop: the loop keeps firing after the pipeline is green, and every
  pass is paid for.
- The interval: one minute feels responsive and mostly buys identical answers.
- This loop dies with your session. Which of these watches should have been a
  routine (`/schedule`), which keeps running with the laptop closed?
