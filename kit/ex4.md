# Exercise 4 · Write your own review loop

**20 minutes · ring 4, the review loop · branch: `./workshop reset ex4`**

Opening a pull request starts `.github/workflows/review.yml`: Claude reads the diff,
posts findings on specific lines and one summary comment. A PR is delivered when that
review has run, been read in both places it writes, and every finding has a fix or a
reply.

## Steps

1. **Fill in the skill skeleton** at `.claude/skills/review-loop/SKILL.md`. Four
   sections are stubbed: when to run, how to wait, where to read, what to answer.
2. **Open a PR and invoke the skill.**

   ```bash
   git push -u origin ex4-work
   gh pr create --fill
   claude            # then: use the review-loop skill on this PR
   ```

   Let the skill do the waiting, not you.
3. **Answer every finding.** Fix it, or reply on the PR saying why not. Push, and let
   the loop run the review again.
4. **Stop only on nothing unanswered.** Then look at the run's duration in the
   Actions tab.

One full review round is the exercise. A second round is the overflow: a review takes
one to eight minutes.

## Useful commands

```bash
gh run watch "$(gh run list --workflow 'Claude review' --branch ex4-work --limit 1 --json databaseId -q '.[0].databaseId')"
gh pr view <n> --comments                               # the summary, not the inline findings
gh api repos/{owner}/{repo}/pulls/<n>/comments \
  --jq '.[] | "\(.path):\(.line // .original_line)\n\(.body)\n"'   # the inline findings
```

## Watch for

- Reading only the summary and missing the inline findings.
- Applying a finding without reproducing it first. The reviewer reads the code; it
  did not run it.
- A review that finished in about fifteen seconds probably reviewed nothing: read its log.
