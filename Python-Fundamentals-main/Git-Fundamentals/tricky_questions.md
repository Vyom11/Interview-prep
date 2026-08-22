# GIT TRICKY QUESTIONS

When you are interviewing for production-focused roles, companies do not just want to hear that you know how to use `git commit` and `git push`. They want to see how you handle high-pressure situations, how you safeguard code quality, and whether you can troubleshoot complex state issues without losing data.

I have structured this guide with **five realistic, production-grade Git scenarios**. Some of these are intentionally vague to mimic real-world interview conditions where you are expected to ask clarifying questions before jumping into a solution.

---

### Scenario 1: The Out-of-Sync Production Hotfix (Vague Scenario)

**The Question:**
> *"We have just identified a critical bug in production that requires an immediate fix. However, our main development branch is already miles ahead with features that are partially completed and not ready for release. How do you safely deploy this hotfix?"*

#### Why this is vague

It does not state the team’s branching strategy (e.g., Git Flow, GitHub Flow, Trunk-based development), how releases are tagged, or how the CI/CD pipeline triggers deployments.

---

#### 🔍 Clarifying Questions the Candidate Should Ask

* *"What branching strategy do we use? Are we on Git Flow with dedicated release/support branches, or Trunk-Based Development?"*
* *"How is production currently deployed? Is it pointing to a specific release tag, a `production` branch, or the head of `main`?"*
* *"Does our CI/CD pipeline allow us to deploy directly from arbitrary hotfix branches, or must everything pass through a specific trunk?"*

---

#### 🟢 Green Flags (What a strong candidate does)

* Recognizes that they should *never* make the fix directly on the unstable development branch.
* Suggests finding the exact commit or tag currently running in production to use as the starting point for the hotfix.
* Emphasizes the "backporting" process—making sure the hotfix is merged back into development/trunk so the bug does not regress in the next release.

#### 🔴 Red Flags (What to look out for)

* Suggests writing the fix on the current development branch and "just deploying that file" manually to production.
* Recommends cherry-picking the entire unstable development branch back to a past state (overcomplicating the issue).
* Forgets that the hotfix needs to be merged back into the main line of development, which will cause the bug to reappear in the next release.

---

#### 📋 Bullet Breakdown of a Strong Answer

* **Locate production state:** Identify the precise commit SHA or Git tag currently active in production.
* **Branch off production:** Create a temporary hotfix branch directly from that production commit/tag (e.g., `git checkout -b hotfix/critical-bug <prod-tag-or-sha>`).
* **Apply and test:** Apply the fix, run local/staging tests on this isolated branch.
* **Deploy:** Merge the hotfix back into the production branch or tag it for the CI/CD pipeline to deploy.
* **Prevent regression:** Merge the hotfix branch back into the active development branch (e.g., `main` or `develop`). If conflicts occur, resolve them carefully in the development branch.

---

### Scenario 2: The Disaster Force-Push

**The Question:**
> *"A developer was trying to resolve a local mismatch and ran `git push --force` on our shared, protected `main` branch. They ended up overwriting the last 15 commits that had already been merged and tested. How do you recover this lost work?"*

#### Why this is tricky

It tests the candidate's understanding of Git's internal database structure. It also tests their ability to remain calm and systematic under pressure.

---

#### 🔍 Clarifying Questions the Candidate Should Ask

* *"Do we have branch protection rules enabled on our remote hosting provider (like GitHub/GitLab)? If so, did they have admin bypass privileges?"*
* *"Has anyone else pulled the overwritten state locally since the force-push happened, or does someone still have the correct history in their local terminal?"*

---

#### 🟢 Green Flags (What a strong candidate does)

* Immediately mentions `git reflog` as the primary tool to recover local or remote state.
* Suggests checking the local environments of other team members or the workspace of the CI/CD runner if the original developer's local reflog is cleared.
* Addresses the root cause by discussing Git hosting security configurations (branch protection).

#### 🔴 Red Flags (What to look out for)

* Panics and claims the work is permanently gone.
* Suggests manually rewriting the 15 commits from memory or reading local file histories.
* Suggests restoring from an old daily backup without checking if git's internal database still holds the dangling commits.

---

#### 📋 Bullet Breakdown of a Strong Answer

* **Freeze activity:** Instruct the team to temporarily stop pushing or pulling to prevent further history contamination.
* **Use Git Reflog:** If the developer who forced the push still has their local repository intact, run `git reflog` on their machine. Find the SHA of the commit right before the force push (usually labeled as `moving from...` or `merge...`).
* **Leverage CI/CD / Peers:** If the developer's local reflog is unavailable, check the CI/CD runner's git cache or ask other team members who recently pulled to locate the last known good commit SHA.
* **Reset and restore:** Create a backup branch of the current broken remote state. Then, reset the local branch to the healthy SHA: `git reset --hard <good-sha>`.
* **Re-push safely:** Force-push the restored branch back to remote (using `--force-with-lease` to prevent overwriting other new changes).
* **Mitigation:** Configure strict branch protection rules in GitHub/GitLab to block force-pushing to trunk branches entirely, even for administrators.

---

### Scenario 3: The Bloated Repository & Failing CI/CD (Vague Scenario)

**The Question:**
> *"Our CI/CD pipeline runs have started failing during the `checkout` phase. They either take 15 minutes just to download the code, or they fail entirely with 'Out of Memory' (OOM) errors. How would you diagnose and fix this?"*

#### Why this is vague

It doesn't tell you the repository's contents. Is it a monorepo? Are there large binary files? Is the commit history millions of lines long?

---

#### 🔍 Clarifying Questions the Candidate Should Ask

* *"What is the approximate size of the `.git` directory?"*
* *"Are we committing large binaries, dependencies (like `node_modules` or build artifacts), or media files directly into the repository?"*
* *"Are we cloning the entire git history (full clone) in our CI/CD pipeline config?"*

---

#### 🟢 Green Flags (What a strong candidate does)

* Identifies that CI/CD usually does not need the entire historical graph to build a specific commit, suggesting *shallow clones*.
* Mentions tools like `git-sizer` or `git filter-repo` to analyze where the bloat resides.
* Suggests Git LFS (Large File Storage) or external artifact registries (like S3 or Artifactory) for binaries.

#### 🔴 Red Flags (What to look out for)

* Suggests upgrading the CI/CD runner hardware (e.g., adding more RAM/CPU) as the first and only solution.
* Suggests deleting the repository and starting a new one.
* Does not seem to understand the difference between file size in the working directory and history size in the `.git` folder.

---

#### 📋 Bullet Breakdown of a Strong Answer

* **Immediate CI/CD relief (Shallow Clone):** Configure the CI/CD workflow to perform a shallow clone with `git clone --depth 1`. This pulls only the latest commit, drastically reducing download time and memory footprint.
* **Analyze the bloat:** Run tools like `git-sizer` to identify if the issue is caused by large files, an excessive number of tags, or deep tree structures.
* **Address binary files:** If binaries are found, migrate them out of the standard git history using **Git LFS** or move them to an artifact repository, ensuring they are added to `.gitignore`.
* **Sparse Checkout:** If it is a massive monorepo and the CI job only builds one service, configure `git sparse-checkout` to only pull the directories relevant to that specific build.
* **Prune historical bloat:** Use `git-filter-repo` (the modern successor to `git filter-branch`) to permanently strip accidentally committed large files from the repo's history.

---

### Scenario 4: The Leaked Production Credential

**The Question:**
> *"A developer accidentally committed an active AWS Secret Access Key to our main repository five commits ago. They realized their mistake and made a new commit that deletes the line containing the key. Is the repository secure? If not, what must be done?"*

#### Why this is tricky

This is a combined Git and Security question. It tests whether the candidate prioritizes immediate security remediation (revocation) over technical housekeeping (cleaning the git history).

---

#### 🔍 Clarifying Questions the Candidate Should Ask

* *"Is this repository hosted publicly (e.g., public GitHub) or is it strictly private/internal?"*
* *"Has the secret been rotated or deactivated yet?"*

---

#### 🟢 Green Flags (What a strong candidate does)

* **First response:** Instantly states that the credential must be rotated/invalidated immediately. No amount of Git history cleaning makes an exposed credential safe.
* Explains that deleting a line in a subsequent commit does *not* remove it from the Git history (the parent commits still store the secret).
* Correctly names modern tools like `git-filter-repo` or BFG Repo-Cleaner to purge the history, rather than the deprecated `git filter-branch`.

#### 🔴 Red Flags (What to look out for)

* Thinks that committing a deletion of the line secures the key.
* Focuses entirely on cleaning the Git history first while leaving the active AWS key exposed.
* Suggests using `git filter-branch` without acknowledging that it is deprecated, slow, and can corrupt repositories.

---

#### 📋 Bullet Breakdown of a Strong Answer

* **Invalidate the secret (Critical first step):** Immediately go to the AWS Console/CLI, revoke the leaked access key, and generate a new one. Treat the old key as compromised.
* **Audit logs:** Check AWS CloudTrail logs to see if the leaked key was exploited during the window of exposure.
* **Purge history:** Use `git-filter-repo` or BFG Repo-Cleaner to search the commit history for the exact key string (or the file containing it) and purge it across all branches and tags.
* **Force push updates:** Force-push the clean history back to the remote. Warn the team that they will need to do a fresh clone or a hard reset to match the rewritten history.
* **Preventative tooling:** Set up pre-commit hooks using tools like `talisman` or `git-secrets`, and enable secrets scanning (e.g., GitHub Secret Scanning) on the remote repository.

---

### Scenario 5: The Overwhelming Merge Conflict (Vague Scenario)

**The Question:**
> *"We have a feature branch that has been active for three months. When the developer attempted to merge it back into `main`, they were hit with hundreds of conflicts across dozens of files. They are stuck and overwhelmed. How do you help them resolve this?"*

#### Why this is vague

It does not define the development lifecycle. It leaves room for the candidate to ask about the nature of the changes, test coverage, and the team's familiarity with advanced Git features.

---

#### 🔍 Clarifying Questions the Candidate Should Ask

* *"Do we have a reliable automated test suite that we can run locally to verify code correctness as we resolve conflicts?"*
* *"Can the three-month-old feature branch be broken down into smaller, logical sub-features, or is it one massive monolithic change?"*
* *"Has the developer been pulling `main` into their branch periodically over these three months, or is this the first sync?"*

---

#### 🟢 Green Flags (What a strong candidate does)

* Identifies that a 3-month-old branch is fundamentally a process failure (suggests moving to Trunk-Based Development or utilizing Feature Flags/Toggles in the future).
* Suggests using `git rerere` (Reuse Recorded Resolution) to automate repetitive conflict resolutions.
* Recommends interactive rebasing (`git rebase -i`) to squash intermediate commits, making conflict resolution far simpler.

#### 🔴 Red Flags (What to look out for)

* Suggests blindly choosing "ours" or "theirs" across all files to get the merge done quickly.
* Does not suggest running tests during or after the conflict resolution process.
* Advises the developer to throw away the branch entirely and rewrite the code from scratch without attempting an organized recovery.

---

#### 📋 Bullet Breakdown of a Strong Answer

* **Assess and Backup:** Create a backup copy of the current state of the feature branch before attempting any heavy-handed git commands (e.g., `git branch feature/backup-state`).
* **Simplify the History (Squash):** If the feature branch has dozens of micro-commits, perform an interactive rebase (`git rebase -i main`) to squash them into fewer, cohesive commits. Resolving conflicts on 3 squashed commits is much easier than resolving conflicts on 50 micro-commits.
* **Enable Git Rerere:** Run `git config --global rerere.enabled true`. If they have to abort and retry the rebase/merge, Git will remember how they resolved conflicts the first time and apply those resolutions automatically.
* **Divide and Conquer:** Resolve conflicts file-by-file or domain-by-domain. If specific files belong to other teams, pull those team members in to resolve those specific conflicts collaboratively.
* **Test and Validate:** Run the test suite at each major resolution milestone to catch logical errors that compilation checks miss.
* **Future Prevention:** Discuss process improvements with the team—such as keeping branches short-lived (no more than a few days), implementing continuous integration, and utilizing feature flags to merge unfinished code safely.

---

### 💡 Mentor Tips on Delivering These Answers

When you are in the hot seat:

1. **Do not rush to write commands.** Take 10 seconds to think. State your assumptions clearly.
2. **Ask the clarifying questions first.** This shows you think like a Systems/Solution Architect. You want to understand the blast radius and constraints before you touch the database (and yes, Git is a database).
3. **Frame your answers structurally.** Walk the interviewer through:
    * *Containment* (How to stop things from getting worse).
    * *Recovery* (How to fix the technical state).
    * *Prevention* (How to ensure it never happens again).
