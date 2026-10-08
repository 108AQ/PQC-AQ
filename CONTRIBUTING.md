# Contributing

1. Do not push directly to `main`.
2. Work on your development branch (`prajjwal-dev` / `manish-dev`).
3. Pull before starting work: `git checkout <branch> && git pull origin <branch>`.
4. Commit logically, with clear messages.
5. Push regularly.
6. Resolve conflicts carefully; they are scientific decisions, not just text.
7. Before a PR: `git fetch origin && git merge origin/main`, resolve conflicts,
   run tests, push, then open the PR into `main`.
8. Do not commit secrets.
9. Do not commit huge generated files (data, results, binaries, papers PDFs).
10. Record experiment configuration and the Git commit hash with every result.
