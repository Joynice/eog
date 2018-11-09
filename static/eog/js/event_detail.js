$(function () {
    $('#dowebok').viewer({   // 调用jquery的放大图像
        url: 'data-original',
    });
});
//  jQuery时间插件
function timeStamp2String(time) {
    var datetime = new Date();
    datetime.setTime(time);
    var year = datetime.getFullYear();
    var month = datetime.getMonth() + 1 < 10 ? "0" + (datetime.getMonth() + 1) : datetime.getMonth() + 1;
    var date = datetime.getDate() < 10 ? "0" + datetime.getDate() : datetime.getDate();
    var hour = datetime.getHours() < 10 ? "0" + datetime.getHours() : datetime.getHours();
    var minute = datetime.getMinutes() < 10 ? "0" + datetime.getMinutes() : datetime.getMinutes();
    var second = datetime.getSeconds() < 10 ? "0" + datetime.getSeconds() : datetime.getSeconds();
    return year + "-" + month + "-" + date + " " + hour + ":" + minute + ":" + second;
}
// 点击编辑按钮，弹出模态框，将对应的事件ID用Ajax传到后端，返回详情页面
$(function () {
    $('.edit-event-btn').click(function (event) {
        event.preventDefault();
        var self = $(this);
        var event_ID = self.parent().parent().parent().attr('data-_id');

        var body = $('#modal_body');
        var modalLeft = body.find('#modal_left');
        var modalRight = body.find("#modal_right");

        var img = modalLeft.find("img[name='event_img']");// 图片
        var domain = modalRight.find("a[name='a_herf']");// 域名
        var id = modalRight.find("td[id='id']");// id
        var event_id = modalRight.find("td[id='event_id']");// 事件id
        var job_id = modalRight.find("td[id='job_id']");// 任务id
        var first_time = modalRight.find("td[id='first_time']");// 首次发现时间
        var keyword = modalRight.find("td[id='keyword']");// 关键字
        var status = modalRight.find("td[id='status']");// 状态
        var event_url = modalRight.find("a[id='event_url']");// 事件


        zlajax.post({
            'url': '/eog/event_detail/',
            'data': {
                "event_id": event_ID
            },
            'success': function (data) {
                console.log('获得的单个数据', data.data);
                console.log('获得的单个数据domain', data.data.domain);
                console.log('获得的单个数据first_time', data.data.first_time['$date']);
                img.attr('src', 'data:image/jpg;base64,' + data.img);
                img.attr('data-original', 'data:image/jpg;base64,' + data.img);  //快照
                domain.attr('href', data.data.domain);
                domain.text(data.data.domain);    //主站域名
                id.html(data.data.id);
                event_id.html(data.data._id);
                job_id.html(data.data.jobid);
                first_time.html(timeStamp2String(data.data.first_time['$date']));
                keyword.html(data.data.keyword);
                status.html(data.data.status);
                event_url.attr('href',data.data.event);
                event_url.text(data.data.event);

            },
            'faild': function (error) {
                zlalert.alertNetworkError()
            }
        })
    })
});


$(function () {
    $('#save-suggestion-btn').click(function (event) {
        event.preventDefault();
        var modal_right = $('#modal_right');
        var event_id = modal_right.find("td[id=event_id]");
        var dialog = $('#event-dialog');
        var selectInput = dialog.find("select[name='select']");
        var suggestionInput = dialog.find("textarea[name='suggestion']");

        var status = selectInput.val();
        var suggestion = suggestionInput.val();
        var eventID = event_id.text();
        console.log('打印数据',
            status, suggestion, eventID,
        );
        if (status=="确认事件" && !suggestion) {
            zlalert.alertInfoToast('请输入提出完整的审核信息');
            return;
        }
        zlajax.post({
            'url': '/eog/event_suggestion/',
            'data': {
                "status": status,
                "suggestion": suggestion,
                "id": eventID,
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    zlalert.alertSuccessToast(message = '提交成功');
                    setTimeout(function () {
                        window.location.reload();
                    }, 900)
                    // window.location.reload();
                } else {
                    zlalert.alertInfo(data['message'])
                }

            },
            'fail': function (error) {
                zlalert.alertNetworkError();
            }

        })


    })
});
