import React, { useState } from "react";
import {
    Stack,
    Paper,
    CardActionArea,
    Typography,
    Input,
    Fade,
    Card,
    Collapse,
} from "@mui/material";
import ContentCopyOutlinedIcon from "@mui/icons-material/ContentCopyOutlined";
import { styled } from "@mui/system";
import "babel-polyfill"; // required to enable the use of async
import { useGoogleReCaptcha } from "react-google-recaptcha-v3";

// custom imports
import GitHubButton from "./github-button";
import customStyles from "./custom-styles";

const api_endpoint = "https://3tu5v12172.execute-api.ap-southeast-2.amazonaws.com/profile";

const defaultStyles = {
    paper: {
        height: "98vh",
        width: "98vw",
        mr: 1,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        mt: 1,
        justifyContent: "center",
    },
    stack: {
        alignItems: "center",
    },
    stackSpacing: 2,
};

export default function ContactInfo(props) {
    return (
        <>
            <Paper variant="outlined" sx={defaultStyles.paper}>
                <Stack spacing={defaultStyles.stackSpacing} sx={defaultStyles.stack}>
                    <Name />
                    <Email />
                    <Typography variant="body2" fontFamily={customStyles.fontFamily}>
                        Sydney, Australia
                    </Typography>
                    <GitHubButton />
                </Stack>
                <ContactForm />
            </Paper>
        </>
    );
}

let Name = () => (
    <Typography
        fontFamily={customStyles.fontFamily}
        variant="h4"
        color={"primary.main"}
        sx={{ mb: 3 }}
    >
        Tony Ding
    </Typography>
);

function Email() {
    let [copied, setCopied] = useState(false);
    let copyEmail = (e) => {
        let text = "0tonyd0@gmail.com";
        navigator.clipboard.writeText(text);
        setCopied(true);
        setTimeout(() => setCopied(false), 100);
    };
    let printCopied = (ifcopied) => (
        <Fade in={ifcopied} timeout={{ enter: 50, exit: 2000 }}>
            <Typography
                variant="body2"
                sx={{ position: "absolute", paddingTop: "0.5rem", fontSize: "small" }}
            >
                copied!
            </Typography>
        </Fade>
    );
    return (
        <Typography
            variant="body2"
            fontFamily={customStyles.fontFamily}
            sx={{ display: "flex", flexDirection: "row" }}
        >
            <CardActionArea
                onClick={copyEmail}
                sx={{ padding: "0.5rem", marginBottom: "-0.5rem" }}
            >
                0tonyd0@gmail.com
                <ContentCopyOutlinedIcon
                    fontSize="x-small"
                    sx={{ ml: 1.2, opacity: 0.75 }}
                />
            </CardActionArea>
            <div style={{ marginLeft: "0.5rem" }}>{printCopied(copied)}</div>
        </Typography>
    );
}

function ContactForm(props) {
    const { executeRecaptcha } = useGoogleReCaptcha();
    const cardStyle = {
        maxHeight: '20rem',
        width: '33rem',
        maxWidth: "80%",
        margin: "3rem",
        p: 1,
        pt: 0,
        mt: "4rem",
    };
    const [state, setState] = useState({ cardStyle });

    const watchForEnter = (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            document.querySelector("#submit-button").click();
        }
    };

    const submit = async (e) => {
        e.preventDefault();
        const red = "#b71c1c30";
        const green = "#64dd1730";
        let payload = {
            name: e.target.name.value,
            contact: e.target.contact.value,
            body: e.target.message.value,
        };
        if ((payload.name || payload.contact || payload.body) && executeRecaptcha) {
            payload.token = await executeRecaptcha();
            changeColor(green);
            sendMessage(payload);
            e.target.reset();
        } else {
            changeColor(red);
            e.target.reset();
        }
    };

    const changeColor = (color) => {
        setState((state) => ({
            cardStyle: {
                ...state.cardStyle,
                bgcolor: color,
            },
        }));
    };

    const sendMessage = (payload) => {
        fetch(api_endpoint, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            mode: "no-cors",
            body: JSON.stringify(payload),
        })
    };
    return (
        <Card variant="outlined" sx={state.cardStyle}>
            <Stack
                component={"form"}
                onSubmit={submit}
                id="contact-form"
                sx={{ justifyContent: "center" }}
            >
                <CustomStyledInput id="name" placeholder="name" sx={{ width: "50%" }} />
                <CustomStyledInput
                    id="contact"
                    placeholder="contact"
                    sx={{ width: "50%" }}
                />
                <CustomStyledInput
                    id="message"
                    placeholder={"message\nshift + enter for new line"}
                    multiline={true}
                    maxRows={8}
                    minRows={2}
                    sx={{ width: "100%" }}
                    onKeyDown={watchForEnter}
                />
                <input id="submit-button" type="submit" hidden />
            </Stack>
        </Card>
    );
}

const CustomStyledInput = styled(Input)({
    width: 150,
    fontSize: "small",
    color: customStyles.color,
});
