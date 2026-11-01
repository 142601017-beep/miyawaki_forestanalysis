# Biomass Estimator

Monte Carlo estimator for above-ground tree biomass. It reports the mean estimate and the 2.5th and 97.5th percentiles for each tree, and saves an uncertainty plot as `Monte_Carlo_Uncertainty.png`.

## Requirements

- Python 3
- `numpy`, `pandas`, and `matplotlib`
- Tkinter, included with most standard Python installations, for the graphical interface

## Setup

### Windows PowerShell

Run these commands from the repository folder:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install numpy pandas matplotlib
```

If PowerShell does not recognize `py`, install Python and make it available on `PATH`, or select a Python interpreter in VS Code and use that interpreter to create the virtual environment.

### macOS or Linux

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install numpy pandas matplotlib
```

## Run the command-line interface

From the repository folder, run:

```powershell
python .\code.py --cli
```

On macOS or Linux, use `python code.py --cli`.

Choose an input method when prompted:

1. Enter comma- or space-separated lists for tree IDs, DBH, height, wood density, and stem count. Each list must contain the same number of values.
2. Enter each tree's values interactively.
3. Run the built-in sample dataset.

Enter the number of Monte Carlo simulations when prompted, or press Enter to use 100,000. The results are printed in the terminal and the plot is saved as `Monte_Carlo_Uncertainty.png` in the current working directory.

## Run the graphical interface

On Windows PowerShell, activate the virtual environment first, then run:

```powershell
$env:DISPLAY = "1"
python .\code.py
```

On macOS or Linux with a graphical desktop session, run `python code.py` without `--cli`. The GUI starts with sample data loaded. Enter or edit tree data, then select **GENERATE GRAPH**. The graph is saved beside `code.py`.

## Data fields

- Tree ID: label for the tree
- DBH: diameter at breast height
- Height: tree height
- Wood density: density value used by the biomass model
- Stems: number of stems represented by the record

The GUI supports batch list entry and a row-by-row table. The CLI supports the same input data in list or interactive form.
