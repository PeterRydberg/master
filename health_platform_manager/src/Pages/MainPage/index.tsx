import React from "react";
import DigitalTwinList from "../../Components/DigitalTwinList";
import "./styles.css";

function MainPage({ className }: Props): JSX.Element {
    return (
        <div className={`main-page ${className || ""}`}>
            <DigitalTwinList />
        </div>
    );
}

interface Props {
    className?: string;
}

export default MainPage;
