import React, { ChangeEvent, useState } from "react";
import { updateUserAttribute } from "../../../services/aws";
import { Appendix } from "../../../types/Appendices";
import { User } from "../../../types/User";

import "./styles.css";

function AppendicesListElement({
    userUuid,
    appendixUuid,
    appendix,
    appendixType,
    className,
}: Props): JSX.Element {
    const [openAppendix, setOpenAppendix] = useState<boolean>(false);

    const toggleConsent = (e: ChangeEvent<HTMLInputElement>): User | void => {
        e.preventDefault();
        const newState: boolean = !appendix.shareConsent ? true : false;
        updateUserAttribute(
            userUuid,
            [
                "appendices",
                "appendices",
                appendixType,
                appendixUuid,
                "shareConsent",
            ],
            newState
        );
    };

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
                    onChange={toggleConsent}
                />
            </div>
        </div>
    ) : (
        <></>
    );

    return (
        <div
            key={appendixUuid}
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
    userUuid: string;
    appendixUuid: string;
    appendix: Appendix;
    appendixType: string;
    className?: string;
}

export default AppendicesListElement;
