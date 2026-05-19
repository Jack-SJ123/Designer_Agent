# Laptop Test Runbook (GPT + AutoCAD)

## Prerequisites
- Windows laptop with AutoCAD installed
- Python installed
- A DWG containing block `DEVICE_TAG` with attribute `TAG`

## Step 1: Start runner
- Simulated: `teams_quickstart/scripts/run_runner_simulated.bat`
- Real mode: `teams_quickstart/scripts/run_runner_real.bat`

Check health:
`curl http://127.0.0.1:8765/health`

## Step 2: Configure GPT
- Paste `prompts/gpt_system_prompt.txt` as system instructions.
- Use command templates from `prompts/see_command_templates.md`.

## Step 3: Execute
- Save GPT output to a json file, e.g. `payload.json`
- Run: `teams_quickstart/scripts/send_payload.bat payload.json`

## Step 4: Validate
- Confirm response includes `status: remote_runner_ok`.
- In real mode, verify DWG attribute changed.

## Failure diagnosis
- `Unsupported action_type`: request exceeded current protocol.
- `No matching attributes found`: block or attribute names mismatch.
- `pywin32 is required`: install dependency in active venv.
