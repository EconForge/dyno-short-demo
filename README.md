# Dyno Examples (`dyno.py`)

A curated collection of example models and Jupyter notebooks demonstrating the core capabilities of **[`dyno.py`](https://github.com/EconForge/dyno.py)**, a modern, high-performance Python package for Dynamic Stochastic General Equilibrium (DSGE) modeling.

---

## Quick Start

### 1. Install Pixi (if not already installed)

[Pixi](https://pixi.sh) is a reproducible package manager that installs all dependencies (Python, Dyno, JupyterLab, compilers) automatically:

```bash
curl -fsSL https://pixi.sh/install.sh | sh
```

### 2. Launch JupyterLab

Clone or navigate into this repository and run:

```bash
pixi run lab
```

This sets up the environment and opens JupyterLab with all example notebooks ready to run.

---

## Notebooks Overview

| Notebook | Topic | Description |
| :--- | :--- | :--- |
| [**`01_getting_started.ipynb`**](01_getting_started.ipynb) | **Stochastic DSGE Workflow** | Loading `.dyno` models and inline strings, checking Blanchard-Kahn conditions, computing 1st-order perturbation solutions, plotting interactive IRFs with Plotly, running stochastic simulations, computing covariance moments, and on-the-fly recalibration. |
| [**`02_deterministic_models.ipynb`**](02_deterministic_models.ipynb) | **Perfect Foresight & Transitions** | Solving stacked-time non-linear boundary value systems using Newton's method with sparse automatic differentiation. Simulating anticipated shock trajectories and post-disaster capital recovery dynamics. |
| [**`03_dynare_compatibility.ipynb`**](03_dynare_compatibility.ipynb) | **Dynare `.mod` Compatibility** | Parsing and running existing Dynare `.mod` files directly in Python without Matlab or Octave. Comparing Dyno and Dynare syntax, computing decision rules, and performing Pythonic downstream data analysis. |
| [**`04_reports_and_pipeline.ipynb`**](04_reports_and_pipeline.ipynb) | **Automated Reports & Pipelines** | Using declarative `@run:` directives with `model.run()`, generating publication-ready interactive DSGE reports via `dsge_report()`, and integrating with the `jupyterlab-dyno` extension. |

---

## Sample Models (`models/`)

- [`models/rbc.dyno`](models/rbc.dyno): Canonical stochastic Real Business Cycle (RBC) model with capital accumulation, variable labor supply, and an AR(1) technology shock.
- [`models/ramsey_deterministic.dyno`](models/ramsey_deterministic.dyno): Neoclassical Ramsey growth model with an anticipated multi-period productivity boom and transition path back to steady state.
- [`models/rbc.mod`](models/rbc.mod): Standard Dynare `.mod` syntax equivalent of the RBC model, demonstrating native compatibility.

---

## Core Capabilities Highlighted

- **Dual Syntax**: Native `.dyno` syntax + direct Dynare `.mod` support.
- **Fast Autodiff**: Automatic differentiation via dual numbers (`DNumber`) for exact symbolic and numerical Jacobians.
- **Solution Methods**:
  - Linear perturbation solver (QZ decomposition and time iteration) for stochastic models.
  - Stacked-time Newton solver with sparse block-tridiagonal Jacobians for perfect-foresight non-linear transitions.
- **Interactive Visualization**: Out-of-the-box interactive Plotly charts for impulse responses and simulations.
- **Python Ecosystem Integration**: Seamless interoperability with NumPy, Pandas, SciPy, and Matplotlib.

---

## Complementary Tools

- **[`jupyterlab-dyno`](https://github.com/EconForge/jupyterlab-dyno)**: A JupyterLab extension providing live side-by-side preview of `.dyno` and `.mod` files, error highlighting, and an interactive solver options panel.

## License

BSD-3-Clause. Created as part of the [EconForge](https://github.com/EconForge) organization.
