# task3_reconstruct_error_all.py
"""
Task 3: Reconstruct, compute errors, and plot for all meshes.
"""
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from utils_mesh import (
    load_mesh_vertices, save_vertices_as_mesh,
    normalize_minmax, denormalize_minmax,
    normalize_unit_sphere, denormalize_unit_sphere,
    quantize_01, dequantize_to_01,
    quantize_minus1_1, dequantize_from_minus1_1,
    mse, mae, per_axis_mae
)

def main(data_dir="../Data", outdir="outputs", n_bins=1024):
    os.makedirs(outdir, exist_ok=True)
    mesh_files = [f for f in os.listdir(data_dir) if f.endswith(".obj")]
    summary_path = os.path.join(outdir, "error_summary.csv")

    results = []

    for fname in mesh_files:
        path = os.path.join(data_dir, fname)
        vertices, mesh = load_mesh_vertices(path)
        faces = getattr(mesh, "faces", None)
        print(f"\nEvaluating: {fname}")

        # --- Min–Max ---
        v_norm_minmax, p_minmax = normalize_minmax(vertices)
        q_minmax = quantize_01(v_norm_minmax, n_bins)
        dq_minmax = dequantize_to_01(q_minmax, n_bins)
        v_rec_minmax = denormalize_minmax(dq_minmax, p_minmax)

        # --- Unit Sphere ---
        v_norm_unit, p_unit = normalize_unit_sphere(vertices)
        q_unit = quantize_minus1_1(v_norm_unit, n_bins)
        dq_unit = dequantize_from_minus1_1(q_unit, n_bins)
        v_rec_unit = denormalize_unit_sphere(dq_unit, p_unit)

        # --- Compute Errors ---
        mse_minmax = mse(vertices, v_rec_minmax)
        mae_minmax = mae(vertices, v_rec_minmax)
        pae_minmax = per_axis_mae(vertices, v_rec_minmax)

        mse_unit = mse(vertices, v_rec_unit)
        mae_unit = mae(vertices, v_rec_unit)
        pae_unit = per_axis_mae(vertices, v_rec_unit)

        # --- Plot per-axis MAE ---
        labels = ["X", "Y", "Z"]
        x = np.arange(3)
        plt.figure()
        plt.bar(x - 0.15, pae_minmax, width=0.3, label="Min–Max")
        plt.bar(x + 0.15, pae_unit, width=0.3, label="Unit Sphere")
        plt.xticks(x, labels)
        plt.ylabel("Per-axis MAE")
        plt.title(fname)
        plt.legend()
        plt.savefig(os.path.join(outdir, f"error_plot_{fname.replace('.obj','')}.png"), dpi=150)
        plt.close()

        # --- Save reconstructions ---
        save_vertices_as_mesh(v_rec_minmax, faces, os.path.join(outdir, f"reconstructed_minmax_{fname}"))
        save_vertices_as_mesh(v_rec_unit, faces, os.path.join(outdir, f"reconstructed_unitsphere_{fname}"))

        results.append([fname, mse_minmax, mae_minmax, *pae_minmax, mse_unit, mae_unit, *pae_unit])

    # Write CSV summary
    with open(summary_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Mesh", "MSE_MinMax", "MAE_MinMax", "Xerr_MinMax", "Yerr_MinMax", "Zerr_MinMax",
                         "MSE_UnitSphere", "MAE_UnitSphere", "Xerr_UnitSphere", "Yerr_UnitSphere", "Zerr_UnitSphere"])
        writer.writerows(results)

    print(f"\nSaved summary to {summary_path}")

if __name__ == "__main__":
    main()
