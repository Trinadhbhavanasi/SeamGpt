# utils_mesh.py
"""
Simple helper functions for 3D mesh assignment.
No fancy tricks — easy and clear for learning.
"""
import numpy as np
import os
try:
    import trimesh
except Exception as e:
    trimesh = None


# ---------- I/O ----------
def load_mesh_vertices(path):
    if trimesh is None:
        raise ImportError("Install trimesh first: pip install trimesh")
    mesh = trimesh.load(path, force="mesh")
    vertices = np.asarray(mesh.vertices, dtype=np.float32)
    return vertices, mesh


def save_vertices_as_mesh(vertices, faces, out_path):
    if trimesh is None:
        raise ImportError("Install trimesh first: pip install trimesh")
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces if faces is not None else [])
    mesh.export(out_path)


# ---------- Stats ----------
def axis_stats(vertices):
    vmin = vertices.min(axis=0)
    vmax = vertices.max(axis=0)
    vmean = vertices.mean(axis=0)
    vstd = vertices.std(axis=0)
    return {"min": vmin, "max": vmax, "mean": vmean, "std": vstd}


# ---------- Normalization ----------
def normalize_minmax(vertices):
    vmin = vertices.min(axis=0)
    vmax = vertices.max(axis=0)
    scale = np.where((vmax - vmin) == 0, 1.0, (vmax - vmin))
    v_norm = (vertices - vmin) / scale
    params = {"type": "minmax", "vmin": vmin, "vmax": vmax, "scale": scale}
    return v_norm, params


def denormalize_minmax(v_norm, params):
    return v_norm * params["scale"] + params["vmin"]


def normalize_unit_sphere(vertices):
    center = vertices.mean(axis=0)
    v_centered = vertices - center
    radius = np.linalg.norm(v_centered, axis=1).max()
    radius = 1.0 if radius == 0 else radius
    v_norm = v_centered / radius
    params = {"type": "unitsphere", "center": center, "radius": radius}
    return v_norm, params


def denormalize_unit_sphere(v_norm, params):
    return v_norm * params["radius"] + params["center"]


# ---------- Quantization ----------
def quantize_01(v01, n_bins=1024):
    v01 = np.clip(v01, 0, 1)
    q = np.floor(v01 * (n_bins - 1)).astype(np.int32)
    return q


def dequantize_to_01(q, n_bins=1024):
    return q.astype(np.float32) / (n_bins - 1)


def quantize_minus1_1(v, n_bins=1024):
    v01 = (v + 1.0) * 0.5
    return quantize_01(v01, n_bins)


def dequantize_from_minus1_1(q, n_bins=1024):
    v01 = dequantize_to_01(q, n_bins)
    return v01 * 2.0 - 1.0


# ---------- Error ----------
def mse(a, b):
    return float(np.mean((a - b) ** 2))


def mae(a, b):
    return float(np.mean(np.abs(a - b)))


def per_axis_mae(a, b):
    return np.mean(np.abs(a - b), axis=0)
