$(function () {
    $("button[title='Upload selected files']").click(function (event) {
        event.preventDefault();
        var formData = new FormData($('#uploadForm')[0]);
        console.log(formData);
        $.ajax({
            url: "/eog/profile/",
            type: "POST",
            data: formData,
            async: true,
            cashe: false,
            contentType: false,
            processData: false,
            success: function (data) {
                if(data['code']==200){
                    zlalert.alertSuccessToast('头像修改成功！');
                    setTimeout(function () {
                        window.location.reload();
                    }, 500)
                }
                else {
                    zlalert.alertInfo(data['message']);
                }
            },
            error: function () {
                zlalert.alertInfo('上传文件太大！')
            }
        });
    });
});