# Primer: LLMs in plain language (about 10 pages' worth, condensed)
**1. What a model does.** A large language model reads text as *tokens* (word pieces) and predicts the next token, over and over. It does not look facts up; it generates plausible continuations. That is why it can be fluent and wrong (*hallucination*).
**2. Why answers vary.** Output is *sampled*. *Temperature* controls how much randomness: 0 is steadier, higher is more varied. Even at 0, treat output as non-deterministic across versions and settings.
**3. Context window.** The model only sees what is in the current prompt: instructions, conversation, documents, tool results. Everything costs tokens (money and time) and a very long context makes the model worse at using it (*context rot*). Good engineers decide deliberately what goes in.
**4. Prompting is engineering.** Be specific, give the output format, give examples, put untrusted text in delimiters, and version your prompts like code. Measure changes; do not judge by eye.
**5. Structured output.** Ask for JSON that matches a schema, then *validate in code*. A validated retry is cheaper than a human cleaning up.
**6. Tools and agents.** A *tool call* lets the model ask your code to do something (look up an order). An *agent* is a model in a loop: decide, use a tool, read the result, repeat, until done or stopped. Limits (steps, tokens, permissions) belong in code, not just in the prompt.
**7. Checking the work.** The writer should not grade its own work. Use specs and tests, and an *independent reviewer* with a fresh context. Evals are the unit tests of agents.
**8. Knowledge (RAG).** Find relevant documents first, then answer from them with citations; say "I don't know" when nothing relevant is found; enforce who may see what.
**9. Security.** Text from documents, emails and web pages is *data*, not instructions (*prompt injection*). Give tools the least access they need; ask a human before sensitive actions; never put secrets in prompts; keep an audit log.
**10. Keep a human in charge** of decisions and exceptions, and know when an agent is the wrong tool (a plain script or a person is often better).
