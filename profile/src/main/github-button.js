import React from 'react'
import GitHubIcon from '@mui/icons-material/GitHub'
import { Box, Button, Typography } from '@mui/material'
import customStyles from './custom-styles'

export default function GitHubButton(props) {
    return (
        <Box sx={props.sx}>
            <Button
                variant='outlined'
                size='small'
                href={props.href || 'https://github.com/usr-tony'}
                sx={{ '&:hover': { color: '#f2efde' } }}
            >
                <GitHubIcon size='small' sx={{ mr: 1 }}></GitHubIcon>
                <Typography variant='body4' component='div' fontFamily={customStyles.fontFamily} fontSize='0.7rem'>
                    github
                </Typography>
            </Button>
        </Box>
    )
}