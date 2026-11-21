## Glossary

Plain-language definitions of the terms you will meet. Keep this open during the first week.

- **Token**: A small piece of text (part of a word) that a model reads and writes. Cost and limits are counted in tokens.

- **Context window**: The amount of text a model can consider at once: your instructions, the conversation, and any documents.

- **Prompt**: The instructions and information you give a model.

- **Temperature**: A setting that controls how much a model's answers vary. Low is steadier; high is more varied.

- **Hallucination**: When a model states something that sounds right but is wrong or made up.

- **Structured output**: Asking the model to answer in a fixed format, such as JSON, so code can use the result.

- **Tool / function calling**: Letting a model ask your code to do something, like look up an order, and use the result.

- **Agent**: A model running in a loop: it decides what to do, uses tools, looks at the result, and repeats until done.

- **Coding agent**: An agent that reads and edits your code and runs commands, for example to fix a bug.

- **Spec**: A written description of what to build, including how you will know it works.

- **Acceptance criterion**: A statement a test can check to confirm a feature works.

- **Independent reviewer**: A second agent with a fresh context that checks the first one's work.

- **Finding**: A problem a reviewer reports, with severity, location and a suggested fix.

- **Skill / hook**: A reusable instruction set for an agent (skill), and an automatic check that runs at a set point, such as before a commit (hook).

- **MCP**: Model Context Protocol: a standard way to offer tools and data to agents.

- **RAG**: Retrieval-augmented generation: find relevant documents first, then let the model answer using them.

- **Embedding**: A list of numbers that represents the meaning of text, used to find similar text.

- **Eval**: A repeatable test that scores how well an agent does on a set of cases.

- **LLM judge**: A model used to grade another model's answers against a rubric.

- **Guardrail**: A limit or check that stops an agent from doing something unsafe or wasteful.

- **Prompt injection**: An attack where text in a document or message tricks the model into following the attacker's instructions.

- **Multi-agent system**: Several agents with different roles working together, often with an orchestrator.

- **Orchestrator**: The part that decides which agent does what, and passes results between them.

- **Hand-off**: The message one agent passes to another.

- **Trace**: A record of every model call and tool call in a run, used to find out what happened.

- **Idempotent**: Safe to repeat: doing it twice has the same effect as doing it once.
