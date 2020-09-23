import React from "react";
import { useParams } from "react-router-dom";
import { useUser } from "../../hooks";

import { User } from "../../types/User";

import "./styles.css";

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
            <p>{JSON.stringify(user)}</p>
        </div>
    );
}

interface Props {
    user: User;
    className?: string;
}

export default UserPage;
