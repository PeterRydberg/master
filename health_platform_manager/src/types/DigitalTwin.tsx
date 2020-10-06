import { DicomScans } from "./DicomScans";

export interface DigitalTwin {
    uuid: string;
    age: number;
    sex: string;
    firstname: string;
    lastname: string;
    conditions: string[];
    dicom_scans: DicomScans;
}

export interface ListDigitalTwin {
    uuid: string;
    firstname: string;
    lastname: string;
}
