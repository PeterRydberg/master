import React, { ChangeEvent, useState } from "react";
import { MdArrowDownward, MdDeleteForever } from "react-icons/md";
import { useDigitalTwinContext } from "../../../hooks";
import { deleteAWSImage, updateDigitalTwinAttribute } from "../../../services/aws";
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

    const deleteImage = (e: React.MouseEvent<SVGElement, MouseEvent>): void => {
        e.preventDefault();
        deleteAWSImage(
            digitalTwinUuid,
            [
                "dicom_scans",
                "dicom_categories",
                imageType,
                imageUuid
            ],
        ).then((updatedDigitalTwin) => {
            if (updatedDigitalTwin)
                digitalTwinSetters.setFullDigitalTwin(updatedDigitalTwin);
        })
    };

    const imageContent = openImage ? (
        <div className="image-content">
            <div>
                <div className="image-item">
                    <h5 style={{display: "inline", margin: 0}}>Last changed: </h5>
                    {new Date(image.lastchanged).toLocaleDateString()}
                </div>

                <div className="image-item">
                    <h5 style={{display: "inline", margin: 0}}>Image path: </h5>"{image.image_path}"
                </div>
            </div>

            <div>
                <div className="image-item">
                    <h5 style={{display: "inline", margin: 0}}>AIAA segmentation result: </h5>{image.segmentation_path || "Unprocessed"}
                </div>

                <div className="image-item">
                    <h5 style={{display: "inline", margin: 0}}>AIAA inference result: </h5>{image.inference_path || "Unprocessed"}
                </div>
            </div>

            <div className="image-item title">
                <h5 style={{display: "inline", margin: 0}}>Patient consent to information share:</h5>
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
            <div className="title">
                <h4>            
                    <div onClick={() => setOpenImage(!openImage)} className="togglable">
                        Image created {new Date(image.created).toLocaleDateString()} <MdArrowDownward/>
                    </div>
                </h4>
                <MdDeleteForever className="togglable" color="#FF1111" size="2em" onClick={deleteImage}/>  
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
