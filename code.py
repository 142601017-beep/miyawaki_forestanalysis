import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def compute_biomass_monte_carlo(tree_ids, dbh_list, h_list, rho_list, stems_list, n_simulations=100000, seed=20261101):
    if seed is not None:
        np.random.seed(seed)
    
    results = []
    tree_ids = list(tree_ids)
    dbh_list = list(dbh_list)
    h_list = list(h_list)
    rho_list = list(rho_list)
    stems_list = list(stems_list)

    n_trees = len(tree_ids)
    for i in range(n_trees):
        d_sim = np.maximum(np.random.normal(dbh_list[i], 0.10, n_simulations), 0.01)
        h_sim = np.maximum(np.random.normal(h_list[i], 0.15, n_simulations), 0.01)
        density_sim = np.random.uniform(0.90 * rho_list[i], 1.10 * rho_list[i], n_simulations)
        biomass = stems_list[i] * 0.0673 * (density_sim * d_sim**2 * h_sim)**0.976

        mean_val = float(np.mean(biomass))
        p2_5 = float(np.percentile(biomass, 2.5))
        p97_5 = float(np.percentile(biomass, 97.5))

        results.append([
            str(tree_ids[i]),
            mean_val,
            p2_5,
            p97_5
        ])

    df = pd.DataFrame(
        results,
        columns=[
            "Tree ID",
            "Mean Biomass (kg)",
            "2.5th Percentile",
            "97.5th Percentile"
        ]
    )
    return df

def plot_uncertainty(df, save_path="Monte_Carlo_Uncertainty.png", fig=None, ax=None):
    if fig is None or ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
    else:
        ax.clear()

    x = np.arange(len(df))
    mean = df["Mean Biomass (kg)"].values
    lower = mean - df["2.5th Percentile"].values
    upper = df["97.5th Percentile"].values - mean

    ax.errorbar(
        x, mean,
        yerr=[lower, upper],
        fmt='o',
        color='#1f77b4',
        ecolor='#d62728',
        elinewidth=1.5,
        capsize=5,
        capthick=1.5,
        markersize=6
    )

    ax.set_xticks(x)
    ax.set_xticklabels(df["Tree ID"], rotation=45, ha='right')
    ax.set_xlabel("Tree ID", fontsize=11, fontweight='bold')
    ax.set_ylabel("Above-ground Biomass (kg)", fontsize=11, fontweight='bold')
    ax.set_title("Monte Carlo Uncertainty in Generic Chave Biomass", fontsize=13, fontweight='bold')
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300)
    return fig

# Sample default data
DEFAULT_SAMPLE = {
    "tree_id": [1101, 1102, 1104, 1105, 1106, 1107, 1108, 1109, 1110, 1111, 1113, 1114, 1115],
    "dbh": [2.32, 3.25, 1.75, 5.35, 6.27, 2.86, 6.37, 5.73, 5.47, 2.23, 1.31, 2.67, 2.55],
    "h": [2.41, 3.68, 2.84, 5.06, 5.27, 2.85, 5.54, 3.22, 3.49, 2.67, 2.62, 3.24, 3.35],
    "rho": [0.64, 0.35, 0.64, 0.35, 0.35, 0.64, 0.64, 0.76, 0.64, 0.35, 0.76, 0.35, 0.64],
    "stems": [1, 1, 3, 1, 2, 1, 1, 1, 1, 1, 1, 1, 3]
}

def run_cli_mode():
    print("=" * 60)
    print("  Monte Carlo Biomass Uncertainty Estimator (CLI Mode)")
    print("=" * 60)
    print("Choose input method:")
    print("1. Enter comma-separated lists for all variables")
    print("2. Enter trees one by one (interactive)")
    print("3. Use sample test data")
    choice = input("Enter choice (1/2/3) [default: 1]: ").strip() or "1"

    tree_ids = []
    dbh_list = []
    h_list = []
    rho_list = []
    stems_list = []

    if choice == "3":
        tree_ids = DEFAULT_SAMPLE["tree_id"]
        dbh_list = DEFAULT_SAMPLE["dbh"]
        h_list = DEFAULT_SAMPLE["h"]
        rho_list = DEFAULT_SAMPLE["rho"]
        stems_list = DEFAULT_SAMPLE["stems"]
    elif choice == "2":
        print("\nEntering trees one by one. Enter an empty Tree ID when done.")
        idx = 1
        while True:
            t_id = input(f"\nTree #{idx} - Tree ID (or press Enter to finish): ").strip()
            if not t_id:
                if len(tree_ids) == 0:
                    print("At least one tree must be entered!")
                    continue
                break
            try:
                dbh_val = float(input(f"Tree #{idx} - DBH (Diameter at breast height): "))
                h_val = float(input(f"Tree #{idx} - Height (H): "))
                rho_val = float(input(f"Tree #{idx} - Wood Density (rho): "))
                stems_val = float(input(f"Tree #{idx} - Number of Stems: "))
                tree_ids.append(t_id)
                dbh_list.append(dbh_val)
                h_list.append(h_val)
                rho_list.append(rho_val)
                stems_list.append(stems_val)
                idx += 1
            except ValueError:
                print("Invalid number entered! Please re-enter this tree.")
    else:
        def parse_floats(prompt, default_list=None):
            val = input(prompt).strip()
            if not val and default_list is not None:
                return default_list
            parts = [p.strip() for p in val.replace(',', ' ').split() if p.strip()]
            return [float(p) for p in parts]

        def parse_strings(prompt, default_list=None):
            val = input(prompt).strip()
            if not val and default_list is not None:
                return [str(x) for x in default_list]
            parts = [p.strip() for p in val.replace(',', ' ').split() if p.strip()]
            return parts

        while True:
            try:
                tree_ids = parse_strings("Enter Tree IDs (comma or space separated): ")
                dbh_list = parse_floats("Enter DBH values: ")
                h_list = parse_floats("Enter Height (H) values: ")
                rho_list = parse_floats("Enter Wood Density (rho) values: ")
                stems_list = parse_floats("Enter Stems count values: ")

                n = len(tree_ids)
                if not (len(dbh_list) == n and len(h_list) == n and len(rho_list) == n and len(stems_list) == n):
                    print(f"Error: Count mismatch! Tree IDs: {n}, DBH: {len(dbh_list)}, H: {len(h_list)}, rho: {len(rho_list)}, stems: {len(stems_list)}. Please re-enter.")
                    continue
                if n == 0:
                    print("Error: No data entered. Please enter at least 1 tree.")
                    continue
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")

    sim_str = input("Number of Monte Carlo simulations [default: 100000]: ").strip()
    n_sim = int(sim_str) if sim_str.isdigit() else 100000

    print("\nRunning Monte Carlo simulations...")
    df = compute_biomass_monte_carlo(tree_ids, dbh_list, h_list, rho_list, stems_list, n_simulations=n_sim)
    print("\nSimulation Results:")
    print(df.round(3).to_string(index=False))

    save_img = "Monte_Carlo_Uncertainty.png"
    fig = plot_uncertainty(df, save_path=save_img)
    print(f"\nGraph saved to: {os.path.abspath(save_img)}")
    plt.show()

def run_gui_mode():
    import tkinter as tk
    from tkinter import ttk, messagebox
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

    root = tk.Tk()
    root.title("Monte Carlo Biomass Uncertainty Estimator")
    root.geometry("1100, 750")
    root.minsize(900, 600)

    # Styling
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TNotebook.Tab", font=('Arial', 10, 'bold'), padding=[12, 6])
    style.configure("Accent.TButton", font=('Arial', 10, 'bold'), foreground='#ffffff', background='#2563eb')
    style.map("Accent.TButton", background=[('active', '#1d4ed8')])

    # Main container
    main_paned = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
    main_paned.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

    # Left frame for inputs
    left_frame = ttk.Frame(main_paned, width=420)
    main_paned.add(left_frame, weight=1)

    # Right frame for plot and results
    right_frame = ttk.Frame(main_paned)
    main_paned.add(right_frame, weight=2)

    # Notebook tabs for Input Methods
    notebook = ttk.Notebook(left_frame)
    notebook.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

    tab_batch = ttk.Frame(notebook)
    tab_table = ttk.Frame(notebook)
    notebook.add(tab_batch, text="Batch List Input")
    notebook.add(tab_table, text="Table / Row Input")

    # --- BATCH TAB ---
    batch_scroll = ttk.Frame(tab_batch)
    batch_scroll.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

    ttk.Label(batch_scroll, text="Enter values separated by commas or spaces:", font=('Arial', 9, 'italic')).pack(anchor='w', pady=(0, 6))

    def make_input_field(parent, label_text):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=4)
        lbl = ttk.Label(frame, text=label_text, font=('Arial', 9, 'bold'))
        lbl.pack(anchor='w')
        entry = ttk.Entry(frame, font=('Arial', 10))
        entry.pack(fill=tk.X, pady=(2, 0))
        return entry

    entry_batch_ids = make_input_field(batch_scroll, "Tree IDs (e.g. 1101, 1102, 1104):")
    entry_batch_dbh = make_input_field(batch_scroll, "DBH - Diameter (e.g. 2.32, 3.25, 1.75):")
    entry_batch_h = make_input_field(batch_scroll, "Height H (e.g. 2.41, 3.68, 2.84):")
    entry_batch_rho = make_input_field(batch_scroll, "Wood Density ρ (e.g. 0.64, 0.35, 0.64):")
    entry_batch_stems = make_input_field(batch_scroll, "Stems Count (e.g. 1, 1, 3):")

    # --- TABLE TAB ---
    row_input_frame = ttk.LabelFrame(tab_table, text="Add Individual Tree", padding=6)
    row_input_frame.pack(fill=tk.X, padx=8, pady=4)

    # Grid for row inputs
    ttk.Label(row_input_frame, text="Tree ID:").grid(row=0, column=0, sticky='w', padx=2, pady=2)
    entry_t_id = ttk.Entry(row_input_frame, width=10)
    entry_t_id.grid(row=0, column=1, padx=2, pady=2)

    ttk.Label(row_input_frame, text="DBH:").grid(row=0, column=2, sticky='w', padx=2, pady=2)
    entry_t_dbh = ttk.Entry(row_input_frame, width=10)
    entry_t_dbh.grid(row=0, column=3, padx=2, pady=2)

    ttk.Label(row_input_frame, text="Height:").grid(row=1, column=0, sticky='w', padx=2, pady=2)
    entry_t_h = ttk.Entry(row_input_frame, width=10)
    entry_t_h.grid(row=1, column=1, padx=2, pady=2)

    ttk.Label(row_input_frame, text="Density ρ:").grid(row=1, column=2, sticky='w', padx=2, pady=2)
    entry_t_rho = ttk.Entry(row_input_frame, width=10)
    entry_t_rho.grid(row=1, column=3, padx=2, pady=2)

    ttk.Label(row_input_frame, text="Stems:").grid(row=2, column=0, sticky='w', padx=2, pady=2)
    entry_t_stems = ttk.Entry(row_input_frame, width=10)
    entry_t_stems.grid(row=2, column=1, padx=2, pady=2)

    treeview_frame = ttk.Frame(tab_table)
    treeview_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

    cols = ("ID", "DBH", "Height", "Density", "Stems")
    tree_table = ttk.Treeview(treeview_frame, columns=cols, show='headings', height=7)
    for col in cols:
        tree_table.heading(col, text=col)
        tree_table.column(col, width=55, anchor='center')
    table_scrollbar = ttk.Scrollbar(treeview_frame, orient=tk.VERTICAL, command=tree_table.yview)
    tree_table.configure(yscrollcommand=table_scrollbar.set)
    tree_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    table_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def add_tree_row():
        t_id = entry_t_id.get().strip()
        t_dbh = entry_t_dbh.get().strip()
        t_h = entry_t_h.get().strip()
        t_rho = entry_t_rho.get().strip()
        t_stems = entry_t_stems.get().strip()

        if not (t_id and t_dbh and t_h and t_rho and t_stems):
            messagebox.showwarning("Incomplete Data", "Please fill in all 5 fields before adding a tree.")
            return
        try:
            float(t_dbh)
            float(t_h)
            float(t_rho)
            float(t_stems)
        except ValueError:
            messagebox.showerror("Invalid Input", "DBH, Height, Density, and Stems must be numeric.")
            return

        tree_table.insert('', tk.END, values=(t_id, t_dbh, t_h, t_rho, t_stems))
        entry_t_id.delete(0, tk.END)
        entry_t_dbh.delete(0, tk.END)
        entry_t_h.delete(0, tk.END)
        entry_t_rho.delete(0, tk.END)
        entry_t_stems.delete(0, tk.END)
        entry_t_id.focus_set()

    def remove_selected_row():
        selected = tree_table.selection()
        if not selected:
            messagebox.showinfo("Select Row", "Please select a row from the table to remove.")
            return
        for item in selected:
            tree_table.delete(item)

    row_btn_frame = ttk.Frame(row_input_frame)
    row_btn_frame.grid(row=2, column=2, columnspan=2, sticky='e', pady=4)
    ttk.Button(row_btn_frame, text="Add Tree", command=add_tree_row).pack(side=tk.LEFT, padx=2)
    ttk.Button(tab_table, text="Delete Selected", command=remove_selected_row).pack(anchor='e', padx=8, pady=2)

    # --- SIMULATION SETTINGS & ACTIONS (Bottom of Left Frame) ---
    settings_frame = ttk.LabelFrame(left_frame, text="Simulation Settings & Actions", padding=8)
    settings_frame.pack(fill=tk.X, padx=8, pady=8)

    sim_row = ttk.Frame(settings_frame)
    sim_row.pack(fill=tk.X, pady=2)
    ttk.Label(sim_row, text="Monte Carlo Iterations (N):").pack(side=tk.LEFT)
    entry_n_sim = ttk.Entry(sim_row, width=12)
    entry_n_sim.pack(side=tk.RIGHT)
    entry_n_sim.insert(0, "100000")

    def load_sample_data():
        # Populate Batch fields
        entry_batch_ids.delete(0, tk.END)
        entry_batch_ids.insert(0, ", ".join(map(str, DEFAULT_SAMPLE["tree_id"])))

        entry_batch_dbh.delete(0, tk.END)
        entry_batch_dbh.insert(0, ", ".join(map(str, DEFAULT_SAMPLE["dbh"])))

        entry_batch_h.delete(0, tk.END)
        entry_batch_h.insert(0, ", ".join(map(str, DEFAULT_SAMPLE["h"])))

        entry_batch_rho.delete(0, tk.END)
        entry_batch_rho.insert(0, ", ".join(map(str, DEFAULT_SAMPLE["rho"])))

        entry_batch_stems.delete(0, tk.END)
        entry_batch_stems.insert(0, ", ".join(map(str, DEFAULT_SAMPLE["stems"])))

        # Also populate table
        for item in tree_table.get_children():
            tree_table.delete(item)
        for i in range(len(DEFAULT_SAMPLE["tree_id"])):
            tree_table.insert('', tk.END, values=(
                DEFAULT_SAMPLE["tree_id"][i],
                DEFAULT_SAMPLE["dbh"][i],
                DEFAULT_SAMPLE["h"][i],
                DEFAULT_SAMPLE["rho"][i],
                DEFAULT_SAMPLE["stems"][i]
            ))
        messagebox.showinfo("Sample Data Loaded", "Loaded 13 sample trees into both Batch Input and Table Input.")

    def clear_all():
        entry_batch_ids.delete(0, tk.END)
        entry_batch_dbh.delete(0, tk.END)
        entry_batch_h.delete(0, tk.END)
        entry_batch_rho.delete(0, tk.END)
        entry_batch_stems.delete(0, tk.END)
        for item in tree_table.get_children():
            tree_table.delete(item)

    btn_grid = ttk.Frame(settings_frame)
    btn_grid.pack(fill=tk.X, pady=(6, 0))
    ttk.Button(btn_grid, text="Load Sample Data", command=load_sample_data).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
    ttk.Button(btn_grid, text="Clear All", command=clear_all).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

    gen_btn = tk.Button(
        settings_frame,
        text="GENERATE GRAPH",
        command=lambda: execute_generation(),
        bg='#16a34a',
        fg='white',
        font=('Arial', 11, 'bold'),
        activebackground='#15803d',
        activeforeground='white',
        relief=tk.RAISED,
        pady=6
    )
    gen_btn.pack(fill=tk.X, pady=(8, 0))

    # --- RIGHT FRAME: Matplotlib Plot & Summary Table ---
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    canvas = FigureCanvasTkAgg(fig, master=right_frame)
    toolbar = NavigationToolbar2Tk(canvas, right_frame)
    toolbar.update()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Results Table Frame
    result_frame = ttk.LabelFrame(right_frame, text="Calculated Results", padding=4)
    result_frame.pack(fill=tk.X, padx=4, pady=4)

    res_cols = ("Tree ID", "Mean Biomass (kg)", "2.5th Percentile", "97.5th Percentile")
    res_table = ttk.Treeview(result_frame, columns=res_cols, show='headings', height=5)
    for col in res_cols:
        res_table.heading(col, text=col)
        res_table.column(col, anchor='center', width=120)
    res_table.pack(fill=tk.X, expand=True)

    status_var = tk.StringVar(value="Ready. Enter data on the left and click 'GENERATE GRAPH'.")
    status_bar = ttk.Label(right_frame, textvariable=status_var, relief=tk.SUNKEN, anchor='w')
    status_bar.pack(fill=tk.X, side=tk.BOTTOM, padx=2, pady=2)

    def execute_generation():
        # Determine which tab is active
        active_tab_index = notebook.index(notebook.select())
        tree_ids, dbh_list, h_list, rho_list, stems_list = [], [], [], [], []

        if active_tab_index == 0:  # Batch tab
            def parse_entry_floats(entry, name):
                text = entry.get().strip()
                if not text:
                    raise ValueError(f"'{name}' is empty.")
                parts = [p.strip() for p in text.replace(',', ' ').split() if p.strip()]
                return [float(p) for p in parts]

            def parse_entry_strs(entry, name):
                text = entry.get().strip()
                if not text:
                    raise ValueError(f"'{name}' is empty.")
                parts = [p.strip() for p in text.replace(',', ' ').split() if p.strip()]
                return parts

            try:
                tree_ids = parse_entry_strs(entry_batch_ids, "Tree IDs")
                dbh_list = parse_entry_floats(entry_batch_dbh, "DBH")
                h_list = parse_entry_floats(entry_batch_h, "Height H")
                rho_list = parse_entry_floats(entry_batch_rho, "Wood Density ρ")
                stems_list = parse_entry_floats(entry_batch_stems, "Stems Count")
            except ValueError as e:
                messagebox.showerror("Input Error", str(e))
                return

            n = len(tree_ids)
            if not (len(dbh_list) == n and len(h_list) == n and len(rho_list) == n and len(stems_list) == n):
                messagebox.showerror(
                    "Count Mismatch",
                    f"Number of values must match across all fields:\n"
                    f"Tree IDs: {n}\nDBH: {len(dbh_list)}\nHeight: {len(h_list)}\n"
                    f"Wood Density: {len(rho_list)}\nStems: {len(stems_list)}"
                )
                return

        else:  # Table tab
            children = tree_table.get_children()
            if not children:
                messagebox.showwarning("No Data", "No trees have been added to the table. Please add at least one tree.")
                return
            for child in children:
                row_vals = tree_table.item(child, 'values')
                tree_ids.append(row_vals[0])
                dbh_list.append(float(row_vals[1]))
                h_list.append(float(row_vals[2]))
                rho_list.append(float(row_vals[3]))
                stems_list.append(float(row_vals[4]))

        n_sim_txt = entry_n_sim.get().strip()
        n_sim = int(n_sim_txt) if n_sim_txt.isdigit() else 100000

        status_var.set("Computing Monte Carlo simulations...")
        root.update_idletasks()

        try:
            df = compute_biomass_monte_carlo(tree_ids, dbh_list, h_list, rho_list, stems_list, n_simulations=n_sim)
            save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Monte_Carlo_Uncertainty.png")
            plot_uncertainty(df, save_path=save_path, fig=fig, ax=ax)
            canvas.draw()

            # Populate results table
            for item in res_table.get_children():
                res_table.delete(item)
            for _, row in df.iterrows():
                res_table.insert('', tk.END, values=(
                    row["Tree ID"],
                    f"{row['Mean Biomass (kg)']:.3f}",
                    f"{row['2.5th Percentile']:.3f}",
                    f"{row['97.5th Percentile']:.3f}"
                ))

            status_var.set(f"Done! Evaluated {len(df)} trees with {n_sim} runs. Graph saved to {os.path.basename(save_path)}.")
        except Exception as ex:
            messagebox.showerror("Calculation Error", f"An error occurred: {ex}")
            status_var.set("Error during computation.")

    # Auto-load sample data on startup for convenience
    load_sample_data()

    root.mainloop()

if __name__ == "__main__":
    # If headless / no DISPLAY or --cli flag passed, run in CLI mode
    if "--cli" in sys.argv or not os.environ.get("DISPLAY"):
        run_cli_mode()
    else:
        try:
            run_gui_mode()
        except Exception as e:
            print(f"Could not initialize GUI ({e}). Falling back to CLI mode...")
            run_cli_mode()
