import json
import urllib.request

class HaloClient:
    """Simple client for Chargeamps Halo charger API."""

    def __init__(self, host: str, api_key: str):
        self.host = host.rstrip('/')
        self.api_key = api_key

    def _request(self, method: str, path: str, data: dict | None = None):
        url = f"{self.host}{path}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        body = None
        if data is not None:
            body = json.dumps(data).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=body,
            headers=headers,
            method=method,
        )
        with urllib.request.urlopen(req) as resp:
            resp_body = resp.read()
            if not resp_body:
                return None
            return json.loads(resp_body.decode())

    def get_status(self, charger_id: str):
        """Return charger status."""
        return self._request("GET", f"/api/chargers/{charger_id}/status")

    def start_charging(self, charger_id: str):
        """Start charging."""
        return self._request("POST", f"/api/chargers/{charger_id}/charge/start")

    def stop_charging(self, charger_id: str):
        """Stop charging."""
        return self._request("POST", f"/api/chargers/{charger_id}/charge/stop")
