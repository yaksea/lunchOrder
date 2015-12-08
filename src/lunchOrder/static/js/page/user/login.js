(function($) {
	var pnlForm, btnLogin, pnlError,btnLoginND, winLoginND;
	var txtUserName, txtPasswords, txtSecurityCode;	
	
	$(function(){
        pnlForm = $('#pnlForm');
        pnlError = $('#pnlError');
        btnLogin = $('#btnLogin');
        txtUserName = $('#txtUserName').focus();
        txtUserName.placeholder();
        txtPasswords = $('#txtPasswords');
        txtPasswords.placeholder();
        txtSecurityCode = $('#txtSecurityCode');
        txtSecurityCode.placeholder();
        
        btnLogin.click(function(){
        	btnLogin.prop('disabled', true);
        	var data = {userName: txtUserName.val(), passwords:txtPasswords.val(), securityCode: txtSecurityCode.val()};
	        var spanContent = pnlError.find('.content');
        	
        	if(!data.userName){
	        	pnlError.css('visibility', 'visible');
        		spanContent.text('请输入用户名。');
        	}else if(!data.passwords){
	        	pnlError.css('visibility', 'visible');
        		spanContent.text('请输入密码。');
        	}
//        	else if(!data.securityCode){
//	        	pnlError.css('visibility', 'visible');
//        		spanContent.text('请输入验证码。');
//        	}
        	
        	$.postJSON('/user/login', data, function(data){
        		btnLogin.prop('disabled', false);
        		pnlError.css('visibility', 'hidden');
        		$.messagelabel.show('登录成功，页面正在跳转...');
        		$.returnBack('/');
        	}, function(data){
        		btnLogin.prop('disabled', false);
	        	pnlError.css('visibility', 'visible');
        		spanContent.text(data.message);
		        refreshSecurityCode();
        		txtSecurityCode.select();
        	});
        });
        
        var securityCode = $('#securityCode');
	    securityCode.click(function(){
	        refreshSecurityCode();
	    });
	    
	    function refreshSecurityCode(){
	        securityCode.prop('src', '/file/securityCode?'+new Date().getTime());
	    }
		
		
	    QC.Login({
	       btnId:"btnQQLogin"    //插入按钮的节点id
	     },function(reqData, opts){//登录成功
		       //根据返回数据，更换按钮显示状态方法
		       var dom = document.getElementById(opts['btnId']),
		       _logoutTemplate=[
		            //头像
		            '<a href="javascript:qqIn()"><span><img src="{figureurl}" class="{size_key}"/></span>',
		            //昵称
		            '<span>{nickname}</span></a> ',
		            ' <span><a href="javascript:QC.Login.signOut();">退出</a></span>' 
		       ].join("");
		       dom && (dom.innerHTML = QC.String.format(_logoutTemplate, {
		           nickname : QC.String.escHTML(reqData.nickname), //做xss过滤
		           figureurl : reqData.figureurl
		       }));
		   });
	     window.refreshIn = function(){
	     	$.messagelabel.show('登录成功，页面正在跳转...');
	    	 $.returnBack('/');
	     }
	     window.qqIn = function(){
	     	var sid = $.getCookie('__qc__k');
	     	sid = sid.substr(6);
	     	$.setCookie('sid', sid);
	     	$.setCookie('site', 'qq');
	     	$.returnBack('/');
	     }
	     btnLoginND = $('#btnLoginND');
	     
	     btnLoginND.click(function(){
	     	if(winLoginND){
	     		winLoginND.close();
	     	}
	     	winLoginND = window.open('/user/loginND','loginND','height=376,width=491,toolbar=no,menubar=no,scrollbars=no,resizable=no,location=no, status=no')
	     });
	});

})(jQuery);



















