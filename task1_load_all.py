# task1_load_all.py
"""
Task 1: Load and inspect all 8 meshes.
It prints:
 - number of vertices
 - min, max, mean, std for each axis
and saves a summary CSV file.
"""
import os
import csv
from utils_mesh import load_mesh_vertices, axis_stats

def main(data_dir="../Data", outdir="../outputs"):
    os.makedirs(outdir, exist_ok=True)
    csv_path = os.path.join(outdir, "mesh_stats.csv")

    mesh_files = [f for f in os.listdir(data_dir) if f.endswith(".obj")]
    results = []

    for fname in mesh_files:
        path = os.path.join(data_dir, fname)
        vertices, _ = load_mesh_vertices(path)
        stats = axis_stats(vertices)
        print(f"\nMesh: {fname}")
        print(f"  Vertices: {len(vertices)}")
        print(f"  X range: {stats['min'][0]:.4f} → {stats['max'][0]:.4f}")
        print(f"  Y range: {stats['min'][1]:.4f} → {stats['max'][1]:.4f}")
        print(f"  Z range: {stats['min'][2]:.4f} → {stats['max'][2]:.4f}")

        results.append([
            fname, len(vertices),
            *stats["min"], *stats["max"], *stats["mean"], *stats["std"]
        ])

    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Mesh", "Vertices",
            "Xmin","Ymin","Zmin","Xmax","Ymax","Zmax",
            "Xmean","Ymean","Zmean","Xstd","Ystd","Zstd"
        ])
        writer.writerows(results)

    print(f"\nSaved stats to {csv_path}")

if __name__ == "__main__":
    main()
