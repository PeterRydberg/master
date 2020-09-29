import React, { useState } from "react";
import { Appendix } from "../../../types/Appendices";

import "./styles.css";

function AppendicesListElement({
    uuid,
    appendix,
    className,
}: Props): JSX.Element {
    const [openAppendix, setOpenAppendix] = useState<boolean>(false);

    const appendixContent = openAppendix ? (
        <div className="appendix-content">
            <p>
                Last changed:{" "}
                {new Date(appendix.lastchanged).toLocaleDateString()}
            </p>
            <p>Content path: "{appendix.value}"</p>
        </div>
    ) : (
        <></>
    );

    return (
        <div
            key={uuid}
            className={`appendices-list-element ${className || ""}`}
        >
            <div
                onClick={() => setOpenAppendix(!openAppendix)}
                className="togglable"
            >
                <h4>
                    Appendix created{" "}
                    {new Date(appendix.created).toLocaleDateString()} ⬇
                </h4>
            </div>

            {appendixContent}
        </div>
    );
}

interface Props {
    uuid: string;
    appendix: Appendix;
    className?: string;
}

export default AppendicesListElement;
