const dataCenter = [];

// --- Enum part
const FileType = {
    PDF: 1,
};

const Status = {
    Uploading: 1, // black
    Parsing: 2, // blue
    Completed: 3, // green
    Failed: 9, // red
};

// --- General function
function deepClone(obj) {
    return JSON.parse(JSON.stringify(obj));
}

function formatUA(timestamp) {
    timestamp = timestamp * 1000;
    const date = new Date(timestamp);

    // 提取月份、日期和年份
    const month = date.getMonth() + 1; // JavaScript 的月份從 0 開始
    const day = date.getDate();
    const year = date.getFullYear();

    // 提取小時、分鐘和秒數
    let hours = date.getHours();
    const minutes = date.getMinutes().toString().padStart(2, "0");
    const seconds = date.getSeconds().toString().padStart(2, "0");

    // 判斷 AM/PM
    const ampm = hours >= 12 ? "PM" : "AM";
    hours = hours % 12 || 12; // 將 0 轉換為 12（12 小時制）

    // 格式化日期字串
    return `${month}/${day}/${year} ${hours}:${minutes}:${seconds} ${ampm}`;
}

function formatFT(fileType){
    switch(fileType){
        case FileType.PDF:
        default:
            return "PDF";
    }
}

function formatStatus(status){
    switch(status){
        case Status.Uploading:
            return "Uploading";
    
        case Status.Parsing:
            return "Parsing";    

        case Status.Completed:
            return "Completed";

        case Status.Failed:
            return "Failed";

        default:
            return "Unknown";
    }
}

// --- Main function
// TODO:: implement ajax
function importData(callbackFun) {
    // --- Fake data for test
    let testData = {
        id: 1,
        fileName: "testFile_1",
        uploadedAt: 1630096372, // 2021年8月28日星期六 04:32:52 GMT+08:00
        fileType: FileType.PDF,
        status: Status.Uploading,
    };
    dataCenter.push(deepClone(testData));

    testData.id++;
    testData.fileName = "testFile_" + testData.id;
    testData.uploadedAt += 10000;
    testData.status = Status.Parsing;
    dataCenter.push(deepClone(testData));

    testData.id++;
    testData.fileName = "testFile_" + testData.id;
    testData.uploadedAt += 10000;
    testData.status = Status.Completed;
    dataCenter.push(deepClone(testData));

    testData.id++;
    testData.fileName = "testFile_" + testData.id;
    testData.uploadedAt += 10000;
    testData.status = Status.Failed;
    dataCenter.push(deepClone(testData));

    console.log(dataCenter);

    callbackFun(dataCenter);
}

function renderData(srcData) {
    const tbody = $("#fileList tbody");
    if (!srcData || srcData.length == 0) {
        // TODO:: render 「No data found.」 hint.
        return;
    }

    tbody.empty();
    for (let i = 0; i < srcData.length; i++) {
        const aFileRec = srcData[i];
        const trEle = $(`<tr rec_id="${aFileRec.id}" rec_status="${aFileRec.status}">`)
            .append($('<td attr_name="id">').text(aFileRec.id))
            .append($('<td attr_name="fileName">').text(aFileRec.fileName))
            .append($('<td attr_name="uploadedAt">').text(formatUA(aFileRec.uploadedAt)))
            .append($('<td attr_name="fileType">').text(formatFT(aFileRec.fileType)))
            .append($('<td attr_name="status">').text(formatStatus(aFileRec.status)))
            .append($('<td attr_name="preview">').append($('<button>').text("Open new Tab")))
            .append($('<td attr_name="deleteCB">').append($("<input>").attr("type", "checkbox")));
        tbody.append(trEle);

        // --- set btn status
        if (aFileRec.status != Status.Completed){
            const previewBtn = $(`tr[rec_id="${aFileRec.id}"] td[attr_name="preview"] button`);
            previewBtn.prop('disabled', true);
        }

        if (aFileRec.status == Status.Uploading || aFileRec.status == Status.Parsing){
            const delCB = $(`tr[rec_id="${aFileRec.id}"] td[attr_name="deleteCB"] input`);
            delCB.prop('disabled', true);
        }
        
    }
}

$(document).ready(function () {
    console.log("--- Run document.ready");

    importData(renderData);
});
