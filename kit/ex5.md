# Exercise 5 · Close the loop on today

**30 minutes, in teams of two or three · ring 5, dogfooding · branch: your `main`**

What broke during exercises 1 to 4 becomes a queue; a routine works the queue at
night; a second routine merges what passes the policy you write. Today you build the
first two steps and write the third one down.

## Steps

1. **File two defects you hit today** with the Defect issue template. The key goes
   in the body: see [failure-shapes.md](ex5/failure-shapes.md). File one of them
   twice from a second session: the second filing must find the first and comment
   on it instead.

   ```bash
   gh issue list --state all --search "<key> in:body"
   ```

2. **Write the repair routine's prompt.** Start from
   [repair-routine.md](ex5/repair-routine.md). Run it once **by hand**, in a Claude
   Code session, before anyone schedules it: does it follow the order, or pick?
3. **Write the merge policy as rules**, in [merge-policy.md](ex5/merge-policy.md):
   what the routine checks, what GitHub enforces, which paths never merge without a
   person.
4. **Decide what stays human**, as a team, out loud. Put those paths in
   `.github/CODEOWNERS`.

If your team is behind, skip the hand run in step 2. Do not skip the merge policy.

## Scheduling it (if your plan has routines)

`/schedule` creates a routine in the cloud. The repair routine runs on a schedule of
an hour or more. The merge routine runs on the pull request label `reviewed`, which
`review.yml` adds when a review has run; the Claude GitHub App you installed for the
review is also what delivers that event to the routine. Without routines, run both prompts by hand in a session.

## Watch for

- The duplicate becomes a new issue the first time: the key was written from the
  description, not from what broke.
- Run by hand, the routine picks the easiest issue instead of the first one.
- A routine acts as **your** GitHub user. GitHub cannot tell the PR it opened from
  the merge it makes. Put the separation where GitHub can see it.
