(function($) {
	var tbList, dlgRecharge,dlgEdit;
	var curUser, curTr;
	
	$(function(){
		tbList = $('#tbList');
		dlgRecharge = $('#dlgRecharge');
		dlgRecharge.find('.save').click(recharge);
		dlgRecharge.find('.cancel').click(function(){
			dlgRecharge.dialog('close');
		});
		dlgEdit = $('#dlgEdit');
		dlgEdit.find('.save').click(edit);
		dlgEdit.find('.cancel').click(function(){
			dlgEdit.dialog('close');
		});
		
		bindUsers();
	})
	
	function bindUsers(){		
		tbList.empty();
		$.getJSON('/user/list',{}, function(data){
			$(data.rows).each(function(i, user){
				var tr = $('<tr />').appendTo(tbList);
				tr.click(function(){
					tbList.children('.selected').removeClass('selected');
					tr.addClass('selected');
					curUser = user;	
					curTr = tr;
				})
				bindUser(tr, user);
			})
		})
	}
	
	function bindUser(tr, user){
		tr.empty();
		
		var td1 = $('<td />').appendTo(tr);
		td1.text(user.name);
		var td2 = $('<td />').appendTo(tr);
		td2.text(user._id);
		var td3 = $('<td class="balance"/>').appendTo(tr);
		td3.text(user.balance);
		var td4 = $('<td />').appendTo(tr);
		
		if(identity.userId!=user._id){
			var btnRecharge = $('<a href="javascript:void(0)" class="linkBtn1">充值</a>').appendTo(td4);
			
			btnRecharge.click(function(){
				dlgRecharge.show();
				dlgRecharge.dialog({
					modal : true,
					title : "充值"
				})
				dlgRecharge.find('.name').text(user.name);
				dlgRecharge.find('.amount').val('');
			})
		}
		if(identity.isAdmin){
			var btnEdit = $('<a href="javascript:void(0)" class="linkBtn1">编辑</a>').appendTo(td4);
			
			btnEdit.click(function(){
				dlgEdit.show();
				dlgEdit.dialog({
					modal : true,
					title : "编辑"
				})
				dlgEdit.find('.id').val(user._id);
				dlgEdit.find('.name').val(user.name);
				dlgEdit.find('.isAdmin').prop('checked', user.isAdmin);
			})
		}
		var btn2 = $('<a target="_blank">账户明细</a>').appendTo(td4);
		btn2.prop('href', '/account?id='+user._id);
		

	}
	
	function recharge(){
		var amount = dlgRecharge.find('.amount').val();
		if(!amount){
			$.messager.alert('', '请填写充值金额。');
			return;
		}
		dlgRecharge.dialog('close');
		$.postJSON('/account/recharge', {'userId':curUser._id, 'amount':amount}, function(data){
			curTr.find('.balance').text(data.balance);
			$.messagelabel.show('充值成功！');
			bindUsers();
		})
	}
	
	function edit(){
		dlgEdit.dialog('close');
		var user = {'_id': parseInt(dlgEdit.find('.id').val())};
		user['name'] = dlgEdit.find('.name').val();
		user['isAdmin'] = dlgEdit.find('.isAdmin').prop('checked');
		
		$.postJSON('/user/edit', user, function(data){
			$.messagelabel.show('操作成功！');
			bindUsers();
		})
	}
	

})(jQuery);



















