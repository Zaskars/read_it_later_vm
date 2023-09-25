const express = require('express');
const puppeteer = require('puppeteer');
const consts = require('./consts')
const app = express();

app.use(express.json()) // for parsing application/json
app.get("/", async (req, res) => {
    const url = req.query[`url`];
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto(url, {waitUntil: 'load', timeout: 0});
    await page.addStyleTag(
        {content: '.fixed {display:none}'
        });
    const pdf = await page.pdf({
        format: 'A5',
        printBackground: true,
        scale: 0.5,
        waitUntil: 'load'
    });
    await browser.close();
    res.contentType("application/pdf");
    res.send(pdf);
});
const PORT = consts.PORT
const HOST = consts.HOST
app.listen(PORT, HOST);
console.log(`webserver started on ${PORT} port`);