# PQC-AQ

Research on post-quantum public-key encryption, focused on three topics: **Kyber**,
**ML-KEM** (FIPS 203) and **dLIN** (the sparse noisy linear equations assumption of
Applebaum, Barak and Wigderson). The work is currently at the reading and notes stage; the
code folders are scaffolding.

> **Visibility:** this repository is currently **public**. Only commit material approved
> for public release. Proprietary Accelequant code, internal research, credentials and
> data belong in a private repository.

## Layout

| Path | Contents |
|---|---|
| `src/pqc/` | Library code: `kyber`, `mlkem`, `dLIN` (empty so far) |
| `experiments/` | Per-topic experiments (`kyber`, `mlkem`, `dLIN`) and `benchmarks/` |
| `scripts/` | `benchmarking`, `data_processing`, `plotting`, `utilities` |
| `notebooks/` | Exploratory notebooks |
| `tests/` | Test suite |
| `configs/` | Experiment configuration |
| `literature/` | Reference papers by topic (`kyber/`, `mlkem/`, `dLIN/`, `common/`), plus `bibliography.bib`, `reading-list.md` and `notes/` |
| `my_notes/` | Our own study notes per topic, e.g. `my_notes/dLIN/` (LaTeX source and PDF) |
| `gpt/` | GPT-assisted dLIN material: seminar slides, concept decks, research proposals, error-count data; see `gpt/README.md` |
| `docs/` | `technical`, `meeting-notes`, `project-plans`, `architecture` |
| `papers/manuscript/` | Sources of our own paper (not reference papers) |
| `presentations/` | Our own slide decks |
| `environment/` | `requirements*.txt`, `environment.yml` (not yet created) |

Rule of thumb: papers we **read** go in `literature/<topic>/`; papers we **write** go in
`papers/manuscript/`; our own notes go in `my_notes/<topic>/`.

Empty folders hold a `.gitkeep`; delete it once real files are added. File and folder
names are kebab-case without spaces.

## Where to start (dLIN)

1. `literature/reading-list.md`: reading order for all topics.
2. `my_notes/dLIN/understanding-dlin-revised.pdf`: current dLIN notes.
3. `literature/dLIN/applebaum-barak-wigderson-2009-pke-from-different-assumptions.pdf`:
   the source paper (§7 and §9 first).

## Branches

`main` is the integrated project. `prajjwal-dev` and `manish-dev` are personal
development branches, merged into `main` via pull request. See `CONTRIBUTING.md`.

## Server layout (EC2)

```
~/prajjwal-dev/PQC-AQ/   Git clone, branch prajjwal-dev
~/manish-dev/PQC-AQ/     Git clone, branch manish-dev
/shared/project_pqc/     (planned) datasets, experiment results, artifacts, archives
```

Reference PDFs and slide decks are committed to Git. Zip archives and generated data
(`data/`, `results/`, `artifacts/`, `scratch/`) are ignored and stay on the server.

## Setup / running / reproducing experiments

TODO: fill in once `environment/` and the first experiment exist.
