from components.Ecosystem import Ecosystem


def experiment_1():
    eco = Ecosystem()

    # eco.knowledge_generation_engine.add_pretrained_model(
    #     "prostate", "clara_train_mri_prostate_cg_and_pz_automl", "1")
    # eco.knowledge_bank.add_model_to_aiaa_server("c19_lung_seg", "clara_train_covid19_ct_lung_seg", "0.0.0.0:80")
    # eco.knowledge_generation_engine.update_virtual_register(image_type="prostate")
    # eco.knowledge_generation_engine.train_external_dataset(
    #     image_type="prostate",
    #     task_type="segmentation",
    #     model="ProstateSegmentationModel",
    #     finetune=False,
    #     gpu="",
    #     validation_split=0.3,
    #     dataset_name="Task05_Prostate"
    # )
    # eco.knowledge_bank.add_model_to_aiaa_server("spleen", "clara_ct_seg_spleen_amp", "0.0.0.0:80")


def experiment_2():
    pass


def experiment_3():
    pass


if __name__ == "__main__":
    experiment_1()

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
