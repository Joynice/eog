/**
 * Created by Administrator on 2016/12/17.
 */

// $(function () {
//     $('.nav-sidebar>li>a').click(function (event) {
//         var that = $(this);
//         if(that.children('a').attr('href') == '#'){
//             event.preventDefault();
//         }
//         if(that.parent().hasClass('active')){
//             that.parent().removeClass('active');
//         }else{
//             that.parent().addClass('active').siblings().removeClass('active');
//         }
//         console.log('coming....');
//     });
//
//     $('.nav-sidebar a').mouseleave(function () {
//         $(this).css('text-decoration','none');
//     });
// });


$(function () {
    var url = window.location.href;
    if(url.indexOf('today_event') >= 0){
        var today_eventLi = $('.today_event');
        today_eventLi.addClass('active').siblings().removeClass('active');
    } else if(url.indexOf('events') >= 0){
        var eventsManageLi = $('.events');
        eventsManageLi.addClass('active').siblings().removeClass('active');
    }else if(url.indexOf('review_event') >= 0){
        var review_eventManageLi = $('.review_event');
        review_eventManageLi.addClass('active').siblings().removeClass('active');
    }else if(url.indexOf('danger_event') >= 0){
        var danger_eventManageLi = $('.danger_event');
        danger_eventManageLi.addClass('active').siblings().removeClass('active');
    }else if(url.indexOf('source') >= 0){
        var sourceManageLi = $('.source');
        sourceManageLi.addClass('active').siblings().removeClass('active');
    }else if(url.indexOf('rules') >= 0){
        var rulesManageLi = $('.rules');
        rulesManageLi.addClass('active').siblings().removeClass('active');
    }else if(url.indexOf('index1') >= 0){
        var index1ManageLi = $('.index1');
        index1ManageLi.addClass('active').siblings().removeClass('active');
    }else if(url.indexOf('index2') >= 0) {
        var index2ManageLi = $('.index2');
        index2ManageLi.addClass('active').siblings().removeClass('active');
    }else if(url.indexOf("log") >= 0){
        var mylogeManageLi = $(".operate_log");
        mylogeManageLi.addClass('active').siblings().removeClass('active');
    }else if(url.indexOf("my_review") >= 0){
        var my_reviewManageLi = $(".my_review");
        my_reviewManageLi.addClass('active').siblings().removeClass('active');
    }else if(url.indexOf("operate_log") >= 0){
        var my_scoreManageLi = $(".my_score");
        my_scoreManageLi.addClass('active').siblings().removeClass('active');
    }else if(url.indexOf("user") >= 0){
        var userManageLi = $(".user");
        userManageLi.addClass('active').siblings().removeClass('active');
    }
});