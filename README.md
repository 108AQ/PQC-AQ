# PQC-AQ

Resources and implementations focused on three topics: **Kyber**, **ML-KEM** and **dLIN**.

> **Visibility:** this repository is currently **public**. Only commit material approved
> for public release. Proprietary Accelequant code, internal research, credentials and
> data belong in a private company repository.

## Layout

| Path | Contents |
|---|---|
| `src/pqc/` | Library code: `common`, `kyber`, `mlkem`, `dLIN` |
| `experiments/` | Per-topic experiments (`kyber`, `mlkem`, `dLIN`) and `benchmarks/` |
| `scripts/` | `benchmarking`, `data_processing`, `plotting`, `utilities` |
| `notebooks/` | Exploratory notebooks |
| `tests/` | Test suite |
| `configs/` | Experiment configuration |
| `docs/` | `technical`, `meeting-notes`, `project-plans`, `architecture` |
| `literature/` | `bibliography.bib`, `reading-list.md`, `notes/` |
| `papers/manuscript/` | Manuscript sources |
| `presentations/` | Slides |
| `environment/` | `requirements*.txt`, `environment.yml` |

Empty folders hold a `.gitkeep`; delete it once real files are added.

## Branches

`main` is the integrated project. `prajjwal-dev` and `manish-dev` are personal
development branches, merged into `main` via pull request. See `CONTRIBUTING.md`.

## Server layout (EC2)

```
~/prajjwal-dev/PQC-AQ/        Git clone (prajjwal-dev)
~/manish-dev/project_pqc/PQC-AQ/  Git clone (manish-dev)
/shared/project_pqc/          (planned) papers, datasets, experiment-results, artifacts, archives
```

Large files stay on the server, not in Git.

## Setup / running / reproducing experiments

TODO: fill in once `environment/` and the first experiment exist.
