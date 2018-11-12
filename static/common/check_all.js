    //查找thead下第一个th下的input
    var chbAll=document.querySelector(
        "thead th:first-child>input"
    );
    //查找tbody中所有第一个td下的input
    var chbs=document.querySelectorAll(
        "tbody td:first-child>input"
    );
    //为chbAll绑定单击事件
    chbAll.onclick=function(){
        //遍历chbs中每个chb
        for(var i=0;i<chbs.length;i++){
            //设置当前chb的checked等于this的checked
            chbs[i].checked=this.checked;
        }
    };
    //为chbs中每chb都绑定单击事件
    for(var i=0;i<chbs.length;i++){
        chbs[i].onclick=function(){
            if(!this.checked)
                chbAll.checked=false;
            else{
                //选择tbody下第一个td中的未选中的input
                var unchecked=
                    document.querySelector(
                        "tbody td:first-child>input:not(:checked)"
                    );
                if(unchecked===null)
                    chbAll.checked=true;
            }
        }
    }