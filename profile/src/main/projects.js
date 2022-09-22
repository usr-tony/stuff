import React from 'react';
import ProjectTile from './project-tile';

export const Autotrader = () => ProjectTile({
    title: 'Project: Trader',
    project_image_link: 'https://images.squarespace-cdn.com/content/v1/5a459ea9692ebe7dcf9ca9ff/1515028331771-FGZ2K9P0VRAB1Q80OYSR/image-asset.jpeg?format=1500w',
    description: 'algorithmic trader written in python and hosted on AWS',
    project_link: '/trader',
    github_link: 'https://github.com/usr-tony/autotrade',
})

export const Jobs = () => ProjectTile({
    title: 'Project: Jobs',
    project_image_link: 'https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?crop=entropy&cs=tinysrgb&fm=jpg&ixlib=rb-1.2.1&q=80&raw_url=true&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1744',
    description: (
        <ul style={{position: 'relative', left: '-1rem'}}>
            <li>Scrapes jobs automatically on seek.com.au</li>
            <li>Visualises and filters jobs based on various criteria</li>
            <li>Hosted on AWS</li>
        </ul>
    ),
    project_link: '/jobs',
    github_link: 'https://github.com/usr-tony/job-search',
})
