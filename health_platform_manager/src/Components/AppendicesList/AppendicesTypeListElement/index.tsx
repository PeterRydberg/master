import React, { useState } from "react";
import { Appendix } from "../../../types/Appendices";
import AppendicesListElement from "../AppendicesListElement";

import "./styles.css";

function AppendicesTypeListElement({
    appendixType,
    userUuid,
    appendixList,
    className,
}: Props): JSX.Element {
    const [openList, setOpenList] = useState<boolean>(false);

    const listContent = openList ? (
        <div className="list-content">
            {Object.entries(appendixList).map(([appendixUuid, appendix]) => (
                <AppendicesListElement
                    key={appendixUuid}
                    userUuid={userUuid}
                    appendixUuid={appendixUuid}
                    appendix={appendix}
                    appendixType={appendixType}
                />
            ))}
        </div>
    ) : (
        <></>
    );

    return (
        <div
            key={appendixType}
            className={`appendices-type-list-element ${className || ""}`}
        >
            <div onClick={() => setOpenList(!openList)} className="togglable">
                <h3>Type {appendixType} ⬇</h3>
            </div>
            {listContent}
        </div>
    );
}

interface Props {
    appendixType: string;
    userUuid: string;
    appendixList: { [uuid: string]: Appendix };
    className?: string;
}

export default AppendicesTypeListElement;
