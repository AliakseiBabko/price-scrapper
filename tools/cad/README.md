# CAD intake

`intake_cad.py` hashes the original DWG, records its release header, optionally
inspects a DXF with `ezdxf`, and writes a report. It does not infer units from
the DWG header and does not generate a canonical BIM model until a control
dimension is manually approved.

The source remains in `00_Inbox/cad/` and the CSV status remains `inbox` until
conversion, units, and a known control dimension have been verified.

The installed ODA File Converter 27.1 can be used directly:

```powershell
.\.venv-ifc314\Scripts\python.exe tools\cad\intake_cad.py `
  --source "00_Inbox\cad\20260727-ZK Dubravinskiy.dwg" `
  --convert --expected-units mm `
  --report data\cad\20260727-ZK-Dubravinskiy.auto.intake.json
```

The current DXF reports millimetre `$INSUNITS`, 7,886 model-space entities,
1,703 dimensions, and the source layers. Unit/control-dimension approval is
still manual and therefore the source remains in the inbox.
