README – SeamGPT Mesh Normalization, Quantization & Analysis

Project Title:
Mesh Normalization, Quantization, and Error Analysis

Company Context:
-This project is part of MixAR’s SeamGPT data preprocessing assignment.
-It shows how raw 3D mesh data (OBJ files) are cleaned and prepared before AI models learn from them.


What This Project Does:
-This project is all about preparing 3D mesh data (the shapes given as .obj files)
so that they can be used by AI systems like SeamGPT.

We take each mesh and:
1. Normalize it → make sure all meshes are within a fixed coordinate range.
2. Quantize it → convert continuous numbers into small fixed steps (like compressing).
3. Reconstruct it → bring it back to the original scale.
4. Measure Errors → check how much data loss happened after these steps.

It’s basically the “data cleaning” and “format standardization” phase for 3D data.


Requirements:
-Python version: 3.9 or higher
Required libraries:
- numpy
- trimesh
- matplotlib

Install them using:
    pip install numpy trimesh matplotlib


-How To Run:
1️ -> Go to the codes folder:
    cd codes

2️ -> Run Task 1 – Load and inspect meshes
    python task1_load_all.py

3️ -> Run Task 2 – Normalize and quantize meshes
    python task2_normalize_quantize_all.py

4️ -> Run Task 3 – Reconstruct and measure error
    python task3_reconstruct_error_all.py

After running all three:
- Check “outputs” folder for results
  → normalized, quantized, reconstructed OBJ files  
  → error plots (.png)  
  → mesh_stats.csv and error_summary.csv  


Outputs and Results:
- mesh_stats.csv: Basic stats (min, max, mean, std) of all meshes.
- error_summary.csv: MSE/MAE comparison of both normalization methods.
- error_plot_.png: Bar charts showing per-axis reconstruction errors.
- normalized/quantized/reconstructed OBJ files: Visual 3D outputs.


Notes:
- You can open OBJ files in tools like Blender or MeshLab to visualize them.
- The difference before and after quantization is usually very small.
- “Min–Max” normalization works better for simple meshes,
  while “Unit Sphere” normalization helps when scale and position vary.


Submission Includes:
1. All Python scripts (Task 1–3 + utils_mesh.py)
2. Outputs folder (OBJ files, plots, CSVs)
3. Original meshes (Data folder)
4. Final_Report.pdf
5. README.txt

