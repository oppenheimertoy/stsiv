"""
"""
import json
from pathlib import Path
from uuid import UUID


class STSConfig:
    """_summary_
    """

    def __init__(self, version_id: UUID, json_config=None):
        # Initialize with default values
        self.file_path: str = str(self._create_path(
            version_id, 'data', self.get_file_name(version_id)))
        self.work_dir: str = str(self._create_path(version_id, 'result', ''))
        self.config = {
            "debuglevel": {"alias": "-v", "value": 1},
            "reportCycle": {"alias": "-I", "value": 1},
            "tests": {"alias": "-t", "value": [0]},
            "parameters": {
                "alias": "-P",
                "blockFrequencyTestBlockLength": {"id": "1", "value": 16384},
                "nonOverlappingTemplateTestBlockLength": {"id": "2", "value": 9},
                "overlappingTemplateTestBlockLength": {"id": "3", "value": 9},
                "approximateEntropyTestBlockLength": {"id": "4", "value": 10},
                "serialTestBlockLength": {"id": "5", "value": 16},
                "linearComplexityTestBlockLength": {"id": "6", "value": 500},
                "numberOfBitcountRuns": {"id": "7", "value": 1},
                "bitsToProcessPerIteration": {"id": "9", "value": 1048576},
                "uniformityCutoffLevel": {"id": "10", "value": 0.0001},
                "alphaConfidenceLevel": {"id": "11", "value": 0.01}
            },
            "iterations": {"alias": "-i", "value": 1000},
            "workDir": {"alias": "-w", "value": self.work_dir},
            "createResultFiles": {"alias": "-s", "value": ""},
            "bitcount": {"alias": "-S", "value": 1048576},
            "numOfThreads": {"alias": "-T", "value": 2},
        }

        # Load configuration from JSON if provided
        if json_config:
            self.load_from_json(json_config)

    def get_file_name(self, version_id: UUID):
        """_summary_

        Args:
            version_id (UUID): _description_

        Raises:
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        data_dir = self._create_path(version_id, 'data', '')
        files = list(data_dir.glob('*'))  # List all files in the directory
        if len(files) == 1:
            return files[0].name  # Return the name of the file
        else:
            raise ValueError(
                f"Expected exactly one file in {data_dir}, found {len(files)}")

    def _create_path(self, version_id: UUID, subdirectory: str, file_name: str):
        """_summary_

        Args:
            version_id (UUID): _description_
            subdirectory (str): _description_
            file_name (str): _description_

        Returns:
            _type_: _description_
        """
        base_dir = Path('.') / 'result'
        full_path = base_dir / str(version_id) / subdirectory / file_name
        return full_path

    def load_from_json(self, json_config):
        """_summary_

        Args:
            json_config (_type_): _description_

        Raises:
            ValueError: _description_
        """
        if isinstance(json_config, str) or isinstance(json_config, bytearray):
            updated_config = json.loads(json_config)
        elif isinstance(json_config, dict):
            updated_config = json_config
        else:
            raise ValueError("Unsupported type for json_config")

        self.deep_update(self.config, updated_config)

    def deep_update(self, original, update):
        """_summary_

        Args:
            original (_type_): _description_
            update (_type_): _description_

        Returns:
            _type_: _description_
        """
        for key, value in update.items():
            if isinstance(value, dict):
                original[key] = self.deep_update(original.get(key, {}), value)
            else:
                original[key] = value
        return original

    def generate_command(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        cmd = ["./bin/sts"]
        # Generate command using aliases and values
        for key, section in self.config.items():
            alias = section.get("alias")
            if key == "parameters":
                param_values = self.generate_parameters_command(section)
                if param_values:
                    cmd.append(f"{alias} {param_values}")
            elif alias:
                value = section.get("value")
                if isinstance(value, list):
                    value_str = ",".join(map(str, value))
                else:
                    value_str = str(value)
                cmd.append(f"{alias} {value_str}")
        if self.file_path:
            cmd.append(str(self.file_path))
        return " ".join(cmd)

    def generate_parameters_command(self, parameters):
        """_summary_

        Args:
            parameters (_type_): _description_

        Returns:
            _type_: _description_
        """
        param_cmd = []
        for param_key, param_value in parameters.items():
            if param_key != "alias" and "id" in param_value:
                param_cmd.append(f"{param_value['id']}={param_value['value']}")
        return ','.join(param_cmd)
