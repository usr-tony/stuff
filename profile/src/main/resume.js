import { Typography, Box } from "@mui/material";
import React from "react";
import customStyles from "./custom-styles";

const sectionStyle = {
    border: "1px solid rgba(100, 100, 100, 0.7)",
    borderRadius: 1,
    p: 1,
    m: 1,
    ml: 0,
    mr: 0,
    width: '28rem',
    maxWidth: "90vw",
};

export function Education(props) {
    return (
        <Box sx={sectionStyle}>
            <Header text={"Education"} />
            <Typography variant="body2">
                <i>
                    <b>FreeCodeCamp</b>
                </i>
                <br />
                2021
                <br />
                <b>certifications completed:</b>
                <ul style={{ fontSize: "0.9rem" }}>
                    <li>Responsive Web Design</li>
                    <li>Javascript algorithms and data structures</li>
                    <li>Front end libraries</li>
                    <li>Scientific computing with Python</li>
                    <li>Data analysis with Python</li>
                    <li>Machine learning with Python</li>
                </ul>
                <div>
                    <b>Master of Commerce</b>
                    <br />
                    <i>University of New South Wales</i>
                    , Sydney NSW
                    <br />
                    2018
                </div>
            </Typography>
        </Box>
    );
}

export function Certs(props) {
    return (
        <Box sx={sectionStyle}>
            <Header text={"Certifications"} />
            <Typography variant="body2" sx={{ marginBottom: "1em" }}>
                <b>
                    <i>AWS solutions architect associate</i>
                </b>
                <br />
                2022
            </Typography>
        </Box>
    );
}

export function Skills(props) {
    return (
        <Box sx={sectionStyle}>
            <Typography variant="body2">
                <Header text={"Skills"}></Header>
                Programming
                <ul style={{ marginBottom: 0 }}>
                    <li>Python (pandas, tensorflow)</li>
                    <li>Javascript (node, React) HTML/CSS</li>
                    <li>SQL (sqlite, mysql) MongoDb</li>
                    <li>C/C++</li>
                </ul>
            </Typography>
        </Box>
    );
}

const headerStyle = {
    color: "text.primary",
    fontFamily: customStyles.fontFamily,
    mb: 1,
};

function Header(props) {
    return (
        <Typography variant="h5" sx={headerStyle}>
            {props.text}
        </Typography>
    );
}
