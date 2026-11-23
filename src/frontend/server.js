const express = require("express");
const path = require("path");
const { createProxyMiddleware } = require("http-proxy-middleware");

const app = express();
const PORT = process.env.PORT || 3000;


app.use(
    createProxyMiddleware({
        pathFilter: "/api",
        target: process.env.BACKEND_URL || "http://localhost:8000",
        changeOrigin: true
    })
);


app.use(express.static(path.join(__dirname, "public")));

app.get("/health", (req, res) => {
    res.json({
        status: "healthy",
        service: "frontend"
    });
});

if (require.main === module) {
    app.listen(PORT, "0.0.0.0", () => {
        console.log(`Frontend running on port ${PORT}`);
    });
}

module.exports = app;