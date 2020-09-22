import React from "react";

import { User } from "../../../types/User";

import "./styles.css";

function DigitalTwinListElement({ user, className }: Props): JSX.Element {
    return (
        <li
            key={user.uuid}
            className={`digital-twin-list-element ${className || ""}`}
        >
            <a href={`/user/${user.uuid}`}>
                {user.firstname} {user.lastname}
            </a>
        </li>
    );
}

interface Props {
    user: User;
    className?: string;
}

export default DigitalTwinListElement;
