# Teams + GPT Electrical Designer Quickstart

This package is a fast-start implementation for your new idea:
- use a commercial GPT chatbot as the primary interface
- constrain output with a strict AutoCAD action protocol
- run generated actions through local AutoCAD runner
- keep workflow simple for Senior Electrical Engineers (SEE)

## What this adds
- Ready-to-paste GPT system prompt for SEE users
- Single-command execution scripts for local testing
- Protocol-aligned payload templates
- Step-by-step test runbook (simulated and real mode)

## Workflow
1. Engineer chats in English with GPT.
2. GPT returns strict runner JSON only.
3. Execute JSON with one command.
4. Validate drawing update in AutoCAD.

## Folder map
- `prompts/`: GPT instructions and SEE command templates
- `examples/`: runner-compatible JSON payloads
- `scripts/`: one-click local run scripts
- `docs/`: test plan, troubleshooting, and Teams integration notes
