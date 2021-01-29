import React, { useState } from "react";
import { useDigitalTwinContext } from "../../hooks";

import { addAWSImage } from "../../services/aws";
import { DicomImages } from "../../types/DicomImages";
import ImageTypesListElement from "./ImageTypesListElement";

import "./styles.css";

function useInput(
    inputProps: FileProps,
    inputType?: string
): { inputValue: string; inputElement: JSX.Element } {
    const [inputValue, setInputValue] = useState<string>("");

    /*if (inputType)
        inputProps["accept"] = `${inputType}\\${inputProps["accept"]
            .split("\\")
            .pop()}`;*/

    const inputElement = (
        <input
            {...inputProps}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
        />
    );
    return { inputValue, inputElement };
}

function useSelect(
    selectProps: DropdownProps,
    options: string[]
): { selectValue: string; selectElement: JSX.Element } {
    const [selectValue, setSelectValue] = useState(options[0]);
    const selectElement = (
        <select
            {...selectProps}
            value={selectValue}
            onChange={(e) => setSelectValue(e.target.value)}
        >
            {options.map((element) => (
                <option key={element} value={element}>
                    {element}
                </option>
            ))}
        </select>
    );
    return { selectValue, selectElement };
}

function createFilePath(
    filename: string,
    filetype: string,
    full?: boolean
): string {
    const paths = filename.split("\\");
    const file = paths ? paths[paths.length - 1] : "";

    const ending = `${process.env.REACT_APP_DATA_SOURCE_PATH}${filetype}\\images\\${file}`;
    if (full) return `${process.env.REACT_APP_FULL_DIRECTORY_PATH}${ending}`;
    return `${ending}`;
}

const fileProps: FileProps = {
    type: "file",
    id: "image_paths",
    accept: ".nii.gz",
    multiple: false,
};

const dropdownProps: DropdownProps = {
    autoFocus: false,
    disabled: false,
    multiple: false,
    required: true,
};

const dropdownOptions: string[] = [
    "heart",
    "braintumour",
    "hippocampus",
    "prostate",
    "spleen",
    "c19_lung_seg"
];

function DicomImagesList({ uuid, dicomImages, className }: Props): JSX.Element {
    const { selectValue, selectElement } = useSelect(
        dropdownProps,
        dropdownOptions
    );
    const { inputValue, inputElement } = useInput(fileProps, selectValue);
    const [, digitalTwinSetters] = useDigitalTwinContext(); // Should use digitalTwin directly, might fix later

    const content = !Object.keys(dicomImages.image_types).length ? (
        <span>No DICOM images to show.</span>
    ) : (
        <div className="image-types-list">
            {Object.entries(dicomImages.image_types).map(
                ([imageType, imageList]) => (
                    <ImageTypesListElement
                        key={imageType}
                        imageType={imageType}
                        digitalTwinUuid={uuid}
                        imageList={imageList}
                    />
                )
            )}
        </div>
    );

    const addImage = (): void => {
        const image = {
            created: Date.now(),
            lastchanged: Date.now(),
            image_path: createFilePath(inputValue, selectValue, false),
            segmentation_path: "",
            inference_path: "",
            aiaa_consented: false,
            aiaa_approved: false
        };

        addAWSImage(uuid, selectValue, image).then((updatedDigitalTwin) => {
            if (updatedDigitalTwin)
                digitalTwinSetters.setFullDigitalTwin(updatedDigitalTwin);
        });
    };

    return (
        <div className={`dicom-images ${className || ""}`}>
            {content}
            <div className="image-adder">
                <label>Add image: </label>
                {selectElement}
                {inputElement}
                <button
                    disabled={!inputValue || !selectValue}
                    onClick={addImage}
                >
                    Submit
                </button>
            </div>
        </div>
    );
}

interface Props {
    uuid: string;
    dicomImages: DicomImages;
    className?: string;
}

interface FileProps {
    type: string;
    id: string;
    accept: string;
    multiple: boolean;
}

interface DropdownProps {
    autoFocus: boolean;
    disabled: boolean;
    multiple: boolean;
    required: boolean;
}

export default DicomImagesList;
