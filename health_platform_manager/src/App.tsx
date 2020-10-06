import React from "react";
import { Route, Switch, BrowserRouter as Router } from "react-router-dom";
import "./App.css";

import MainPage from "./Pages/MainPage";
import DigitalTwinPage from "./Pages/DigitalTwinPage";

function App() {
    return (
        <Router>
            <div className="App">
                <Switch>
                    <Route
                        path="/digitalTwin/:digitalTwinUuid"
                        component={DigitalTwinPage}
                    />
                    <Route path="/" component={MainPage} />
                </Switch>
            </div>
        </Router>
    );
}

export default App;
