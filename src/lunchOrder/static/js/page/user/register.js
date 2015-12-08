(function($) {
	var form, btnSubmit, btnReturn, pnlFail, securityCode;
	
	$(function(){
		form = $('#form');
//		securityCode = $('#securityCode');
//	    securityCode.click(function(){
//	        refreshSecurityCode();
//	    });		
		pnlFail = $('#pnlFail');
		btnSubmit = $('#btnSubmit');
		btnReturn = $('#btnReturn');
		btnSubmit.click(submit);
		btnReturn.click(function(){
			$.returnBack('/');
		});
		//
		form.find('.userName').inputHint({
			name : 'userName',
			validTypes: ['username', 'noDuplicated'],
			info : '6-16个字符的字母、数字或下划线，以字母开头',
			isRequired : true,
			rules:{noDuplicated:{
				validator : function(value) {
					var pass = false;
					$.postJSON('/user/CheckUnique', {userName:value}, function(data){
						pass = true;
					}, function(data){
						pass = false;
					},{async:false});
					return pass;
				},
				message : '该用户名已被申请，请另选其他用户名'
			
			}}
		});
		form.find('.passwords').inputHint({
			name : 'passwords',
			validTypes: ['minLength[6]'],
			isRequired : true
		});
		form.find('.passwords1').inputHint({
			name : 'passwords1',
			validTypes: ['same[".passwords"]'],
			isRequired : true
		});
		form.find('.realName').inputHint({
			name : 'realName',
			validTypes: ['name'],
			isRequired : true
		});
		form.find('.email').inputHint({
			name : 'email',
			info : '用于找回密码，务必认真填写',
			validTypes: ['email'],
			isRequired : true
		});
//		form.find('.securityCode').inputHint({
//			name : 'securityCode',
//			isRequired : true
//		});
		form.find('.mobile').inputHint({
			name : 'mobile',
			validTypes: ['mobile']
		});
		form.find('.address').inputHint({
			name : 'address'
		});
		
	})
	
	
	
	function submit(){
		if($.InputHint.validate()){
			pnlFail.css('visibility', 'hidden');
			var data = $.InputHint.val();
			data['passwords'] = $.md5(data['passwords']);
			delete(data['passwords1']);
			$.postJSON('/user/register', data, function(){
				$.messager.alert('','注册成功。', null, function(){
					$.returnBack('/');
				});
			}, function(data){
				pnlFail.css('visibility', 'visible');
				pnlFail.find('.text').text(data.message);
				refreshSecurityCode()
			});
		}
	}
    function refreshSecurityCode(){
        securityCode.prop('src', '/file/securityCode?rg=1&'+new Date().getTime());
    }	

})(jQuery);



















