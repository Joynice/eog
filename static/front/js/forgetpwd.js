$(function () {
    $("#email-captcha-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var email = $("input[name='email']").val();
        if (!email) {
            zlalert.alertInfoToast('请输入邮箱');
            return;
        }
        zlajax.get({
            'url': '/front/email_captcha/',
            'data': {
                'email': email
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    zlalert.alertSuccessToast('邮件已发送，请注意查收！');
                    self.attr("disabled",'disabled');
                    var timeCount = 60;
                    var timer = setTimeout(function () {
                        timeCount--;
                        self.text(timeCount);
                        if(timeCount<=0){
                            self.removeAttr('disabled');
                            clearInterval(timer);
                            self.text('发送验证码');
                        }
                    },1000);
                } else {
                    zlalert.alertInfo(data['message']);
                }
            },
            'fail': function (error) {
                zlalert.alertNetworkError();
            }

        });

    });
});

$(function () {
    $('#submit').click(function (event) {
        event.preventDefault();
        var email_input = $("input[name='email']");
        var newpwdE = $("input[name='newpwd']");
        var newpwd2E = $("input[name='newpwd2']");
        var email_captcha_input = $("input[name='captcha']");

        var email = email_input.val();
        var email_captcha = email_captcha_input.val();
        var password1 = newpwdE.val();
        var password2 = newpwd2E.val();

        zlajax.post({
            'url': '/front/forgetpwd/',
            'data':{
                'email': email,
                'email_captcha': email_captcha,
                'password1': password1,
                'password2': password2
            },
            'success':function (data) {
                if(data['code']==200){
                    zlalert.alertSuccessToast('密码修改成功！');
                    newpwdE.val("");
                    newpwd2E.val("");
                    setTimeout(function () {
                            window.location = '/front/login/';
                        },2000);
                }else{
                    zlalert.alertInfo(data['message'])
                }

            },
            'fail': function (error)
            {
             zlalert.alertNetworkError()
            }
        });
    });
});