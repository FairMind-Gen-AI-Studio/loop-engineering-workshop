# Exercise 1 · Watch the loop you already run

**10 minutes · ring 1, the agentic loop · branch: `./workshop reset ex1`**

One turn of Claude Code is many passes: the model asks for a tool, the harness runs
it, the result goes back in, until the model answers without asking for a tool.
Here you count those passes, then make the harness record them for you.

## The task

`python3 -m shop` prints a receipt with amounts like `24.5 EUR`. Money should always
show two decimals: `24.50 EUR`.

## Steps

1. **Run the task headless, streaming every event to a file.**

   ```bash
   claude -p "Receipts must always show two decimals, like 24.50 EUR. Fix it and add a test." \
     --output-format stream-json --verbose > run.jsonl
   ```

   `--verbose` is required: in print mode, stream-json refuses without it.

2. **Count the tool calls, and the passes.**

   ```bash
   jq -r 'select(.type=="assistant") | .message.content[] | select(.type=="tool_use") | .name' run.jsonl
   jq 'select(.type=="result") | .num_turns' run.jsonl
   ```

3. **Make the harness log every tool call.** Create `.claude/settings.json`:

   ```json
   {"hooks": {"PostToolUse": [{"matcher": "*", "hooks": [
     {"type": "command", "command": "jq -r '.tool_name' >> tool-log.txt"}]}]}}
   ```

   Undo the fix (`git checkout shop/`), run step 1 again, and read `tool-log.txt`.
   The hook gets each event as JSON on stdin. It fires on successful calls only;
   failed ones fire `PostToolUseFailure`.

4. **Find the moment it decided to stop.** The last assistant message with no tool
   call. Who chose it?

## Watch for

- How many passes read and how many write.
- Nobody but the model decided the turn was over. Hold that thought: ring 3 answers it.
