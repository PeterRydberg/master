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


def prepare_LUNA16_training_data_remote(
    image_type: str,
    task_type: str,
    model: str = "",
    use_existing_mmar: bool = False,
    validation_split: float = 0.3,
    dataset_subsets: list[str] = [""],
    ssh_client: SSHClient = SSHClient()
):
    if(not use_existing_mmar):
        # Clone MMAR to new model
        command = "./components/knowledge_generation_engine/clara/clone_mmar.sh"
        flags = f"-t {image_type} -n {model}"
        ssh_client.run_ssh_command(command=command, flags=flags, docker=True, container="aiaa")

    mmar_path = f"{KGE_PATH}clara/models/{image_type}/{model}"
    datapath = f"{KGE_PATH}external_registers/LUNA16/"
    datalist = {
        "training": [],
        "validation": [],
        "test": []
    }
    environment = {
        "DATA_ROOT": f"{datapath}",
        "DATASET_JSON": f"{mmar_path}/config/dataset_0.json",
        "PROCESSING_TASK": task_type,
        "MMAR_CKPT_DIR": "models",
        "MMAR_EVAL_OUTPUT_PATH": "eval",
        "PRETRAIN_WEIGHTS_FILE": "/var/tmp/resnet50_weights_tf_dim_ordering_tf_kernels.h5"
    }

    with tempfile.TemporaryDirectory() as dirpath:
        for dir in dataset_subsets:
            directory = f"{EXTERNAL_REGISTERS}/LUNA16/{dir}"
            data_pairs = [{
                "image": f"./{dir}-conv/{filename.split('.mhd')[0]}.nii.gz",
                "label": f"./seg-lungs-LUNA16-conv/{filename.split('.mhd')[0]}.nii.gz"
            } for filename in os.listdir(directory) if filename.endswith(".mhd")]

            val_datalist = random.sample(data_pairs, round(len(data_pairs) * validation_split))
            train_datalist = [x for x in data_pairs if x not in val_datalist]

            datalist["training"].extend(train_datalist)
            datalist["validation"].extend(val_datalist)

        # Create datalist config file
        datalist_file = open(f'{dirpath}\\dataset_0.json', "w+")
        json.dump(datalist, datalist_file, indent=4)
        datalist_file.close()

        # Create environment config file
        environment_file = open(f'{dirpath}\\environment.json', "w+")
        json.dump(environment, environment_file, indent=4)
        environment_file.close()

        # Send configs to remote server
        remote_path = f'/data/hmrydber{mmar_path}'
        scp = SCPClient(ssh_client.get_paramiko_transport())
        scp.put(
            [f'{dirpath}\\dataset_0.json', f'{dirpath}\\environment.json'],
            remote_path=f'{remote_path}/config'
        )
        scp.close()


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
        ssh_client.run_ssh_command(command=command, flags=flags, docker=True, container="aiaa_training")

    mmar_path = f"{KGE_PATH}clara/models/{image_type}/{model}"
    datapath = f"{KGE_PATH}external_registers/medical_image_decathlon/{dataset_name}"
    datalist = {
        "training": [],
        "validation": [],
        "test": []
    }
    environment = {
        "DATA_ROOT": f"{datapath}",
        "DATASET_JSON": f"{mmar_path}/config/dataset_0.json",
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
        remote_path = f'/data/hmrydber{mmar_path}'
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
    batch: Dict[str, Dict],
    finetune_path: str,
    validation_split: float,
    ssh_client: SSHClient = SSHClient()
):
    mmar_path = f"{KGE_PATH}clara/models/{image_type}/{model}"

    remote_dataset: dict[str, list] = ssh_client.get_remote_json(f'{mmar_path}/config/dataset_0.json')
    datalist = remote_dataset
    environment = {
        "DATA_ROOT": finetune_path,
        "DATASET_JSON": f"{mmar_path}/config/dataset_1.json",
        "PROCESSING_TASK": task_type,
        "MMAR_CKPT_DIR": "models",
        "MMAR_EVAL_OUTPUT_PATH": "eval",
        "PRETRAIN_WEIGHTS_FILE": "/var/tmp/resnet50_weights_tf_dim_ordering_tf_kernels.h5"
    }

    def add_image(image: str, type: str, folder: str):
        image_path = shutil.copy(
            batch[image]["image_path"],
            f'{dirpath}\\finetune\\{folder}'
        )
        label_path = shutil.copy(
            batch[image][f"{task_type}_path"],
            f'{dirpath}\\finetune\\{folder}'
        )
        image_file = image_path.split('\\')[-1]
        label_file = label_path.split('\\')[-1]
        datalist[type].append({
            "image": f'./finetune/{folder}/{image_file}',
            "label": f'./finetune/{folder}/{label_file}'
        })

    with tempfile.TemporaryDirectory() as dirpath:
        os.makedirs(os.path.dirname(f'{dirpath}\\finetune\\train\\'), exist_ok=True)
        os.makedirs(os.path.dirname(f'{dirpath}\\finetune\\val\\'), exist_ok=True)

        val_datalist = random.sample(batch.keys(), round(len(batch) * validation_split))
        train_datalist = [x for x in batch.keys() if x not in val_datalist]

        [add_image(image, "training", "train") for image in train_datalist]
        [add_image(image, "validation", "val") for image in val_datalist]

        # Create datalist config file
        datalist_file = open(f'{dirpath}\\dataset_1.json', "w+")
        json.dump(datalist, datalist_file, indent=4)
        datalist_file.close()

        # Create environment config file
        environment_file = open(f'{dirpath}\\environment.json', "w+")
        json.dump(environment, environment_file, indent=4)
        environment_file.close()

        # Send files to remote server
        remote_path = f'/data/hmrydber{mmar_path}'
        scp = SCPClient(ssh_client.get_paramiko_transport())
        scp.put(f'{dirpath}\\finetune', recursive=True, remote_path=f'/data/hmrydber{finetune_path}')
        scp.put(
            [f'{dirpath}\\dataset_1.json', f'{dirpath}\\environment.json'],
            remote_path=f'{remote_path}/config'
        )
        scp.close()
