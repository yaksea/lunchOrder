(function($) {
	var txtContent,btnPost, btnReturn;
	
	$(function(){
		txtContent = $('#txtContent');
		btnPost = $('#btnPost');
		btnReturn = $('#btnReturn');
		btnReturn.click(function(){
			$.returnBack('/');
		});
		txtContent.placeholder();
		btnPost.click(function(){
			btnPost.prop('disabled', true);
			var message = txtContent.val();
			if(message.length===0){
				alert('请填写建议哈~');
				btnPost.prop('disabled', false);
				return;
			}
			if(message.length>1000){
				alert('您的建议真的有点长哦，能否精简一点哈~');
				btnPost.prop('disabled', false);
				return;
			}
			$.postJSON('/feedback', {message:message}, function(data){
				$.messagelabel.show('已收到您的建议，我们将在第一时间处理并回复，再次感谢您的宝贵意见。');
				btnPost.hide();
			});
		
		});
	});
	
})(jQuery);



















