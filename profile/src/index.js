import ReactDOM from "react-dom";
import React, { lazy, Suspense } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./styles.css"
import { BrowserRouter, Routes, Route, HashRouter } from "react-router-dom";

const App = () => (
    <HashRouter>
        <Routes>
            {newRoute('/', lazy(() => import('./main')))}
            {/* {newRoute('/trader', lazy(() => import('./trader')))} */}
            {newRoute('/jobs', lazy(() => import('./jobs')))}
        </Routes>
    </HashRouter>
);

function newRoute(path, Component) {
    return (
        <Route
            exact
            path={path}
            element={
                <Suspense fallback={<div />}>
                    <Component />
                </Suspense>
            }
        />
    )
}

ReactDOM.render(<App />, document.querySelector("#app"));
