import { useEffect, useState } from "react";
import JSZip from 'jszip';
import UploadView from "./view";
import { ArchivosAPI } from "../../services";

const UploadPage = () => {
    const [fileName, setFileName] = useState<string | null>(null);
    const [fileContents, setFileContents] = useState<Record<string, string>>({});
    const [allow, setAllow] = useState<boolean>(false)
    const [loadingUpload, setLoadingUpload] = useState<boolean>(false)

    // Funcion para la carga de archivos
    const handleUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        // Que exista el archivo y que sea .zip
        if (file && file.type === 'application/x-zip-compressed') {
            // Nombre del .zip para despliegue
            setFileName(file.name);
            // Largo del nombre del archivo .zip
            const nameLength = file.name.length - 3;

            // Asignación del .zip
            const zip = new JSZip();
            const zipContent = await zip.loadAsync(file);
            // Variable del objeto que se va a mandar a la api
            const newFileContents: Record<string, string> = {};

            // Generación del objeto
            await Promise.all(
                Object.keys(zipContent.files).map(async (fileName: any) => {
                    const fileData = zipContent.file(fileName);
                    if (fileData) {
                        // Contenido del archivo
                        const fileText = await fileData.async("text");
                        // Nombre de la llave
                        const key = fileName.substring(nameLength, nameLength + 9);
                        // Asignación
                        newFileContents[key] = fileText;
                    }
                })
            );

            setFileContents(newFileContents);

        } else {
            alert('Por favor, sube un archivo .zip');
        }
    };

    // Se intenta subir los archivos al servidor
    useEffect(() => {
        // Función para subir
        const sendData = async () => {
            setLoadingUpload(true);
            if (Object.keys(fileContents).length > 0) {
                // Transforma la varible de los archivos a un json
                const jsonContent = JSON.stringify(fileContents, null, 2);
                // Llamada a la api
                const res = await ArchivosAPI(jsonContent);
                if (res === 204) {
                    // Si se pudieron subir, deja continuar el flujo
                    setAllow(true);
                } else {
                    // Si no, manda un alert
                    setAllow(false)
                    alert('Ocurrió un error en la carga del .zip');
                }
            }
        }
        // Llamada a la función
        sendData();
        setLoadingUpload(false);
    }, [fileContents])

    return (
        <UploadView
            fileName={fileName}
            handleUpload={handleUpload}
            allow={allow}
            loadingUpload={loadingUpload}
        />
    );
}

export default UploadPage;