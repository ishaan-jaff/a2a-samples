# LangGraph Local Agent

A simple LangGraph agent that can be run locally using `langgraph dev`.

## Features

- Weather lookup (mock data)
- Calculator tool
- Uses GPT-4o-mini

## Setup

1. Create a `.env` file with your OpenAI API key:
   ```bash
   echo "OPENAI_API_KEY=your_key_here" > .env
   ```

2. Install dependencies:
   ```bash
   pip install -e .
   ```

3. Run the agent server:
   ```bash
   langgraph dev
   ```

4. Open LangGraph Studio at the URL provided in the terminal output.

## Testing the API

```bash
curl -s --request POST \
    --url "http://localhost:2024/runs/stream" \
    --header 'Content-Type: application/json' \
    --data '{
        "assistant_id": "agent",
        "input": {
            "messages": [
                {
                    "role": "human",
                    "content": "What is the weather in Tokyo?"
                }
            ]
        },
        "stream_mode": "messages-tuple"
    }'
```

