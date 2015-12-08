(function($) {
	var form, btnSubmit, btnReturn;
	
	$(function(){
		form = $('#form');
		btnSubmit = $('#btnSubmit');
		btnReturn = $('#btnReturn');
		btnSubmit.click(submit);
		btnReturn.click(function(){
			location.replace('/');
		});
		
		$.getJSON('/user/getinfo', function(data){
			form.find('.realName').val(data.realName);
			form.find('.email').val(data.email);
			form.find('.mobile').val(data.mobile||'');
			form.find('.address').val(data.address||'');
		});
		
		//
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
		form.find('.mobile').inputHint({
			name : 'mobile',
			validTypes: ['mobile']
		});
		//
		$('.topMenu').children().eq(0).addClass('active');
	})
	
	
	function submit(){
		if($.InputHint.validate()){
			var data = $.InputHint.val();
			$.postJSON('/user/changeinfo', data, function(){
				$.messagelabel.show('保存成功。');
			});
		}
	}
	
})(jQuery);



















