export interface DicomScans {
    lastchanged: number;
    dicom_categories: {
        [imageType: string]: {
            [uuid: string]: Image;
        };
    };
}

export interface Image {
    created: number;
    lastchanged: number;
    image_path: string;
    segmentation_path: string;
    inference_path: string;
    share_consent: boolean;
}
