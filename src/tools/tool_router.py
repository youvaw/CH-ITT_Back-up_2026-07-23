# -*- coding: utf-8 -*-

from src.tools.system_tools import SystemTools


class ToolRouter:
    """Deterministic local tool registry/router for MYX."""

    def __init__(self):
        self.system_tools = SystemTools()

    def match(self, command: str):
        """Match a command to a local tool without executing it."""
        command = str(command or "").strip().lower()
        if not command:
            return None

        if any(x in command for x in ("system status", "system health", "health check")):
            return {"tool": "system", "action": "health", "query": command}

        if any(x in command for x in ("cpu usage", "processor usage", "cpu")):
            return {"tool": "system", "action": "cpu", "query": command}

        if any(x in command for x in ("ram usage", "ram status", "memory usage", "memory status", "memory", "ram")):
            return {"tool": "system", "action": "memory", "query": command}

        if any(x in command for x in ("battery status", "battery")):
            return {"tool": "system", "action": "battery", "query": command}

        if any(x in command for x in ("disk status", "disk usage", "storage status", "storage usage", "hard drive", "disk", "storage")):
            return {"tool": "system", "action": "disk", "query": command}

        if any(x in command for x in ("system information", "system info", "computer information", "computer info")):
            return {"tool": "system", "action": "system_info", "query": command}

        return None

    def execute(self, tool_request):
        """Execute an already matched local tool request."""
        if not isinstance(tool_request, dict):
            return {"success": False, "stage": "execution", "message": "Invalid tool request."}

        tool = str(tool_request.get("tool", "")).strip().lower()
        action = str(tool_request.get("action", "")).strip().lower()

        if tool != "system":
            return {"success": False, "stage": "execution", "message": f"Unknown local tool: {tool}"}

        methods = {
            "health": self.system_tools.health,
            "cpu": self.system_tools.cpu,
            "memory": self.system_tools.memory,
            "battery": self.system_tools.battery,
            "disk": self.system_tools.disk,
            "system_info": self.system_tools.system_info,
        }

        method = methods.get(action)
        if method is None:
            return {
                "success": False,
                "stage": "execution",
                "tool": tool,
                "action": action,
                "message": f"Unknown system action: {action}",
            }

        try:
            return {
                "success": True,
                "stage": "execution",
                "tool": tool,
                "action": action,
                "data": method(),
            }
        except Exception as exc:
            return {
                "success": False,
                "stage": "execution",
                "tool": tool,
                "action": action,
                "message": str(exc),
            }

    def process(self, command: str):
        request = self.match(command)
        if request is None:
            return {
                "success": False,
                "stage": "matching",
                "tool": None,
                "action": None,
                "message": "No matching local tool found.",
            }
        return self.execute(request)


if __name__ == "__main__":
    print("=" * 60)
    print("MYX TOOL ROUTER TEST")
    print("=" * 60)

    router = ToolRouter()
    tests = [
        "system status",
        "cpu usage",
        "memory status",
        "battery status",
        "disk status",
        "system information",
    ]

    all_passed = True
    for command in tests:
        print()
        print("COMMAND:", command)
        request = router.match(command)
        print("MATCH :", request)
        result = router.execute(request)
        print("RESULT:", result)
        if not result.get("success", False):
            all_passed = False

    print()
    print("TOOL ROUTER : PASS" if all_passed else "TOOL ROUTER : FAIL")
    print("=" * 60)

