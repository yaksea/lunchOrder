(function($) {
	var txtContent,btnPost,pnlList,ulList;
	
	$(function(){
		txtContent = $('#txtContent');
		btnPost = $('#btnPost');
		pnlList = $('#pnlList');
		ulList = $('#ulList');
		
		txtContent.placeholder();
		btnPost.click(function(){
			var message = txtContent.val();
			if(message.length===0){
				alert('请填写建议哈~');
				return;
			}
			if(message.length>1000){
				alert('您的建议真的有点长哦，能否精简一点哈~');
				return;
			}
			$.postJSON('/feedback', {message:message}, function(data){
				$.messagelabel.show('已收到您的建议，我们将在第一时间处理并回复，再次感谢您的宝贵意见。');
				bindList()
			});
		
		});
		bindList();
	});
	
	function bindList(){
		$.getJSON('/feedback/myList', {}, function(data){
			var count = data.rows.length;
			var replied = 0;
			if(count){
				pnlList.find('.count').text(count);
				pnlList.show();
				ulList.empty();
				$.each(data.rows, function(i, fb){
					var li = $('<li class="fb"/>').appendTo(ulList);
					var txtMessage = $('<div />').appendTo(li);
					txtMessage.text(fb.message);
					var txtCreateTime = $('<div class="createTime" />').appendTo(li);
					txtCreateTime.text(fb.createTime);
					if(fb.status){
						replied ++;
						var ul = $('<ul/>').appendTo(li);
						$.each(fb.reply, function(i, rep){
							var li = $('<li class="reply"/>').appendTo(ul);
							var txtMessage = $('<div />').appendTo(li);
							txtMessage.text("回复："+rep.message);
							var txtCreateTime = $('<div class="createTime" />').appendTo(li);
							txtCreateTime.text(rep.createTime);
						});
					}
				});
				if(replied){
					pnlList.find('.replied').text('，其中'+replied+'条已回复');
				}
			}
		})
	}
})(jQuery);



















