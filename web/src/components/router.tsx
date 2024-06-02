import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import HomePage from "../pages/home";
import UploadPage from "../pages/upload";

const Router = () => {
    const routes = (
        <Routes>
            <Route path="/Home" element={<HomePage />} />
            <Route path="/*" element={<Navigate to={"/Home"}/>} />

            <Route path="/Upload" element={<UploadPage />} />
        </Routes>
    )

    return ( 
        <BrowserRouter>
            {routes}
        </BrowserRouter>
    );
}

export default Router;