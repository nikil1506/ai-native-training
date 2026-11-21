# Lab grading sheets

A lab counts when **all** acceptance criteria are met; facilitators may accept a documented, reasoned exception. Labs are 40% of the final result (14 labs).

## L1 · Your first API call: structured output and model trade-offs

**Deliverables**

- Your script and scoring output
- `results.md` with the comparison table and three sentences of conclusions
- At least two prompt versions in git history

**Acceptance criteria**

- [ ] Output passes the validator on all 20 tickets
- [ ] Best prompt reaches the accuracy target set by the facilitator
- [ ] Table shows cost per 1,000 tickets for both model sizes
- [ ] No API key committed

Exception accepted? ☐ yes (reason: ______________)   Result: ☐ met  ☐ not met

## L2 · Fix three bugs with a coding agent

**Deliverables**

- Fixed repository
- `steering-log.md`

**Acceptance criteria**

- [ ] All tests pass
- [ ] You wrote a review comment for each diff
- [ ] At least one agent mistake caught and recorded
- [ ] No unrelated files changed

Exception accepted? ☐ yes (reason: ______________)   Result: ☐ met  ☐ not met

## L3 · Build an agent loop from a template

**Deliverables**

- Completed `agent.py`
- Run logs for the five tasks

**Acceptance criteria**

- [ ] Solves at least three of five tasks
- [ ] Stops at the step limit on the impossible task
- [ ] A `../` path attempt is blocked and logged
- [ ] Each step prints tokens and the tool name

Exception accepted? ☐ yes (reason: ______________)   Result: ☐ met  ☐ not met

## L4 · From a vague request to a working feature

**Deliverables**

- `spec.md`, `plan.md`, `deviations.md`
- Acceptance tests
- One commit per task

**Acceptance criteria**

- [ ] At least four unclear points resolved and written down
- [ ] Every acceptance criterion has a test
- [ ] All tests pass
- [ ] Deviations written down, or "none" with a reason

Exception accepted? ☐ yes (reason: ______________)   Result: ☐ met  ☐ not met

## L5 · An independent reviewer and a reusable skill

**Deliverables**

- Skill folder with README
- `findings.md` with your decisions
- Hook or script
- Notes on rounds one and two

**Acceptance criteria**

- [ ] The reviewer runs in a fresh context
- [ ] Findings use the fixed format
- [ ] At least one finding dismissed with a good reason
- [ ] Round two shows the reviewer re-checking the fixes
- [ ] The hook blocks a commit when a test fails
- [ ] The skill ran in `sample-repo-2` from your README alone

Exception accepted? ☐ yes (reason: ______________)   Result: ☐ met  ☐ not met

## L6 · A backlog item to a pull request, gate by gate

**Deliverables**

- `artifacts/` folder with six files
- Merged branch
- Decision log

**Acceptance criteria**

- [ ] Six stage files exist
- [ ] At least one gate decision is "no-go / rework", with a reason
- [ ] The two branches merged, with any conflicts noted
- [ ] The PR description links criteria to tests

Exception accepted? ☐ yes (reason: ______________)   Result: ☐ met  ☐ not met

## L7 · Design tools for an agent, and wrap them in MCP

**Deliverables**

- Your tool code and MCP server
- `tool-design.md`
- Before/after table

**Acceptance criteria**

- [ ] The destructive action needs confirmation, or is left out with a reason
- [ ] At least five of eight tasks succeed
- [ ] The before/after table shows a difference and you explain it
- [ ] Errors include a hint

Exception accepted? ☐ yes (reason: ______________)   Result: ☐ met  ☐ not met

## L8 · A support agent with limits that are enforced

**Deliverables**

- Agent code
- `guardrails.md`
- Failure-injection run report

**Acceptance criteria**

- [ ] No run goes past the step or token limit in 10 runs
- [ ] No refund is ever carried out without escalation
- [ ] Every injected failure ends in a recovery or an escalation
- [ ] Missing order numbers lead to a question

Exception accepted? ☐ yes (reason: ______________)   Result: ☐ met  ☐ not met

## L9 · Give the agent knowledge: RAG with citations

**Deliverables**

- Your pipeline code
- `retrieval-report.md`

**Acceptance criteria**

- [ ] hit@5 reported for two chunk sizes
- [ ] Every answer cites sources that were retrieved
- [ ] At least three of four unanswerable questions handled correctly
- [ ] The access test passes

Exception accepted? ☐ yes (reason: ______________)   Result: ☐ met  ☐ not met

## L10 · Build an evaluation and improve by evidence

**Deliverables**

- Your `eval/` folder
- Baseline and after reports
- Threshold script

**Acceptance criteria**

- [ ] At least 20 cases, each with a category
- [ ] Judge agrees with your labels on at least 4 of 6, or you explain the gap
- [ ] Two improvements linked to specific failures
- [ ] The threshold script fails on a deliberately worse version

Exception accepted? ☐ yes (reason: ______________)   Result: ☐ met  ☐ not met

## L11 · Trace it, measure it, make it cheaper

**Deliverables**

- Tracing code
- `report.md` with before and after

**Acceptance criteria**

- [ ] Every run produces a complete trace
- [ ] Cost per task drops by at least 20% with quality within the tolerance you were given
- [ ] The report names the top three costs

Exception accepted? ☐ yes (reason: ______________)   Result: ☐ met  ☐ not met

## L12 · A multi-agent pipeline versus one agent

**Deliverables**

- Your system code
- `comparison.md`

**Acceptance criteria**

- [ ] All hand-offs are checked against a schema
- [ ] The reviewer catches at least one planted mistake
- [ ] The comparison covers quality, cost and time
- [ ] Your conclusion is backed by the numbers

Exception accepted? ☐ yes (reason: ______________)   Result: ☐ met  ☐ not met

## L13 · Make it recoverable, with a human decision point

**Deliverables**

- Your orchestrator code
- A short crash-and-resume demonstration
- Decision log

**Acceptance criteria**

- [ ] Resuming does not repeat finished work
- [ ] The approval step blocks when findings are open
- [ ] The decision log is complete

Exception accepted? ☐ yes (reason: ______________)   Result: ☐ met  ☐ not met

## L14 · Attack an agent, then harden it

**Deliverables**

- `threat-model.md`
- Attack notes
- Hardened code
- Sample tool-call log

**Acceptance criteria**

- [ ] Three attacks worked before hardening and are recorded
- [ ] The same attacks fail afterwards, or the remaining risk is written down
- [ ] Sensitive actions need approval
- [ ] Secrets never appear in prompts or logs

Exception accepted? ☐ yes (reason: ______________)   Result: ☐ met  ☐ not met
