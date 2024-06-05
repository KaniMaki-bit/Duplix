import { useEffect, useState } from "react";
import HeatmapView from "./view";
import { EstudiantesAPI, HeatmapAPI } from "../../services";

const HeatmapPage = () => {
    const [data, setData] = useState({})
    const [estudiantes, setEstudiantes] = useState([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const fetchAnalisis = async () => {
            const res = await HeatmapAPI()
            if (res?.status === 200) {
                setData(res.data)
            } else {
                alert('Ocurrió un problema al analizar.');
            }
        }

        const fetchEstudiantes = async () => {
            const res = await EstudiantesAPI()
            if (res?.status === 200) {
                setEstudiantes(res.data)
            } else {
                alert('Ocurrió un problema al obtener estudiantes.');
            }
        }

        fetchAnalisis();
        fetchEstudiantes();
    }, [])

    useEffect(() => {
        if(estudiantes.length !== 0 && Object.keys(data).length !== 0) setLoading(false)
    }, [data, estudiantes])

    return (
        <HeatmapView
            loading={loading}
            data={data}
            estudiantes={estudiantes}
        />
    );
}

export default HeatmapPage;