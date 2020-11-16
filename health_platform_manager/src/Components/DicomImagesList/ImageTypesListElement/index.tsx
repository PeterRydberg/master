import React, { useState } from "react";

import { MdArrowDownward } from "react-icons/md";

import { Image } from "../../../types/DicomImages";
import DicomImagesListElement from "../DicomImagesListElement";

import "./styles.css";

function ImageTypesListElement({
    imageType,
    digitalTwinUuid,
    imageList,
    className,
}: Props): JSX.Element {
    const [openList, setOpenList] = useState<boolean>(false);

    const listContent = openList ? (
        <div className="list-content">
            {Object.entries(imageList).map(([imageUuid, image]) => (
                <DicomImagesListElement
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
            className={`image-types-list-element ${className || ""}`}
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

export default ImageTypesListElement;
