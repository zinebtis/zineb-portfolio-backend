import json

import httpx


def main() -> None:
    url = "http://127.0.0.1:8000/api/chat"
    payload = {
        "query": "What is your research focus?",
        "client_id": "test-user",
    }
    response = httpx.post(url, json=payload, timeout=30)
    print("Status:", response.status_code)
    try:
        print(json.dumps(response.json(), indent=2))
    except Exception:
        print(response.text)


if __name__ == "__main__":
    main()
