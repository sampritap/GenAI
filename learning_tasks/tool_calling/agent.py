import json
from .llm import call_llm
from .schemas import TOOL_SCHEMAS
from .dispatcher import dispatch_tool

MAX_STEPS = 5


def run_agent(user_query: str):
    messages = [
        {"role": "system", "content": "You are an AI assistant with tool access."},
        {"role": "user", "content": user_query}
    ]

    for _ in range(MAX_STEPS):

        print("Calling LLM...")
        response = call_llm(messages, TOOL_SCHEMAS)
        print("LLM responded")

        if response.tool_calls:

            # ✅ Append assistant message EXACTLY as returned
            messages.append(response.model_dump())

            # ✅ Handle ALL tool calls
            for tool_call in response.tool_calls:

                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                try:
                    result = dispatch_tool(tool_name, arguments)
                except Exception as e:
                    result = f"Tool execution error: {str(e)}"

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })

        else:
            return response.content

    return "Agent stopped: max steps reached."
