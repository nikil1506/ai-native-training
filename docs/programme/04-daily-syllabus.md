## Daily syllabus

Each day: outcomes, a morning of short concept blocks followed by a guided walkthrough of the lab, and then the lab itself.

### Week 1 · Foundations and AI-native development

Day 1

### How LLMs behave, and how to talk to them
*[Foundations]*

#### By the end of the day you can

- Explain why model output varies and what drives cost and latency.
- Call a model through an API and get validated, structured output.
- Choose a model tier on evidence, not habit.

#### Morning session

|  |  |
| --- | --- |
| 30 min | How LLMs work for engineers: tokens, context window, sampling, temperature |
| 20 min | Model landscape: capability tiers, cost and latency trade-offs, when a small model is enough |
| 40 min | Prompting as engineering: roles, instructions, examples, delimiters, output schemas, prompt versioning |
| 15 min | Failure modes: hallucination, sycophancy, instruction drift, non-determinism |
| 45 min | Guided walkthrough: the facilitator live-codes the first steps of today's lab; you follow along |

#### Afternoon
- L1 · Your first API call: structured output and model trade-offs 3 h

Day 2

### Context engineering and the anatomy of an agent
*[Foundations]*

#### By the end of the day you can

- Describe what belongs in context and what degrades it.
- Explain the agent loop: model, tools, observations, memory, stop condition.
- Use a coding agent safely: modes, permissions, rules files.

#### Morning session

|  |  |
| --- | --- |
| 30 min | Context engineering: what goes in, ordering, compaction, context rot over long sessions |
| 30 min | What an agent is: workflows vs agents, the autonomy spectrum, the loop |
| 20 min | Tool calling mechanics: schemas, results, errors |
| 25 min | First look at coding agents: plan vs act modes, permissions, project rules files |
| 45 min | Guided walkthrough: the facilitator live-codes the first steps of today's lab; you follow along |

#### Afternoon
- L2 · Fix three bugs with a coding agent 1.5 h- L3 · Build an agent loop from a template 1.5 h

Day 3

### Spec-driven development
*[Track A · Building with agents]*

#### By the end of the day you can

- Turn a vague request into a spec an agent can build against.
- Write acceptance tests before implementation.
- Break work into small, independently verifiable tasks.

#### Morning session

|  |  |
| --- | --- |
| 30 min | Why specs: agent output quality tracks the clarity of intent |
| 35 min | Spec anatomy: problem, scope, what is out of scope, requirements (what it must do and how well), testable acceptance criteria, assumptions |
| 20 min | Project context files: conventions, commands, architecture notes |
| 20 min | Plan → tasks → implement; task sizing; steering and interrupting; reading diffs critically |
| 45 min | Guided walkthrough: the facilitator live-codes the first steps of today's lab; you follow along |

#### Afternoon
- L4 · From a vague request to a working feature 3 h

Day 4

### Verification, independent review and reusable agent assets
*[Track A · Building with agents]*

#### By the end of the day you can

- Explain why self-review fails and how independent review fixes it.
- Produce and triage structured review findings.
- Package team knowledge as skills, commands, hooks and subagents.

#### Morning session

|  |  |
| --- | --- |
| 30 min | Why verification is the core skill: the writer should not grade its own work |
| 30 min | Independent reviewer design: fresh context, structured findings (ID, severity, location, remedy), confidence |
| 20 min | Triage: acknowledge, dismiss with a recorded reason, escalate; quality gates and thresholds |
| 25 min | Reusable assets: skills, slash commands, hooks, subagents; guardrail hooks |
| 45 min | Guided walkthrough: the facilitator live-codes the first steps of today's lab; you follow along |

#### Afternoon
- L5 · An independent reviewer and a reusable skill 3 h

Day 5

### Agents across the SDLC, parallel work, Week-1 checkpoint
*[Track A · Building with agents]*

#### By the end of the day you can

- Apply agents to refinement, design, build, test, security review, docs and PRs.
- Run agents in parallel without collisions.
- Decide when to take the keyboard back.

#### Morning session

|  |  |
| --- | --- |
| 30 min | Agents by lifecycle stage: stories, design, code, tests, security review, docs, PR descriptions |
| 20 min | Legacy code: understanding and modernisation with agents |
| 30 min | Parallel and background agents: worktrees, branch hygiene, merge strategy |
| 25 min | Human gates and decision records; when to stop the agent and take over |
| 45 min | Guided walkthrough: the facilitator live-codes the first steps of today's lab; you follow along |

#### Afternoon
- L6 · A backlog item to a pull request, gate by gate 2 h

> **Checkpoint:** A1 · Practical checkpoint: review a flawed agent-authored PR (1 h)

### Week 2 · Building single-agent applications

Day 6

### Tool design and MCP
*[Track B · Building agentic systems]*

#### By the end of the day you can

- Design tools an agent can use reliably.
- Expose a system safely through MCP or native function calling.
- Measure the effect of tool-description quality.

#### Morning session

|  |  |
| --- | --- |
| 30 min | Function calling schemas; tool names and descriptions are prompts |
| 20 min | Tool granularity, idempotency, safe vs destructive actions, confirmation patterns |
| 20 min | Actionable errors and bounded outputs |
| 35 min | Model Context Protocol: servers, tools, resources, prompts; auth and permissions |
| 45 min | Guided walkthrough: the facilitator live-codes the first steps of today's lab; you follow along |

#### Afternoon
- L7 · Design tools for an agent, and wrap them in MCP 3 h

Day 7

### Single-agent design: planning, recovery, guardrails
*[Track B · Building agentic systems]*

#### By the end of the day you can

- Pick a planning pattern and justify it.
- Enforce limits in code, not just in the prompt.
- Handle failure and ambiguity predictably.

#### Morning session

|  |  |
| --- | --- |
| 30 min | Planning patterns: ReAct, plan-then-execute, reflection |
| 25 min | Stop conditions, step and token budgets, runaway protection |
| 25 min | Error recovery: retries, fallbacks, escalation to a human; asking clarifying questions |
| 25 min | Guardrails: input and output validation, permission tiers, short-term memory management |
| 45 min | Guided walkthrough: the facilitator live-codes the first steps of today's lab; you follow along |

#### Afternoon
- L8 · A support agent with limits that are enforced 3 h

Day 8

### Knowledge and memory: RAG
*[Track B · Building agentic systems]*

#### By the end of the day you can

- Choose between RAG, long context and other approaches.
- Build and measure a retrieval pipeline with citations.
- Enforce access control on knowledge.

#### Morning session

|  |  |
| --- | --- |
| 25 min | RAG vs long context vs fine-tuning: decision criteria |
| 35 min | Chunking, embeddings, hybrid search, reranking |
| 25 min | Grounding and citations; saying "I don't know" |
| 20 min | Memory patterns, freshness, access control on retrieved content |
| 45 min | Guided walkthrough: the facilitator live-codes the first steps of today's lab; you follow along |

#### Afternoon
- L9 · Give the agent knowledge: RAG with citations 3 h

Day 9

### Evaluation: the unit tests of agents
*[Track B · Building agentic systems]*

#### By the end of the day you can

- Build a labelled eval set and graders.
- Calibrate an LLM judge against human labels.
- Gate changes on eval results.

#### Morning session

|  |  |
| --- | --- |
| 30 min | Why evals come first: eval-driven development, offline vs online |
| 30 min | Datasets: from logs, edge cases, adversarial cases; held-out sets |
| 30 min | Graders: code-based, rubric LLM-judge, pairwise; judge biases and calibration |
| 15 min | Regression gates in CI; variance and repeated runs |
| 45 min | Guided walkthrough: the facilitator live-codes the first steps of today's lab; you follow along |

#### Afternoon
- L10 · Build an evaluation and improve by evidence 3 h

Day 10

### Observability, cost and reliability, Week-2 checkpoint
*[Track B · Building agentic systems]*

#### By the end of the day you can

- Trace a multi-step agent run end to end.
- Cut cost without losing quality.
- Diagnose failures from traces.

#### Morning session

|  |  |
| --- | --- |
| 30 min | Tracing: spans for LLM and tool calls; metrics that matter (success, latency, tokens, cost per task) |
| 30 min | Cost levers: model routing, caching, context trimming, output caps |
| 25 min | Reliability: timeouts, retries, idempotency, rate limits |
| 20 min | Debugging from traces: common root causes (bad tool description, context overflow, loops) |
| 45 min | Guided walkthrough: the facilitator live-codes the first steps of today's lab; you follow along |

#### Afternoon
- L11 · Trace it, measure it, make it cheaper 2 h

> **Checkpoint:** A2 · Practical checkpoint: diagnose failing agent runs from traces (1 h)

### Week 3 · Multi-agent systems, security and capstone

Day 11

### Multi-agent patterns
*[Track B · Building agentic systems]*

#### By the end of the day you can

- Name the main multi-agent patterns and when each fits.
- Design typed hand-offs between agents.
- Show with data when multi-agent beats a single agent, and when it does not.

#### Morning session

|  |  |
| --- | --- |
| 30 min | Why multi-agent: context isolation, specialisation, parallelism, independent review |
| 35 min | Patterns: orchestrator-worker, pipeline, fan-out/fan-in, critic loop, router and hand-off |
| 20 min | Costs: tokens, latency, compounding errors; when one agent wins |
| 20 min | Communication contracts: schemas for hand-offs; agent-to-agent protocols awareness |
| 45 min | Guided walkthrough: the facilitator live-codes the first steps of today's lab; you follow along |

#### Afternoon
- L12 · A multi-agent pipeline versus one agent 3 h

Day 12

### State, orchestration and human-in-the-loop
*[Track B · Building agentic systems]*

#### By the end of the day you can

- Make a multi-agent run durable and resumable.
- Add risk-based human approval gates.
- Scope the capstone.

#### Morning session

|  |  |
| --- | --- |
| 30 min | Durable state, checkpoints, resumability, idempotent side effects |
| 25 min | Orchestration choices: framework vs hand-rolled, trade-offs |
| 30 min | Approval gates, confidence thresholds, escalation; shared-artifact conflicts |
| 20 min | Long-running and asynchronous work |
| 45 min | Guided walkthrough: the facilitator live-codes the first steps of today's lab; you follow along |

#### Afternoon
- L13 · Make it recoverable, with a human decision point 2 h

> **Checkpoint:** Capstone scoping session (1 h): choose a scenario and plan your minimum scope

Day 13

### Security, safety and governance for agents
*[Cross-cutting · Security & governance]*

#### By the end of the day you can

- Threat-model an agent system.
- Attack and harden an agent.
- Produce audit evidence a reviewer would accept.

#### Morning session

|  |  |
| --- | --- |
| 30 min | Agent threat model: indirect prompt injection, confused deputy, exfiltration, excessive agency |
| 25 min | Least privilege, sandboxing, egress allow-lists, secrets handling |
| 25 min | Audit trails, traceability, decision records; IP, licensing and data classification |
| 25 min | Supply chain: vetting skills, MCP servers and third-party tools |
| 45 min | Guided walkthrough: the facilitator live-codes the first steps of today's lab; you follow along |

#### Afternoon
- L14 · Attack an agent, then harden it 3 h

Day 14

### Capstone build day
*[Capstone]*

#### By the end of the day you can

- Build your capstone to the brief.
- Get a design check and run a mid-day eval.

#### Morning session

|  |  |
| --- | --- |
| 30 min | Stand-up and plan for the day |
| 120 min | Build time, with a 10-minute one-to-one design check with a facilitator (10:00–12:00) |
| 30 min | Mid-day eval and trace review (13:30) |

#### Afternoon
- Capstone build

Day 15

### Capstone finish, demos and assessment
*[Capstone]*

#### By the end of the day you can

- Finish, evaluate and present the capstone.
- Reflect and plan adoption.

#### Morning session

|  |  |
| --- | --- |
| 60 min | Finish line: final eval run, threat model and cost report |
| 150 min | Individual demos: 7 minutes each plus questions (two rooms for larger cohorts) |
| 30 min | Retrospective and your 30/60/90-day adoption plan |

#### Afternoon
- Capstone build

> **Checkpoint:** Capstone assessment and retrospective
