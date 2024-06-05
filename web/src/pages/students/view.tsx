import React, { useState, useEffect } from "react";
import axios from 'axios';

import Navbar from "../../components/navbar";

import { Button, Grid, Paper, Typography } from "@mui/material";
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import { styled } from '@mui/material/styles';

const StudentsView: React.FC = () => {
    
    const [lista]
    const [student_a, setStudent_a] = React.useState('');
    const [student_b, setStudent_b] = React.useState('');

    const Item = styled(Paper)(({ theme }) => ({
        backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
        ...theme.typography.body2,
        padding: theme.spacing(1),
        textAlign: 'center',
        color: theme.palette.text.secondary,
    }));

    const handleChange = (event: SelectChangeEvent) => {
        setStudent_a(event.target.value as string);
      };

    return (
        <>
            <Navbar />
            <Grid container columns={2}
                height='90vh'
                // alignContent='center'
                // justifyContent='center'
                gap={5}
                sx={{
                    display: 'flex'
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
                    <Typography>
                        Contenido de la vista de estudiantes
                    </Typography>
                    <FormControl fullWidth>
                        <InputLabel id="demo-simple-select-label">Estudiante 1</InputLabel>
                        <Select
                            labelId="demo-simple-select-label"
                            id="demo-simple-select"
                            value={student_a}
                            label="Age"
                            onChange={handleChange}
                        >
                            <MenuItem value={10}>Ten</MenuItem>
                            <MenuItem value={20}>Twenty</MenuItem>
                            <MenuItem value={30}>Thirty</MenuItem>
                        </Select>
                    </FormControl>
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
                    <Typography>
                        Contenido de la vista de estudiantes
                    </Typography>
                </Grid>

            </Grid>
        </>
    );
}

export default StudentsView;
