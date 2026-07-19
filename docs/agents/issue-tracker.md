# Issue tracker: GitHub

Issues and planning artifacts for this fork live in `suainam/dailycheckin` GitHub Issues. Use the `gh` CLI from this clone so the `origin` remote selects the repository.

## Conventions

- Create: `gh issue create --title "..." --body "..."`
- Read: `gh issue view <number> --comments`
- List: `gh issue list --state open --json number,title,body,labels,assignees`
- Comment: `gh issue comment <number> --body "..."`
- Label: `gh issue edit <number> --add-label "..."` or `--remove-label "..."`
- Close: `gh issue close <number> --comment "..."`

Issue titles should describe an outcome or decision. Never include credentials, cookies, raw provider responses, or workflow logs containing account data.

Pull requests are not an implicit triage queue. Inspect or modify a PR only when the user places it in scope.

## Wayfinding operations

Wayfinding is optional and used only for work too uncertain or large for one implementation session.

- Map: one issue labelled `wayfinder:map` containing Destination, Notes, Decisions so far, Not yet specified, and Out of scope.
- Ticket: a child issue labelled `wayfinder:research`, `wayfinder:prototype`, `wayfinder:grilling`, or `wayfinder:task`.
- Child relationship: prefer GitHub sub-issues. If unavailable, add the child to the map task list and put `Part of #<map>` at the top of the child.
- Blocking: prefer GitHub native issue dependencies. If unavailable, use `Blocked by: #<number>` at the top of the blocked ticket.
- Claim: assign the ticket to the driving developer before work begins.
- Frontier: open, unblocked, unassigned children in map order.
- Resolve: post the decision as a comment, close the ticket, then add a one-line linked gist to the map's Decisions so far.

Do not create a map for a small, already understood change. A cancelled destination does not create placeholder issues.
