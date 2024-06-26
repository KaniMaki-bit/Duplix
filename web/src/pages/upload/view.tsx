import { Button, Grid, Paper, Typography } from "@mui/material";
import Navbar from "../../components/navbar";
import React from "react";
import { ArrowForward, Upload } from "@mui/icons-material";
import { LoadingButton } from '@mui/lab';
import { useNavigate } from "react-router-dom";

interface Props {
    fileName: string | null;
    handleUpload: (event: React.ChangeEvent<HTMLInputElement>) => void;
    allow: boolean;
    loadingUpload: boolean;
}

const UploadView: React.FC<Props> = ({
    fileName,
    handleUpload,
    allow,
    loadingUpload,
}) => {
    const navigate = useNavigate();

    return (
        <>
            <Navbar />
            <Grid container
                height='90vh'
                alignContent='center'
                justifyContent='center'
                gap={4}
            >
                <Grid item xs={12}>
                    <Typography variant="h3">
                        Carga de archivo
                    </Typography>
                </Grid>
                <Paper
                    elevation={5}
                    sx={{
                        backgroundColor: "#333333",
                        color: "#FFFFFF",
                        p: 4,
                        width: "600px",
                        minHeight: "300px",
                    }}
                >
                    <Grid container
                        justifyContent='center'
                        gap={4}
                    >
                        <Typography>
                            A continuación suba un .ZIP con los scripts de la actividad a evaluar.
                            Cada uno de los archivos deberá deberá tener la matricula del alumno al inicio.
                        </Typography>
                        <Paper
                            elevation={2}
                            sx={{
                                backgroundColor: "#1E1C1C",
                                color: "#FFFFFF",
                                minWidth: "350px",
                                p: 1
                            }}
                        >
                            <Typography mb={1}>
                                Ejemplos:
                            </Typography>
                            <Typography>
                                A01735334_actividad1.py
                            </Typography>
                            <Typography>
                                A01735334-actividad1.py
                            </Typography>
                            <Typography>
                                A01735334Actividad1.py
                            </Typography>
                        </Paper>
                        <Grid item xs={12}
                            display="flex"
                            justifyContent="left"
                        >
                            <input
                                accept=".zip"
                                style={{ display: 'none' }}
                                id="upload-file"
                                type="file"
                                onChange={handleUpload}
                            />
                            <label htmlFor="upload-file">
                                <Button
                                    startIcon={<Upload />}
                                    variant="contained"
                                    component="span"
                                    sx={{
                                        backgroundColor: "#4D17BF",
                                        textTransform: "none",
                                        ":hover": {
                                            backgroundColor: "#4D17BF",
                                        }
                                    }}
                                >
                                    Cargar archivo
                                </Button>
                            </label>
                            <Typography
                                sx={{
                                    alignContent: "center",
                                    ml: 1
                                }}
                            >
                                {fileName || "Seleccione archivo..."}
                            </Typography>
                        </Grid>
                        <Grid item xs={12}
                            display="flex"
                            justifyContent="flex-end"
                        >
                            <LoadingButton
                                variant="contained"
                                disabled={!allow}
                                loading={loadingUpload}
                                onClick={() => navigate("/Heatmap")}
                                sx={{
                                    backgroundColor: "#4D17BF",
                                    ":hover": {
                                        backgroundColor: "#4D17BF",
                                    }
                                }}
                                endIcon={<ArrowForward/>}
                            >
                                Comenzar analisis
                            </LoadingButton>
                        </Grid>
                    </Grid>
                </Paper>
            </Grid>
        </>
    );
}

export default UploadView;