# smart_charger

This repository contains a simple Python client for interacting with a Chargeamps Halo charger.

## Requirements

The scripts rely only on the Python standard library and therefore do not require any third-party packages.

## Usage

The `cli.py` script provides a small command-line interface. The charger must expose an HTTP API compatible with the endpoints used in `halo_client.py`.

```bash
python3 cli.py --host http://halo.local --api-key YOUR_KEY --charger-id CHARGER_ID status
```

Supported commands are:

- `status` – display current charger status
- `start` – begin charging
- `stop` – stop charging

See `halo_client.py` for the API calls performed.
