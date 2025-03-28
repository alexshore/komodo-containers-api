from fastapi import FastAPI, Request
import httpx
import os

KOMODO_URL = os.environ.get("KOMODO_URL", None)

KOMODO_STATE_MAP = {
    "empty": "stopped",
    "created": "stopped",
    "running": "running",
    "paused": "stopped",
    "restarting": "stopped",
    "removing": "stopped",
    "exited": "stopped",
    "dead": "stopped",
}

app = FastAPI()


@app.get("/containers")
async def containers(request: Request):
    if KOMODO_URL is None:
        return {
            "error": "Must provide KOMODO_URL in docker env vars.",
            "status_code": 400,
        }

    headers = {
        key: value
        for key, value in request.headers.items()
        if key in ["x-api-key", "x-api-secret"]
    }

    async with httpx.AsyncClient() as client:
        komodo_response = await client.post(
            f"{KOMODO_URL}/read",
            headers=headers,
            json={
                "type": "ListAllDockerContainers",
                "params": {},
            },
        )

    if komodo_response.status_code != 200:
        print(komodo_response)
        return {
            "error": f"Something went wrong accessing {KOMODO_URL}",
            "status_code": 500,
        }

    response = {"running": 0, "stopped": 0, "total": 0}

    for container in komodo_response.json():
        response["total"] += 1
        response[KOMODO_STATE_MAP[container["state"]]] += 1

    return response
