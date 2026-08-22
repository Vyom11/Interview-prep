# GitHub and Git Interview Prep

## Fresher level

1. **What problem does version control solve in a team project?**  
   Version control keeps a history of changes, helps multiple people work on the same codebase without overwriting each other, and makes it possible to roll back mistakes. In practice, it is what lets a team collaborate safely instead of editing files manually and losing context.  
   ```bash
   git init
   git status
   git add .
   git commit -m "Initial commit"
   ```  
 [docs.github](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/merging-a-pull-request)

2. **What is the difference between Git and GitHub in a real project?**  
   Git is the tool that tracks changes locally, while GitHub is where the team shares code, opens pull requests, reviews changes, and automates checks. A good interview answer is to emphasize that Git works even offline, but GitHub adds collaboration and governance on top of it.  
   ```bash
   git clone <repo-url>
   git remote -v
   git push origin main
   ```  
 [docs.github](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts/resolving-a-merge-conflict-using-the-command-line)

3. **How do you start working on a new feature safely?**  
   You create a new branch so the feature does not affect the stable branch until it is ready. This avoids accidental breakage on `main` and makes reviews much easier.  
   ```bash
   git checkout -b feature/login-form
   git add .
   git commit -m "Add login form"
   git push -u origin feature/login-form
   ```  
 [docs.github](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/merging-a-pull-request)

4. **A junior developer asks why they should not commit directly to `main`. What do you say?**  
   Direct commits make it easy to introduce bugs into the stable branch and harder to review or revert changes later. Branches and pull requests create a controlled path where tests and reviews can catch problems before production.  
   ```bash
   git checkout -b feature/new-api
   ```  
 [docs.github](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts/resolving-a-merge-conflict-using-the-command-line)

5. **What should you do if you accidentally changed the wrong file?**  
   First check the status, then discard or stash the incorrect change depending on whether you want to keep it for later. In a real team, the important thing is to correct the mistake before it reaches the shared branch.  
   ```bash
   git status
   git restore <file>
   git stash
   ```  
 [docs.github](https://docs.github.com/articles/resolving-a-merge-conflict-using-the-command-line)

## Intermediate level

6. **How do you keep your local branch updated with the latest remote changes?**  
   Fetch first so you can inspect what changed, then merge or rebase depending on your team’s workflow. This is the safest way to avoid surprise conflicts during a big integration step.  
   ```bash
   git fetch origin
   git pull --rebase origin main
   ```  
 [atlassian](https://www.atlassian.com/git/tutorials/merging-vs-rebasing)

7. **What is a merge conflict, and how do you usually solve it?**  
   A merge conflict happens when two branches change the same lines or related parts of a file. The right way to handle it is to open the conflicted file, decide what the final code should be, resolve it manually, and then run tests before pushing.  
   ```bash
   git status
   git merge origin/main
   git add <resolved-file>
   git commit
   ```  
 [docs.github](https://docs.github.com/articles/resolving-a-merge-conflict-using-the-command-line)

8. **When should you use rebase instead of merge?**  
   Rebase is useful when you want a linear history and you are working on a private feature branch. Merge is better when you want to preserve the exact history of branch integration or when multiple people are already using the branch.  
   ```bash
   git fetch origin
   git rebase origin/main
   ```  
 [youtube](https://www.youtube.com/watch?v=0chZFIZLR_0)

9. **How do you review changes in a pull request effectively?**  
   Focus first on correctness, then on maintainability, edge cases, and test coverage. A reviewer should try to understand the business logic and whether the code is easy to support later, not just whether it “looks fine.”  
   ```bash
   git diff main...feature-branch
   git log --oneline --graph --decorate
   ```  
 [docs.github](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/merging-a-pull-request)

10. **How do you undo a bad commit that is already local?**  
    If the commit has not been pushed, you can reset or amend it depending on whether you want to keep the changes. In interviews, it is good to mention that the safe choice depends on whether the history is already shared.  
    ```bash
    git reset --soft HEAD~1
    git commit --amend
    ```  
 [docs.github](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts/resolving-a-merge-conflict-using-the-command-line)

11. **What is the practical difference between `git reset` and `git revert`?**  
    `reset` changes local history and is usually best for unpushed work, while `revert` creates a new commit that undoes a previous commit and is safer for shared branches. In real teams, `revert` is usually preferred once code is already public or deployed.  
    ```bash
    git reset --hard HEAD~1
    git revert <commit-id>
    ```  
 [docs.github](https://docs.github.com/articles/resolving-a-merge-conflict-using-the-command-line)

12. **What is the best way to explain a commit message in an interview?**  
    A commit message should describe the intent of the change, not just the file touched. Clear messages help debugging, code review, and release tracking later.  
    ```bash
    git commit -m "Fix token refresh on expired sessions"
    ```  
 [docs.github](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/merging-a-pull-request)

## GitFlow level

13. **What is GitFlow, and why do some teams prefer it?**  
   GitFlow is a branching strategy that separates work into `feature`, `develop`, `release`, and `hotfix` branches. It is useful when releases are planned and teams want a clear process for development, stabilization, and emergency fixes. [docs.aws.amazon](https://docs.aws.amazon.com/prescriptive-guidance/latest/choosing-git-branch-approach/branches-in-a-gitflow-strategy.html)
   ```bash
   git flow init
   ```

14. **How does a feature branch work in GitFlow?**  
    You start a feature branch from `develop`, complete the work there, and then finish it back into `develop`. This keeps incomplete work isolated and keeps the integration branch cleaner.  
    ```bash
    git flow feature start user-auth
    git flow feature finish user-auth
    ```  
 [danielkummer.github](https://danielkummer.github.io/git-flow-cheatsheet/)

15. **What is the role of the `develop` branch in GitFlow?**  
    `develop` acts as the integration branch where completed features are gathered and tested before release. It gives teams a stable place to consolidate work without touching production code directly. [docs.aws.amazon](https://docs.aws.amazon.com/prescriptive-guidance/latest/choosing-git-branch-approach/branches-in-a-gitflow-strategy.html)
    ```bash
    git checkout develop
    git pull origin develop
    ```

16. **How do release branches help in a real project?**  
    Release branches let a team freeze new feature work while focusing on stabilization, versioning, and final bug fixes. This is especially useful when a product needs controlled release management.  
    ```bash
    git flow release start 1.4.0
    git flow release finish 1.4.0
    ```  
 [theserverside](https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/Gitflow-release-branch-process-start-finish)

17. **How is a hotfix handled in GitFlow?**  
    A hotfix branch is created from `main` when production needs an urgent fix. After the fix is merged, it should be brought back into `develop` so the patch is not lost in future releases. [danielkummer.github](https://danielkummer.github.io/git-flow-cheatsheet/)
    ```bash
    git flow hotfix start 1.4.1
    git flow hotfix finish 1.4.1
    ```

18. **When is GitFlow a bad fit?**  
    GitFlow can become heavy if the team deploys frequently, ships small incremental changes, or prefers trunk-based development. In such cases, the process overhead may slow the team more than it helps. [docs.aws.amazon](https://docs.aws.amazon.com/prescriptive-guidance/latest/choosing-git-branch-approach/branches-in-a-gitflow-strategy.html)
    ```bash
    git branch
    git log --graph --oneline --decorate
    ```

## Advanced level

19. **How do you handle a protected branch that blocks direct merges?**  
    You usually resolve the conflict on a separate branch, run tests, and then open a new pull request into the protected branch. This keeps the branch rules intact while still allowing the conflict to be fixed. [stackoverflow](https://stackoverflow.com/questions/59293731/how-do-i-solve-merge-conflicts-on-a-protected-branch)
    ```bash
    git fetch origin
    git checkout -b conflict-fix origin/main
    git merge origin/release
    git push -u origin conflict-fix
    ```

20. **What would you do if a release branch diverges too much from `main`?**  
    You should merge or rebase it early and frequently so the divergence stays manageable. The longer branches stay apart, the more likely conflicts and integration surprises become.  
    ```bash
    git fetch origin
    git merge origin/main
    ```

21. **How do you investigate a bug introduced somewhere in history?**  
    Use `git bisect` to narrow down the commit that introduced the bug by testing good and bad revisions. This is one of the most practical tools for real debugging in a large repository.  
    ```bash
    git bisect start
    git bisect bad
    git bisect good <known-good-commit>
    ```  
 [docs.github](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts/resolving-a-merge-conflict-using-the-command-line)

22. **How do you recover from an accidental force push?**  
    Check remote and local reflogs, identify the lost commit, and restore it if possible before more changes overwrite it. In a team environment, this is why force pushes should be tightly controlled.  
    ```bash
    git reflog
    git reset --hard <commit-id>
    git push --force-with-lease
    ```

23. **How do you manage long-lived feature branches without making merges painful?**  
    Rebase or merge from the target branch frequently, keep commits small, and avoid letting one branch drift for weeks. In practice, long-lived branches are one of the biggest causes of difficult merges.  
    ```bash
    git fetch origin
    git rebase origin/develop
    ```  
 [atlassian](https://www.atlassian.com/git/tutorials/merging-vs-rebasing)

24. **How do you keep GitHub Actions or CI from merging broken code?**  
    Require pull requests, branch protection, and passing checks before merge. The practical goal is to make the merge button unavailable until the code meets the team’s quality bar. [docs.github](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/merging-a-pull-request)
    ```bash
    git push origin feature-branch
    ```

## Real-world scenario questions

25. **A teammate added a quick fix directly on `main` and now another feature branch is failing. What do you do?**  
    First identify the exact commit that caused the issue, then decide whether to revert, cherry-pick, or reapply the fix properly through a feature branch. The goal is to restore process discipline without losing the needed correction. [docs.github](https://docs.github.com/articles/resolving-a-merge-conflict-using-the-command-line)
    ```bash
    git log --oneline
    git revert <bad-commit>
    ```

26. **A pull request contains both a feature and a refactor, and reviewers are confused. How do you handle it?**  
    Split the work if possible, because one PR should ideally solve one problem. If splitting is too expensive, explain clearly in the PR description and keep the refactor and feature changes easy to distinguish. [docs.github](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts/resolving-a-merge-conflict-using-the-command-line)
    ```bash
    git checkout -b refactor-only
    git cherry-pick <commit-id>
    ```

27. **A release is blocked because of a merge conflict in a config file. What is your approach?**  
    Treat config conflicts carefully because they often change runtime behavior, not just syntax. Resolve the file, validate the final configuration in the target environment, and rerun deployment checks before merging. [stackoverflow](https://stackoverflow.com/questions/59293731/how-do-i-solve-merge-conflicts-on-a-protected-branch)
    ```bash
    git merge origin/release
    git add config.yml
    git commit
    ```

28. **A hotfix must be shipped tonight, but the team is mid-sprint. What would you do?**  
    Create a minimal hotfix branch from production, fix only the urgent issue, test it, and merge it back into both production and development lines. That keeps the patch small and prevents the same bug from reappearing later. [danielkummer.github](https://danielkummer.github.io/git-flow-cheatsheet/)
    ```bash
    git flow hotfix start 2.1.1
    git flow hotfix finish 2.1.1
    ```

29. **A merge passed, but the application behavior changed unexpectedly. How do you troubleshoot it?**  
    Compare the merged branch against the previous known-good state, inspect recent commits, and use `git bisect` if needed to isolate the culprit. In real projects, unexpected behavior after a clean merge is often caused by business logic drift rather than syntax issues. [docs.github](https://docs.github.com/articles/resolving-a-merge-conflict-using-the-command-line)
    ```bash
    git diff main..HEAD
    git bisect start
    ```

30. **Your team wants a clean codebase but different developers prefer different workflows. How do you standardize it?**  
    Standardize the parts that matter most: branch naming, PR reviews, test requirements, and release rules. You can allow some flexibility on local workflow, but the shared integration process should be consistent so the codebase stays clean. [theserverside](https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/Gitflow-release-branch-process-start-finish)
    ```bash
    git branch -a
    git log --graph --oneline --decorate
    ```

## Quick command patterns

- Create a feature branch:  
  ```bash
  git checkout -b feature/name
  ```  
 [docs.github](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts/resolving-a-merge-conflict-using-the-command-line)

- Sync with remote main:  
  ```bash
  git fetch origin
  git pull --rebase origin main
  ```  
 [atlassian](https://www.atlassian.com/git/tutorials/merging-vs-rebasing)

- Resolve a conflict:  
  ```bash
  git status
  git add <file>
  git commit
  ```  
 [docs.github](https://docs.github.com/articles/resolving-a-merge-conflict-using-the-command-line)

- Start GitFlow feature work:  
  ```bash
  git flow feature start <name>
  ```  
 [theserverside](https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/Gitflow-release-branch-process-start-finish)

- Start GitFlow release/hotfix work:  
  ```bash
  git flow release start <version>
  git flow hotfix start <version>
  ```  
