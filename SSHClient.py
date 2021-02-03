import json
import os
from copy import copy
import paramiko

from paramiko.client import SSHClient as ParamikoClient

from dotenv import load_dotenv
load_dotenv()


class SSHClient():
    def __init__(self) -> None:
        self.ssh_client: ParamikoClient = ParamikoClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def run_ssh_command(self, command: str, flags: str = "", docker: bool = False, container: str = ""):
        self.ssh_client.connect(
            hostname="heid.idi.ntnu.no",
            username=os.getenv('HEID_USER'),
            password=os.getenv('HEID_PWD'),
        )
        command = f"{command} {flags}"
        full_command = f"docker exec {container} {command}" if docker else command
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh_client.exec_command(full_command)

        for line in ssh_stdout:
            print(line.strip())

        self.ssh_client.close()

    def get_remote_json(self, path):
        self.ssh_client.connect(
            hostname="heid.idi.ntnu.no",
            username=os.getenv('HEID_USER'),
            password=os.getenv('HEID_PWD'),
        )
        sftp_file = self.ssh_client.open_sftp().open(path)
        sftp_file.prefetch()
        file = json.load(sftp_file)
        self.ssh_client.close()

        return file

    def get_paramiko_transport(self):
        self.ssh_client.connect(
            hostname="heid.idi.ntnu.no",
            username=os.getenv('HEID_USER'),
            password=os.getenv('HEID_PWD'),
        )
        return self.ssh_client.get_transport()
