(function($) {
	var ulGroups;
	
	$(function(){
		ulGroups = $('#ulGroups');
		bindGroupList();
	});
	function bindGroupList(){
		$.getJSON('/group/list',{}, function(data){
			if(data.rows.length){
				ulGroups.empty();
				ulGroups.show();
				$.each(data.rows, function(i, row){
					bindGroup(row);
				});
			}
		});
	}
	
	function bindGroup(group){
		var li = $('<li class="groupBlock"/>').appendTo(ulGroups);
		li.prop('id', 'gb'+group._id);
		var txtName = $('<div class="name"/>').appendTo(li);
		txtName.text(group.name);
		//
		var pnl2 = $('<div class="pnl2"/>').appendTo(li);
		var txtUsers = $('<div class="users left"/>').appendTo(pnl2);
		txtUsers.text('成员：' + group.users +'人');	
		
		var txtFounder = $('<div class="founder right"/>').appendTo(pnl2);
		txtFounder.text('群主：' + group.founder.realName);
		
		var txtPayment = $('<div class="payment"/>').appendTo(li);
		var payment = '结算规则：';
		if(group.payment.clear){
			payment += '每次结清';
		}else{
			if(group.payment.byTurns){
				payment += '轮流付饭钱';
			}else{
				payment += '指定人员统一管理饭钱';
			}
		}
		txtPayment.text(payment);

		var txtBrief = $('<div class="brief"/>').appendTo(li);
		txtBrief.text('简介：'+ group.brief);
		txtBrief.dotdotdot({wrap:'letter'});
		
		var pnlBottom = $('<div class="bottom"/>').appendTo(li);		
		var txtAddress = $('<div class="address left"/>').appendTo(pnlBottom);
		txtAddress.text('地址：'+ group.address);
		txtAddress.css({width:240, height:34});
		txtAddress.dotdotdot({wrap:'letter'});
		var pnlOperation = $('<div class="operation"/>').appendTo(pnlBottom);
		
		var ag = $('<a target="_blank" href="/?force=1&groupId='+group._id+'" />').appendTo(pnlOperation);
		ag.text('进入群');
		
	}	
})(jQuery);



















