(function($) {
	var pnlForm, btnLogin, pnlError;
	
	$(function(){
        pnlForm = $('#pnlForm');
        pnlError = $('#pnlError');
        btnLogin = $('#btnLogin');
        txtUserName = $('#txtUserName').focus();;
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
        	
        	$.postJSON('/user/loginND', data, function(data){
        		btnLogin.prop('disabled', false);
        		pnlError.css('visibility', 'hidden');
        		$('#pnlMain').text('登录成功，页面正在跳转...');
        		window.close();
        		window.opener.refreshIn();
        		
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
	        securityCode.prop('src', '/file/securityCode?nd=1&'+new Date().getTime());
	    }
		
	});

})(jQuery);



















