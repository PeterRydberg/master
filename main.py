from components.Ecosystem import Ecosystem


def experiment_1_a():
    eco = Ecosystem()

    eco.knowledge_generation_engine.train_external_dataset(
        image_type="c19_lung_seg",
        task_type="segmentation",
        model="LungSegmentationModel_2",
        use_existing_mmar=True,
        finetune=False,
        gpu="_4gpu",
        validation_split=0.3,
        dataset_name="Task06_Lung"
    )
    # eco.knowledge_bank.add_model_to_aiaa_server("c19_lung_seg", "LungSegmentationModel_2", "0.0.0.0:80")


def experiment_1_b():
    eco = Ecosystem()

    datapath = "/master/components/knowledge_generation_engine/external_registers/medical_image_decathlon/Task06_Lung"

    eco.knowledge_generation_engine.update_virtual_register(image_type="c19_lung_seg")
    eco.knowledge_generation_engine.train_virtual_register_batch(
        image_type="c19_lung_seg",
        task_type="segmentation",
        model="LungSegmentationModel_2_finetuned",
        batch_id=None,
        finetune=True,
        finetune_path=datapath,
        gpu="_2gpu",
        update_batch=False,
        validation_split=0.3
    )
    # eco.knowledge_bank.add_model_to_aiaa_server("c19_lung_seg", "LungSegmentationModel_2_finetuned", "0.0.0.0:80")


def experiment_2():
    pass


def experiment_3():
    pass


if __name__ == "__main__":
    experiment_1_b()

    # eco = Ecosystem()

    # eco.digital_twin_population.generate_new_population(size=100)
    # eco.knowledge_generation_engine.update_virtual_register(image_type="prostate")
    # eco.knowledge_generation_engine.add_pretrained_model("prostate", "clara_train_mri_prostate_cg_and_pz_automl", "1")
    # eco.knowledge_bank.add_model_to_aiaa_server("prostate", "clara_train_mri_prostate_cg_and_pz_automl", "0.0.0.0:80")
    # eco.knowledge_bank.process_new_images()
    # eco.knowledge_generation_engine.train_virtual_register_batch(
    #     image_type="prostate",
    #     task_type="segmentation",
    #     model=None,
    #     model_ver=None,
    #     batch_id=None,
    #     finetune=True,
    #     gpu="",
    #     update_batch=False,
    #     validation_split=0.3
    # )
