$(function () {
   $("#submit2").click(function (event) {
       event.preventDefault();
       var username_input = $("input[name='username']");

       var username = username_input.val();
       zlajax.post({
           'url': '/eog/resetusername/',
           'data':{
               'username': username,
           },
           'success': function (data) {
               if(data['code']==200){
                   zlalert.alertSuccessToast();
                   setTimeout(function () {
                       window.location.reload();
                   },1000)
               }else {
                   zlalert.alertInfo(data['message']);
               }
           },
           'fail': function (error) {
               zlalert.alertNetworkError();
           }
       });
   });
});