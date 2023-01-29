import React from "react";
import { Grid, Container } from "@mui/material";

import { Certs, Skills, Education } from "./resume";
import { Jobs } from "./projects";
import ContactInfo from "./contact-info";
import { Parallax, ParallaxLayer } from "@react-spring/parallax";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import { GoogleReCaptchaProvider } from "react-google-recaptcha-v3";

import customStyles from "./custom-styles";

const scale_height = 1

const theme = createTheme({
    palette: {
        mode: "dark",
    },
    typography: {
        fontFamily: customStyles.fontFamily,
        button: {
            textTransform: "none",
        },
    },
});
const recaptcha_key = "6LcVpQggAAAAALaMRxlxtXsMAmjvsej8-N8aW2U_";

export default () => {
    return (
        <ThemeProvider theme={theme}>
            <div class="container-fluid">
                <GoogleReCaptchaProvider reCaptchaKey={recaptcha_key}>
                    <Parallax pages={getPages()}>
                        <ParallaxLayer
                            offset={0}
                            speed={2.5}
                            style={{
                                zIndex: 1,
                                top: 0,
                                left: 0,
                                display: "flex",
                                justifyContent: "center",
                            }}
                        >
                            <ContactInfo />
                        </ParallaxLayer>
                        <ParallaxLayer style={{ zIndex: 0 }}>
                            <Container sx={{ paddingTop: '23rem' }}>
                                <Grid
                                    container
                                    columnSpacing={10}
                                    rowSpacing={0}
                                    direction="row-reverse"
                                    sx={{ justifyContent: "center" }}
                                >
                                    <Grid item>
                                        <Jobs />
                                        <Skills />
                                    </Grid>
                                    <Grid item>
                                        <Education />
                                        <Certs />
                                    </Grid>
                                </Grid>
                            </Container>
                        </ParallaxLayer>
                    </Parallax>
                </GoogleReCaptchaProvider>
            </div>
        </ThemeProvider>
    );
}

function getPages() {
    const remToPx = getComputedStyle(document.documentElement).fontSize
    const totalHeightPx = parseInt(remToPx) * 65 * scale_height
    if (window.innerWidth > 1010) {
        return totalHeightPx / getViewportHeight()
    }
    return 2.5 * scale_height
}

// gets the width viewport
function getViewportHeight() {
    if (self.innerHeight) {
        return self.innerHeight;
    }
    if (document.documentElement && document.documentElement.clientHeight) {
        return document.documentElement.clientHeight;
    }
    if (document.body) {
        return document.body.clientHeight;
    }
}