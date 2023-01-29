import React, { useState } from "react";
import Highcharts from "highcharts";
import HighchartsMore from "highcharts/highcharts-more";
import darkTheme from "highcharts/themes/brand-dark.src";
import "babel-polyfill";
import Jobs from './jobs'
import Keywords from './keywords'
import { Grid, Paper } from "@mui/material";
import SideSection from "./side-section";
HighchartsMore(Highcharts);
darkTheme(Highcharts);


export default () => {
    let useGlobalState = useState({
        by: "sector",
        filters: { sector: 'Information & Communication Technology' },
        type: "bubbles",
    })
    const [state, setState] = useGlobalState
    return <Grid container>
        <Grid item xs={9}>
            <Jobs useGlobalState={useGlobalState} />
            <Keywords useGlobalState={useGlobalState} />
        </Grid>
        <Grid item xs={3}>
            <Paper variant='outlined' sx={{ position: 'sticky', top: 0}}>
                <SideSection state={state} setState={setState} />
            </Paper>
        </Grid>
    </Grid>
}

