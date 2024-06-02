import { Button, Grid, Typography } from "@mui/material";
import Navbar from "../../components/navbar";
import { useNavigate } from "react-router-dom";

const HomePage = () => {
    const navigate = useNavigate();

    return (
        <>
            <Navbar />
            <Grid container
                height='90vh'
                alignContent='center'
                gap={10}
            >
                <Grid item xs={12}>
                    <Typography variant="h2">
                        ¡Bienvenido!
                    </Typography>
                </Grid>
                <Grid item xs={12}>
                    <Button
                        variant="contained"
                        onClick={() => navigate('/Upload')}
                        sx={{ backgroundColor: "#4D17BF" }}
                    >
                        Empezar herramienta
                    </Button>
                </Grid>
            </Grid>
        </>
    );
}

export default HomePage;