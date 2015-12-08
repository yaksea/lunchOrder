(function($) {
	var tbUserList, dlgRecharge;
	var curUser, curTr;
	var cashBalance;
	
	$(function(){
		tbUserList = $('#tbUserList');
		cashBalance = $('#cashBalance');
		dlgRecharge = $('#dlgRecharge');
		dlgRecharge.find('.save').click(recharge);
		dlgRecharge.find('.cancel').click(function(){
			dlgRecharge.dialog('close');
		});

		
		bindUsers();
		bindGroupCash();
	})
	
	function bindGroupCash(){
		if(!identity.payment.byTurns){
			cashBalance.empty();
			$.getJSON('/account/groupbalance',{}, function(data){
				cashBalance.text('现金账户余额：'+Math.toMoney(data.balance)+"   ");
				var a = $('<a href="/account?group=1" target="_blank">账户明细</a>').appendTo(cashBalance);
			})
		}
	}
	function bindUsers(){		
		tbUserList.empty();
		$.getJSON('/user/list',{}, function(data){
			var trFounder = null;
			$(data.rows).each(function(i, user){
				var role = $.inArray("founder", user.roles)>=0 ? 'founder': 
								$.inArray("admin", user.roles)>=0 ? 'admin': '';
				var tr;
				
				if(role==='founder'){
					tr = $('<tr />').prependTo(tbUserList);
					trFounder = tr;
				}else if(role==='admin'){
					if(trFounder){
						tr = $('<tr />').insertAfter(trFounder);
					}else{
						tr = $('<tr />').prependTo(tbUserList);
						trFounder = tr;
					}
				}else{
					tr = $('<tr />').appendTo(tbUserList);
				}
				if(curUser && curUser._id===user._id){
					tr.addClass('selected');
				}
				tr.click(function(){
					tbUserList.children('.selected').removeClass('selected');
					tr.addClass('selected');
					curUser = user;	
				});
				var td1 = $('<td />').appendTo(tr);
				if(role==='founder'){
					var img = $('<img src="/static/images/founder.png" class="imgRole" title="群主"/>').appendTo(td1);
					var txtName = $('<span title="群主" />').appendTo(td1);
					txtName.text(user.remarkName || user.realName);
				}else if(role==='admin'){
					var img = $('<img src="/static/images/admin.png" class="imgRole"  title="管理员"/>').appendTo(td1);
					var txtName = $('<span title="管理员" />').appendTo(td1);
					txtName.text(user.remarkName || user.realName);
				}else{
					td1.text(user.remarkName || user.realName);
				}
				var td2 = $('<td />').appendTo(tr);
				td2.text(user.userName);
				var td3 = $('<td class="balance"/>').appendTo(tr);
				td3.text(Math.toMoney(user.balance));
				var td4 = $('<td />').appendTo(tr);
				
				function _recharge(){
					var btnRecharge = $('<a href="javascript:void(0)" class="linkBtn1">充值</a>').appendTo(td4);
					
					btnRecharge.click(function(){
						dlgRecharge.show();
						dlgRecharge.dialog({
							modal : true,
							title : "充值"
						})
						dlgRecharge.find('.name').text(user.remarkName||user.realName);
						dlgRecharge.find('.amount').val('');
					})
				}
				
				if(identity.payment.byTurns){
					if(identity._id!=user._id){
						_recharge();
					}
				}else{
					if(identity.isAdmin){
						_recharge();
					}
				}
		
				var btn2 = $('<a target="_blank">账户明细</a>').appendTo(td4);
				btn2.prop('href', '/account?id='+user._id);
			});
		});
	}	
	function recharge(){
		var amount = dlgRecharge.find('.amount').val();
		if(!amount){
			$.messager.alert('', '请填写充值金额。');
			return;
		}
		dlgRecharge.dialog('close');
		$.postJSON('/account/recharge', {'id':curUser._id, 'amount':amount}, function(data){
			$.messagelabel.show('充值成功！');
			bindUsers();
			bindGroupCash();
		})
	}
	

	

})(jQuery);



















