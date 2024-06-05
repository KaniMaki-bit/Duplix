import { Card, CardContent, CircularProgress, Grid, Typography } from "@mui/material";
import Navbar from "../../components/navbar";
import { Link } from "react-router-dom";

interface Props {
    loading: boolean;
    data: any;
    estudiantes: string[];
}

const HeatmapView: React.FC<Props> = ({
    loading,
    data,
    estudiantes,
}) => {

    return (
        <>
            <Navbar />
            <Grid container
                height="90vh"
                alignContent="center"
                justifyContent="center"
                gap={0.5}
            >
                {loading ? (
                    <CircularProgress />
                ) : (
                    <>
                        {/* Header Row */}
                        <Grid container direction="row" alignContent="center" justifyContent="center" gap={0.5}>
                            <Grid item>
                                <Typography variant="caption" sx={{ mr: `${600 / estudiantes.length}px` }} />
                            </Grid>
                            {estudiantes.map((est, index) => (
                                <Grid item key={index}>
                                    <Typography
                                        variant="caption"
                                        sx={{
                                            width: 600 / estudiantes.length,
                                            textAlign: 'center',
                                            writingMode: 'vertical-rl',
                                            transform: 'rotate(180deg)',
                                            alignContent: "center",
                                            justifyContent: "center"
                                        }}
                                    >
                                        {est}
                                    </Typography>

                                </Grid>
                            ))}
                        </Grid>

                        {/* Data Rows */}
                        {estudiantes.map((est1: string, rowIndex: number) => (
                            <Grid container
                                key={rowIndex}
                                direction="row"
                                alignContent="center"
                                justifyContent="center"
                                gap={0.5}
                            >
                                <Typography
                                    variant="caption"
                                    sx={{
                                        alignContent: 'center',
                                        mr: 1,
                                        width: 600 / estudiantes.length,
                                        textAlign: 'center'
                                    }}
                                >
                                    {est1}
                                </Typography>
                                {Object.keys(data[est1]).map((est2: string, colIndex: number) => (
                                    <Grid item key={colIndex}>
                                        <Link to="/Students" state={{est1: est1, est2: est2}} style={{ textDecoration: 'none' }}>
                                            <Card
                                                elevation={5}
                                                sx={{
                                                    width: 600 / estudiantes.length,
                                                    height: 300 / estudiantes.length,
                                                    justifyContent: 'center',
                                                    alignContent: 'center',
                                                    backgroundColor: est1 === est2 ? "#1E1E1E" :
                                                        data[est1][est2] <= 1 && data[est1][est2] >= 0.67 ? '#E15658' :
                                                            data[est1][est2] <= 0.66 && data[est1][est2] >= 0.34 ? '#E0C255' :
                                                                '#555661'
                                                }}
                                            >
                                                <CardContent>
                                                    <Typography variant="caption">
                                                        {data[est1][est2]}
                                                    </Typography>
                                                </CardContent>
                                            </Card>
                                        </Link>
                                    </Grid>
                                ))}
                            </Grid>
                        ))}
                    </>
                )}
            </Grid>
        </>
    );
}

export default HeatmapView;
