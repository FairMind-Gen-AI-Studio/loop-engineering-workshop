# Exercise 1 · Watch the loop you already run

**10 minutes · ring 1, the agentic loop · branch: `./workshop reset ex1`**

One turn of Claude Code is many passes: the model asks for a tool, the harness runs
it, the result goes back in, until the model answers without asking for a tool.
Here you count those passes, then make the harness record them for you.

> **Commands** go in your terminal; on Windows type `py workshop` wherever this page
> says `./workshop`. **Prompts** go inside Claude Code and are the same everywhere.

## The task

`python3 -m shop` prints a receipt with amounts like `24.5 EUR`. Money should always
show two decimals: `24.50 EUR`.

## Steps

### 1 · Start clean

```bash
./workshop reset ex1
```

**Expect:** `on branch ex1-work, starting point of ex1`.

### 2 · Run the task headless, streaming every event to a file

One line: copy all of it.

```bash
claude -p "Receipts must always show two decimals, like 24.50 EUR. Fix it and add a test." --output-format stream-json --verbose --permission-mode acceptEdits > run.jsonl
```

It prints nothing for a minute or two: every event goes into `run.jsonl`.
`--verbose` is required, because in print mode stream-json refuses without it.
`--permission-mode acceptEdits` lets it edit files; the test commands it runs are
pre-approved in `.claude/settings.json`.

### 3 · Count the tool calls, and the passes

```bash
./workshop events run.jsonl
```

**Expect:** a numbered list of tool calls (`Bash`, `Read`, `Edit`…), the number of
turns the run reports, and the last message Claude wrote.

### 4 · Make the harness log every tool call

```bash
./workshop hook
```

It writes `.claude/settings.local.json` and prints it. **Read it before going on:** a
`PostToolUse` hook with matcher `*` runs a command after every tool call. The hook gets
the event as JSON on its stdin; the command appends the event's `tool_name` to
`tool-log.txt`. The file is gitignored and `./workshop reset` removes it.

Put the code back the way it was, so Claude has the same work to do again:

```bash
git stash -u
```

Run the step 2 command again, then compare what the hook saw with what the stream
recorded:

```bash
./workshop events run.jsonl
```

Open `tool-log.txt` in your editor, next to that output.

**Expect:** the same tools in the same order, **or fewer**. The hook fires on
successful calls only; a call that fails fires `PostToolUseFailure`, which this hook
does not listen to.

### 5 · Find the moment it decided to stop

```bash
claude
```

```text
Open run.jsonl. It is the event stream of a headless Claude Code run. Find the last
assistant message that contains no tool_use block and quote it. Then tell me what
decided that this was the end of the turn: a test, a hook, a limit, or the model
itself?
```

## Variant · make the hook catch the failures too

In the same session:

```text
Add a PostToolUseFailure hook to .claude/settings.local.json that runs exactly the
same command as the PostToolUse one. Then tell me why PostToolUse alone missed the
failed calls.
```

Run `git stash -u` and the step 2 command again, and read `tool-log.txt`.

## Watch for

- How many passes read and how many write.
- Nobody but the model decided the turn was over. Hold that thought: ring 3 answers it.
