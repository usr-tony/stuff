import React from 'react'
import Breadcrumbs from './breadcrumbs'
import { ThemeProvider, createTheme } from '@mui/material/styles'
import customStyles from '../main/custom-styles';
import App from './app'
import './styles.css'

const theme = createTheme({
    palette: {
        mode: 'dark',
    },
    typography: {
        fontFamily: customStyles.fontFamily,
        button: {
            textTransform: 'none',
            fontSize: 12,
        },
        fontSize: 10,
    }
});

export default () => {
    return (
        <ThemeProvider theme={theme} >
            <Breadcrumbs />
            <App />
        </ThemeProvider>
    )
}
