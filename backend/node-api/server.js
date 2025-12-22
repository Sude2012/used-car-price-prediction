const express = require("express");
const axios = require("axios");

const app = express();
const PORT = 4000;

app.use(express.json());

// CORS
app.use((req, res, next) => {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Content-Type, Authorization");
    res.header("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
    next();
});





app.get("/api/fuel", async (req, res) => {
    try {
        const response = await axios.get(

            "https://api.collectapi.com/gasPrice/turkeyGasoline?district=kadikoy&city=istanbul",
            {
                headers: {

                    authorization: "apikey 7141t5QMQ4MFrk3PGX8cKq:3RlQH7ZRHsDcMlTbt16IyF",
                    "content-type": "application/json"
                }
            }
        );

        const state = response.data.result.state[0];

        res.json({
            success: true,
            result: [{
                gasoline: state.gasoline,
                diesel: state.diesel,
                fuelOil: state.diesel
            }],
            note: "Demo data used"
        });

    } catch (error) {
        res.json({
            success: true,
            result: [{
                gasoline: 45.32,
                diesel: 46.81,
                fuelOil: 39.75
            }]
        });
    }
});


// PYTHON API
app.post("/api/predict", async (req, res) => {
    try {
        const response = await axios.post(
            "http://127.0.0.1:8000/predict",
            req.body
        );
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: "Python API hatası" });
    }
});

app.listen(PORT, () => {
    console.log(`Node API aktif: http://localhost:${PORT}`);
});