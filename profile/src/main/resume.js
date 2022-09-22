import { Typography, Box } from "@mui/material";
import React from "react";
import Timeline from "@mui/lab/Timeline";
import TimelineItem from "@mui/lab/TimelineItem";
import TimelineSeparator from "@mui/lab/TimelineSeparator";
import TimelineConnector from "@mui/lab/TimelineConnector";
import TimelineDot from "@mui/lab/TimelineDot";
import TimelineOppositeContent from "@mui/lab/TimelineOppositeContent";
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
                    <b>Master's of Commerce</b>
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

export function Experience(props) {
    return (
        <Box sx={sectionStyle}>
            <Header text="Experience" />
            <Teleresult />
            <Cwh />
        </Box>
    );
}

function Teleresult(props) {
    return (
        <Typography variant="body2">
            <b>Software Developer</b>
            <br />
            <i>Teleresult</i>
            , Sydney NSW
            <br />
            MAR 2022 - Present
            <ul>
                <li>
                    Develop Web applications with React, Graphql. Hosted with AWS amplify
                </li>
                <li>
                    Maintain and develop legacy websites with PHP, MySQL, MS SQL Server
                </li>
                <li>Create data pipelines with Talend open studio, Java and Python</li>
            </ul>
        </Typography>
    );
}

function Cwh(props) {
    const timelineContentStyle = (h) => {
        return {
            maxWidth: "1px",
            paddingLeft: "0.5rem",
            paddingTop: "0.3rem",
            paddingBottom: 0,
            height: h,
        };
    };
    const dotStyle = {
        padding: "2px",
        borderWidth: "2px",
    };
    return (
        <Typography variant="body2">
            <i>Chemist Warehouse</i>, Sydney NSW
            <Timeline
                sx={{
                    marginTop: "-0.6rem",
                    marginBottom: 0,
                    paddingBottom: 0,
                }}
            >
                {/* start pharmacist section */}

                <TimelineItem sx={{ minHeight: 0 }}>
                    <TimelineSeparator>
                        <TimelineDot variant="outlined.secondary" sx={dotStyle} />
                        <TimelineConnector sx={{ backgroundColor: customStyles.color }} />
                    </TimelineSeparator>
                    <TimelineOppositeContent sx={timelineContentStyle("7.25rem")}>
                        <Typography
                            variant="body2"
                            sx={{ position: "absolute", textAlign: "left" }}
                        >
                            <b>Pharmacist</b>
                            <br />
                            DEC 2019 - MAR 2022
                            <br />
                            <ul style={{ listStyleType: "disc" }}>
                                <li>Manages pharmacy that sees 300+ patients per day</li>
                                <li>Prepares pharmacy for inspections</li>
                            </ul>
                        </Typography>
                    </TimelineOppositeContent>
                </TimelineItem>

                {/* intern pharmacist section */}

                <TimelineItem sx={{ minHeight: "3rem" }}>
                    <TimelineSeparator>
                        <TimelineDot variant="outlined.secondary" sx={dotStyle} />
                    </TimelineSeparator>
                    <TimelineOppositeContent sx={timelineContentStyle("1rem")}>
                        <Typography
                            variant="body2"
                            sx={{ position: "absolute", textAlign: "left" }}
                        >
                            <b>Intern Pharmacist</b>
                            <br />
                            AUG 2018 - NOV 2019
                            <br />
                        </Typography>
                    </TimelineOppositeContent>
                </TimelineItem>
            </Timeline>
        </Typography>
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
            <Typography variant="body2">
                <b>
                    <i>CFA level II</i>
                </b>
                <br />
                2018
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
