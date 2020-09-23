import React from "react";

import DigitalTwinListElement from "./DigitalTwinListElement";
import { useUsers } from "../../hooks";

import "./styles.css";

function DigitalTwinList({ className }: Props): JSX.Element {
    const users = useUsers();

    if (users === undefined) return <></>;
    if (users === null || !users.length) return <span>No users found.</span>;

    const userList = users.map((user) => (
        <DigitalTwinListElement user={user} key={user.uuid} />
    ));

    return (
        <div className={`digital-twin-list ${className || ""}`}>
            <ul>{userList}</ul>
        </div>
    );
}

interface Props {
    className?: string;
}

export default DigitalTwinList;
