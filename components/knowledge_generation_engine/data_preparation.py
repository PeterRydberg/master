import os
import json
import shutil
import tempfile
import random

from scp import SCPClient
from typing import Dict

from SSHClient import SSHClient


KGE_PATH = '/master/components/knowledge_generation_engine/'
EXTERNAL_REGISTERS = 'components\\knowledge_generation_engine\\external_registers'


def prepare_MID_training_data_remote(
    image_type: str,
    task_type: str,
    model: str = "",
    use_existing_mmar: bool = False,
    validation_split: float = 0.3,
    dataset_name: str = "",
    ssh_client: SSHClient = SSHClient()
):
    if(not use_existing_mmar):
        # Clone MMAR to new model
        command = "./components/knowledge_generation_engine/clara/clone_mmar.sh"
        flags = f"-t {image_type} -n {model}"
        ssh_client.run_ssh_command(command=command, flags=flags, docker=True)

    datapath = f"{KGE_PATH}external_registers/medical_image_decathlon/{dataset_name}"
    datalist = {
        "training": [],
        "validation": [],
        "test": []
    }
    environment = {
        "DATA_ROOT": f"{datapath}",
        "DATASET_JSON": f"{KGE_PATH}clara/models/{image_type}/{model}/config/dataset_0.json",
        "PROCESSING_TASK": task_type,
        "MMAR_CKPT_DIR": "models",
        "MMAR_EVAL_OUTPUT_PATH": "eval",
        "PRETRAIN_WEIGHTS_FILE": "/var/tmp/resnet50_weights_tf_dim_ordering_tf_kernels.h5"
    }

    with tempfile.TemporaryDirectory() as dirpath:
        with open(f"{EXTERNAL_REGISTERS}/medical_image_decathlon/{dataset_name}/dataset.json", 'r') as file:
            dataset = json.load(file)
            MID_datalist = dataset["training"]

            val_datalist = random.sample(MID_datalist, round(len(MID_datalist) * validation_split))
            train_datalist = [x for x in MID_datalist if x not in val_datalist]

            datalist["training"] = train_datalist
            datalist["validation"] = val_datalist
            datalist["test"] = dataset["test"]

        # Create datalist config file
        datalist_file = open(f'{dirpath}\\dataset_0.json', "w+")
        json.dump(datalist, datalist_file, indent=4)
        datalist_file.close()

        # Create environment config file
        environment_file = open(f'{dirpath}\\environment.json', "w+")
        json.dump(environment, environment_file, indent=4)
        environment_file.close()

        # Send configs to remote server
        remote_path = f'~/Prosjekter{KGE_PATH}clara/models/{image_type}/{model}'
        scp = SCPClient(ssh_client.get_paramiko_transport())
        scp.put(
            [f'{dirpath}\\dataset_0.json', f'{dirpath}\\environment.json'],
            remote_path=f'{remote_path}/config'
        )
        scp.close()


def prepare_batch_training_data_remote(
    image_type: str,
    task_type: str,
    model: str,
    batch: Dict,
    validation_split: float,
    ssh_client: SSHClient = SSHClient()

):
    datapath = f"{KGE_PATH}clara/models/{image_type}/{model}/data"
    datalist = {
        "training": [],
        "validation": []
    }
    environment = {
        "DATA_ROOT": f"{datapath}",
        "DATASET_JSON": f"{KGE_PATH}clara/models/{image_type}/{model}/config/dataset_0.json",
        "PROCESSING_TASK": task_type,
        "MMAR_CKPT_DIR": "models",
        "MMAR_EVAL_OUTPUT_PATH": "eval",
        "PRETRAIN_WEIGHTS_FILE": "/var/tmp/resnet50_weights_tf_dim_ordering_tf_kernels.h5"
    }

    with tempfile.TemporaryDirectory() as dirpath:
        os.makedirs(os.path.dirname(f'{dirpath}\\data\\train\\'), exist_ok=True)
        os.makedirs(os.path.dirname(f'{dirpath}\\data\\val\\'), exist_ok=True)

        # Create dataset folder
        for i, image in enumerate(batch):
            split = ["training", "train"] if i/len(batch) > validation_split else ["validation", "val"]
            image_path = shutil.copy(
                batch[image]["image_path"],
                f'{dirpath}\\data\\{split[1]}'
            )
            label_path = shutil.copy(
                batch[image][f"{task_type}_path"],
                f'{dirpath}\\data\\{split[1]}'
            )
            image_file = image_path.split('\\')[-1]
            label_file = label_path.split('\\')[-1]
            datalist[f"{split[0]}"].append({
                "image": f'{split[1]}/{image_file}',
                "label": f'{split[1]}/{label_file}'
            })

        # Create datalist config file
        datalist_file = open(f'{dirpath}\\dataset_0.json', "w+")
        json.dump(datalist, datalist_file, indent=4)
        datalist_file.close()

        # Create environment config file
        environment_file = open(f'{dirpath}\\environment.json', "w+")
        json.dump(environment, environment_file, indent=4)
        environment_file.close()

        # Send files to remote server
        remote_path = f'~/Prosjekter{KGE_PATH}clara/models/{image_type}/{model}'
        scp = SCPClient(ssh_client.get_paramiko_transport())
        scp.put(f'{dirpath}\\data', recursive=True, remote_path=remote_path)
        scp.put(
            [f'{dirpath}\\dataset_0.json', f'{dirpath}\\environment.json'],
            remote_path=f'{remote_path}/config'
        )
        scp.close()
