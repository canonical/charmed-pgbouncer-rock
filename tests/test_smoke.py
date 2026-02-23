# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.
import subprocess

import yaml


def test_upload():
    with open("rockcraft.yaml") as file:
        rockcraft = yaml.safe_load(file)
        name = rockcraft["name"]
        version = rockcraft["version"]

        subprocess.run([
            "rockcraft.skopeo",
            "copy",
            f"oci-archive:{name}_{version}_amd64.rock",
            f"docker-daemon:{name}:test",
        ])


def test_all_apps():
    with open("rockcraft.yaml") as file:
        rockcraft = yaml.safe_load(file)
        name = rockcraft["name"]

        override = {
            "pgbackrest": "version",
        }

        apps = [
            "/usr/sbin/pgbouncer",
            "/usr/bin/psql",
        ]

        for app in apps:
            print(f"Running {app}...")
            try:
                subprocess.check_output([
                    "docker",
                    "run",
                    "--entrypoint",
                    app,
                    f"{name}:test",
                    override.get(app, "--help"),
                ])
            except subprocess.CalledProcessError as e:
                print(e)
                raise e


def test_version():
    with open("rockcraft.yaml") as file:
        rockcraft = yaml.safe_load(file)
        name = rockcraft["name"]
        version = rockcraft["version"]
        app_version = ".".join(
            subprocess
            .check_output([
                "docker",
                "run",
                "--entrypoint",
                "/usr/sbin/pgbouncer",
                f"{name}:test",
                "--version",
            ])
            .decode()
            .split()[1]
            .split(".")[:-1]
        )
        assert version == app_version
