$(document).ready(function () {
    if (msg['alert'] != "") {
        alert(msg['alert']);
        if (msg['type'] == '0') {
            window.location.href = '../index';
        }
    }
});