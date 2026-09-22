---
name: review-loop
description: Close the review loop on a pull request — wait for the Claude review, read both places it writes, answer every finding. Use right after opening a PR and after every push to it.
---

# Review loop

A pull request is delivered when its review has run, been read, and every finding
has a fix or a reply.

## When to run

Right after `gh pr create`, and again after every push to the pull request: each push
cancels the review in flight and starts a new one, so the last read does not cover the
new commits.

## How to wait

Do not refresh a page. Watch the run:

```bash
gh run watch "$(gh run list --workflow 'Claude review' --branch "$(git branch --show-current)" \
  --limit 1 --json databaseId -q '.[0].databaseId')"
```

A real review takes one to eight minutes. A run that finished in about fifteen seconds
probably reviewed nothing: open its log before believing a green check.

## Where to read

Both, every time:

```bash
gh pr view <n> --comments                                    # the summary and verdict
gh api repos/{owner}/{repo}/pulls/<n>/comments \
  --jq '.[] | "\(.path):\(.line // .original_line)\n\(.body)\n"'   # inline findings
```

`.line` is null when a later push moved the line a comment was anchored to; the
`// .original_line` fallback keeps those findings visible.

## What to answer

For each finding: reproduce it first, because the reviewer read the code and did not
run it. If it is real, fix it and say what changed. If it is not, reply on the PR
saying why. A finding with neither reads as one nobody looked at. The loop ends when a
review of the latest push leaves nothing unanswered.
