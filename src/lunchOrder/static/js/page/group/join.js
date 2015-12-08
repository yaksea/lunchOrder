(function($) {
	var ulGroups, dlgApply, curGroup, tbApplyList, pnlApply;
	var approvedIds={};
	
	$(function(){
		ulGroups = $('#ulGroups');
		pnlApply = $('#pnlApply');
		tbApplyList = $('#tbApplyList');
		dlgApply = $('#dlgApply');
		dlgApply.find('.save').click(apply);
		dlgApply.find('.cancel').click(function(){
			dlgApply.dialog('close');
		});
		
		getApprovedIds(bindGroupList);
	})
	
	function bindApplyList(){
		$.getJSON('/group/myapply',{}, function(data){
			tbApplyList.empty();
			if(data.rows.length){
				pnlApply.show();
			}
			$.each(data.rows, function(i, apply){
				var status = apply.result.approved;
				var tr = $('<tr />').appendTo(tbApplyList);
				var td1 = $('<td />').appendTo(tr);
				if(status==1){
					var ag = $('<a href="/?groupId='+apply.group._id+'" />').appendTo(td1);
					ag.text(apply.group.name);
					var li = $('#gb'+apply.group._id);
					if(li){
						li.find('.operation').html('<a href="/?groupId='+apply.group._id+'" >进入群</a>')
					}
				}else{
					td1.text(apply.group.name);
					if(status==0){
						var li = $('#gb'+apply.group._id);
						if(li){
							li.find('.operation').text('审核中');
						}
					}
				}
				var td2 = $('<td />').appendTo(tr);
				td2.text(apply.createTime);
				var td21 = $('<td />').appendTo(tr);
				td21.text(apply.reason);
				var td3 = $('<td />').appendTo(tr);
				td3.text(status==-1?'被拒绝':status==0?'请耐心等待群主审核':'已通过');
				var td4 = $('<td />').appendTo(tr);
				td4.text(apply.group.founder.realName);
			});
			setTimeout(bindApplyList, 20000);
		});
	}
	
	function getApprovedIds(callback){
		$.getJSON('/group/MyGroups',{}, function(data){
			$.each(data.rows, function(i, row){
				approvedIds[row.groupId] = 1;
			});
			if(callback){
				callback();
			}
		});
	}
	
	function bindGroupList(){
		$.getJSON('/group/list',{}, function(data){
			$.each(data.rows, function(i, row){
				bindGroup(row);
			});
			bindApplyList();
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
		
		if(approvedIds[group._id]){
			var ag = $('<a href="/?groupId='+group._id+'" />').appendTo(pnlOperation);
			ag.text('进入群');
		}else{
			var btnApply = $('<a href="javascript:void(0);" class="">加入群</a>').appendTo(pnlOperation);
			btnApply.click(function(){
				curGroup = group;
				dlgApply.show();
				dlgApply.dialog({
					modal : true,
					title : "加入群"
				});
				btnApply.find('.name').text(group.name);
			});
		}
		
	}
	
	function apply(){
		$.postJSON('/group/apply',{'reason':dlgApply.find('.reason').val(), 'groupId':curGroup._id}, function(data){
			if(data.status){
				$.messagelabel.show('您的加群请求已通过。');
			}else{
				$.messagelabel.show('您的加群请求已发送成功，请等候群主/管理员验证。');
			}			
			
			dlgApply.dialog('close');
			bindApplyList();
		});		
	}
})(jQuery);



















