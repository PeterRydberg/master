import React, { useState } from "react";
import { Appendix } from "../../../types/Appendices";
import AppendicesListElement from "../AppendicesListElement";

import "./styles.css";

function AppendicesTypeListElement({
    elementKey,
    appendixList,
    className,
}: Props): JSX.Element {
    const [openList, setOpenList] = useState<boolean>(false);

    const listContent = openList ? (
        <div className="list-content">
            {Object.entries(appendixList).map(([uuid, appendix]) => (
                <AppendicesListElement
                    key={uuid}
                    uuid={uuid}
                    appendix={appendix}
                />
            ))}
        </div>
    ) : (
        <></>
    );

    return (
        <div
            key={elementKey}
            className={`appendices-type-list-element ${className || ""}`}
        >
            <div onClick={() => setOpenList(!openList)} className="togglable">
                <h3>Type {elementKey} ⬇</h3>
            </div>
            {listContent}
        </div>
    );
}

interface Props {
    elementKey: string;
    appendixList: { [uuid: string]: Appendix };
    className?: string;
}

export default AppendicesTypeListElement;
