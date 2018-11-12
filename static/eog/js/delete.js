$(function () {
    $("#delete").click(function (event) {
        zlalert.alertConfirm({
            'msg':'确认要删除此账号？',
            'confirmCallback' :function () {
                zlajax.get(
                    {
                        'url': '/eog/remove/',
                        'data':{
                            'tag': 1,
                        },
                        'success': function (data) {
                            if(data['code']==200){
                                console.log(data);
                                setTimeout(function () {
                                    window.location = '/front/signup/';
                                    zlalert.alertSuccessToast('改账号已经被删除，如有需要请重新注册！');
                                },2000)
                            }

                        },
                        'fail': function () {
                            zlalert.alertNetworkError()
                        }
                    }
                )
            }
        });
    });
});