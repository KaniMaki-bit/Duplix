import { useState } from "react";
import UploadView from "./view";

const UploadPage = () => {
    const [fileName, setFileName] = useState<string | null>(null);

    const handleUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (file && file.type === 'application/x-zip-compressed') {
            setFileName(file.name);
            console.log(file.text)
        } else {
            alert('Por favor, sube un archivo .zip');
        }
    };

    return (
        <UploadView
            fileName={fileName}
            handleUpload={handleUpload}
        />
    );
}

export default UploadPage;