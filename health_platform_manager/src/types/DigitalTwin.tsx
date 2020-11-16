import { DicomImages } from "./DicomImages";

export interface DigitalTwin {
    uuid: string;
    age: number;
    sex: string;
    firstname: string;
    lastname: string;
    conditions: string[];
    dicom_images: DicomImages;
}

export interface ListDigitalTwin {
    uuid: string;
    firstname: string;
    lastname: string;
}
