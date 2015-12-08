(function($) {
	var headInfo, form, divTabs, pnlBody, btnSubmit, pnlSpread, 
	spreadUrl, tbApplyList, dlgReject, tbUserList, dlgEdit, btnDismiss;
	var tabIndex=0, bound=[], curPanel;
	var curUser, curApply;
	
	$(function(){
		headInfo = $('#headInfo');
		form = $('#form');
		divTabs = $('#divTabs');
		pnlBody = $('#pnlBody');
		btnDismiss = $('#btnDismiss');
		tbApplyList = $('#tbApplyList');
		tbUserList = $('#tbUserList');
		pnlSpread = $('.pnlSpread');
		btnSubmit = $('#btnSubmit');
		btnSubmit.click(function(){
			var data = {'address':form.find('.address').val(), brief:form.find('.brief').val(), 
							noAudit:form.find('.noAudit').prop('checked')?1:0};
			if(!data.address){
				alert('地址必填');
				return;
			}			
			
			$.postJSON('/group/edit',data, function(){
				$.messagelabel.show('修改资料成功！');
			})
		})
		//
		dlgReject = $('#dlgReject');
		dlgReject.find('.save').click(function(){
			dlgReject.dialog('close');
			$.postJSON('/group/Audit', {'id':curApply._id, 'status':-1}, function(){
				bindApply();
				$.messagelabel.show('操作成功！');
			})
		});
		dlgReject.find('.cancel').click(function(){
			dlgReject.dialog('close');
		});
		bindInfo();
		divTabs.children().click(function(){
			var $this = $(this);
			divTabs.children().removeClass('selected');
			$this.addClass('selected');;
			tabIndex = $this.index();
			pnlBody.children().hide();
			curPanel = pnlBody.children().eq(tabIndex);
			curPanel.show();
			bindBody();
		});
		
		dlgEdit = $('#dlgEdit');
		dlgEdit.find('.save').click(editUser);
		dlgEdit.find('.cancel').click(function(){
			dlgEdit.dialog('close');
		});
		
		btnDismiss.click(function(){
			$.getJSON('/group/dismiss',{}, function(data){
				if(data.success){
					$.messager.confirm('解散该群','您确定要解散该群？解散后该群相关数据将不可恢复。', function(answer){	
						if(answer){	
							$.postJSON('/group/dismiss',{}, function(){
								$.messagelabel.show('已成功解散该群，页面正在跳转...');
								location.href = '/';
							})	
						}
					});					
				}else{
					btnDismiss.hide();
					btnDismiss.prev().show();
				}
			})
		});
	})
	function bindInfo(){	
		$.getJSON('/group/detail',{}, function(data){			
			headInfo.find('.name').text(data.name);
			headInfo.find('.users').text(data.users);
			if(data.payment.byTurns){
				headInfo.find('.payment').text('轮流付饭钱');
			}else{
				headInfo.find('.payment').text('指定人员统一管理饭钱');
			}
			form.find('.address').val(data.address);
			form.find('.brief').val(data.brief);
			form.find('.noAudit').prop('checked', data.noAudit===1?true:false);
			bound[0] = true;
		})
	}
	function bindBody(){
		if(bound[tabIndex]){
			return;
		}
		switch(tabIndex){
			case 0:
				bindInfo();
				break;
			case 1:
				bindSpead();
				break;
			case 2:
				bindApply();
				setInterval(bindApply, 20000);
				break;
			case 3:
				bindUsers();
				break;
				
		}
		bound[tabIndex] = true;
	}
	
	function bindSpead(){
		ZeroClipboard.config( { swfPath: "/static/js/base/ZeroClipboard.swf" } );
		var client = new ZeroClipboard(pnlSpread.find('.copy'));
		spreadUrl = $('#spreadUrl').select();
		spreadUrl.click(function(){
			spreadUrl.select();		
		})
		client.on('aftercopy', function(e){
			$('#spreadUrl').select();
			$.messagelabel.show('已将推广地址复制到剪贴板。');
		});
	}
	function bindApply(){
		$.getJSON('/group/MyApproves',{}, function(data){
			if(!data.rows.length){
				$('.noApply').show();
				$('.listApply').hide();
				return;
			}
			tbApplyList.empty();
			$('.noApply').hide();
			$('.listApply').show();
			$.each(data.rows, function(i, apply){
				var status = apply.result.approved;
				var tr = $('<tr />').appendTo(tbApplyList);
				var td1 = $('<td />').appendTo(tr);
				td1.text(apply.applicant.realName);
				var td12 = $('<td />').appendTo(tr);
				td12.text(apply.reason);
				var td2 = $('<td />').appendTo(tr);
				td2.text(apply.createTime);
				var td3 = $('<td />').appendTo(tr);
				td3.text(status==-1?'被拒绝':status==0?'等待审核':'已通过');
				var td4 = $('<td />').appendTo(tr);
				if(status==0){
					var btnApprove = $('<a href="javascript:void(0)" class="linkBtn1">接受</a>').appendTo(td4);
					btnApprove.click(function(){
						$.messager.confirm('接受申请','您确定要接受申请？', function(answer){	
							$.postJSON('/group/audit', {'id':apply._id, 'status':1}, function(){
								bindApply();
								$.messagelabel.show('操作成功！');
							});
						});
					});
					
					var btnReject = $('<a href="javascript:void(0)" class="linkBtn1">拒绝</a>').appendTo(td4);
					btnReject.click(function(){
						curApply = apply;
						dlgReject.show();
						dlgReject.dialog({'modal':true,'title':'拒绝理由'});
					})
				}
				else{
					if(apply.result.operator){
						td4.text(apply.result.operator.realName+(status==-1?'已拒绝':'已接受'));
					}else if(status===1){
						td4.text('系统开放免审');
					}
				}
			});
		});
	}
	function bindUsers(){		
		$.getJSON('/user/list',{}, function(data){
			tbUserList.empty();
			var trFounder=null;
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
				
				if(identity._id!=user._id){
					var btnEdit = $('<a href="javascript:void(0)" class="linkBtn1">编辑</a>').appendTo(td4);
					
					btnEdit.click(function(){
						curUser = user;
						dlgEdit.show();
						dlgEdit.dialog({
							modal : true,
							title : "编辑"
						})
						dlgEdit.find('.id').text(user.userName);
						dlgEdit.find('.name').text(user.realName);
						dlgEdit.find('.remarkName').val(user.remarkName);
						dlgEdit.find('.isAdmin').prop('checked', $.inArray("admin", user.roles)>=0);
					});
					//
					if(!user.balance){
						var btnOut = $('<a href="javascript:void(0)" class="linkBtn1">踢出群</a>').appendTo(td4);
						btnOut.click(function(){
							$.messager.confirm('踢出群','您确定要将'+ (user.remarkName || user.realName) +'踢出群？', function(answer){	
								if(answer){	
									tr.remove();
									$.postJSON('/group/out',{'ugid':user._id}, function(){
										$.messagelabel.show('已成功将'+ (user.remarkName || user.realName) +'踢出群');
										bindInfo();
									})	
								}
							})
							return false;						
						});
					}
				}
			});
		});
	}
	function editUser(){
		dlgEdit.dialog('close');
		var user = {'id': curUser._id};
		user['remarkName'] = dlgEdit.find('.remarkName').val();
		user['isAdmin'] = dlgEdit.find('.isAdmin').prop('checked');
		
		$.postJSON('/user/edit', user, function(data){
			$.messagelabel.show('修改成功！');
			bindUsers();
		});
	}

})(jQuery);



















