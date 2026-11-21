import importlib.util
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location("support_agent_mod", HERE / "agent.py")
agent = importlib.util.module_from_spec(spec); sys.modules[spec.name] = agent; spec.loader.exec_module(agent)
tools = agent.tools_mod


def msg(content="", calls=None, tokens=10):
    m = {"role": "assistant", "content": content}
    if calls:
        m["tool_calls"] = [{"function": {"name": n, "arguments": a}} for n, a in calls]
    return m, {"in_tokens": tokens, "out_tokens": 0, "seconds": 0.0}


def scripted(*replies):
    it = iter(replies); seen = []
    def fn(messages, tools=None, model=None, **kw):
        seen.append(messages)
        return next(it, msg("done"))
    fn.seen = seen
    return fn


class Guardrails(unittest.TestCase):
    def setUp(self):
        tools.reset()

    def test_step_limit_enforced_and_escalates(self):
        chat = scripted(*[msg("", [("search_kb", {"query": "shipping"})])] * 20)
        o = agent.run("How long does shipping take?", chat_fn=chat, log=lambda *a: None)
        self.assertEqual(o.stopped, "step_limit")
        self.assertLessEqual(o.steps, agent.MAX_STEPS)
        self.assertTrue(o.escalated)

    def test_token_budget_enforced(self):
        chat = scripted(*[msg("", [("search_kb", {"query": "shipping"})], tokens=agent.TOKEN_BUDGET)] * 5)
        o = agent.run("How long does shipping take?", chat_fn=chat, log=lambda *a: None)
        self.assertEqual(o.stopped, "token_budget")

    def test_refund_request_never_reaches_model_or_tool(self):
        chat = scripted(msg("I will refund you", [("process_refund", {"order_id": "10001"})]))
        o = agent.run("I want a refund for order 10001", chat_fn=chat, log=lambda *a: None)
        self.assertTrue(o.escalated)
        self.assertEqual(tools.REFUNDS, [])

    def test_model_tries_refund_tool_anyway(self):
        chat = scripted(msg("", [("process_refund", {"order_id": "10001"})]), msg("ok"))
        agent.run("Where is order 10001?", chat_fn=chat, log=lambda *a: None)
        self.assertEqual(tools.REFUNDS, [], "process_refund must never execute")

    def test_missing_order_number_asks_question(self):
        chat = scripted(msg("guess: 12345"))
        o = agent.run("Where is my package?", chat_fn=chat, log=lambda *a: None)
        self.assertTrue(o.asked_question)
        self.assertEqual(chat.seen, [], "should not call the model at all")

    def test_plan_is_written_and_logged(self):
        lines = []
        chat = scripted(msg("Plan: look up the order, then report status."), msg("Order 10001 is shipped."))
        o = agent.run("Where is order 10001?", chat_fn=chat, log=lambda *a: lines.append(" ".join(map(str, a))))
        self.assertIn("Plan", o.plan)
        self.assertTrue(any("plan" in l.lower() for l in lines))

    def test_tool_failing_twice_escalates(self):
        calls = [("lookup_order", {"order_id": "10001"})]
        import os
        os.environ["INJECT_FAILURES"] = "1"
        try:
            failing = agent.failure
            failing._rng.seed(0)
            orig = failing.inject
            failing.inject = lambda name, fn: (lambda **kw: (_ for _ in ()).throw(TimeoutError("x")))
            chat = scripted(msg("Plan: look up."), msg("", calls), msg("", calls), msg("", calls), msg("cannot"))
            o = agent.run("Where is order 10001?", chat_fn=chat, log=lambda *a: None)
        finally:
            failing.inject = orig
            os.environ.pop("INJECT_FAILURES", None)
        self.assertTrue(o.escalated)


if __name__ == "__main__":
    unittest.main()
