import os
import json
import urllib.request
import urllib.error

print("=" * 60)
print("GEMINI DIRECT REST TEST")
print("=" * 60)

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("RESULT: NO API KEY")
    raise SystemExit(1)

print("KEY SET: True")
print("KEY LENGTH:", len(api_key))
print("ASCII:", api_key.isascii())

url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

payload = {
    "contents": [
        {
            "parts": [
                {
                    "text": "Reply with exactly: Gemini REST connection working."
                }
            ]
        }
    ]
}

data = json.dumps(payload).encode("utf-8")

request = urllib.request.Request(
    url,
    data=data,
    headers={
        "Content-Type": "application/json",
        "x-goog-api-key": api_key,
    },
    method="POST",
)

try:
    with urllib.request.urlopen(request, timeout=30) as response:
        raw = response.read().decode("utf-8")
        result = json.loads(raw)

        print("HTTP STATUS:", response.status)
        print("RAW RESPONSE:", raw)

        text = ""

        try:
            text = result["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            pass

        print("MODEL RESPONSE:", text)

        if text:
            print("GEMINI DIRECT REST : PASS")
        else:
            print("GEMINI DIRECT REST : FAIL")

except urllib.error.HTTPError as e:
    body = e.read().decode("utf-8", errors="replace")

    print("HTTP STATUS:", e.code)
    print("SERVER RESPONSE:", body)
    print("GEMINI DIRECT REST : FAIL")

except Exception as e:
    print("ERROR:", repr(e))
    print("GEMINI DIRECT REST : FAIL")

print("=" * 60)
