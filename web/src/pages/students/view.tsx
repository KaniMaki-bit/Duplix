import React, { useState, useEffect } from "react";
import axios from 'axios';

import Navbar from "../../components/navbar";

import { Button, Grid, Paper, Typography } from "@mui/material";
import { TableContainer, Table, TableHead, TableBody, TableRow, TableCell } from '@mui/material';
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import CircularProgress from '@mui/material/CircularProgress';
import { styled } from '@mui/material/styles';
import Stack from "@mui/material";

import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { dracula } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { useLocation } from "react-router-dom";

const StudentsView: React.FC = () => {
    const location = useLocation();

    const [res, setRes] = useState<any>();

    const [lista, setLista] = useState<string[]>([]);
    const [student_a, setStudent_a] = React.useState(location.state.est1 || "");
    const [student_b, setStudent_b] = React.useState(location.state.est2 || "");
    let datosEstudiantes = null;

    const [codigo1, setCodigo1] = useState<string>('');
    const [codigo2, setCodigo2] = useState<string>('');

    const [similitud_global, setSimilitud_global] = useState(0);

    const Item = styled(Paper)(({ theme }) => ({
        backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
        ...theme.typography.body2,
        padding: theme.spacing(1),
        textAlign: 'left',
        color: theme.palette.text.secondary,
    }));

    const buildApiUrl = (matricula1: string, matricula2: string) => {
        const baseUrl = 'http://127.0.0.1:5000/comparar';
        const queryParams = `?matricula1=${matricula1}&matricula2=${matricula2}`;
        return baseUrl + queryParams;
    };


    const handleStudentAChange = (event: React.ChangeEvent<{ value: unknown }>) => {
        setStudent_a(event.target.value as string);
    };

    const handleStudentBChange = (event: React.ChangeEvent<{ value: unknown }>) => {
        setStudent_b(event.target.value as string);
    };


    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get<string[]>('http://localhost:5000/estudiantes');
                setLista(response.data);
                // console.log(response.data);
            } catch (error) {
                console.error('Error obteniendo los estudiantes:', error);
            }

            if (student_a && student_b) {
                // console.log("Los estudiantes son válidos");
                try {
                    const apiUrl = buildApiUrl(student_a, student_b);
                    const response = await axios.get(apiUrl);
                    datosEstudiantes = response.data;

                    if (datosEstudiantes) {
                        const codigo = datosEstudiantes.codigo;
                        const codigo1 = Object.values(codigo)[0];
                        setCodigo1(codigo1);
                        const codigo2 = Object.values(codigo)[1];
                        setCodigo2(codigo2);
                        setSimilitud_global(datosEstudiantes.similitud);
                    } else {
                        console.warn('No hay datos disponibles en datosEstudiantes.');
                    }
                    console.log('Respuesta de la API:', response.data);
                    setRes(response.data)
                    // const porcentaje_similitud = response.data.similitud * 100;

                } catch (error) {
                    console.error('Error al obtener datos de la API:', error);
                }
            }
        };

        fetchData();
    }, [student_a, student_b]);




    const studentMap: { [key: string]: string } = {};
    lista.forEach((studentId) => {
        studentMap[studentId] = studentId;
    });

    return (
        <>
            <Navbar />
            <Grid container columns={2}
                height='90vh'
                // alignContent='center'
                // justifyContent='center'
                gap={5}
                sx={{
                    display: 'flex',
                    m: 2,
                }}
            >
                <Grid
                    sx={{
                        backgroundColor: "#CFCFCF",
                        color: "#FFFFFF",
                        p: 4,
                        width: "600px",
                        // minHeight: "300px",
                    }}
                >
                    <Grid item xs={12}
                        sx={{
                            p: 1
                        }}>
                        <Typography variant="h5"
                        sx={{
                            color: 'black',
                        }}>
                            Análisis por bloques
                        </Typography>
                    </Grid>
                    <Typography variant="subtitle1" gutterBottom
                        sx={{
                            marginBottom: 2,
                            textAlign: 'initial',
                            color: 'black',
                        }}
                    >
                        A continuación seleccione los archivos correspondientes a analizar:
                    </Typography>
                    <FormControl fullWidth sx={{ color: 'black' }}>
                        <InputLabel id="demo-simple-select-label" sx={{
                            color: 'black',
                        }}
                        >Estudiante 1</InputLabel>
                        <Select
                            labelId="demo-simple-select-label"
                            id="demo-simple-select"
                            value={student_a}
                            label="Estudiante1"
                            sx={{
                                color: 'black',
                                borderColor: "white",
                            }}
                            onChange={() => handleStudentAChange}
                        >
                            {Object.keys(studentMap).map((studentId) => (
                                <MenuItem key={studentId} value={studentId}>
                                    {studentMap[studentId]}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                    <SyntaxHighlighter language="python" style={dracula}>
                        {codigo1}
                    </SyntaxHighlighter>
                    <FormControl fullWidth>
                        <InputLabel id="demo-simple-select-label" sx={{ color: 'black' }}>Estudiante 2</InputLabel>
                        <Select
                            labelId="demo-simple-select-label"
                            id="demo-simple-select"
                            value={student_b}
                            sx={{
                                color: 'black',
                            }}
                            label="Estudiante2"
                            onChange={() => handleStudentBChange}
                        >
                            {Object.keys(studentMap).map((studentId) => (
                                <MenuItem key={studentId} value={studentId}>
                                    {studentMap[studentId]}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                    <SyntaxHighlighter language="python" style={dracula}>
                        {codigo2}
                    </SyntaxHighlighter>
                </Grid>
                <Grid
                    container
                    sx={{
                        backgroundColor: "#333333",
                        color: "#FFFFFF",
                        p: 4,
                        width: "600px",
                    }}
                >
                    {
                        res && (
                            <>
                                <Grid item xs={12}
                                    sx={{
                                        p: 1
                                    }}>
                                    <Typography variant="h5">
                                        Resumen de similitud
                                    </Typography>
                                </Grid>
                                <TableContainer component={Paper}>
                                    <Table>
                                        <TableBody>
                                            <TableRow>
                                                <TableCell>Porcentaje de similitud por bloques:</TableCell>
                                                <TableCell>{res.codigo.similitud*100}%</TableCell>
                                            </TableRow>
                                            <TableRow>
                                                <TableCell>Porcentaje de similitud por métricas:</TableCell>
                                                <TableCell>{res.metricas.similitud*100}%</TableCell>
                                            </TableRow>
                                            <TableRow>
                                                <TableCell>Porcentaje de similitud global:</TableCell>
                                                <TableCell>{res.similitud*100}%</TableCell>
                                            </TableRow>
                                            <TableRow>
                                                <TableCell>Clasificación de métricas: </TableCell>
                                                <TableCell>{res.metricas.clasificacion}</TableCell>
                                            </TableRow>
                                        </TableBody>
                                    </Table>
                                </TableContainer>
                                <Grid item
                                    xs={12}
                                    sx={{
                                        p: 2
                                    }}>
                                    <Typography variant="h5">
                                        Expresiones
                                    </Typography>
                                    <Typography variant="subtitle1" gutterBottom
                                        sx={{
                                            textAlign: 'initial',
                                            color: 'white',
                                        }}
                                    >
                                        En esta sección se muestra un análisis de métricas de la categoría de expresiones de cada uno de los archivos.
                                    </Typography>
                                </Grid>
                                <TableContainer component={Paper}>
                                    <Table>
                                        <TableHead>
                                            <TableRow>
                                                <TableCell>Expresión</TableCell>
                                                <TableCell>Est1</TableCell>
                                                <TableCell>Est2</TableCell>
                                                <TableCell>Clasificación</TableCell>
                                            </TableRow>
                                        </TableHead>
                                        <TableBody>
                                            {Object.keys(res.metricas.deltas.expresiones).map((key) => (
                                                <TableRow key={key}>
                                                    <TableCell>{key}:</TableCell>
                                                    <TableCell>{res.metricas.deltas.expresiones[key]["archivo 1"]}</TableCell>
                                                    <TableCell>{res.metricas.deltas.expresiones[key]["archivo 2"]}</TableCell>
                                                    <TableCell>{res.metricas.deltas.expresiones[key]["clasificacion"]}</TableCell>
                                                </TableRow>
                                            ))}
                                        </TableBody>
                                    </Table>
                                </TableContainer>
                                <Grid item
                                    xs={12}
                                    sx={{
                                        p: 2
                                    }}>
                                    <Typography variant="h5">
                                        Flujo de Control
                                    </Typography>
                                    <Typography variant="subtitle1" gutterBottom
                                        sx={{
                                            textAlign: 'initial',
                                            color: 'white',
                                        }}
                                    >
                                        En este apartado se muestra un análisis de métricas de la categoría del flujo de control de cada uno de los archivos, donde se describe la secuencia en la que se ejecutan las instrucciones.
                                    </Typography>
                                </Grid>
                                <TableContainer component={Paper}>
                                    <Table>
                                        <TableHead>
                                            <TableRow>
                                                <TableCell>Expresión</TableCell>
                                                <TableCell>Est1</TableCell>
                                                <TableCell>Est2</TableCell>
                                                <TableCell>Clasificación</TableCell>
                                            </TableRow>
                                        </TableHead>
                                        <TableBody>
                                            {Object.keys(res.metricas.deltas["flujo de control"]).map((key) => (
                                                <TableRow key={key}>
                                                    <TableCell>{key}:</TableCell>
                                                    <TableCell>{res.metricas.deltas["flujo de control"][key]["archivo 1"]}</TableCell>
                                                    <TableCell>{res.metricas.deltas["flujo de control"][key]["archivo 2"]}</TableCell>
                                                    <TableCell>{res.metricas.deltas["flujo de control"][key]["clasificacion"]}</TableCell>
                                                </TableRow>
                                            ))}
                                        </TableBody>
                                    </Table>
                                </TableContainer>
                                <Grid item
                                    xs={12}
                                    sx={{
                                        p: 2
                                    }}
                                >
                                    <Typography variant="h5">
                                        Layout
                                    </Typography>
                                    <Typography variant="subtitle1" gutterBottom
                                        sx={{
                                            textAlign: 'initial',
                                            color: 'white',
                                        }}
                                    >
                                        En este último apartado se muestra un análisis de métricas de la categoría de layout, donde se analisa la organización y la disposición visual del código.
                                    </Typography>
                                </Grid>
                                <TableContainer component={Paper}>
                                    <Table>
                                        <TableHead>
                                            <TableRow>
                                                <TableCell>Expresión</TableCell>
                                                <TableCell>Est1</TableCell>
                                                <TableCell>Est2</TableCell>
                                                <TableCell>Clasificación</TableCell>
                                            </TableRow>
                                        </TableHead>
                                        <TableBody>
                                            {Object.keys(res.metricas.deltas.layout).map((key) => (
                                                <TableRow key={key}>
                                                    <TableCell>{key}:</TableCell>
                                                    <TableCell>{res.metricas.deltas.layout[key]["archivo 1"]}</TableCell>
                                                    <TableCell>{res.metricas.deltas.layout[key]["archivo 2"]}</TableCell>
                                                    <TableCell>{res.metricas.deltas.layout[key]["clasificacion"]}</TableCell>
                                                </TableRow>
                                            ))}
                                        </TableBody>
                                    </Table>
                                </TableContainer>
                            </>
                        )
                    }
                </Grid>

            </Grid>
        </>
    );
}

export default StudentsView;
