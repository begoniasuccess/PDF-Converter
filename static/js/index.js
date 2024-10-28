let dataCenter = [];

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

function formatFT(fileType) {
    switch (fileType) {
        case FileType.PDF:
        default:
            return "PDF";
    }
}

function formatStatus(status) {
    switch (status) {
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
function importData(callbackFun) {
    $.ajax({
        url: 'api/files', // 請求的 URL
        method: 'GET', // 或 'POST'，視需求而定
        // data: {
        //     key1: 'value1',
        //     key2: 'value2'
        // },
        dataType: 'json', // 返回的資料格式，常用 json
        success: function (response) {
            dataCenter = response;
            console.log(dataCenter);
            callbackFun(dataCenter);
        },
        error: function (xhr, status, error) {
            console.error('發生錯誤:', error); // 處理錯誤
        }
    });
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
        if (aFileRec.status != Status.Completed) {
            const previewBtn = $(`tr[rec_id="${aFileRec.id}"] td[attr_name="preview"] button`);
            previewBtn.prop('disabled', true);
        }

        if (aFileRec.status == Status.Uploading || aFileRec.status == Status.Parsing) {
            const delCB = $(`tr[rec_id="${aFileRec.id}"] td[attr_name="deleteCB"] input`);
            delCB.prop('disabled', true);
        }

    }
}

function loadFilesData() {
    importData(renderData);
}

$(document).ready(function () {
    console.log("--- Run document.ready");

    loadFilesData();
});

// --- Button click event
function checkedAll(srcCheckbox){
    $('input[type="checkbox"]:not(:disabled)').prop('checked', $(srcCheckbox).prop('checked'));
}
