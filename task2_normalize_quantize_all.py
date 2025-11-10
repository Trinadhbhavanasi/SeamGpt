# task2_normalize_quantize_all.py
"""
Task 2: Normalize + Quantize all meshes (Min–Max and Unit Sphere)
"""
import os
from utils_mesh import (
    load_mesh_vertices, save_vertices_as_mesh,
    normalize_minmax, normalize_unit_sphere,
    quantize_01, dequantize_to_01,
    quantize_minus1_1, dequantize_from_minus1_1
)

def main(data_dir="../Data", outdir="outputs", n_bins=1024):
    os.makedirs(outdir, exist_ok=True)
    mesh_files = [f for f in os.listdir(data_dir) if f.endswith(".obj")]

    for fname in mesh_files:
        path = os.path.join(data_dir, fname)
        vertices, mesh = load_mesh_vertices(path)
        faces = getattr(mesh, "faces", None)
        print(f"\nProcessing: {fname}")

        # --- Min–Max ---
        v_norm_minmax, p_minmax = normalize_minmax(vertices)
        q_minmax = quantize_01(v_norm_minmax, n_bins)
        dq_minmax = dequantize_to_01(q_minmax, n_bins)
        save_vertices_as_mesh(v_norm_minmax, faces, os.path.join(outdir, f"normalized_minmax_{fname}"))
        save_vertices_as_mesh(dq_minmax, faces, os.path.join(outdir, f"quantized_minmax_{fname}"))

        # --- Unit Sphere ---
        v_norm_unit, p_unit = normalize_unit_sphere(vertices)
        q_unit = quantize_minus1_1(v_norm_unit, n_bins)
        dq_unit = dequantize_from_minus1_1(q_unit, n_bins)
        save_vertices_as_mesh(v_norm_unit, faces, os.path.join(outdir, f"normalized_unitsphere_{fname}"))
        save_vertices_as_mesh(dq_unit, faces, os.path.join(outdir, f"quantized_unitsphere_{fname}"))

    print("\nAll meshes normalized and quantized successfully!")

if __name__ == "__main__":
    main()
