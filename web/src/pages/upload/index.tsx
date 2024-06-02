import { PingAPI } from "../../services/ping";
import UploadView from "./view";

const UploadPage = () => {

    PingAPI();

    const handleUpload = () => {

    }

    return (
        <UploadView
            handleUpload={handleUpload}
        />
    );
}

export default UploadPage;