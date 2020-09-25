import React, { useCallback, useState } from "react";

import DigitalTwinListElement from "./DigitalTwinListElement";
import { useUsers } from "../../hooks";

import "./styles.css";

function DigitalTwinList({ className }: Props): JSX.Element {
    const [page, setpage] = useState<number>(1);
    const [users, lastpage] = useUsers(10, page);

    const onClickRight = useCallback(() => {
        setpage(page + 1);
    }, [page]);

    const onClickLeft = useCallback(() => {
        setpage(page - 1);
    }, [page]);

    if (users === undefined) return <></>;

    const userList = (
        <ul>
            {users.map((user) => (
                <DigitalTwinListElement user={user} key={user.uuid} />
            ))}
        </ul>
    );

    const content =
        users === null || !users.length ? (
            <span>No users found.</span>
        ) : (
            userList
        );

    return (
        <div className={`digital-twin-list ${className || ""}`}>
            {content}
            <div>
                <button onClick={onClickLeft} disabled={page < 2}>
                    {"<--"}
                </button>
                {page}
                <button onClick={onClickRight} disabled={lastpage}>
                    {"-->"}
                </button>
            </div>
        </div>
    );
}

interface Props {
    className?: string;
}

export default DigitalTwinList;
