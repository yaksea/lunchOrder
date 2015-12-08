(function($) {
	var tbList, txtUserName, txtBalance;
	var logType = {'1':'充值', '-2':'消费' , '2':'结单',  '-1':'为他人充值', '0':'开设账户'};
	
	$(function(){
		tbList = $('#tbList');
		txtUserName = $('#txtUserName');
		txtBalance = $('#txtBalance');
		bindList();
	})
	
	function bindList(){
		var forGroup = $.getUrlParam('group');
		$.getJSON('/account/detailList',{id:$.getUrlParam('id'),group:forGroup}, function(data){
			
			txtUserName.text(data.remarkName);
			if(forGroup){
				txtBalance.text(-Math.toMoney(data.balance));
			}else{
				txtBalance.text(Math.toMoney(data.balance));
			}
			
			$(data.rows).each(function(i, log){
				var tr = $('<tr />').appendTo(tbList);
				var td1 = $('<td />').appendTo(tr);
				td1.text(log.dateTime);
				var td2 = $('<td />').appendTo(tr);
				td2.text(logType[log.type]);
				var td3 = $('<td />').appendTo(tr);
				var td4 = $('<td/>').appendTo(tr);
				if(forGroup){
					td3.text(-log.amount.toFixed(2));
					td4.text( Math.toMoney(-log.balance - log.amount));
				}
				else{
					td3.text(log.amount);
					td4.text( Math.toMoney(log.balance + log.amount));
				}
				var td5 = $('<td/>').appendTo(tr);
				td5.text(log.description);
			})
		})
	}
	
	

})(jQuery);



















