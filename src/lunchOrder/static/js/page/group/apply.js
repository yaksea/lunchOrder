(function($) {
	var pnlNamecard,pnlTitle,btnSubmit,tbForm, groupId;
	
	$(function(){
		pnlNamecard = $('#pnlNamecard');
		pnlTitle = $('#pnlTitle');
		btnSubmit = $('#btnSubmit');
		tbForm = $('.tbForm');
		groupId = $.getUrlParam('groupId');
		//
		bindNamecard();
		btnSubmit.click(function(){
			btnSubmit.prop('disabled', true);
			$.postJSON('/group/apply',{'reason':tbForm.find('.reason').val(), 'groupId':groupId}, function(data){
				if(data.status){
					$.messagelabel.show('您的加群请求已通过。页面将要跳转...');
					setTimeout(function(){
						location.replace('/?groupId='+groupId);
					}, 200);
				}else{
					$.messagelabel.show('您的加群请求已发送成功，请耐心等候群主/管理员验证。页面将要跳转...');
					setTimeout(function(){
						location.replace('/group/join');
					}, 2000);
				}
			});				
		});
	})
	
	function bindNamecard(){	
		$.getJSON('/group/detail',{id:groupId}, function(group){	
			if(group.statusCode!=200){
				location.replace('/group/join');
			}else{
				pnlTitle.text('正在申请加入群：'+group.name);
				var txtName = $('<div class="name"/>').appendTo(pnlNamecard);
				txtName.text('群名片');
				//
				var pnl2 = $('<div class="pnl2"/>').appendTo(pnlNamecard);
				var txtUsers = $('<div class="users left"/>').appendTo(pnl2);
				txtUsers.text('成员：' + group.users +'人');	
				
				var txtFounder = $('<div class="founder right"/>').appendTo(pnl2);
				txtFounder.text('群主：' + group.founder.realName);
				
				var txtPayment = $('<div class="payment"/>').appendTo(pnlNamecard);
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
		
				var txtBrief = $('<div class="brief"/>').appendTo(pnlNamecard);
				txtBrief.text('简介：'+ group.brief);
				
				var pnlBottom = $('<div class="bottom"/>').appendTo(pnlNamecard);		
				var txtAddress = $('<div class="address left"/>').appendTo(pnlBottom);
				txtAddress.text('地址：'+ group.address);
			}
		});
	}

})(jQuery);



















