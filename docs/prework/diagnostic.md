# Diagnostic (20 minutes; does not affect your result)
## Part 1: self-rating (1 = never, 2 = with help, 3 = comfortably, 4 = could teach it)
| Skill | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| Reading and writing Python | | | | |
| Git: commit, branch, merge | | | | |
| Running tests from the command line | | | | |
| Using a coding assistant (any) | | | | |
| Calling an HTTP API | | | | |
| Reading JSON | | | | |

## Part 2: three short practical questions
1. **Code reading.** What does this print, and why?
   ```python
   def f(xs, seen=[]):
       for x in xs:
           if x not in seen:
               seen.append(x)
       return seen
   print(f([1, 2]), f([2, 3]))
   ```
2. **Debugging.** `split_bill(1000, 3)` returns `[333, 333, 333]` but the total must be exactly 1000. Describe (or write) a fix.
3. **HTTP/JSON.** Using any language or tool, call `GET http://localhost:11434/api/tags` and name two things in the JSON response. (If you cannot, say what you tried.)
