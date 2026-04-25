# Workflow

## Intent parsing

Convert the user's request into one of these selector types:

- single commit
- multiple commits
- range `A..B`
- branch diff
- recent commits from a branch

Reject ambiguous placeholder patterns such as:

- `459591xx`
- `A~B`

## Safe workflow

1. Identify the target repository and current branch.
2. Confirm the request is about applying changes into the current branch.
3. Analyze the source selection.
4. Review the mapping output before editing files.
5. Port the equivalent behavior into the current branch.
6. Check Android follow-up items.
7. Summarize what was ported and what still needs human attention.

## What not to do automatically

- do not modify the source branch
- do not switch branches without explicit permission
- do not blindly apply `cherry-pick`
- do not overwrite current-branch custom logic when the repository clearly diverged
