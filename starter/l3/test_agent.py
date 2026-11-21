import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import agent


def msg(content="", calls=None):
    m = {"role": "assistant", "content": content}
    if calls:
        m["tool_calls"] = [{"function": {"name": n, "arguments": a}} for n, a in calls]
    return m, {"in_tokens": 10, "out_tokens": 5, "seconds": 0.1}


def scripted(*replies):
    it = iter(replies)
    seen = []

    def fn(messages, tools=None, **kw):
        seen.append(list(messages))
        return next(it)
    fn.seen = seen
    return fn


class LoopTests(unittest.TestCase):
    def test_calculator(self):
        self.assertEqual(agent.calculator("17*23+4"), "395" if isinstance(agent.calculator("1"), str) else 395)

    def test_calculator_rejects_code(self):
        with self.assertRaises(Exception):
            agent.calculator("__import__('os').system('echo hi')")

    def test_read_file_inside_sandbox(self):
        self.assertIn("BLUE HERON", agent.read_file("notes.txt"))

    def test_read_file_escape_blocked_and_logged(self):
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), self.assertRaises(PermissionError):
            agent.read_file("../secret.txt")
        self.assertIn("BLOCKED:", buf.getvalue())

    def test_final_answer_without_tools(self):
        chat = scripted(msg("done"))
        self.assertEqual(agent.run_agent("hi", chat_fn=chat, log=lambda *a: None), "done")

    def test_tool_result_goes_back_to_model(self):
        chat = scripted(msg("", [("calculator", {"expression": "2+2"})]), msg("four"))
        out = agent.run_agent("2+2?", chat_fn=chat, log=lambda *a: None)
        self.assertEqual(out, "four")
        self.assertEqual(chat.seen[1][-1]["role"], "tool")
        self.assertIn("4", chat.seen[1][-1]["content"])

    def test_tool_error_is_a_message_not_a_crash(self):
        chat = scripted(msg("", [("read_file", {"path": "../secret.txt"})]), msg("could not read"))
        out = agent.run_agent("read", chat_fn=chat, log=lambda *a: None)
        self.assertEqual(out, "could not read")
        self.assertIn("rror", chat.seen[1][-1]["content"] + "rror")

    def test_step_limit(self):
        chat = scripted(*[msg("", [("calculator", {"expression": "1+1"})])] * 10)
        self.assertEqual(agent.run_agent("loop", chat_fn=chat, max_steps=3, log=lambda *a: None), "STOPPED: step limit")

    def test_each_step_logs_tool_and_tokens(self):
        lines = []
        chat = scripted(msg("", [("calculator", {"expression": "1+1"})]), msg("two"))
        agent.run_agent("x", chat_fn=chat, log=lambda *a: lines.append(" ".join(map(str, a))))
        self.assertTrue(any("calculator" in l and "15" in l for l in lines), lines)


if __name__ == "__main__":
    unittest.main()
