import React from "react";
import { useParams } from "react-router-dom";
import AppendicesList from "../../Components/DigitalTwinList/AppendicesList";
import { useUser } from "../../hooks";

import { User } from "../../types/User";

import "./styles.css";

function capitalize(str: string) {
    return str[0].toUpperCase() + str.slice(1);
}

function UserPage({ className }: Props): JSX.Element {
    const { userUuid } = useParams<{ userUuid: string }>();
    const user = useUser(userUuid);

    if (user === undefined) return <></>;
    if (user === null) return <span>User data not found.</span>;

    return (
        <div className={`main-page ${className || ""}`}>
            <h1>
                {user.firstname} {user.lastname}
            </h1>
            <div className="personalia">
                <h2>Age</h2>
                <span>{user.age}</span>

                <h2>Sex</h2>
                <span>{capitalize(user.sex)}.</span>

                <h2>Conditions</h2>
                {user.conditions.length ? (
                    <ul>
                        {user.conditions.map((condition) => (
                            <li>{condition}</li>
                        ))}
                    </ul>
                ) : (
                    <span>No conditions to show.</span>
                )}

                <h2>Appendices</h2>
                <AppendicesList appendices={user.appendices} />
            </div>
        </div>
    );
}

interface Props {
    user: User;
    className?: string;
}

export default UserPage;
