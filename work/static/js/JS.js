/**
 * Created by WZL on 2016/11/10.
 */
$(function() {
    //点击登录按钮 弹出层并初始化弹出层位置
    $("#btnlogin").click(function() {
        $("#corBackground").animate({ opacity:"show"},"slow");
        $("#corInsertHref").animate({ opacity:"show"},"slow");
        autoSize($("#corInsertHref"));
    });

    //点击注册按钮 弹出层并初始化弹出层位置
    $("#btnlogon").click(function() {
        $("#corBackground2").animate({ opacity:"show"},"slow");
        $("#corInsertHref2").animate({ opacity:"show"},"slow");
        autoSize($("#corInsertHref2"));
    });

    $("#btnlogon2").click(function() {

        $("#corBackground").animate(function(){
            $("#corBackground").stop(false,true).animate();
        });
        document.getElementById("corBackground").style.display="none";
        //停止动画
        $("#corInsertHref").animate(function(){
            $("#corInsertHref").stop(false,true).animate();
        });
        document.getElementById("corInsertHref").style.display="none";

        document.getElementById("exampleInputEmail1").value="";
        document.getElementById("exampleInputPassword1").value="";
        $("#corBackground2").animate({ opacity:"show"},"slow");
        $("#corInsertHref2").animate({ opacity:"show"},"slow");
        autoSize($("#corInsertHref2"));
    });
    //登陆窗口大小缩放事件
    $(window).resize(function() {
        autoSize($("#corInsertHref"));
    });
    //注册窗口大小缩放事件
    $(window).resize(function() {
        autoSize($("#corInsertHref2"));
    });
    //窗口大小缩放时调整弹出层的位置
    var autoSize=function(corObj) {
        var wWidth = $(window).width(), wHeight = $(window).height();
        var ihWidth = corObj.outerWidth(true), ihHeight = corObj.outerHeight(true);

        corObj.css({ "top": ((wHeight - ihHeight) / 2) + "px", "left": ((wWidth - ihWidth) / 2) + "px" });
    };
    //关闭登陆窗口
    $("#cBtn").click(function() {
        //停止动画
        $("#corBackground").animate(function(){
            $("#corBackground").stop(false,true).animate();
        });
        document.getElementById("corBackground").style.display="none";
        //停止动画
        $("#corInsertHref").animate(function(){
            $("#corInsertHref").stop(false,true).animate();
        });
        document.getElementById("corInsertHref").style.display="none";

        document.getElementById("exampleInputEmail1").value="";
        document.getElementById("exampleInputPassword1").value="";
    });
    //关闭注册窗口
    $("#cBtn2").click(function() {
        //停止动画
        $("#corBackground2").animate(function(){
            $("#corBackground2").stop(false,true).animate();
        });
        document.getElementById("corBackground2").style.display="none";
        //停止动画
        $("#corInsertHref").animate(function(){
            $("#corInsertHref2").stop(false,true).animate();
        });
        document.getElementById("corInsertHref2").style.display="none";
        document.getElementById("exampleInputEmail2").value="";
        document.getElementById("exampleInputPassword2").value="";
        document.getElementById("exampleInputPassword3").value="";
        document.getElementById("checkName").innerHTML="";
        document.getElementById("checkPwd").innerHTML="";
        document.getElementById("checkOk").innerHTML="";
        document.getElementById("ruo").style.backgroundColor = "#CCC";
        document.getElementById("zhong").style.backgroundColor = "#CCC";
        document.getElementById("qiang").style.backgroundColor = "#CCC";
    });
});

//刚加载页面的时候焦点移到用户名文本框内
function myFocus() {
    document.getElementById("exampleInputEmail2").focus();
}
//设置cookie
function setCookie(str, strValue) {
    var exp = new Date();
    exp.setTime(exp.getTime() + 1 * 24 * 60 * 60 * 1000);
    document.cookie = str + "=" + strValue + ";expires=" + exp.toGMTString();
    location.href = "Login.html"; //接收页面
}
//验证用户名和密码
function validateRegister() {
    var exampleInputEmail2 = document.getElementById("exampleInputEmail2").value;
    var password = document.getElementById("exampleInputPassword2").value;
    var pwdOk = document.getElementById("pwdOk").value;
    if (blurName(exampleInputEmail2) && blurPwd(password) && blurPwdOk(pwdOk)) {
        setCookie("exampleInputEmail2", exampleInputEmail2);
        setCookie("password", password);
    }
}
//验证密码强度
function pwdValidate() {
    var password = document.getElementById("exampleInputPassword2").value;
    if (password.length > 0 && password.length <= 4) {
        return -1;
    }
    else if (password.length > 4 && password.length <= 8) {
        return 0;
    }
    else if (password.length > 8 && password.length <= 12) {
        return 1;
    }
}
//用户名框
function blurName(name) {
    if (name == null || name == "") {
        checkName.innerHTML = "用户名不能为空";
    }
    else {
        checkName.innerHTML = "用户名可用";
        return true;
    }
}
//密码框
function blurPwd(password) {
    if (password == null || password == "") {
        checkPwd.innerHTML = "密码不能为空";
    }
    else if (password.match(/[^A-Za-z0-9]/ig)) {
        checkPwd.innerHTML = "密码必须为数字和字母";
    }
    else {
        if (pwdValidate() == -1) {
            ruo.style.backgroundColor = "orangered";
            zhong.style.backgroundColor = "#CCC";
            qiang.style.backgroundColor = "#CCC";
        }
        else if (pwdValidate() == 0) {
            ruo.style.backgroundColor = "#CCC";
            zhong.style.backgroundColor = "yellow";
            qiang.style.backgroundColor = "#CCC";
        }
        else if (pwdValidate() == 1) {
            ruo.style.backgroundColor = "#CCC";
            zhong.style.backgroundColor = "#CCC";
            qiang.style.backgroundColor = "greenyellow";
        }
        checkPwd.innerHTML = "密码可用";
        return true;
    }
}
//确认密码框
function blurPwdOk(pwdOk) {
    var password = document.getElementById("exampleInputPassword2").value;
    if (pwdOk == null || pwdOk == "") {
        checkOk.innerHTML = "确认密码输入不能为空";
    }
    else if (password != pwdOk) {
        checkOk.innerHTML = "两次输入的密码不一致";
    }
    else {
        checkOk.innerHTML = "输入正确";
        return false;
    }
}
