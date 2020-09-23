import React, { useCallback, useState } from "react";

import DigitalTwinListElement from "./DigitalTwinListElement";
import { useUsers } from "../../hooks";

import "./styles.css";

function DigitalTwinList({ className }: Props): JSX.Element {
    const [page, setpage] = useState<number>(1);
    const users = useUsers(10, page);

    const onClickRight = useCallback(() => {
        setpage(page + 1);
    }, [page]);

    const onClickLeft = useCallback(() => {
        setpage(page - 1);
    }, [page]);

    if (users === undefined) return <></>;
    if (users === null || !users.length) return <span>No users found.</span>;

    const userList = users.map((user) => (
        <DigitalTwinListElement user={user} key={user.uuid} />
    ));

    return (
        <div className={`digital-twin-list ${className || ""}`}>
            <ul>{userList}</ul>
            <button onClick={onClickLeft} disabled={page < 2}>
                {page - 1}
            </button>
            {page}
            <button onClick={onClickRight}>{page + 1}</button>
        </div>
    );
}

interface Props {
    className?: string;
}

export default DigitalTwinList;
