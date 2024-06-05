import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import HomePage from "../pages/home";
import UploadPage from "../pages/upload";
import StudentsPage from "../pages/students";

const Router = () => {
    const routes = (
        <Routes>
            <Route path="/Home" element={<HomePage />} />
            <Route path="/*" element={<Navigate to={"/Home"}/>} />

            <Route path="/Upload" element={<UploadPage />} />
            <Route path="/Students" element={<StudentsPage />} />
        </Routes>
    )

    return ( 
        <BrowserRouter>
            {routes}
        </BrowserRouter>
    );
}

export default Router;