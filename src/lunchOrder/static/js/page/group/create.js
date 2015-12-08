(function($) {
	var btnSubmit, form, btnGoBack, btnCheck, pnlCheck, checking;
	
	$(function(){
		btnSubmit = $('#btnSubmit');
		btnGoBack = $('#btnGoBack');
		btnCheck = $('#btnCheck');
		pnlCheck = $('#pnlCheck');
		checking = $('#checking');
		form = $('#form');
		btnSubmit.click(function(){
			btnSubmit.prop('disabled', true);
			var data = {name: form.find('.name').val(), address:form.find('.address').val(),
				brief:form.find('.brief').val(), 'payment':{'clear':0, 'byTurns': $('#byTurns1').prop('checked')?1:0},
				noAudit:form.find('.noAudit').prop('checked')?1:0
			}
			if(!data.name){
				alert('群名称必填');
				btnSubmit.prop('disabled', false);
				return;
			}
			if(!data.address){
				alert('地址必填');
				btnSubmit.prop('disabled', false);
				return;
			}
			
			$.postJSON('/group/create', data, function(){
				$.messagelabel.show('创建成功！页面将要跳转...');
				setTimeout(function(){
					location.replace('/group/admin');
				}, 2000);
			});
			
		});
		
		btnGoBack.click(function(){
			$.returnBack();
		});
		
		btnCheck.click(function(){
			var name = form.find('.name').val();
			if(!name){
				alert('名称不能为空');
				return;
			}
			var divRes = pnlCheck.find('.checkResult');
			pnlCheck.hide();
			checking.show();
			$.postJSON('/group/checkname', {name:name}, function(data){
				pnlCheck.show();
				checking.hide();
				divRes.show();
				btnCheck.text('重新检测')
				if(data.success){
					divRes.text('名称合法有效。');
					divRes.css('color', '#669900');
				}else{
					divRes.text('该群名称已被注册，请另起。');
					divRes.css('color', '#ff9900');
				}
			});			
			
		});
	});
})(jQuery);



















