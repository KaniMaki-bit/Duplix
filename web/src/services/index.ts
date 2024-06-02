import axios from "axios";

export const PingAPI = async () => {
    try {
        const res = await axios.request({
            method: 'GET',
            url: 'http://localhost:5000/ping'
        });
        console.log(res.data)
    } catch (error) {
        console.error(error);
    }
}