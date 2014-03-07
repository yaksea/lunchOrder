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
		$.getJSON('/account/detailList',{id:$.getUrlParam('id')}, function(data){
			
//			var balance = data.userGroup.balance||0;
			
			txtUserName.text(data.realName);
			txtBalance.text(balance);
			
			$(data.rows).each(function(i, log){
				var tr = $('<tr />').appendTo(tbList);
				var td1 = $('<td />').appendTo(tr);
				td1.text(log.dateTime);
				var td2 = $('<td />').appendTo(tr);
				td2.text(logType[log.type]);
				var td3 = $('<td />').appendTo(tr);
				td3.text(log.amount);
				var td4 = $('<td/>').appendTo(tr);
//				if(balance!=((log.user.balance||0)+log.amount)){
//					tr.css('background', 'red');
//					console.info(balance)
//					console.info((log.user.balance||0)+log.amount)
//				}
				td4.text( log.balance - log.amount);
				var td5 = $('<td/>').appendTo(tr);
				td5.text(log.description);
//				balance -= log.amount;
			})
		})
	}
	
	

})(jQuery);



















