function timeStamp2String(time1) {
    var datetime = new Date();
    var time = time1 - 8 * 60 * 60 * 1000;
    datetime.setTime(time);
    var year = datetime.getFullYear();
    var month = datetime.getMonth() + 1 < 10 ? "0" + (datetime.getMonth() + 1) : datetime.getMonth() + 1;
    var date = datetime.getDate() < 10 ? "0" + datetime.getDate() : datetime.getDate();
    var hour = datetime.getHours() < 10 ? "0" + datetime.getHours() : datetime.getHours();
    var minute = datetime.getMinutes() < 10 ? "0" + datetime.getMinutes() : datetime.getMinutes();
    var second = datetime.getSeconds() < 10 ? "0" + datetime.getSeconds() : datetime.getSeconds();
    return year + "-" + month + "-" + date + " " + hour + ":" + minute + ":" + second;
}

$(function () {
    $("#query").click(function (event) {
        event.preventDefault();
        var realname_input = $("#realname");
        var date1_input = $("#date1");
        var date2_input = $("#date2");

        var realname = realname_input.val();
        var date1 = date1_input.val();
        var date2 = date2_input.val();
        // alert(realname,date1,date2);
        if (realname == '' && date1 == '' && date2 == '') {
            zlalert.alertInfoToast('请选择查询信息！');
            return;
        }
        zlajax.post({
            'url': '/eog/log/',
            'data': {
                'realname': realname,
                'date1': date1,
                'date2': date2,
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    zlalert.alertSuccessToast(data['message']);
                    var logs = data['data']['logs'];
                    console.log(logs);
                    var count = data['data']['count'];
                    $("tr#log").remove();
                    var html = "";
                    for (var i = 0; i < logs.length; i++) {
                        html += "<tr>";
                        html += "<td>" + "<input type=\"checkbox\"/>" + "</td>";
                        html += "<td>" + logs[i]['realname'] + "</td>";
                        html += "<td>" + "安全专家" + "</td>";
                        html += "<td>" + timeStamp2String(logs[i]['operate_time']['$date']) + "</td>";
                        html += "<td>" + logs[i]['ip'] + "</td>";
                        html += "<td>" + logs[i]['path'] + "</td>";
                        html += "<td>" + logs[i]['operation'] + "</td>";
                        html += "</tr>";
                    }
                    $("#log1").html(html);
                    $("#log2").remove();

                }
                else {
                    zlalert.alertInfoToast(data['message']);
                }
            },
            'fail': function (error) {
                zlalert.alertNetworkError();
            }
        })

    })
});

