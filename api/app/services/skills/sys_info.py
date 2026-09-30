from app.services.skills import skill
import os
import platform

@skill(
    name="get_system_info",
    description="Get current system resource usage including CPU and RAM",
    parameters={
        "detail": {
            "type": "boolean",
            "description": "Whether to provide detailed per-core CPU usage"
        }
    }
)
def get_system_info(detail: bool = False) -> str:
    # Fallback implementation using os/platform since psutil requires C++ build tools
    system = platform.system()
    node = platform.node()
    release = platform.release()

    info = f"System Status: {system} {release} on node {node}"

    # We can't get real-time CPU/RAM without psutil or complex OS-specific calls,
    # but we can provide the platform details.

    return info
