(function($) {
	var ddlType,tbUnReply,tbReplied,pnlList,dlgReply;
	var type=0, curFb, curTr;
	
	$(function(){
		ddlType = $('#ddlType');
		tbUnReply = $('#tbUnReply');
		tbReplied = $('#tbReplied');
		pnlList = $('#pnlList');
		dlgReply = $('#dlgReply');
		
		ddlType.change(function(){
			type = parseInt(ddlType.val());
			bindList();
		});
		
		dlgReply.find('.save').click(function(){
			$.postJSON('/feedback/reply',{id:curFb._id, 'message':dlgReply.find('.message2').val()}, function(){
				$.messagelabel.show('回复成功！');
				bindList();
			});
			dlgReply.dialog('close');
		});
		dlgReply.find('.cancel').click(function(){
			dlgReply.dialog('close');
		});
		bindList();
	})
	
	function bindList(){
		pnlList.children().hide();
		pnlList.children().eq(type).show();
		var tbList = type==0?tbUnReply:tbReplied;
		tbList.empty();
		$.getJSON('/feedback/AllList', {status:type}, function(data){
			$.each(data.rows, function(i, fb){
				var tr = $('<tr />').appendTo(tbList);
				var td1 = $('<td />').appendTo(tr);
				td1.text(fb.createTime);
				var td2 = $('<td />').appendTo(tr);
				if(fb.user){
					td2.text(fb.user.realName);
				}
				var td3 = $('<td />').appendTo(tr);
				td3.text(fb.message);
				if(type==0){
					var td4 = $('<td />').appendTo(tr);
					var btnReply = $('<a href="javascript:void(0)" class="linkBtn1">回复</a>').appendTo(td4);
					btnReply.click(function(){
						curFb = fb;
						curTr = tr;
						dlgReply.show();
						dlgReply.dialog({
							modal : true,
							title : "回复"
						});	
						dlgReply.find('.message1').text(fb.message);
					})
				}else{
					var td4 = $('<td />').appendTo(tr);
					td4.text(fb.reply.message);
					var td5 = $('<td />').appendTo(tr);
					td5.text(fb.reply.createTime);
					
				}
			});
		})
	}
})(jQuery);



















