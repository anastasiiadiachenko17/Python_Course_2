"""Combine the device list with the lab environment descriptions."""

import json

import yaml

DEVICES_FILE = "devices.yaml"
LAB_ENVS_FILE = "lab_envs.json"
COMBINED_FILE = "combined_devices.yaml"


def combine_devices(devices, lab_envs):
    """Return the devices with their lab environment filled in.

    Args:
        devices: Mapping of a device name to its attributes.
        lab_envs: Mapping of an environment name to its description.

    Returns:
        A new mapping where lab_env holds the description of the
        environment of the device, or None when the environment is
        not described in lab_envs.

    Raises:
        TypeError: If the attributes of a device are not a mapping.
        KeyError: If a device has no lab_env attribute.
    """
    combined = {}

    for device, attributes in devices.items():
        if not isinstance(attributes, dict):
            raise TypeError(f"Device {device!r} has no attributes.")

        if "lab_env" not in attributes:
            raise KeyError(f"Device {device!r} has no lab_env attribute.")

        combined[device] = dict(attributes)
        combined[device]["lab_env"] = lab_envs.get(attributes["lab_env"])

    return combined


def combine_files(
    devices_path=DEVICES_FILE,
    lab_envs_path=LAB_ENVS_FILE,
    combined_path=COMBINED_FILE,
):
    """Read both input files and write the combined YAML file.

    Args:
        devices_path: Path to the YAML file that lists the devices.
        lab_envs_path: Path to the JSON file that describes the
            lab environments.
        combined_path: Path of the YAML file to write.
    """
    try:
        with open(devices_path, encoding="utf-8") as devices_file:
            devices = yaml.safe_load(devices_file)

        with open(lab_envs_path, encoding="utf-8") as lab_envs_file:
            lab_envs = json.load(lab_envs_file)
    except FileNotFoundError as error:
        print(f"Input file is missing: {error.filename!r}")
        return
    except (yaml.YAMLError, json.JSONDecodeError) as error:
        print(f"Input file cannot be parsed: {error}")
        return

    combined = combine_devices(devices or {}, lab_envs or {})

    with open(combined_path, "w", encoding="utf-8") as combined_file:
        yaml.safe_dump(combined, combined_file, sort_keys=False)

    print(f"Wrote {len(combined)} devices to {combined_path!r}.")


if __name__ == "__main__":
    combine_files()
