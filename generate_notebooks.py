"""
Script to generate and execute all four example notebooks for dyno.py.
"""
import nbformat as nbf
from nbclient import NotebookClient
import os
from pathlib import Path

def create_and_execute_notebook(cells_data, output_path):
    nb = nbf.v4.new_notebook()
    nb.metadata["kernelspec"] = {
        "display_name": "Python 3 (ipykernel)",
        "language": "python",
        "name": "python3"
    }
    nb.metadata["language_info"] = {
        "name": "python",
        "version": "3.13"
    }

    cells = []
    for cell_type, content in cells_data:
        if cell_type == "markdown":
            cells.append(nbf.v4.new_markdown_cell(content))
        elif cell_type == "code":
            cells.append(nbf.v4.new_code_cell(content))
    nb["cells"] = cells

    print(f"Executing {output_path.name}...")
    client = NotebookClient(nb, timeout=60, kernel_name="python3")
    executed_nb = client.execute()

    with open(output_path, "w", encoding="utf-8") as f:
        nbf.write(executed_nb, f)
    print(f"Saved {output_path.name} with execution outputs.")


def build_notebook_1():
    cells = [
        ("markdown", """# 01. Getting Started with `dyno.py`: Stochastic DSGE Modeling

[`dyno.py`](https://github.com/EconForge/dyno.py) is a modern, high-performance Python package for specifying, solving, and simulating Dynamic Stochastic General Equilibrium (DSGE) models.

In this notebook, you will learn the core workflow for stochastic models:
1. **Loading a Model**: From a native `.dyno` file or an inline Python string.
2. **Model Inspection**: Variables, parameters, equations, and steady states.
3. **Checking Stability**: Residuals and the Blanchard-Kahn rank condition.
4. **Solving via 1st-Order Perturbation**: Decision rules and policy functions.
5. **Impulse Response Functions (IRFs)**: Computing and plotting responses to shocks.
6. **Stochastic Simulation & Moments**: Simulating time series and computing variance-covariance matrices.
7. **Recalibration on the Fly**: Modifying parameters and re-solving dynamically.
"""),
        ("code", """import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dyno import DynoModel, simulate, irfs

# Configure display options
pd.set_option('display.precision', 4)
pd.set_option('display.max_columns', 10)
"""),
        ("markdown", """## 1. Loading a Model

Dyno models are typically written in clean, human-readable `.dyno` files. Let's load the canonical Real Business Cycle (RBC) model located in `models/rbc.dyno`.
"""),
        ("code", """# Load model from file
model = DynoModel("models/rbc.dyno")
print(f"Loaded model: {model.name}")
"""),
        ("markdown", """### Prototyping Inline with Python Strings
You can also define and solve models dynamically in Python without creating a separate file, using the `txt` argument:
"""),
        ("code", """# Inline model example: simple AR(1) endowment process
toy_txt = '''
rho   <- 0.85
sigma <- 0.02
x[~]  <- 0.0
e[t]  <- N(0, sigma^2)
x[t] = rho * x[t-1] + e[t]
'''

toy_model = DynoModel(txt=toy_txt)
toy_sol = toy_model.solve()
print("Toy model decision rule:")
display(toy_sol.decision_rule.coefficients_as_df())
"""),
        ("markdown", """## 2. Inspecting Model Structure

Dyno parses your model equations and organizes variables and parameters:
"""),
        ("code", """print("Endogenous variables :", model.symbols["endogenous"])
print("Exogenous shocks     :", model.symbols["exogenous"])
print("Parameters           :", model.symbols["parameters"])
print("Total equations      :", len(model.equations))
"""),
        ("markdown", """### Steady State & Residuals
Let's inspect the calculated steady-state values and verify that the equation residuals are virtually zero:
"""),
        ("code", """# Display steady-state values as a table
ss_df = pd.DataFrame.from_dict(model.steady_state, orient='index', columns=['Steady State Value'])
ss_df
"""),
        ("code", """# Verify equation residuals at steady state
residuals = model.residuals
print(f"Maximum absolute residual: {np.max(np.abs(residuals)):.2e}")
assert np.allclose(residuals, 0, atol=1e-6), "Residuals must be close to 0"
print("✓ Steady state is exact!")
"""),
        ("markdown", """## 3. Checking the Blanchard-Kahn Conditions

Before solving, `model.check()` evaluates the generalized eigenvalues of the system to check the **Blanchard-Kahn conditions** (the number of eigenvalues outside the unit circle must match the number of forward-looking / non-predetermined variables for a unique stable saddle-path solution).
"""),
        ("code", """model.check()
"""),
        ("markdown", """## 4. Solving the Model (1st-Order Perturbation)

`model.solve()` computes the linear perturbation solution (recursive decision rule):
$$y_t = y^* + A (y_{t-1} - y^*) + B \epsilon_t$$

Where:
- $y^*$ is the steady state vector
- $A$ is the transition matrix for predetermined/lagged states
- $B$ is the impact matrix for exogenous shocks
"""),
        ("code", """solution = model.solve()
dr = solution.decision_rule

# Display the decision rule Jacobian (policy functions)
coef_df = dr.coefficients_as_df()
coef_df
"""),
        ("markdown", """## 5. Impulse Response Functions (IRFs)

Dyno computes impulse response functions across a chosen horizon $T$. You can request:
- `"log-deviation"`: Percentage deviations from steady state ($100 \\times \\frac{y_t - y^*}{y^*}$)
- `"deviation"`: Level differences ($y_t - y^*$)
- `"level"`: Raw variable values ($y_t$)
"""),
        ("code", """# Generate 40-period IRFs in log-deviations
irf_dict = solution.irfs(type="log-deviation", T=40)

# Inspect the response to the TFP shock (epsilon)
tfp_irf = irf_dict["epsilon"]
tfp_irf.head(10)
"""),
        ("markdown", """### Built-in Interactive Visualization
`solution.plot()` produces interactive Plotly figures out of the box:
"""),
        ("code", """fig = solution.plot(type="log-deviation")
# Adjust figure size for notebook display
fig.update_layout(height=500, width=800, title="Impulse Responses to TFP Shock (log-deviation)")
fig.show()
"""),
        ("markdown", """## 6. Stochastic Simulation & Moments

We can generate simulated paths under random shock draws using `simulate(solution, T=...)`:
"""),
        ("code", """# Simulate 120 periods (e.g. 30 years of quarterly data)
sim_df = simulate(solution, T=120)
sim_df.head(10)
"""),
        ("code", """# Plot selected simulated trajectories
fig, axes = plt.subplots(2, 2, figsize=(11, 6), sharex=True)

axes[0, 0].plot(sim_df["y"], label="Output (y)", color="#1f77b4", lw=1.5)
axes[0, 0].plot(sim_df["c"], label="Consumption (c)", color="#ff7f0e", lw=1.5)
axes[0, 0].set_title("Output & Consumption")
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].plot(sim_df["i"], label="Investment (i)", color="#2ca02c", lw=1.5)
axes[0, 1].set_title("Investment")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

axes[1, 0].plot(sim_df["n"], label="Labor Hours (n)", color="#9467bd", lw=1.5)
axes[1, 0].set_title("Labor Hours")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

axes[1, 1].plot(sim_df["r"], label="Interest Rate (r)", color="#d62728", lw=1.5)
axes[1, 1].set_title("Rental Rate / Interest Rate")
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
"""),
        ("markdown", """### Analytical Moments
Dyno can also compute the exact analytical unconditional and conditional covariance matrices:
"""),
        ("code", """cov_uncond, cov_cond = dr.moments()
var_names = model.symbols["endogenous"]

cov_df = pd.DataFrame(cov_uncond, index=var_names, columns=var_names)
print("Unconditional Covariance Matrix:")
cov_df
"""),
        ("markdown", """## 7. Model Recalibration on the Fly

You can modify parameter values and re-solve without editing or re-parsing the original model file using `model.recalibrate()`:
"""),
        ("code", """# Recalibrate TFP persistence (rho) from 0.90 to 0.98
model_high_rho = model.recalibrate(rho=0.98)
sol_high_rho = model_high_rho.solve()

# Compare the output IRF between baseline and high persistence
irf_base = solution.irfs(type="log-deviation", T=40)["epsilon"]["y"]
irf_high = sol_high_rho.irfs(type="log-deviation", T=40)["epsilon"]["y"]

comp_df = pd.DataFrame({
    "Baseline (rho = 0.90)": irf_base,
    "High Persistence (rho = 0.98)": irf_high
})

plt.figure(figsize=(8, 4.5))
plt.plot(comp_df.index, comp_df["Baseline (rho = 0.90)"], label="Baseline (rho = 0.90)", lw=2)
plt.plot(comp_df.index, comp_df["High Persistence (rho = 0.98)"], label="High Persistence (rho = 0.98)", lw=2, linestyle="--")
plt.title("Output Response to TFP Shock: Effect of Shock Persistence")
plt.xlabel("Periods")
plt.ylabel("% Deviation from Steady State")
plt.grid(True, alpha=0.3)
plt.legend(frameon=True)
plt.tight_layout()
plt.show()
""")
    ]
    return cells


def build_notebook_2():
    cells = [
        ("markdown", """# 02. Perfect Foresight & Deterministic Transitions in `dyno.py`

In macroeconomics, many questions involve **deterministic simulations** (perfect foresight) rather than stochastic perturbations:
- Anticipated future policy changes (e.g. pre-announced tax reforms).
- Large transition paths away from steady state where linearization errors would be severe (e.g. demographic shifts, post-crisis recovery, climate transitions).
- Temporary or permanent structural shocks.

In this notebook, we demonstrate how `dyno.py` handles deterministic models:
1. **Specifying Deterministic Models**: Initial conditions and anticipated shock paths.
2. **Stacked-Time Boundary Value Problem**: How Dyno solves the non-linear system.
3. **Solving with `deterministic_solve()`**: Full trajectory simulation.
4. **Visualizing Transition Dynamics**: Capital accumulation and consumption smoothing.
5. **Capital Disaster / Recovery Experiment**: Convergence from an initial capital deviation.
"""),
        ("code", """import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dyno import DynoModel, deterministic_solve

pd.set_option('display.precision', 4)
"""),
        ("markdown", """## 1. Specifying a Deterministic Model in Dyno

A model is deterministic if it contains no stochastic distributions (i.e. no `N(...)` shocks) or specifies explicit time trajectories.

Let's inspect `models/ramsey_deterministic.dyno`. Notice:
1. **Initial condition / shock path**:
   ```text
   x[1] <- 1.10
   x[2] <- 1.30
   forall t, 3 <= t < T : x[t] <- 1.0 + (1.30 - 1.0) * exp(-(t - 1))
   ```
   This specifies an anticipated 2-period productivity boom followed by an exponential decay back to steady state ($x = 1.0$).
"""),
        ("code", """model = DynoModel("models/ramsey_deterministic.dyno")

print(f"Model name        : {model.name}")
print(f"Is deterministic? : {model.is_deterministic}")
print(f"Endogenous vars   : {model.symbols['endogenous']}")
print(f"Exogenous paths   : {model.symbols['exogenous']}")
print(f"Parameters        : {model.symbols['parameters']}")
"""),
        ("markdown", """## 2. Solving with `deterministic_solve()`

Dyno solves the stacked-time non-linear system:
$$F(V) = 0$$
where $V = (v_0, v_1, \\dots, v_T)$ contains all variables stacked across all periods $t=0, \\dots, T$.

Dyno uses **automatic differentiation** to compute exact sparse Jacobians and solves the block-tridiagonal system using Newton's method.
"""),
        ("code", """# Solve the deterministic trajectory over the full horizon
traj_df = deterministic_solve(model, verbose=True)

print(f"Trajectory shape: {traj_df.shape} (periods x variables)")
traj_df.head(10)
"""),
        ("markdown", """## 3. Visualizing Transition Dynamics

Let's examine how the economy responds to the anticipated productivity boom:
"""),
        ("code", """fig, axes = plt.subplots(3, 1, figsize=(9, 8), sharex=True)

# Productivity path x_t
axes[0].plot(traj_df['t'], traj_df['x'], color='#1f77b4', lw=2, marker='o', markersize=3)
axes[0].axhline(model.steady_state['x'], color='gray', linestyle=':', label='Steady State')
axes[0].set_ylabel('TFP (x)')
axes[0].set_title('Anticipated Productivity Shock Trajectory')
axes[0].grid(True, alpha=0.3)
axes[0].legend()

# Capital stock k_t
axes[1].plot(traj_df['t'], traj_df['k'], color='#2ca02c', lw=2)
axes[1].axhline(model.steady_state['k'], color='gray', linestyle=':', label='Steady State')
axes[1].set_ylabel('Capital (k)')
axes[1].set_title('Capital Accumulation')
axes[1].grid(True, alpha=0.3)
axes[1].legend()

# Consumption c_t
axes[2].plot(traj_df['t'], traj_df['c'], color='#d62728', lw=2)
axes[2].axhline(model.steady_state['c'], color='gray', linestyle=':', label='Steady State')
axes[2].set_ylabel('Consumption (c)')
axes[2].set_xlabel('Time Period (t)')
axes[2].set_title('Consumption Smoothing')
axes[2].grid(True, alpha=0.3)
axes[2].legend()

plt.tight_layout()
plt.show()
"""),
        ("markdown", """### Economic Insights:
1. **Consumption Smoothing**: Households foresee higher future productivity and immediately increase consumption at $t=1$, even though capital has not accumulated yet.
2. **Capital Deepening**: Higher productivity boosts the marginal product of capital, leading to rapid investment and capital accumulation peaking around $t=4-5$.
3. **Smooth Convergence**: As the shock decays, the economy smoothly converges back to its stationary steady state.
"""),
        ("markdown", """## 4. Experiment: Initial Condition Shock (Capital Disaster)

Deterministic models are ideal for analyzing recovery from a large initial disruption (e.g., a natural disaster destroying 40% of the capital stock).

We can set this up inline with `DynoModel(txt=...)`:
"""),
        ("code", """disaster_model_txt = '''
# Parameters
alph <- 0.50
gam  <- 0.50
delt <- 0.02
bet  <- 0.051
aa   <- 0.511
T    <- 50

# Steady-state values
x[~] <- 1.0
k[~] <- ((delt + bet) / (1.0 * aa * alph))^(1 / (alph - 1))
c[~] <- aa * k[~]^alph - delt * k[~]

# Dynamic equations
0 = c[t] + k[t] - aa*x[t]*k[t-1]^alph - (1 - delt)*k[t-1]
0 = c[t]^(-gam) - (1 + bet)^(-1) * (aa*alph*x[t+1]*k[t]^(alph-1) + 1 - delt) * c[t+1]^(-gam)

# Constant productivity path
x[1] <- 1.0
forall t, 2 <= t < T : x[t] <- 1.0

# Initial condition override: capital destroyed by 40%
k[0] <- 0.60 * k[~]
'''

disaster_model = DynoModel(txt=disaster_model_txt)

# Construct initial guess based on steady state with k[0] = 0.60 * k_ss
v0 = np.concatenate(disaster_model.__steady_state_vectors__)[None, :].repeat(51, axis=0)
k_idx = disaster_model.symbols['variables'].index('k')
v0[:, k_idx] = disaster_model.steady_state['k']
v0[0, k_idx] = 0.60 * disaster_model.steady_state['k']

disaster_traj = deterministic_solve(disaster_model, x0=v0, verbose=False)

# Plot recovery trajectory
plt.figure(figsize=(9, 4.5))
plt.plot(disaster_traj['t'], disaster_traj['k'], label='Capital Stock $k_t$', lw=2, color='#2ca02c')
plt.plot(disaster_traj['t'], disaster_traj['c'], label='Consumption $c_t$', lw=2, color='#d62728')
plt.axhline(disaster_model.steady_state['k'], color='#2ca02c', linestyle='--', alpha=0.7, label='Steady State $k^*$')
plt.axhline(disaster_model.steady_state['c'], color='#d62728', linestyle='--', alpha=0.7, label='Steady State $c^*$')
plt.title('Post-Disaster Recovery Dynamics ($k_0 = 0.60 k^*$)')
plt.xlabel('Period $t$')
plt.ylabel('Level')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()
""")
    ]
    return cells


def build_notebook_3():
    cells = [
        ("markdown", """# 03. Dynare Compatibility in `dyno.py`

[Dynare](https://www.dynare.org/) is the widely used standard in central banks and academia for macroeconomic DSGE modeling. However, Dynare typically requires Matlab or Octave and external preprocessors.

`dyno.py` provides native parsing and execution of Dynare `.mod` files directly in Python!

In this notebook, we cover:
1. **Loading a `.mod` File**: Seamless import with `DynoModel("models/rbc.mod")`.
2. **Syntax Comparison**: How `.mod` syntax maps to `.dyno` syntax.
3. **Solving & Simulating**: Computing decision rules and IRFs from a `.mod` model.
4. **Leveraging Python**: Combining Dynare models with the modern Python data science ecosystem.
"""),
        ("code", """import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dyno import DynoModel, simulate, irfs

pd.set_option('display.precision', 4)
"""),
        ("markdown", """## 1. Loading a Dynare `.mod` File

Let's load `models/rbc.mod` directly using `DynoModel`:
"""),
        ("code", """# Load standard Dynare .mod file
mod_model = DynoModel("models/rbc.mod")

print(f"Model name      : {mod_model.name}")
print(f"Endogenous vars : {mod_model.symbols['endogenous']}")
print(f"Exogenous vars  : {mod_model.symbols['exogenous']}")
print(f"Parameters      : {mod_model.symbols['parameters']}")
"""),
        ("markdown", """## 2. Syntax Comparison: Dyno vs. Dynare

| Feature | Dynare (`.mod`) | Dyno (`.dyno`) |
| :--- | :--- | :--- |
| **Variable Declaration** | `var c, k, y;` | Inferred automatically from equations |
| **Shocks Declaration** | `varexo epsilon;` | Inferred from shock assignments |
| **Parameter Assignment**| `beta = 0.985;` | `beta <- 0.985` |
| **Time Indexing** | `k(-1)`, `c(+1)`, `c` | `k[t-1]`, `c[t+1]`, `c[t]` |
| **Equations Block** | `model; 1/c = ...; end;` | Direct equation list (`1/c[t] = ...`) |
| **Steady State** | `steady_state_model; ... end;` | `k[~] <- ...` or `c[~] <- ...` |
| **Shock Distribution** | `shocks; var epsilon; stderr 0.009; end;` | `epsilon[t] <- N(0, 0.009^2)` |

Dyno parses Dynare's `var`, `varexo`, `parameters`, `model;`, `steady_state_model;`, and `shocks;` blocks seamlessly.
"""),
        ("markdown", """## 3. Steady State and Blanchard-Kahn Verification

Let's check the steady-state solution and eigenvalue conditions computed from the `.mod` file:
"""),
        ("code", """# Display steady state
ss_df = pd.DataFrame.from_dict(mod_model.steady_state, orient='index', columns=['Steady State'])
display(ss_df)

# Run Blanchard-Kahn check
mod_model.check()
"""),
        ("markdown", """## 4. Solving the Dynare Model

Now we solve for the recursive decision rule and policy functions:
"""),
        ("code", """solution = mod_model.solve()
dr = solution.decision_rule

# Display policy function coefficients (Jacobian)
dr.coefficients_as_df()
"""),
        ("markdown", """## 5. Interactive Impulse Response Functions

Let's compute the IRFs and render them using Plotly:
"""),
        ("code", """# Compute IRFs (log-deviation)
irf_dict = solution.irfs(type="log-deviation", T=40)
tfp_irf = irf_dict["epsilon"]
display(tfp_irf.head())

# Plot interactive IRFs
fig = solution.plot(type="log-deviation")
fig.update_layout(height=500, width=800, title="Dynare Model: IRFs to TFP Shock (log-deviation)")
fig.show()
"""),
        ("markdown", """## 6. Seamless Integration with Python Ecosystem

Unlike traditional Dynare workflows that produce `.mat` files or raw command-line text, Dyno returns native **Pandas DataFrames** and **NumPy arrays**.

You can immediately perform custom downstream analysis:
"""),
        ("code", """# 1. Stochastic simulation
sim_data = simulate(solution, T=200)

# 2. Compute summary statistics (volatilities relative to output)
std_y = sim_data['y'].std()
relative_vol = sim_data.std() / std_y

# 3. Compute cross-correlations with output
corrs = sim_data.corrwith(sim_data['y'])

summary_table = pd.DataFrame({
    'Std. Dev.': sim_data.std(),
    'Relative Vol (σ_x / σ_y)': relative_vol,
    'Corr with Output': corrs
})
summary_table
""")
    ]
    return cells


def build_notebook_4():
    cells = [
        ("markdown", """# 04. Automated Reports & Pipelines in `dyno.py`

When working with macroeconomic models, communicating results through clear, standardized reports is essential.

`dyno.py` provides built-in tools for:
1. **Pipeline Execution (`model.run()`)**: Executing end-to-end DSGE workflows defined by `@run:` directives.
2. **Automated DSGE Reports (`dsge_report()`)**: Generating interactive HTML and Markdown model summaries.
3. **Integration with JupyterLab Dyno Extension (`jupyterlab-dyno`)**: Live interactive side-by-side editing.
"""),
        ("code", """import numpy as np
import pandas as pd
from dyno import DynoModel
from dyno.report import dsge_report

pd.set_option('display.precision', 4)
"""),
        ("markdown", """## 1. The `model.run()` Pipeline

`.dyno` files can include declarative `@run:` directives at the bottom of the file. For example, in `models/rbc.dyno`:
```text
@run: check
@run: solve
```

Calling `model.run()` executes these steps sequentially and packages all outputs into a `RunResults` object:
"""),
        ("code", """model = DynoModel("models/rbc.dyno")

# Execute the pipeline
results = model.run()

print(f"Results object type: {type(results)}")
print(f"Available fields   : {[f for f in dir(results) if not f.startswith('_')]}")
"""),
        ("markdown", """### Accessing Pipeline Outputs
The `RunResults` object gives you convenient programmatic access to each stage of the analysis:
"""),
        ("code", """# 1. Model & Solution
print("Solution object:", results.solution)

# 2. Blanchard-Kahn check passed?
print("BK check status :", results.bk_check)

# 3. Equation residuals
print("Max residual    :", np.max(np.abs(results.residuals)))

# 4. Eigenvalues
print("Eigenvalues     :", results.eigenvalues)
"""),
        ("markdown", """## 2. Automated DSGE Reports with `dsge_report()`

The `dsge_report()` function generates a full diagnostic and analytical report of the model.

It automatically includes:
- Metadata & parameter calibrations
- Symbolic equations and LaTeX representations
- Steady-state check and residuals
- Generalized eigenvalues and stability diagnostics
- Decision rules and policy functions
- Impulse response functions and simulation plots
"""),
        ("code", """# Generate report for rbc.dyno
report = dsge_report(filename="models/rbc.dyno")

# In Jupyter, calling display() or letting the object return renders the rich HTML/Markdown report
report.display()
"""),
        ("markdown", """## 3. JupyterLab Dyno Extension (`jupyterlab-dyno`)

If you are using JupyterLab with the `jupyterlab-dyno` extension installed:
1. **Live Model Preview**: Double-click any `.dyno` or `.mod` file to open a split-view editor with live re-rendering of steady state, checks, and IRFs as you type.
2. **Dyno Options Sidebar**: Use the sidebar panel to configure solver parameters (e.g. perturbation order, horizon, steady state only) on a per-file basis.
3. **Error Highlighting**: Syntax and convergence errors are highlighted directly in the editor on the offending line.

This creates an interactive, reactive development environment for macroeconomic modeling!
""")
    ]
    return cells


def main():
    repo_dir = Path("/home/pablo/Econforge/dyno-examples")
    
    print("Building Notebook 1...")
    create_and_execute_notebook(build_notebook_1(), repo_dir / "01_getting_started.ipynb")
    
    print("Building Notebook 2...")
    create_and_execute_notebook(build_notebook_2(), repo_dir / "02_deterministic_models.ipynb")
    
    print("Building Notebook 3...")
    create_and_execute_notebook(build_notebook_3(), repo_dir / "03_dynare_compatibility.ipynb")
    
    print("Building Notebook 4...")
    create_and_execute_notebook(build_notebook_4(), repo_dir / "04_reports_and_pipeline.ipynb")
    
    print("All notebooks built and executed successfully!")

if __name__ == "__main__":
    main()
