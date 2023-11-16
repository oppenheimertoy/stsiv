import json

class STSConfig:
    def __init__(self, json_config=None):
        # Aliases are defined internally and not stored in the database
        self.aliases = {
            "tests": "-t",
            "iterations": "-i",
            "workDir": "-w",
            "createResultFiles": "-s",
            "randdataFormat": "-F",
            "bitcount": "-S",
            "numOfThreads": "-T",
            "randdataPath": "-r"
        }

        # Initialize with default values
        self.config = {
            "tests": [0],
            "parameters": {
                "blockFrequencyTestBlockLength": 16384,
                # Initialize other parameters with their default values
            },
            "iterations": 1000,
            "workDir": ".",
            "createResultFiles": "",
            "randdataFormat": "r",
            "bitcount": 1048576,
            "numOfThreads": 1,
            "randdataPath": None
        }

        # Load configuration from JSON if provided
        if json_config:
            self.load_from_json(json_config)

    def load_from_json(self, json_config):
        updated_config = json.loads(json_config)
        self.config.update(updated_config)

    def generate_command(self):
        cmd = ["./bin/sts"]
        # Generate command using aliases and values
        for key, value in self.config.items():
            alias = self.aliases.get(key)
            if alias:
                if isinstance(value, list):
                    value_str = ",".join(map(str, value))
                elif value is not None:
                    value_str = str(value)
                else:
                    continue  # Skip if value is None
                cmd.append(f"{alias} {value_str}")
        return " ".join(cmd)

# Example usage
json_config_from_db = '{"tests": [1,2,3], "iterations": 1000, "workDir": "/path/to/some/dir"}'
sts_config = STSConfig(json_config_from_db)
command = sts_config.generate_command()
print(command)
