import React from "react";
import {
  CardContent,
  CardActionArea,
  Card,
  CardMedia,
  CardActions,
  Typography,
  Box,
} from "@mui/material/";
import { useNavigate } from "react-router-dom";

import GitHubButton from "./github-button";
import customStyles from "./custom-styles";

const placeholder_state = {
    title: "Auto trader",
    project_image_link: "https://smallideas.com.au/wp-content/uploads/2019/06/smallideas.png",
    description: (
        <ul>
            <li>hello</li>
            <li>dsjfkjds</li>
            <li>wsfdsfsfsdfs</li>
        </ul>
    ),
    project_link: "https://youtube.com",
    github_link: "https://github.com",
};

export default (props) => {
    const navigate = useNavigate()
    for (let s in placeholder_state) {
        if (!props[s]) {
            props[s] = placeholder_state[s];
        }
    }
    let cardSx = {
        color: customStyles.color,
        bgcolor: customStyles.bgcolor,
        m: 1,
        ml: 0,
        mr: 0,
        width: 433,
        maxWidth: "90vw",
    }
    return (
        <Card variant="outlined" sx={cardSx}>
            <CardActionArea onClick={() => navigate(props.project_link)} LinkComponent="a">
                <CardMedia
                    component="img"
                    image={props.project_image_link}
                    sx={{ height: '13rem' }}
                />
                <CardContent>
                    <Typography
                        variant="h6"
                        sx={{ color: "text.primary", fontSize: "1.2rem" }}
                    >
                        {props.title}   
                    </Typography>
                    <Typography variant="body2" color={customStyles.color}>
                        {props.description}
                    </Typography>
                </CardContent>
            </CardActionArea>
            <CardActions>
                <GitHubButton href={props.github_link} />
            </CardActions>
        </Card>
    )
}
