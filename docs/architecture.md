# Electrical Designer Agent Architecture (v1)

## Services
- **Orchestrator API**: receives task requests and coordinates planning, approval, and execution.
- **Rules Engine**: validates action plans against project drafting standards.
- **CAD Execution Worker**: applies approved actions to DWG files (dry-run stub included).
- **QA Validator**: runs post-change checks and emits structured QA reports.

## Workflow
1. Engineer submits `TaskRequest`.
2. Planner returns `ActionPlan`.
3. Human approval gate is enforced.
4. CAD worker applies actions.
5. QA check emits `QaReport`.
6. Outputs are archived for audit.

## Local testing strategy with your laptop AutoCAD
- Keep server in this repo and run AutoCAD executor locally on your machine.
- Start with dry-run mode, then swap in a COM/.NET-backed executor.
- Record each action and snapshot pre/post state for traceability.
