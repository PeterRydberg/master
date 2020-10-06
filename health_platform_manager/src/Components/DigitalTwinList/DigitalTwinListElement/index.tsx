import React from "react";
import { Link } from "react-router-dom";
import { ListDigitalTwin } from "../../../types/DigitalTwin";

import "./styles.css";

function DigitalTwinListElement({
    digitalTwin,
    className,
}: Props): JSX.Element {
    return (
        <li className={`digital-twin-list-element ${className || ""}`}>
            <Link to={`/digitalTwin/${digitalTwin.uuid}`}>
                {digitalTwin.firstname} {digitalTwin.lastname}
            </Link>
        </li>
    );
}

interface Props {
    digitalTwin: ListDigitalTwin;
    className?: string;
}

export default DigitalTwinListElement;
