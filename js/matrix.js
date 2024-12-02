let gridInstances = {};
  
function isNumberMy(value) {
  return !isNaN(parseFloat(value)) && isFinite(value);
}

function loadTableData() {
    const storedData = localStorage.getItem("tableData");
    if (storedData) {
        return JSON.parse(storedData);
    }
    return null;
}

// same to local
function saveTableData(data) {
    localStorage.setItem("tableData", JSON.stringify(data));
}

function openModal() {
    // get matrix
    const rows = parseInt(document.getElementById("rows").value);
    const cols = parseInt(document.getElementById("cols").value);

    if (isNaN(rows) || isNaN(cols) || rows <= 0 || cols <= 0) {
        alert("Please enter valid");
        return;
    }

    // generate
    let table = "<thead><tr><th class='row-title'></th>";
    for (let c = 1; c <= cols; c++) {
        table += `<th class='title'>Store ${c}</th>`;
    }
    table += "<th class='title'>Supply</th></tr></thead><tbody>";

    for (let r = 1; r <= rows+1; r++) {
        table += "<tr>";
        if (r === rows+1) {
          table += `<td class="row-title">Demand</td>`;
        } else {
          table += `<td class="row-title">Factory ${r}</td>`;
        }
        for (let c = 1; c <= cols+1; c++) {
            if (r === rows+1 || c === cols+1) {
              if (r === rows+1 && c === cols+1) {
                table += `<td class="editable-cell"><input id="total" type="text" style="width:100%" readonly></td>`;
              } else {
                table += `<td class="editable-cell"><input class="last" type="text"></td>`;
              }
              continue
            }
            table += `<td class="editable-cell"><input type="text"></td>`;
        }
        table += "</tr>";
    }
    table += "</tbody>";

    document.getElementById("table").innerHTML = table;
    document.getElementById("modal").style.display = "flex";

    const storedData = loadTableData();
    if (storedData && storedData.length === (rows+1) * (cols+1)) {
        let dataIndex = 0;
        const inputs = document.querySelectorAll("#table input");
        inputs.forEach(input => {
            input.value = storedData[dataIndex++];
        });
    }
    const lastInputs = document.querySelectorAll('.last');

    lastInputs.forEach(input => {
      input.addEventListener('input', () => {
      calculateAndDisplaySum(rows+1, cols+1);
  })
});
}

function closeModal() {
    document.getElementById("modal").style.display = "none";
}

function confirmTable() {
    const inputs = document.querySelectorAll("#table input");
    let allFilled = true;
    let allNumber = true;
    let resultArray = [];

    for (let i = 0; i < inputs.length - 1; i++) {
      const input = inputs[i];
      if (input.value.trim() === "") {
          allFilled = false;
      } else if (!isNumberMy(input.value.trim())) {
          allNumber = false;
      } else {
          resultArray.push(input.value.trim());
      }
    }

    if (!allFilled) {
        alert("Please enter");
    } else if (!allNumber) {
        alert("Please enter");
    } else {
        resultArray.push(inputs[inputs.length - 1].value.trim());
        document.getElementById("result").textContent = resultArray.join(",");
        saveTableData(resultArray);
        document.getElementById('show_data_tabel').click();
        closeModal(); 
    }
}

// last row and column
function calculateAndDisplaySum(rows, cols) {
    const inputs = document.querySelectorAll("#table input");
    let rowSum = 0;
    let colSum = 0;
    for (let c = 0; c < cols; c++) {
        let value = inputs[inputs.length - cols + c].value;
        if(isNumberMy(value)) {
          value = parseFloat(value);
        } else {
          value = 0
        }
        rowSum += value;
    }
    for (let r = 0; r < rows; r++) {
        let value = inputs[r * cols + cols - 1].value;
        if(isNumberMy(value)) {
          value = parseFloat(value);
        } else {
          value = 0
        }
        colSum += value;
    }

    document.getElementById("total").value  = `${rowSum} / ${colSum}`;
}

function str2Aarry(str) {
    str = str.slice(1, -1); 

    let arr = str.split(',').map(item => {
      item = item.trim();
      item = item.replace(/^'|'$/g, '');

      return item;
    });

    return arr
}

function str2Aarry2D(str) {
  str = str.slice(1, -1);

  let innerArrayStrs = str.split('], [');

  let twoDArray = innerArrayStrs.map(str2Aarry)

  return twoDArray
}

function updateGridData(newData) {
  gridInstance.updateConfig({
    data: newData
  }).forceRender();  
}

function setTable(headers, data, renderId) {
  const gridData = {
    columns: str2Aarry(headers).map((header, index) => ({
      id: `column-${index}`,  
      name: header            
    })),
    data: str2Aarry2D(data)
  }

  const container = document.getElementById(renderId);
  container.innerHTML = '';
  if (gridInstances[renderId]) {
    gridInstances[renderId].destroy();
  } 
  gridInstances[renderId] = new gridjs.Grid(gridData)
  gridInstances[renderId].render(container);
}
