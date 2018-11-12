$(function () {
    $("#query").click(function (event) {
        event.preventDefault();
        var date1 = $("#date1").val();
        var date2 = $("#date2").val();
        if (date1 == '' && date2 == '') {
            zlalert.alertInfo('请选择查询日期！');
            return;
        }
        zlajax.post({
            'url': '/eog/account/',
            'data': {
                'date1': date1,
                'date2': date2,
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    zlalert.alertSuccessToast('查询成功');
                    var accountList = data['data'];
                    $('tr#account').hide();
                    var html = "";
                        for (var i = 0; i < accountList.length; i++) {
                            html += "<tr>";
                            html += "<td>" + timeStamp2String(accountList[i]['operate_time']['$date']) + "</td>";
                            html += "<td>" + accountList[i]['ip'] + "</td>";
                            html += "<td>" + accountList[i]['operate_detail'];
                            html += "</tr>";
                        }
                        $(".center1").html(html);
                } else {
                    zlalert.alertInfo(data['message']);
                }
            },
            'fail': function (error) {
                zlalert.alertNetworkError();
            }
        })
    })
});