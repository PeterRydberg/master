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
    value: any;
    share_consent: boolean;
}
