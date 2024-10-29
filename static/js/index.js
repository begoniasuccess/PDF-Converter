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
function getFiles(fileId, success) {
    let url = "api/files";
    if (fileId) url += "/" + fileId;
    $.ajax({
        url,
        method: "GET",
        dataType: "json",
        success,
        error: function (xhr, status, error) {
            console.error("發生錯誤:", error);
        },
    });
}

function addFile(data, success) {
    let url = "api/files";
    $.ajax({
        url,
        method: "POST",
        data,
        dataType: "json",
        success,
        error: function (xhr, status, error) {
            console.error("發生錯誤:", error);
        },
    });
}

function delFile(fileId, success) {
    let url = "api/files/" + fileId;
    $.ajax({
        url,
        method: "DELETE",
        dataType: "json",
        success,
        error: function (xhr, status, error) {
            console.error("發生錯誤:", error);
        },
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
        const trEle = $(`<tr file_id="${aFileRec.id}" file_status="${aFileRec.status}">`)
            .append($('<td attr_name="id">').text(aFileRec.id))
            .append($('<td attr_name="fileName">').text(aFileRec.fileName))
            .append($('<td attr_name="uploadedAt">').text(formatUA(aFileRec.uploadedAt)))
            .append($('<td attr_name="fileType">').text(formatFT(aFileRec.fileType)))
            .append($('<td attr_name="status">').html(formatStatus(aFileRec.status)))
            .append($('<td attr_name="preview">').append($("<button>").text("Open new Tab")))
            .append($('<td attr_name="deleteCB">').append($("<input>").attr("type", "checkbox")));
        tbody.append(trEle);

        // --- set btn status
        if (aFileRec.status != Status.Completed) {
            const previewBtn = $(`tr[file_id="${aFileRec.id}"] td[attr_name="preview"] button`);
            previewBtn.prop("disabled", true);
        }

        if (aFileRec.status == Status.Uploading || aFileRec.status == Status.Parsing) {
            const delCB = $(`tr[file_id="${aFileRec.id}"] td[attr_name="deleteCB"] input`);
            delCB.prop("disabled", true);
        }
    }
}

function loadFilesData() {
    getFiles(null, renderData);
}

$(document).ready(function () {
    loadFilesData();
});

// --- Elements events
function showPopup(msg) {
    $("#popup_msg").html(msg);
    document.getElementById("popupOverlay").style.display = "flex";
}

function closePopup() {
    document.getElementById("popupOverlay").style.display = "none";
}

function checkedAll(srcCheckbox) {
    $('input[type="checkbox"]:not(:disabled)').prop("checked", $(srcCheckbox).prop("checked"));
}

function delFiles() {
    const checkedBoxes = $('tbody input[type="checkbox"]:checked:not(:disabled)');
    if (checkedBoxes.length < 1) {
        showPopup("No file selected！");
        return;
    }
    // console.log({checkedBoxs});
    checkedBoxes.each(function () {
        const fileId = $(this).closest("tr").attr("file_id");
        delFile(fileId, loadFilesData);
    });
}

// function delBtnStatus(){
//     // --- 計算已勾選的項目

// }
