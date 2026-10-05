# Recovered from the team report appendix; see README.md for credit and input requirements.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

base = Path(".")

instron_files = {
    "0": base / "A06CCF00_1.csv",
    "45": base / "A06CCF45_1.csv",
    "90": base / "A06CCF90_1.csv",
}

dic_files = {
    "0": base / "Strain_0.csv",
    "45": base / "Strain_45.csv",
    "90": base / "Strain_90.csv",
}

def read_instron(path):
    meta = {}
    lines = path.read_text().splitlines()

    for line in lines[:26]:
        parts = [p.strip().strip('"') for p in line.split(",")]
        if len(parts) >= 3 and parts[0]:
            meta[parts[0]] = parts[2]

    df = pd.read_csv(path, skiprows=26)

    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(
        subset=["Time", "Force", "Tensile strain (Strain 1)"]
    ).copy()

    width = float(meta["Width"])
    thickness = float(meta["Thickness"])
    area = width * thickness

    # Force is in kN and area is in mm^2.
    # 1 kN/mm^2 = 1000 MPa.
    df["stress_MPa"] = df["Force"] * 1000.0 / area

    return meta, df

instron = {}
dic = {}

for angle, path in instron_files.items():
    meta, df = read_instron(path)
    instron[angle] = (meta, df)

for angle, path in dic_files.items():
    d = pd.read_csv(path)
    d = d.rename(columns={"mean(eyy)": "DIC_axial_strain"})

    _, idf = instron[angle]

    # Approximate synchronization between DIC frames and Instron time.
    d["Time"] = np.linspace(idf["Time"].min(), idf["Time"].max(), len(d))
    d["stress_MPa"] = np.interp(d["Time"], idf["Time"], idf["stress_MPa"])

    dic[angle] = d

labels = {
    "0": "$0^\\circ$",
    "45": "$\\pm45^\\circ$",
    "90": "$90^\\circ$",
}

for angle in ["0", "45", "90"]:
    _, idf = instron[angle]
    d = dic[angle]

    imax = idf["stress_MPa"].idxmax()
    tmax = idf.loc[imax, "Time"]

    idf_plot = idf[idf["Time"] <= tmax].copy()
    d_plot = d[d["Time"] <= tmax].copy()

    # Remove obvious failed-correlation outliers.
    d_plot = d_plot[
        (d_plot["DIC_axial_strain"] >= -0.005)
        & (d_plot["DIC_axial_strain"] <= 0.09)
    ]

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(
        idf_plot["Tensile strain (Strain 1)"],
        idf_plot["stress_MPa"],
        label="Extensometer",
    )
    ax.plot(
        d_plot["DIC_axial_strain"],
        d_plot["stress_MPa"],
        label="DIC",
    )
    ax.set_xlabel("Strain")
    ax.set_ylabel("Stress (MPa)")
    ax.grid(True)
    ax.legend()
    fig.tight_layout()
    fig.savefig(f"lab6_stress_strain_{angle}.pdf")
    plt.close(fig)
