# Dyno examples

Four executable notebooks tell a progression from a model file to an economic result, a nonlinear transition, a Dynare comparison, and a reusable report. They use [dyno.py](https://github.com/EconForge/dyno.py) **0.1.13**, pinned in `pixi.toml` and `pixi.lock`.

## New to economics?

Start with notebook 1. It opens with a plain-language story — *an island economy, a discovery that surprises it* — and defines every term where it first appears. A **glossary** at its end collects the dozen or so recurring words. No economics background is assumed anywhere: each chart is introduced with what you should see and why. The charts are all Dyno's built-in plots (Altair), so no plotting library is imported or configured in the notebooks.

## Start here

Install [Pixi](https://pixi.sh), clone this repository, and run from its root:

```bash
pixi run lab
```

Open the notebooks in order. All paths in the notebooks are relative to the repository root. The Pixi environment includes JupyterLab, the Dyno Lab extension, and the packages used by the examples.

| Notebook | Economic question | Dyno capabilities |
| --- | --- | --- |
| [1. Getting started](01_getting_started.ipynb) | How does a technology innovation move an RBC economy? | Native and inline model text, checks, first-order solution, built-in impulse-response plots, seeded simulation, analytical moments, calibration variants |
| [2. Deterministic models](02_deterministic_models.ipynb) | How do announced productivity gains and a large capital loss affect the transition path? | Perfect-foresight nonlinear solve, exogenous paths, initial conditions, convergence diagnostics |
| [3. Dynare compatibility](03_dynare_compatibility.ipynb) | Does the supplied `.mod` model agree with its `.dyno` equivalent? | Dynare-style import, decision rules, numerical steady-state and impulse-response comparison, model moments vs simulated sample |
| [4. Reports and pipeline](04_reports_and_pipeline.ipynb) | How do we repeat checks and share model results? | File-declared `@run:` workflow (check, solve, simulate, plot), `RunResults`, `dsge_report()`, Dyno Lab |

The source models are [`models/rbc.dyno`](models/rbc.dyno), [`models/rbc.mod`](models/rbc.mod), and [`models/ramsey_deterministic.dyno`](models/ramsey_deterministic.dyno). The two RBC files use the same shock **standard deviation** of 0.009, so their results can be compared directly. The Dynare notebook demonstrates the syntax supported by this supplied `.mod` file; it is not a test of every Dynare feature. `rbc.dyno` ends with `@run:` directives declaring a full check-solve-simulate-plot workflow; `ramsey_deterministic.dyno` declares `@run: solve`.

## Re-execute the notebooks

After editing a notebook or a model, refresh all committed outputs with:

```bash
pixi run python generate_notebooks.py
```

The notebooks are the editable source; this script executes them in order with the active Pixi Python kernel and fails if a cell raises an error. Random simulations use explicit seeds every time (7 in notebook 1, 11 in notebook 3), so refreshed outputs are reproducible. To work on a single file in JupyterLab, run its cells from top to bottom.

For Dyno's broader API and installation details, see the [Dyno documentation](https://econforge.github.io/dyno.py/).
