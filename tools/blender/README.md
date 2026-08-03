# Blender/Bonsai verification

The verified local pair is Blender 5.2.0 LTS with Bonsai
0.8.6-alpha260801 (Windows x64, Python 3.13 dependency wheels). The portable
Blender binary, Bonsai package, and profile are ignored from source control.

Run the probe with the pinned profile:

```powershell
.\.venv-ifc314\Scripts\python.exe tools\blender\verify_environment.py `
  --blender tools\blender\bin\blender-5.2.0-windows-x64\blender.exe `
  --profile tools\blender\profile3 `
  --bonsai-site tools\blender\profile3\extensions\.local\lib\python3.13\site-packages `
  --ifc data\outputs\design_poc.ifc `
  --blend-output data\outputs\bonsai_design_poc_verified.blend `
  --output data\outputs\blender_bonsai_environment.json
```

The probe successfully enabled Bonsai, registered 1,312 BIM operators, loaded
the IFC, and saved a Blender file. The deterministic IfcOpenShell pipeline
remains the authoritative IFC core.
