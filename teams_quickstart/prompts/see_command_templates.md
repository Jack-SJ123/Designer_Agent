# SEE English Command Templates

## 1) Single tag update
Update drawing `C:/demo/SLD-001.dwg`. For block `DEVICE_TAG`, set attribute `TAG` to `MCC-101-FDR-01`. Return runner JSON only.

## 2) Batch normalization
In drawing `C:/demo/SLD-001.dwg`, normalize all feeder tags under MCC-101 to format `MCC-101-FDR-##`. Return runner JSON only using update_attribute actions.

## 3) Safe refusal pattern
If requested action is not supported by current protocol, return empty actions and explain limitation in assumptions.
