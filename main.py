from Ecosystem import Ecosystem

if __name__ == "__main__":
    eco = Ecosystem()

    # eco.digital_twin_population.generate_new_population(size=100)
    # eco.knowledge_generation_engine.update_virtual_register(image_type="prostate")
    eco.knowledge_generation_engine.add_pretrained_model("spleen", "clara_ct_seg_spleen_amp", "1")
    # eco.knowledge_bank.add_model_to_aiaa_server(
    #    "prostate", "clara_train_mri_prostate_cg_and_pz_automl_v1", "0.0.0.0:80")
    # eco.knowledge_bank.process_new_images()

    # Opprette nye modeller til AIAA automatisk
    # Tren automatisk
