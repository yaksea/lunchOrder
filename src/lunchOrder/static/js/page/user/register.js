(function($) {
	var form, btnSubmit;
	
	$(function(){
		form = $('#form');
		btnSubmit = $('#btnSubmit');
		btnSubmit.click(submit);
	})
	
	
	
	function submit(){
		var data = {loginName: form.find('.loginName').val(),
				passwords: form.find('.passwords').val(),
				passwords1: form.find('.passwords1').val(),
				realName: form.find('.realName').val(),
				email: form.find('.email').val(),
				mobile: form.find('.mobile').val(),
		}
		if(!data.loginName||!data.passwords||!data.passwords1||!data.realName||!data.email||!data.mobile){			
			$.messager.alert('','请正确填写表单。');	
			return;
		}else if(data.passwords!=data.passwords1){
			$.messager.alert('','密码不同。');	
			return;
		}
		
		$.postJSON('/user/register', data, function(){
			$.messager.alert('','注册成功。');	
			
		})
	}
	

})(jQuery);



















