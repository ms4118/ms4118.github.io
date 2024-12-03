let gridInstances = {};
  
function isNumberMy(value) {
  return !isNaN(parseFloat(value)) && isFinite(value);
}

// 读取存储的表格数据（如果存在）
function loadTableData() {
    const storedData = localStorage.getItem("tableData");
    if (storedData) {
        return JSON.parse(storedData);
    }
    return null;
}

// 将表格数据存储到本地
function saveTableData(data) {
    localStorage.setItem("tableData", JSON.stringify(data));
}

function openModal() {
    // 获取输入框的值
    const rows = parseInt(document.getElementById("rows").value);
    const cols = parseInt(document.getElementById("cols").value);

    if (isNaN(rows) || isNaN(cols) || rows <= 0 || cols <= 0) {
        alert("请输入有效的行数和列数！");
        return;
    }

    // 生成表格内容
    let table = "<thead><tr><th class='row-title'></th>";
    for (let c = 1; c <= cols; c++) {
        table += `<th class='title'>Store ${c}</th>`;
    }
    table += "<th class='title'>Supply</th></tr></thead><tbody>";

    for (let r = 1; r <= rows+1; r++) {
        table += "<tr>";
        // 每一行前面加上一个显示行号的列
        if (r === rows+1) {
          table += `<td class="row-title">Demand</td>`;
        } else {
          table += `<td class="row-title">Factory ${r}</td>`;
        }
        for (let c = 1; c <= cols+1; c++) {
            // 最后一行和最后一列增加last的class名，用于监听事件
            if (r === rows+1 || c === cols+1) {
              if (r === rows+1 && c === cols+1) {
                table += `<td class="editable-cell"><input id="total" type="text" style="width:100%" readonly></td>`;
              } else {
                table += `<td class="editable-cell"><input class="last" type="text"></td>`;
              }
              continue
            }
            // 每个单元格是一个可编辑的输入框
            table += `<td class="editable-cell"><input type="text"></td>`;
        }
        table += "</tr>";
    }
    table += "</tbody>";

    // 显示表格并弹出弹窗
    document.getElementById("table").innerHTML = table;
    document.getElementById("modal").style.display = "flex";

    // 如果有存储的数据并且行列数匹配，填充表格
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
    // 获取表格所有单元格的输入框
    const inputs = document.querySelectorAll("#table input");
    let allFilled = true;
    let allNumber = true;
    let resultArray = [];

    // 检查每个单元格是否有值
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

    // 如果有空单元格，提醒用户
    if (!allFilled) {
        alert("请确保每个单元格都有值！");
    } else if (!allNumber) {
        alert("请确保每个单元格都是数字！");
    } else {
        // 如果所有单元格都有值，展示所有输入值
        resultArray.push(inputs[inputs.length - 1].value.trim());
        document.getElementById("result").textContent = resultArray.join(",");
        // 保存数据到本地存储
        saveTableData(resultArray);
        document.getElementById('show_data_tabel').click();
        closeModal(); // 关闭弹窗
    }
}

// 计算最后一行和最后一列的和
function calculateAndDisplaySum(rows, cols) {
    const inputs = document.querySelectorAll("#table input");
    let rowSum = 0;
    let colSum = 0;

    // 计算最后一行的和
    for (let c = 0; c < cols; c++) {
        let value = inputs[inputs.length - cols + c].value;
        if(isNumberMy(value)) {
          value = parseFloat(value);
        } else {
          value = 0
        }
        rowSum += value;
    }

    // 计算最后一列的和
    for (let r = 0; r < rows; r++) {
        let value = inputs[r * cols + cols - 1].value;
        if(isNumberMy(value)) {
          value = parseFloat(value);
        } else {
          value = 0
        }
        colSum += value;
    }

    // 显示和
    document.getElementById("total").value  = `${rowSum} / ${colSum}`;
}

function str2Aarry(str) {
    str = str.slice(1, -1); // 使用 slice 方法去除第一个和最后一个字符（即方括号）

    // 步骤2: 使用 split 方法按逗号分割字符串
    // 注意：这里我们得到一个包含字符串元素的数组，可能还需要进一步处理
    let arr = str.split(',').map(item => {
      // 去除元素两侧的空格（如果有的话）
      item = item.trim();
      item = item.replace(/^'|'$/g, '');

      return item;
    });

    return arr
}

function str2Aarry2D(str) {
  // 第一步：去除最外层的方括号
  str = str.slice(1, -1);

  // 第二步：按外部逗号分割字符串以获取内部数组的字符串表示
  let innerArrayStrs = str.split('], [');

  // 第三步：将每个内部数组的字符串表示转换为真正的数组
  let twoDArray = innerArrayStrs.map(str2Aarry)

  return twoDArray
}

function updateGridData(newData) {
  gridInstance.updateConfig({
    data: newData
  }).forceRender();  // 强制重新渲染
}

function setTable(headers, data, renderId) {
  const gridData = {
    columns: str2Aarry(headers).map((header, index) => ({
      id: `column-${index}`,  // 设置每列的唯一 ID
      name: header            // 使用列名作为显示的标题
    })),
    data: str2Aarry2D(data)
  }

  // 获取容器元素
  const container = document.getElementById(renderId);
  // 清空容器元素（虽然在这个例子中它应该是空的，但这是一个好习惯）
  container.innerHTML = '';
  // 渲染 Grid.js 表格
  if (gridInstances[renderId]) {
    gridInstances[renderId].destroy();
  } 
  gridInstances[renderId] = new gridjs.Grid(gridData)
  gridInstances[renderId].render(container);
}