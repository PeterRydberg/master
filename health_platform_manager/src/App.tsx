import React from "react";
import { Route, Switch, BrowserRouter as Router } from "react-router-dom";
import "./App.css";

import MainPage from "./Pages/MainPage";
import UserPage from "./Pages/UserPage";

function App() {
    return (
        <Router>
            <div className="App">
                <Switch>
                    <Route path="/user/:userUuid" component={UserPage} />
                    <Route path="/" component={MainPage} />
                </Switch>
            </div>
        </Router>
    );
}

export default App;
