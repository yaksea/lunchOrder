(function($) {
	var ulGroups;
	
	$(function(){
		ulGroups = $('#ulGroups');
		$('.topMenu').children().eq(1).addClass('active');
		bindGroupList();
	});
	function bindGroupList(){
		$.getJSON('/group/mygroups',{groupDetail:1}, function(data){
			if(data.rows.length){
				ulGroups.empty();
				ulGroups.show();
				$.each(data.rows, function(i, row){
					bindGroup(row);
				});
			}else{
				$('#pnlNoGroup').show();
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

		var txtBalance = $('<div class="balance"/>').appendTo(li);
		txtBalance.text('我的账户余额：'+ group.balance);
		if(!group.balance && identity.userId!=group.founder.userId){
			var btnOut = $('<a href="javascript:void(0)" class="linkBtn1">退出该群</a>').appendTo(txtBalance);
			btnOut.click(function(){
				$.messager.confirm('退出该群','您确定要退出该群，以后不再参加['+ group.name +']的饭事？', function(answer){	
					if(answer){	
						li.remove();
						$.postJSON('/group/out',{'gid':group._id}, function(){
							$.messagelabel.show('已成功退出'+ group.name);
						})	
					}
				})
				return false;
			});
		}
		
		var txtBrief = $('<div class="brief"/>').appendTo(li);
		txtBrief.text('简介：'+ group.brief);
		txtBrief.dotdotdot({wrap:'letter'});
		
		var pnlBottom = $('<div class="bottom"/>').appendTo(li);		
		var txtAddress = $('<div class="address left"/>').appendTo(pnlBottom);
		txtAddress.text('地址：'+ group.address);
		txtAddress.css({width:240, height:34});
		txtAddress.dotdotdot({wrap:'letter'});
		var pnlOperation = $('<div class="operation"/>').appendTo(pnlBottom);
		
		var ag = $('<a href="/?groupId='+group._id+'" />').appendTo(pnlOperation);
		ag.text('进入群');
		
	}	
})(jQuery);



















