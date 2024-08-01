const express = require("express");
const bodyParser = require("body-parser");
const axios = require("axios");

const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

module.exports = app;

function generateTableHTML(data, options) {
  let template = `
      <!doctype html>
      <style>
      ::-webkit-scrollbar {
        width: 0.6em;
      }

      ::-webkit-scrollbar-thumb {
        background-color: #b8d1b9;
        border-radius: 10px;
        border: 7px solid #b8d1b9;
      }

      ::-webkit-scrollbar-track {
        background-color: rbga(0, 0, 0, 0);
      }
      .active {
        background-color:#a5d6a7
      }

      table {
        border: 1px #a39485 solid;
        font-size: 0.9em;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.25);
        width: 100%;
        border-collapse: collapse;
        border-radius: 5px;
        overflow: hidden;
      }

      th {
        text-align: center;
      }

      thead {
        font-weight: bold;
        color: #fff;
        background: #2f6e54;
      }

      td,
      th {
        padding: 1em 0.5em;
        vertical-align: middle;
        text-align: center;
      }

      td {
        border-bottom: 1px solid rgba(0, 0, 0, 0.1);
        background: #fff;
      }

      @media all and (max-width: 768px) {
        table,
        thead,
        tbody,
        th,
        td,
        tr {
          display: block;
        }

        th {
          text-align: right;
        }

        table {
          position: relative;
          padding-bottom: 0;
          border: none;
          box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
        }

        thead {
          float: left;
          white-space: nowrap;
        }

        tbody {
          overflow-x: auto;
          overflow-y: hidden;
          position: relative;
          white-space: nowrap;
        }

        tr {
          display: inline-block;
          vertical-align: top;
        }

        th {
          border-bottom: 1px solid #a39485;
        }

        td {
          border-bottom: 1px solid #e5e5e5;
        }
      }

      </style>
      <table>
        <thead>
          <tr>
            <th>순위</th>
            <th>지역</th>
            <th>종합</th>
            <th>교육</th>
            <th>안전</th>
            <th>의료</th>
            <th>환경</th>
          </tr>
        </thead>
        <tbody>
      `;
  if (!options) {
    for (var i = 0; i < Object.keys(data).length; i++) {
      template += `
                <tr>
                    <td>${i + 1}</td>
                    <td>${data[i]["loc"]}</td>
                    <td>${data[i]["tot"]}</td>
                    <td>${data[i]["edu"]}</td>
                    <td>${data[i]["saf"]}</td>
                    <td>${data[i]["med"]}</td>
                    <td>${data[i]["env"]}</td>
                </tr>
            `;
    }
  } else {
    for (let i = 0; i < Object.keys(data).length; i++) {
      template += `
      <tr>
        <td>${i + 1}</td>
        <td>${data[i]["loc"]}</td>
        <td${options.length === 4 ? ' class="active"' : ""}>${
        data[i]["tot"]
      }</td>
        <td${options.includes("1") ? ' class="active"' : ""}>${
        data[i]["edu"]
      }</td>
        <td${options.includes("2") ? ' class="active"' : ""}>${
        data[i]["saf"]
      }</td>
        <td${options.includes("3") ? ' class="active"' : ""}>${
        data[i]["med"]
      }</td>
        <td${options.includes("4") ? ' class="active"' : ""}>${
        data[i]["env"]
      }</td>
      </tr>
    `;
    }
  }

  template += `
  </tbody>
</table>
`;

  return template;
}

const fetchCategoryTop3 = async () => {
  try {
    const response = await axios.get(
      "http://192.168.1.81:3000/select/categorytop3"
    );
    return response.data;
  } catch (error) {
    console.error(error);
    throw new Error("Failed to fetch category top 3");
  }
};

app.get("/search", (req, res) => {
  const city = req.query.city;
  const optionsQuery = req.query.options;
  let options = optionsQuery;
  var url = "http://192.168.1.81:3000/search";
  url += "?addr=";
  url += city;
  if (!req.query.options) {
    console.log("no option");
    options = ["1", "2", "3", "4"];
  }
  for (i = 0; i < options.length; i++) {
    url += "&options=";
    url += options[i];
  }
  // 서버로 요청 보내기
  axios
    .get(url)
    .then(function (response) {
      // 결과를 받아와서 템플릿 채우기
      var data = response.data;
      res.writeHead(200);
      var template = generateTableHTML(data, options);
      res.end(template);
    })
    .catch(function (error) {
      console.log(error);
    });
});

app.get("/select/top10", (req, res) => {
  axios
    .get("http://192.168.1.81:3000/select/top10")
    .then((response) => {
      const data = response.data;
      res.writeHead(200);
      var template = generateTableHTML(data);
      res.end(template);
    })
    .catch((error) => {
      res
        .status(500)
        .json({ error: "Failed to fetch data from FastAPI server" });
    });
});

app.get("/select/categorytop3/:category", async (req, res) => {
  const category = req.params.category;

  try {
    let ctg;
    const data = await fetchCategoryTop3();
    await axios.get("http://192.168.1.81:3000/select/categorytop3/graphs");
    const medData = data[0];
    const envData = data[1];
    const eduData = data[2];
    const safData = data[3];
    if (category == "med") {
      ctg = medData;
    } else if (category == "env") {
      ctg = envData;
    } else if (category == "edu") {
      ctg = eduData;
    } else if (category == "saf") {
      ctg = safData;
    } else {
      return res.status(400).json({ error: "Invalid" });
    }

    res.writeHead(200);
    var template = generateTableHTML(ctg);
    res.end(template);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "An error occurred" });
  }
});
