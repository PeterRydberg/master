import React from "react";
import { Link, useParams } from "react-router-dom";
import {MdArrowBack} from 'react-icons/md'

import DicomScansList from "../../Components/DicomScansList";
import { useDigitalTwin, DigitalTwinContext } from "../../hooks";
import { DigitalTwin } from "../../types/DigitalTwin";

import "./styles.css";

function capitalize(str: string) {
    return str[0].toUpperCase() + str.slice(1);
}

function DigitalTwinPage({ className }: Props): JSX.Element {
    const { digitalTwinUuid } = useParams<{ digitalTwinUuid: string }>();
    const [digitalTwin, digitalTwinSetters] = useDigitalTwin(digitalTwinUuid);

    if (digitalTwin === undefined) return <></>;
    if (digitalTwin === null) return <span>DigitalTwin data not found.</span>;

    return (
        <DigitalTwinContext.Provider value={[digitalTwin, digitalTwinSetters]}>
            <div className={`digital-twin-page ${className || ""}`}>
                <Link to="/" className="home-icon">
                    <MdArrowBack/>
                </Link>
                <h1>
                    {digitalTwin.firstname} {digitalTwin.lastname}
                </h1>
                <div className="personalia">
                    <div className="personalia-item">
                        <h2>Age</h2>
                        <span>{digitalTwin.age}</span>
                    </div>

                    <div className="personalia-item">
                        <h2>Sex</h2>
                        <span>{capitalize(digitalTwin.sex)}.</span>
                    </div>

                    <div className="personalia-item">
                        <h2>Conditions</h2>
                        {digitalTwin.conditions.length ? (
                            <ul>
                                {digitalTwin.conditions.map((condition) => (
                                    <li>{condition}</li>
                                ))}
                            </ul>
                        ) : (
                            <span>No conditions to show.</span>
                        )}
                    </div>

                    <div className="personalia-item fullwidth">
                        <h2>DICOM scans</h2>
                        <DicomScansList
                            uuid={digitalTwin.uuid}
                            dicomScans={digitalTwin.dicom_scans}
                        />
                    </div>
                </div>
            </div>
        </DigitalTwinContext.Provider>
    );
}

interface Props {
    digitalTwin: DigitalTwin;
    className?: string;
}

export default DigitalTwinPage;
