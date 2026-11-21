# Acceptable use and data handling (read before Day 1)
- **No real customer data** in any lab, prompt, trace or log. Use the synthetic data provided.
- **No secrets in prompts or code.** Keys come from environment variables; never commit them. `make doctor` checks for committed keys.
- **No production credentials** or access to production systems.
- Use the shared model gateway with your own `PARTICIPANT` name; it enforces a per-participant spending cap. Do not share your name/key with others.
- Agents act on your machine: read how your coding agent's permissions work before using it (L2), and keep it in the project folder.
- Do not paste proprietary code from your employer into any tool not approved for it.
- Report accidental exposure of data or a secret to a facilitator immediately.
