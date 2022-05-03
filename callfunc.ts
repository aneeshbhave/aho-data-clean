const HttpRequest = require("xhr2")
const fs = require("fs")

const Http = new HttpRequest()
const dict =[
 {
   "name": "Ema Pratt",
   "number": 2626967298
 },
 {
   "name": "Esmeralda Roberts",
   "number": 9145259670
 },
 {
   "name": "Carl Todd",
   "number": 6794748377
 },
 {
   "name": "Peyton Williams",
   "number": 7682207191
 },
 {
   "name": "Denny Carson",
   "number": "7304890075"
 },
 {
   "name": "Rosemary Nelson",
   "number": "+1 726-684-(2617)"
 },
 {
   "name": "Jack Forth",
   "number": "+91 2137158 2 3 3"
 },
]

const files = [
    "dba.csv",
    "dbb.csv",
    "dbc.csv",
]

const url = `https://us-central1-aneesh-data-clean-aho.cloudfunctions.net/data-clean-aho?bucket=${"phone-numberdb"}&db=${JSON.stringify(files)}&dict=${JSON.stringify(dict)}`;
Http.open("POST", url)
Http.send();

Http.onreadystatechange = (e) => {
    console.log(Http.responseText)
}
