import axios from "axios";

export const PingAPI = async () => {
    try {
        const res = await axios.request({
            method: 'GET',
            url: 'http://localhost:5000/ping'
        });
        console.log(res)
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