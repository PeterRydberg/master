import React from "react";
import { Link } from "react-router-dom";

import { User } from "../../../types/User";

import "./styles.css";

function DigitalTwinListElement({ user, className }: Props): JSX.Element {
    return (
        <li className={`digital-twin-list-element ${className || ""}`}>
            <Link to={`/user/${user.uuid}`}>
                {user.firstname} {user.lastname}
            </Link>
        </li>
    );
}

interface Props {
    user: User;
    className?: string;
}

export default DigitalTwinListElement;
