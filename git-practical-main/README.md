---
# **Git/GitHub Practical**
---
## **Practical 1: Repository Initialization & Understanding Git State**
**Objective:**
Initialize a Git repository and understand basic Git states.
**Following commands were used to achieve the desired results:**
1. `git --version`
: To check the installed Git version.
2. `git init`
: To initialize a new Git repository.
3. `git status`
: To check the current repository state.
4. `git add .`
: To stage all files.
5. `git commit -m "Initial commit"`
: To create the first commit.
---
<img width="738" height="375" alt="Screenshot from 2026-01-21 11-24-02" src="https://github.com/user-attachments/assets/dcd46e18-cfb3-4c94-a7fe-06b10ee22290" />

## **Practical 2: Ignoring Files & Clean Repository**
**Objective:**
Prevent unnecessary files from being tracked.
**Following commands were used to achieve the desired results:**
1. `.gitignore`
: Used to list files/folders Git should ignore.
2. `git status`
: To verify ignored files are not tracked.
---

<img width="1807" height="996" alt="Screenshot from 2026-01-21 12-48-11" src="https://github.com/user-attachments/assets/6d974c8e-b3df-4814-be96-aeef151757d6" />

## **Practical 3: Atomic Commits & Commit Discipline**
**Objective:**
Ensure one logical task per commit.
**Following commands were used to achieve the desired results:**
1. `git add <file>`
2. `git commit -m "Clear atomic message"`
---
<img width="438" height="142" alt="Screenshot from 2026-01-21 13-00-45" src="https://github.com/user-attachments/assets/19c3a98e-0aac-4048-896b-b5510fa2c8e0" />
<img width="1504" height="214" alt="Screenshot from 2026-01-21 13-09-02" src="https://github.com/user-attachments/assets/40704585-6e92-4134-ad3e-15e67fbeae98" />

## **Practical 4: Reading History, Diff & Blame**
**Objective:**
Understand commit history and file-level changes.
**Following commands were used to achieve the desired results:**
1. `git log --oneline --graph --all`
: To view graphical commit history.
2. `git diff <commit1> <commit2>`
: To compare changes between commits.
3. `git blame main.py`
: To see who modified each line.
4. `git tag -a v0.1.0 -m "Initial version"`
: To create an annotated tag.
---
<img width="682" height="294" alt="Screenshot from 2026-01-21 13-15-52" src="https://github.com/user-attachments/assets/5567f65d-0036-421a-b5af-76da0a83e105" />
<img width="693" height="240" alt="Screenshot from 2026-01-21 13-16-08" src="https://github.com/user-attachments/assets/dbfc544f-dd5b-4554-99ee-db216d4153f5" />
<img width="654" height="107" alt="Screenshot from 2026-01-21 17-40-53" src="https://github.com/user-attachments/assets/09bc8631-d3bf-46c8-927d-7cdf8d92ce1d" />

## **Practical 5: Branching Fundamentals (Git Flow)**
**Objective:**
Use Git Flow branching structure.
**Following commands were used to achieve the desired results:**
1. `git flow init`
: Initialize Git Flow.
2. `git flow feature start login-feature`
: Create feature branch from develop.
3. `git commit -m "Add logic functionality"`
: Commit feature changes.
4. `git flow feature finish login-feature`
: Merge feature back into develop.
---

<img width="1920" height="1080" alt="Screenshot from 2026-01-22 14-28-58" src="https://github.com/user-attachments/assets/40de9edb-b33b-4900-b9b5-0a2c38e3b2e4" />

## **Practical 6: Commit Message Enforcement (Git Hooks)**
**Objective:**
Enforce structured commit messages.
**Following commands were used to achieve the desired results:**
1. `cd .git/hooks`
2. Create `commit-msg` hook.
3. `chmod +x commit-msg`
4. Attempt invalid commit → commit rejected.

Git hooks are useful because they let you automatically run checks or scripts at specific points in the Git workflow(like before a commit or before a push)

---

<img width="1303" height="895" alt="Screenshot from 2026-01-19 12-52-10" src="https://github.com/user-attachments/assets/bdb2db8a-ff8a-4dc2-847f-225fc90f40d3" />

## **Practical 7: Pull Request Workflow (Simulation)**
**Objective:**
Simulate collaborative Git Flow usage.
**Following commands were used to achieve the desired results:**
1. `git flow feature start pr-feature`
2. `git push origin feature/pr-feature`
3. Create PR → develop.
4. Create another feature branch.
5. Rebase with latest develop before PR.
---
<img width="1782" height="939" alt="Screenshot from 2026-01-22 11-41-39" src="https://github.com/user-attachments/assets/e3558730-b9de-4a76-9975-e8c71d1273e2" />
<img width="1782" height="939" alt="Screenshot from 2026-01-22 11-41-51" src="https://github.com/user-attachments/assets/4a7eeb5d-96b6-450f-bd0b-b199511e5e57" />

## **Practical 8: Versioning & Tagging (Git Flow Release)**
**Objective:**
Track releases properly.
**Following commands were used to achieve the desired results:**
1. `git flow release start v0.1.0`
2. Final fixes committed.
3. `git flow release finish v0.1.0`
4. Tag automatically created.
---
<img width="1796" height="965" alt="Screenshot from 2026-01-22 12-41-37" src="https://github.com/user-attachments/assets/d85748f2-dd88-4ec3-9aa5-8711259c0098" />


## **Practical 9: Cherry-Picking & Commit Rewriting**
**Objective:**
Apply specific commits across branches.
**Following commands were used to achieve the desired results:**
1. `git flow feature start doc-update`
2. Commit README change.
3. `git flow feature start ui-fix`
4. `git cherry-pick <commit-hash>`
5. `git commit --amend`
6. `git reset --hard HEAD~1`
---
<img width="1303" height="895" alt="Screenshot from 2026-01-19 12-53-38" src="https://github.com/user-attachments/assets/9a0ebea3-9bf1-4d63-a504-69e969c41249" />


## **Practical 10: Merge Conflicts & Resolution**
**Objective:**
Resolve conflicts in Git Flow branches.
**Following commands were used to achieve the desired results:**
1. Modify same file in two feature branches.
2. `git flow feature finish branch1`
3. Conflict appears.
4. Resolve manually.
5. `git add .`
6. `git commit`

Git tries its best to resolve conflicts, if unable to do so need to discuss manually and resolve any remaining merge issues.

---
<img width="938" height="363" alt="Screenshot from 2026-01-22 14-29-05" src="https://github.com/user-attachments/assets/e2c80263-7906-4c0d-b1b1-a49d9fc6cb03" />



## **Practical 11: Finding Bugs Using Git Bisect**
**Objective:**
Identify bug-introducing commit.
**Following commands were used to achieve the desired results:**
1. `git bisect start`
2. `git bisect bad`
3. `git bisect good v1.0.0`
4. Test suggested commits.
5. `git bisect reset`

Git bisect is a powerful debugging tool in Git that uses a binary search algorithm to identify the specific commit that introduced a bug or regression. By marking a known "bad" (broken) commit and a known "good" (working) commit, it narrows down the culprit by checking out intermediate commits and having you test them.

---
<img width="950" height="378" alt="Screenshot from 2026-01-22 15-44-34" src="https://github.com/user-attachments/assets/5e32a4fd-1043-47d8-8612-62aa920e47fc" />
<img width="950" height="378" alt="Screenshot from 2026-01-22 15-45-55" src="https://github.com/user-attachments/assets/4276b1c7-cbca-4912-ac08-7dd5b7fcf149" />

## **Practical 12: Rebasing, Interactive Rebase & Amend**
**Objective:**
Clean feature history before merge.
**Following commands were used to achieve the desired results:**
1. `git flow feature start cleanup-history`
2. Create multiple commits.
3. `git rebase -i develop`
4. Squash and reorder commits.
5. `git commit --amend`

git rebase is often used instead of git merge to maintain a clean, linear project history free of unnecessary merge commits. It makes the commit history easier to read and navigate, which can simplify debugging and code reviews.

---
<img width="991" height="433" alt="Screenshot from 2026-01-22 16-02-41" src="https://github.com/user-attachments/assets/a659610f-0df5-4249-a14f-baaf01b288a9" />
<img width="991" height="433" alt="Screenshot from 2026-01-22 18-51-37" src="https://github.com/user-attachments/assets/996f1f62-02ef-425a-948a-1046ba9cb546" />
<img width="991" height="433" alt="Screenshot from 2026-01-22 19-01-29" src="https://github.com/user-attachments/assets/277d63db-878a-43f2-9889-5c40cd180158" />
<img width="992" height="412" alt="Screenshot from 2026-01-22 19-04-55" src="https://github.com/user-attachments/assets/5f9b32e6-05ee-4c36-8b6f-e8ebdcb1d89e" />
<img width="993" height="422" alt="Screenshot from 2026-01-22 19-06-08" src="https://github.com/user-attachments/assets/e2490cb9-cee3-4c71-8f05-04603c800044" />

## **Practical 13: Cherry-Pick Scenario**
**Objective:**
Apply only bugfix from another feature.
**Following commands were used to achieve the desired results:**
1. `git flow feature start alpha`
2. Commit bugfix.
3. `git flow feature start beta`
4. `git cherry-pick <bugfix-commit>`

Merging is generally preferred over cherry-picking because it preserves the full, accurate commit history, ensures all dependencies of a change are included, and prevents duplicate commit IDs. Merging handles conflicts better, maintains branch structure, and allows for easier debugging, whereas cherry-picking can lead to fragmented, hard-to-track histories.

---

<img width="575" height="420" alt="Screenshot from 2026-01-22 19-09-47" src="https://github.com/user-attachments/assets/2b57b8fa-96a9-4600-8ad8-956c571f64b9" />
<img width="575" height="420" alt="Screenshot from 2026-01-22 19-09-52" src="https://github.com/user-attachments/assets/82bf0f7f-9d0d-45bc-89ad-064a04c1e63d" />

## **Practical 14: Diverged Branch Reconciliation**
**Objective:**
Handle diverged branches.
**Following commands were used to achieve the desired results:**
1. Create `divA` and `divB` from develop.
2. Push both branches.
3. `git pull` shows divergence.
4. Resolve using:
* `git merge`
* `git rebase`

"Divergent branches" in Git occur when both your local branch and the remote branch have moved forward with different, non-overlapping commits, making a direct update impossible. To resolve this, you must instruct Git how to combine these separate histories, typically by merging the remote changes into your local, or rebasing your local commits on top of the remote.

---
<img width="575" height="420" alt="Screenshot from 2026-01-22 19-10-07" src="https://github.com/user-attachments/assets/40f701d4-47fa-4c3b-8629-b531fd605f21" />
<img width="697" height="424" alt="Screenshot from 2026-01-22 19-15-47" src="https://github.com/user-attachments/assets/0248bb57-d7a1-40fc-8091-6edcf93b89ec" />
<img width="686" height="412" alt="Screenshot from 2026-01-22 19-17-44" src="https://github.com/user-attachments/assets/957466e4-475e-45e9-96ae-b484dcd1ebcc" />
<img width="686" height="412" alt="Screenshot from 2026-01-22 19-22-23" src="https://github.com/user-attachments/assets/3062fb74-cb8f-4f82-8647-532fafe29010" />

## **Practical 15: Detached HEAD & Reattachment**
**Objective:**
Recover work from detached HEAD.
**Following commands were used to achieve the desired results:**
1. `git checkout <commit-hash>`
2. HEAD becomes detached.
3. Make commit.
4. `git checkout -b recovered-branch`

A "detached HEAD" state in Git occurs when your
HEAD pointer references a specific commit hash rather than a branch name. While not an error, it is considered dangerous because any new commits made while in this state are not associated with any branch and can become "orphaned". 

---
<img width="686" height="412" alt="Screenshot from 2026-01-22 19-25-56" src="https://github.com/user-attachments/assets/8de1d932-c8d3-41bb-8bb3-5b96024cc76e" />


## **Practical 16: Advanced Git Hooks**
**Objective:**
Automate quality checks.
**Following commands were used to achieve the desired results:**
1. Create `pre-commit` hook.
2. Block commits with TODOs.
3. Create `prepare-commit-msg` hook.
4. Invalid commit rejected.
---

<img width="686" height="412" alt="Screenshot from 2026-01-22 19-25-56" src="https://github.com/user-attachments/assets/da123c2b-961a-4a44-a06d-ecdb6bda385a" />
<img width="683" height="1003" alt="Screenshot from 2026-01-22 19-29-24" src="https://github.com/user-attachments/assets/e1eaa23a-c401-4ed6-823e-25826a7a83c1" />

## **Practical 17: Git Spaghetti Challenge**
**Objective:**
Clean complex Git Flow history.
**Following commands were used to achieve the desired results:**
1. Analyze history using:
`git log --graph --all`
2. Fix duplicate hotfix.
3. Clean feature branches using rebase.
4. Merge cleanly into develop.
5. Merge develop into main.

Git spaghetti refers to tangled, non-linear, and chaotic commit histories often caused by frequent force-pushes, direct-to-main commits, or un-rebased feature branches. Risks include severe merge conflicts, loss of work , and impossible-to-trace code changes. Mitigating this requires maintaining a linear history, regular rebase practices, and using protective branch rules. 
Risks of Git Spaghetti
1. Merge Conflict Hell: Complex, tangled branches make merging a nightmare, leading to time-consuming manual fixes.
2. Lost Work: Improper use of git push --force or premature git push --force-with-lease can overwrite teammate changes.
3. Impossible Debugging: A chaotic history makes it difficult to locate when a specific bug was introduced.
4. "Merge Bubbles": Frequent merges instead of rebases create hard-to-read, knotted commit graphs.
5. Detached HEAD Issues: Working directly on commits instead of branches risks losing new, unattached work. 
---

<img width="1281" height="476" alt="Screenshot from 2026-01-27 12-35-24" src="https://github.com/user-attachments/assets/4c5c5a1c-2689-4325-8390-c684652d52d1" />
<img width="1281" height="476" alt="Screenshot from 2026-01-27 12-57-23" src="https://github.com/user-attachments/assets/f008b9d0-6a40-414f-aed2-c6140de4ea59" />

## **Practical 18: Conflict Resolution Advanced**
**Objective:**
Resolve conflicts from different Git operations.
**Following commands were used to achieve the desired results:**
1. Create conflicting changes in feature branches.
2. Conflict during merge:
`git merge`
3. Conflict during rebase:
`git rebase`
4. Conflict during cherry-pick:
`git cherry-pick`
5. Conflicts resolved manually in each case.
<img width="1146" height="983" alt="Screenshot from 2026-01-27 16-28-44" src="https://github.com/user-attachments/assets/80b84c5f-daa8-4d90-8d00-d80d7bf1b8be" />
<img width="486" height="652" alt="Screenshot from 2026-01-27 16-29-10" src="https://github.com/user-attachments/assets/dca0e031-0560-4918-95a5-49f0207865f8" />


