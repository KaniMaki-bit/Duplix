import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import HomePage from "../pages/home";
import UploadPage from "../pages/upload";
import HeatmapPage from "../pages/heatmap";

const Router = () => {
    const routes = (
        <Routes>
            <Route path="/Home" element={<HomePage />} />
            <Route path="/*" element={<Navigate to={"/Home"}/>} />

            <Route path="/Upload" element={<UploadPage />} />
            <Route path="/Heatmap" element={<HeatmapPage />} />
        </Routes>
    )

    return ( 
        <BrowserRouter>
            {routes}
        </BrowserRouter>
    );
}

export default Router;