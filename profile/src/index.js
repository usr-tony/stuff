import ReactDOM from "react-dom";
import React, { lazy, Suspense } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./styles.css"
import { BrowserRouter, Routes, Route } from "react-router-dom";
const Main = lazy(() => import('./main'))
const Trader = lazy(() => import('./trader'))
const Jobs = lazy(() => import('./jobs'))

const App = () => (
    <BrowserRouter>
        <Routes>
            <Route
                exact
                path={"/"}
                element={
                    <Suspense fallback={<div />}>
                        <Main />
                    </Suspense>
                }
            />
            <Route
                exact
                path={"/trader"}
                element={
                    <Suspense fallback={<div />}>
                        <Trader />
                    </Suspense>
                }
            />
            <Route
                exact
                path={"/jobs"}
                element={
                    <Suspense fallback={<div />}>
                        <Jobs />
                    </Suspense>
                }
            />
        </Routes>
    </BrowserRouter>
);

ReactDOM.render(<App />, document.querySelector("#app"));
