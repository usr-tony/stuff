import React from "react"
import { Link, Breadcrumbs, Typography, Paper } from '@mui/material'
import HomeIcon from '@mui/icons-material/Home'
import CurrencyBitcoinIcon from '@mui/icons-material/CurrencyBitcoin'

export default (props) => (
    <Paper className='container-fluid' sx={{ p: 1, m: 0.5, width: 'fit-content', height: 34 }} elevation={3}>
        <Breadcrumbs separator="/" aria-label="breadcrumb" sx={{ fontSize: 12 }}>
            <Link 
                underline="hover"  
                key="1" 
                color='inherit'
                href="/" 
                sx={{ 
                    display: 'flex', 
                    alignItems: 'center', 
                    mr: 0.5, 
                    fontSize: 'inherit', 
                    '&:hover': { color: 'inherit' }
                }}
            >
                <HomeIcon sx={{ mr: 0.7, fontSize: 15 }}/> 
                profile 
            </Link>
            <Typography 
                key="3" 
                color="text.primary" 
                sx={{ display: 'flex', alignItems: 'center', fontSize: 'inherit' }}
            >
                <CurrencyBitcoinIcon sx={{ mr: 0.5, fontSize: 15 }} /> 
                trader
            </Typography>
        </Breadcrumbs>
    </Paper>
)
