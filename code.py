import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

N = 100000
np.random.seed(20261101)

tree_id = np.array([
    1101, 1102, 1104, 1105, 1106,
    1107, 1108, 1109, 1110, 1111,
    1113, 1114, 1115
])

DBH = np.array([
    2.32, 3.25, 1.75, 5.35, 6.27,
    2.86, 6.37, 5.73, 5.47, 2.23,
    1.31, 2.67, 2.55
])

H = np.array([
    2.41, 3.68, 2.84, 5.06, 5.27,
    2.85, 5.54, 3.22, 3.49, 2.67,
    2.62, 3.24, 3.35
])

rho = np.array([
    0.64, 0.35, 0.64, 0.35, 0.35,
    0.64, 0.64, 0.76, 0.64, 0.35,
    0.76, 0.35, 0.64
])

stems = np.array([
    1, 1, 3, 1, 2, 1, 1,
    1, 1, 1, 1, 1, 3
])

results = []

for i in range(len(tree_id)):

    D = np.maximum(
        np.random.normal(DBH[i], 0.10, N), 0.01
    )

    height = np.maximum(
        np.random.normal(H[i], 0.15, N), 0.01
    )

    density = np.random.uniform(
        0.90 * rho[i],
        1.10 * rho[i],
        N
    )

    biomass = stems[i] * 0.0673 * (
        density * D**2 * height
    )**0.976

    results.append([
        tree_id[i],
        np.mean(biomass),
        np.percentile(biomass, 2.5),
        np.percentile(biomass, 97.5)
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

print(df.round(3))

x = np.arange(len(df))

mean = df["Mean Biomass (kg)"]
lower = mean - df["2.5th Percentile"]
upper = df["97.5th Percentile"] - mean

plt.figure(figsize=(10, 6))

plt.errorbar(
    x, mean,
    yerr=[lower, upper],
    fmt='o',
    capsize=4
)

plt.xticks(x, df["Tree ID"], rotation=45)
plt.xlabel("Tree ID")
plt.ylabel("Above-ground Biomass (kg)")
plt.title("Monte Carlo Uncertainty in Generic Chave Biomass")

plt.grid(axis='y', alpha=0.25)
plt.tight_layout()

plt.savefig("Monte_Carlo_Uncertainty.png", dpi=300)
plt.show()
