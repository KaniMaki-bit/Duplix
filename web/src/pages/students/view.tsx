import React, { useState, useEffect } from "react";
import axios from 'axios';

import Navbar from "../../components/navbar";

import { Button, Grid, Paper, Typography } from "@mui/material";
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

const StudentsView: React.FC = () => {

    const [lista, setLista] = useState<string[]>([]);
    const [student_a, setStudent_a] = React.useState('');
    const [student_b, setStudent_b] = React.useState('');
    let datosEstudiantes = null;

    const [codigo1, setCodigo1] = useState<string>('');
    const [codigo2, setCodigo2] = useState<string>('');

    const [similitud_global,setSimilitud_global] = useState(0);

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
                    elevation={5}
                    sx={{
                        backgroundColor: "#333333",
                        color: "#FFFFFF",
                        p: 4,
                        width: "600px",
                        // minHeight: "300px",
                    }}
                >
                    <Typography variant="subtitle1" gutterBottom
                        sx={{
                            marginBottom: 2,
                            textAlign: 'initial'
                        }}
                    >
                        A continuación seleccione los archivos correspondientes a analizar:
                    </Typography>
                    <FormControl fullWidth sx={{ color: 'white' }}>
                        <InputLabel id="demo-simple-select-label" sx={{
                            color: 'white',
                        }}
                        >Estudiante 1</InputLabel>
                        <Select
                            labelId="demo-simple-select-label"
                            id="demo-simple-select"
                            value={student_a}
                            label="Estudiante1"
                            sx={{
                                color: 'white',
                                borderColor: "white",
                            }}
                            onChange={handleStudentAChange}
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
                        <InputLabel id="demo-simple-select-label" sx={{ color: 'white' }}>Estudiante 2</InputLabel>
                        <Select
                            labelId="demo-simple-select-label"
                            id="demo-simple-select"
                            value={student_b}
                            sx={{ 
                                color: 'white',
                             }}
                            label="Estudiante2"
                            onChange={handleStudentBChange}
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
                    elevation={5}
                    sx={{
                        backgroundColor: "#333333",
                        color: "#FFFFFF",
                        p: 4,
                        width: "600px",
                        // minHeight: "300px",
                    }}
                >
                    <Typography variant="subtitle1" gutterBottom
                        sx={{
                            marginBottom: 2,
                            textAlign: 'initial'
                        }}
                    >
                        En esta sección puede visualizar la similitudes de los códigos de acuerdo a sus cadenas de texto, métricas, y su similitud en conjunto:
                    </Typography>
                    <Box >
                   
                    </Box>
                </Grid>

            </Grid>
        </>
    );
}

export default StudentsView;
