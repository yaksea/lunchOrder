(function($) {
	var form, btnSubmit, btnReturn, pnlSent, pnlFail;
	
	$(function(){
		form = $('#form');
		btnSubmit = $('#btnSubmit');
		btnReturn = $('#btnReturn');
		pnlSent = $('#pnlSent');
		pnlFail = $('#pnlFail');
		btnSubmit.click(submit);
		btnReturn.click(function(){
			$.returnBack('/');
		});
		//
		form.find('.userName').inputHint({
			name : 'userName',
			validTypes: ['username'],
			info : '6-16个字符的字母、数字或下划线，以字母开头',
			isRequired : true
		});
		form.find('.email').inputHint({
			name : 'email',
			validTypes: ['email'],
			isRequired : true
		});
		
	})
	
	
	
	function submit(){
		if($.InputHint.validate()){
			btnSubmit.prop('disabled', true);
			var data = $.InputHint.val();
			$.postJSON('/user/forget', data, function(){
				$.messagelabel.show('邮件已发送');
				btnSubmit.hide();
				pnlFail.hide();
				pnlSent.show();
				pnlSent.find('.email').text(data.email);
				pnlSent.find('.btnRecieve').prop('href', "http://"+data.email.split('@')[1]);
				pnlSent.find('.btnResend').unbind('click').click(submit);
			}, function(data){
				btnSubmit.show();
				btnSubmit.prop('disabled', false);
				pnlFail.show();
				pnlSent.hide();
				pnlFail.find('.text').text(data.message);
			});
		}
	}
	

})(jQuery);



















