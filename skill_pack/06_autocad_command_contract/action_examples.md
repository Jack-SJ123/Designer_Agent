# AutoCAD Action Plan Examples

## Example JSON
```json
{
  "drawing": "SLD-001.dwg",
  "assumptions": ["Template is loaded"],
  "actions": [
    {
      "action_type": "update_attribute",
      "target": {"block_name": "DEVICE_TAG", "attribute": "TAG"},
      "params": {"value": "MCC-101-FDR-01"},
      "reason": "Align feeder tag with project standard"
    }
  ],
  "qa_checks": ["layer_compliance", "tag_uniqueness", "titleblock_completeness"]
}
```
