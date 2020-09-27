import React from "react";
import { Appendices } from "../../../types/Appendices";

import "./styles.css";

function AppendicesList({ appendices, className }: Props): JSX.Element {
    if (!Object.keys(appendices).length)
        return <span>No appendices to show.</span>;

    console.log(appendices);

    return (
        <div className={`appendices-list ${className || ""}`}>
            {Object.entries(appendices.appendices).map(
                ([key, appendixList]) => (
                    <div>
                        <h3>Type {key}:</h3>
                        <div>
                            {Object.entries(appendixList).map(
                                ([name, appendix]) => (
                                    <div>
                                        <h4>Appendix name {name}:</h4>
                                        <p>Created: {appendix.created}</p>
                                        <p>
                                            Last changed: {appendix.lastchanged}
                                        </p>
                                        <p>Contents: {appendix.value}</p>
                                    </div>
                                )
                            )}
                        </div>
                    </div>
                )
            )}
        </div>
    );
}

interface Props {
    appendices: Appendices;
    className?: string;
}

export default AppendicesList;
