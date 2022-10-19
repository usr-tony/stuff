import React from "react";
import { Grid, Container } from "@mui/material";

import { Certs, Experience, Skills, Education } from "./resume";
import { Autotrader, Jobs } from "./projects";
import ContactInfo from "./contact-info";
import { Parallax, ParallaxLayer } from "@react-spring/parallax";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import { GoogleReCaptchaProvider } from "react-google-recaptcha-v3";

import customStyles from "./custom-styles";

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
                                        <Certs />
                                    </Grid>
                                    <Grid item>
                                        <Experience />
                                        <Education />
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
    const totalHeightPx = parseInt(remToPx) * 85
    if (window.innerWidth > 1010) {
        return totalHeightPx / getViewportHeight()
    }
    return 3.3
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