import React, { useCallback, useState } from "react";

import DigitalTwinListElement from "./DigitalTwinListElement";
import { useDigitalTwins } from "../../hooks";

import "./styles.css";

function DigitalTwinList({ className }: Props): JSX.Element {
    const [page, setpage] = useState<number>(1);
    const [digitalTwins, lastpage] = useDigitalTwins(10, page);

    const onClickRight = useCallback(() => {
        setpage(page + 1);
    }, [page]);

    const onClickLeft = useCallback(() => {
        setpage(page - 1);
    }, [page]);

    if (digitalTwins === undefined) return <></>;

    const digitalTwinList = (
        <ul>
            {digitalTwins.map((digitalTwin) => (
                <DigitalTwinListElement
                    digitalTwin={digitalTwin}
                    key={digitalTwin.uuid}
                />
            ))}
        </ul>
    );

    const content =
        digitalTwins === null || !digitalTwins.length ? (
            <span>No digitalTwins found.</span>
        ) : (
            digitalTwinList
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
