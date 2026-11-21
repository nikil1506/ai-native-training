# L14: Attack an agent, then harden it (Day 13, 3 h)
Everything is simulated (`world.py`, fake secrets). Run `python starter/vulnerable-agent/run_attack.py 1` ... `5`.
Tasks: threat model (`threat-model.md`), try 3 of the 5 attacks, harden `agent.py` (least-privilege tools, URL allow-list, approvals for sensitive actions,
document text = data not instructions, tool-call log), re-run, record what remains. `breach.py` tells you objectively whether an attack worked.
Stretch: add your attacks to your L10 eval as test cases.
