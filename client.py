"""Minimal Aitells client. Free: POST /v1/aitells. Paid detailed report via x402."""
import json, urllib.request

BASE = "https://utils.bigfloppy.net"

def analyze(text: str) -> dict:
    req = urllib.request.Request(BASE + "/v1/aitells", method="POST",
        data=json.dumps({"text": text}).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

def detailed(text: str, x_payment: str | None = None) -> dict:
    headers = {"Content-Type": "application/json"}
    if x_payment:
        headers["X-PAYMENT"] = x_payment
    req = urllib.request.Request(BASE + "/v1/aitells/detailed", method="POST",
        data=json.dumps({"text": text}).encode(), headers=headers)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

if __name__ == "__main__":
    import sys
    text = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(json.dumps(analyze(text), indent=2))
