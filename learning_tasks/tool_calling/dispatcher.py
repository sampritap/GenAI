from .tools import calculator, get_current_date

TOOLS = {
    "calculator": calculator,
    "get_current_date": get_current_date,
}


def dispatch_tool(name: str, arguments: dict):
    if name not in TOOLS:
        raise ValueError(f"Unknown tool: {name}")

    return TOOLS[name](**arguments)
