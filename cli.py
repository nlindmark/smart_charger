#!/usr/bin/env python3
"""Command-line interface for interacting with a Chargeamps Halo charger."""

import argparse
import json
from halo_client import HaloClient


def main() -> None:
    parser = argparse.ArgumentParser(description="Interact with Chargeamps Halo charger")
    parser.add_argument("--host", required=True, help="Base URL of the charger API")
    parser.add_argument("--api-key", required=True, help="API key for authentication")
    parser.add_argument("--charger-id", required=True, help="ID of the charger to control")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("status", help="Show charger status")
    subparsers.add_parser("start", help="Start charging")
    subparsers.add_parser("stop", help="Stop charging")

    args = parser.parse_args()

    client = HaloClient(args.host, args.api_key)

    if args.command == "status":
        result = client.get_status(args.charger_id)
        print(json.dumps(result, indent=2))
    elif args.command == "start":
        client.start_charging(args.charger_id)
        print("Charging started")
    elif args.command == "stop":
        client.stop_charging(args.charger_id)
        print("Charging stopped")


if __name__ == "__main__":
    main()
