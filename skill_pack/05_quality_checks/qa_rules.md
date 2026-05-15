# QA Rules (Chatbot Output)

Return QA as:
- `pass` or `fail`
- list of violations with severity: `critical|major|minor`
- recommended remediation action per violation

Minimum checks:
1. layer_compliance
2. tag_uniqueness
3. mandatory_attributes
4. titleblock_completeness
5. revision_consistency
