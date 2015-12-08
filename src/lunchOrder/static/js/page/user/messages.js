(function($) {
	var tbMessages;
	
	$(function(){
		tbMessages = $('#tbMessages');
		bindMessages();
	})
	
	
	
	function bindMessages(){
		$.getJSON('/group/myapply', function(data){
			$.each(data.rows, function(i, message){
				var tr = $('<tr />').appendTo(tbMessages);
				var td1 = $('<td />').appendTo(tr);
				td1.text(message.group.name);
				var td2 = $('<td />').appendTo(tr);
				td2.text(message.createTime);
				var td3 = $('<td />').appendTo(tr);
				td3.text(message.reply);
				var td4 = $('<td />').appendTo(tr);
				td4.text(message.updateTime);
			})
		})
	}
	

})(jQuery);



















