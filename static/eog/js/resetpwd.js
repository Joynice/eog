
$(function () {
    $("#submit1").click(function (event) {
        // 为了阻止按钮默认提交表单事件
        event.preventDefault();
        var oldpwdE = $("input[name=oldpwd]");
        var newpwdE = $("input[name=newpwd]");
        var newpwd2E = $("input[name=newpwd2]");

        var oldpwd = oldpwdE.val();
        var newpwd = newpwdE.val();
        var newpwd2 = newpwd2E.val();
        // console.log(oldpwd,newpwd,newpwd2)
        zlajax.post({
           'url': '/eog/resetpwd/',
           'data':{
               'oldpwd': oldpwd,
               'newpwd': newpwd,
               'newpwd2': newpwd2
           } ,
            'success':function (data) {
                if (data['code'] == 200){
                    zlalert.alertSuccessToast("密码修改成功！");
                    oldpwdE.val("");
                    newpwdE.val("");
                    newpwd2E.val("");

                }else {
                    var message = data['message'];
                    zlalert.alertInfo(message);
                    oldpwdE.val("");
                    newpwdE.val("");
                    newpwd2E.val("");
                }
            },
            'fail':function (error) {
                zlalert.alertNetworkError()
            }
        });
    });
});