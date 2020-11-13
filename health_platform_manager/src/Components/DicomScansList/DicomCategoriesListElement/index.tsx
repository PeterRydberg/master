import React, { useState } from "react";

import { MdArrowDownward } from "react-icons/md";

import { Image } from "../../../types/DicomScans";
import DicomScansListElement from "../DicomScansListElement";

import "./styles.css";

function DicomCategoriesListElement({
    imageType,
    digitalTwinUuid,
    imageList,
    className,
}: Props): JSX.Element {
    const [openList, setOpenList] = useState<boolean>(false);

    const listContent = openList ? (
        <div className="list-content">
            {Object.entries(imageList).map(([imageUuid, image]) => (
                <DicomScansListElement
                    key={imageUuid}
                    digitalTwinUuid={digitalTwinUuid}
                    imageUuid={imageUuid}
                    image={image}
                    imageType={imageType}
                />
            ))}
        </div>
    ) : (
        <></>
    );

    return (
        <div
            key={imageType}
            className={`dicom-categories-list-element ${className || ""}`}
        >
            <div onClick={() => setOpenList(!openList)} className="togglable">
                <h3>Type {imageType} ({Object.keys(imageList).length} images available) <MdArrowDownward/> </h3>
            </div>
            {listContent}
        </div>
    );
}

interface Props {
    imageType: string;
    digitalTwinUuid: string;
    imageList: { [uuid: string]: Image };
    className?: string;
}

export default DicomCategoriesListElement;
