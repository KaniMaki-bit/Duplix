import axios from "axios";

export const PingAPI = async () => {
    try {
        const res = await axios.request({
            method: 'GET',
            url: 'http://localhost:5000/ping'
        });
        return(res)
    } catch (error) {
        console.error(error);
    }
}

export const ArchivosAPI = async (archivos: any) => {
    try {
        const res = await axios.request({
            method: 'POST',
            url: 'http://localhost:5000/archivos',
            headers: {
                'Content-Type': 'application/json'
            },
            data: archivos
        });
        return(res.status)
    } catch (error) {
        console.error(error);
    }
}

export const EstudiantesAPI = async () => {
    try {
        const res = await axios.request({
            method: 'GET',
            url: 'http://localhost:5000/estudiantes'
        });
        return(res)
    } catch (error) {
        console.error(error);
    }
}

export const HeatmapAPI = async () => {
    try {
        const res = await axios.request({
            method: 'GET',
            url: 'http://localhost:5000/heatmap'
        });
        return(res)
    } catch (error) {
        console.error(error);
    }
}