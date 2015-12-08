(function($) {
	
	$(function(){
		form = $('#form');
		btnSubmit = $('#btnSubmit');
		btnReturn = $('#btnReturn');
		btnSubmit.click(submit);
		btnReturn.click(function(){
			location.replace('/');
		});		
		//
		form.find('.old').inputHint({
			name : 'old',
			validTypes: ['minLength[6]'],
			isRequired : true
		});
		form.find('.new').inputHint({
			name : 'new',
			validTypes: ['minLength[6]'],
			isRequired : true
		});
		form.find('.passwords1').inputHint({
			name : 'passwords1',
			validTypes: ['same[".new"]'],
			isRequired : true
		});
		//		
		$('.topMenu').children().eq(2).addClass('active');
	})
	
	function submit(){
		if($.InputHint.validate()){
			var data = $.InputHint.val();
			data['old'] = $.md5(data['old']);
			data['new'] = $.md5(data['new']);
			delete(data['passwords1']);
			$.postJSON('/user/changepasswords', data, function(){
				$.messagelabel.show('修改密码成功。');
			}, function(){
				form.find('.old').val();
				$.messagelabel.show('修改密码失败，请检查原密码是否正确。');
			});
		}
	}
})(jQuery);



















