import React from "react";
import { Link, useParams } from "react-router-dom";

import AppendicesList from "../../Components/AppendicesList";
import { useUser, UserContext } from "../../hooks";
import { User } from "../../types/User";

import "./styles.css";

function capitalize(str: string) {
    return str[0].toUpperCase() + str.slice(1);
}

function UserPage({ className }: Props): JSX.Element {
    const { userUuid } = useParams<{ userUuid: string }>();
    const [user, userSetters] = useUser(userUuid);

    if (user === undefined) return <></>;
    if (user === null) return <span>User data not found.</span>;

    return (
        <UserContext.Provider value={[user, userSetters]}>
            <div className={`main-page ${className || ""}`}>
                <Link to="/" className="home-icon">
                    ⬅
                </Link>
                <h1>
                    {user.firstname} {user.lastname}
                </h1>
                <div className="personalia">
                    <div className="personalia-item">
                        <h2>Age</h2>
                        <span>{user.age}</span>
                    </div>

                    <div className="personalia-item">
                        <h2>Sex</h2>
                        <span>{capitalize(user.sex)}.</span>
                    </div>

                    <div className="personalia-item">
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
                    </div>

                    <div className="personalia-item fullwidth">
                        <h2>Appendices</h2>
                        <AppendicesList
                            uuid={user.uuid}
                            appendices={user.appendices}
                        />
                    </div>
                </div>
            </div>
        </UserContext.Provider>
    );
}

interface Props {
    user: User;
    className?: string;
}

export default UserPage;
