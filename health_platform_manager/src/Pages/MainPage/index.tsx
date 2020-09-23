import React from "react";
import DigitalTwinList from "../../Components/DigitalTwinList";
import "./styles.css";

function MainPage({ className }: Props): JSX.Element {
    return (
        <div className={`main-page ${className || ""}`}>
            <h1>Health Platform Manager</h1>
            <DigitalTwinList />
        </div>
    );
}

interface Props {
    className?: string;
}

export default MainPage;
