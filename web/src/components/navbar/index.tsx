import { Grid, IconButton, Typography } from "@mui/material";
import { useLocation, useNavigate } from "react-router-dom";
import { ArrowBackIosNew, Menu } from '@mui/icons-material/';

const Navbar = () => {
    const location = useLocation();
    const route = location.pathname;
    const navigate = useNavigate();


    return (
        <Grid container
            sx={{
                backgroundColor: "#4D17BF",
                height: "50px"
            }}
            alignContent="center"
            justifyContent="center"
        >
            {route === "/Home" ? (
                <Grid item xs={12}
                    alignItems="center"
                >
                    <Typography>
                        DUPLIX - Herramienta de deteccion de plagio
                    </Typography>
                </Grid>
            ) : (
                <Grid container
                    justifyContent="space-between"
                    alignItems="center"
                    pr={2}
                >
                    <IconButton
                        sx={{
                            color: "#FFFFFF"
                        }}
                        onClick={() => navigate(-1)}
                    >
                        <ArrowBackIosNew />
                    </IconButton>
                    <Typography>
                        DUPLIX - Herramienta de deteccion de plagio
                    </Typography>
                    <Menu />
                </Grid>
            )}
        </Grid>
    );
}

export default Navbar;