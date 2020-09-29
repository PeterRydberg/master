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
            <div className="appendix-item">
                <label>Last changed: </label>
                {new Date(appendix.lastchanged).toLocaleDateString()}
            </div>

            <div className="appendix-item">
                <label>Content path: </label>"{appendix.value}"
            </div>

            <div className="appendix-item">
                <label>Automatic model evaluation: </label>[NONE]
            </div>

            <div className="appendix-item">
                <label>Doctor evaluation: </label>[NONE]
            </div>

            <div className="appendix-item">
                <label>Patient consent to information share:</label>
                <input
                    type="checkbox"
                    name="consent"
                    id="consent-checkbox"
                    value="Consent"
                    checked={appendix.shareConsent ? true : false}
                />
            </div>
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
