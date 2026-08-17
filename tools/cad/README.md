# CAD intake

`intake_cad.py` hashes the original DWG, records its release header, optionally
inspects a DXF with `ezdxf`, and writes a report. It does not infer units from
the DWG header and does not generate a canonical BIM model until a control
dimension is manually approved.

The source remains in `_Inbox/cad/` and the CSV status remains `inbox` until
conversion, units, and a known control dimension have been verified.

The installed ODA File Converter 27.1 can be used directly:

```powershell
.\.venv-ifc314\Scripts\python.exe tools\cad\intake_cad.py `
  --source "_Inbox\cad\20260727-ZK Dubravinskiy.dwg" `
  --convert --expected-units mm `
  --report data\cad\20260727-ZK-Dubravinskiy.auto.intake.json
```

The current DXF reports millimetre `$INSUNITS`, 7,886 model-space entities,
1,703 dimensions, and the source layers. Unit/control-dimension approval is
still manual and therefore the source remains in the inbox.

To create a non-destructive cleaned reference DXF after control-candidate
extraction:

```powershell
.\.venv-ifc314\Scripts\python.exe tools\cad\clean_homestyler_apartment.py `
  --source "data\cad\dxf\20260727-ZK Dubravinskiy.dxf" `
  --candidates "data\cad\20260727-ZK-Dubravinskiy.control-candidates.json" `
  --output "data\cad\20260727-ZK-Dubravinskiy.current-apartment.cleaned.dxf" `
  --report "data\cad\20260727-ZK-Dubravinskiy.current-apartment.cleaned.json"
```

The script preserves the source and selects the repeated plan instance using
the combined control-dimension evidence. Review the derived DXF in DWG
TrueView before using it as a BIM underlay.
