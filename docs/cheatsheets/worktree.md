# Worktree cheat sheet (L6: two agents at the same time)
A git *worktree* is a second working folder on a different branch, sharing the same repository. Two agents can edit in parallel without touching each other's files.
```
git worktree add ../orders-task-a -b task-a        # new folder + branch for agent A
git worktree add ../orders-task-b -b task-b        # new folder + branch for agent B
# start one agent in each folder, give each a DIFFERENT file or folder to work on
git worktree list
# when both are done and reviewed:
git switch main
git merge task-a
git merge task-b          # a conflict here is normal: resolve it, note it in your decision log
git worktree remove ../orders-task-a
git worktree remove ../orders-task-b
git branch -d task-a task-b
```
Rules: one task per branch; commit small; never let two agents edit the same file; run the tests after each merge.
