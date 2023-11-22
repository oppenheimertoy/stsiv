"""
"""
import subprocess
from typing import Optional

from app.services.argument_parser.args_parser_extended import STSConfig


class STSProcessController:
    """_summary_
    """

    def __init__(self, config: STSConfig):
        self.config: STSConfig = config
        self.process: Optional[subprocess.Popen] = None

    def start_process(self):
        """
        Starts the subprocess using the command from STSConfig.
        """
        command = self.config.generate_command()
        self.process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def get_output(self):
        """
        Gets the output of the subprocess.
        """
        if self.process:
            stdout, stderr = self.process.communicate()
            return stdout.decode(), stderr.decode()
        return None, None

    def is_running(self):
        """
        Checks if the subprocess is still running.
        """
        if self.process:
            return self.process.poll() is None
        return False

    def stop_process(self):
        """
        Stops the subprocess.
        """
        if self.process and self.is_running():
            self.process.terminate()
