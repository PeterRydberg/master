export interface DicomImages {
    lastchanged: number;
    image_types: {
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
    aiaa_consented: boolean;
    aiaa_approved: boolean;
}
