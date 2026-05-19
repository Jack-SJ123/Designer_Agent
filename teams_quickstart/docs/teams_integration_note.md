# Teams Integration Note (No new backend required)

This quickstart is compatible with an internal Teams chatbot:
1. Set the chatbot system instruction using `prompts/gpt_system_prompt.txt`.
2. Engineer asks in English using SEE templates.
3. Bot returns runner JSON.
4. Execution can be manual (copy JSON -> send_payload.bat) or automated later.

This keeps rollout simple while preserving a clear upgrade path to full automation.
