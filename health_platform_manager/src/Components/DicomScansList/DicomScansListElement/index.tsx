import React, { ChangeEvent, useState } from "react";
import { useDigitalTwinContext } from "../../../hooks";
import { updateDigitalTwinAttribute } from "../../../services/aws";
import { Image } from "../../../types/DicomScans";

import "./styles.css";

function DicomScansListElement({
    digitalTwinUuid,
    imageUuid,
    image,
    imageType,
    className,
}: Props): JSX.Element {
    const [openImage, setOpenImage] = useState<boolean>(false);
    const [, digitalTwinSetters] = useDigitalTwinContext(); // Should use digitalTwin directly, might fix later

    const toggleConsent = (e: ChangeEvent<HTMLInputElement>): void => {
        e.preventDefault();
        const newState: boolean = !image.share_consent ? true : false;
        updateDigitalTwinAttribute(
            digitalTwinUuid,
            [
                "dicom_scans",
                "dicom_categories",
                imageType,
                imageUuid,
                "share_consent",
            ],
            newState
        ).then((updatedDigitalTwin) => {
            if (updatedDigitalTwin)
                digitalTwinSetters.setFullDigitalTwin(updatedDigitalTwin);
        });
    };

    const imageContent = openImage ? (
        <div className="image-content">
            <div className="image-item">
                <label>Last changed: </label>
                {new Date(image.lastchanged).toLocaleDateString()}
            </div>

            <div className="image-item">
                <label>Content path: </label>"{image.image_path}"
            </div>

            <div className="image-item">
                <label>AIAA segmentation result: </label>{image.segmentation_path || "Unprocessed"}
            </div>

            <div className="image-item">
                <label>AIAA inference result: </label>{image.inference_path || "Unprocessed"}
            </div>

            <div className="image-item">
                <label>Patient consent to information share:</label>
                <input
                    type="checkbox"
                    name="consent"
                    id="consent-checkbox"
                    value="Consent"
                    checked={image.share_consent ? true : false}
                    onChange={toggleConsent}
                />
            </div>
        </div>
    ) : (
        <></>
    );

    return (
        <div
            key={imageUuid}
            className={`dicom-scans-list-element ${className || ""}`}
        >
            <div onClick={() => setOpenImage(!openImage)} className="togglable">
                <h4>
                    Image created {new Date(image.created).toLocaleDateString()}{" "}
                    ⬇
                </h4>
            </div>

            {imageContent}
        </div>
    );
}

interface Props {
    digitalTwinUuid: string;
    imageUuid: string;
    image: Image;
    imageType: string;
    className?: string;
}

export default DicomScansListElement;
