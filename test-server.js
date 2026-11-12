const http = require('http');
const server = http.createServer(async (req, res) => {
    res.end('<h1 style="color:green;">Todo List App is working!</h1>');
});

async function start() {
    const port = 63330;
    await new Promise((resolve) => server.listen(port, resolve));
    console.log(`Server running on http://localhost:${port}/`);
    process.exit(0);
}

start();
