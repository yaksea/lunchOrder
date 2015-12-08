(function($) {
	var tbList,tbDishCount,tbDishes,tbOrderDetail,pnlSum,pnlPayer,pnlMenu,pnlOrderDetail,dlgPay;
	var curOrder, curTr;
	var status= {'0':'正在点餐中', '1':'停止点餐', '2':'已经结单', '-1':'已取消'}
	
	$(function(){
		tbList = $('#tbList');
		tbDishCount = $('#tbDishCount');
		tbDishes = $('#tbDishes');
		tbOrderDetail = $('#tbOrderDetail');
		//
		pnlSum = $('#pnlSum');
		pnlPayer = $('#pnlPayer');		
		pnlMenu = $('#pnlMenu');
		pnlOrderDetail = $('#pnlOrderDetail');
		//
		dlgPay = $('#dlgPay');
		dlgPay.find('.save').click(pay);
		dlgPay.find('.cancel').click(function(){
			dlgPay.dialog('close');
		});		
		//
		bindOrders();
		bindPayerList();
	})
	
	function bindOrders(){	
		$.getJSON('/order/list',{}, function(data){			
			$(data.rows).each(function(i, order){
				var tr = $('<tr />').appendTo(tbList);
				bindRow(tr, order);	
				if(i==0){
					selectRow(tr, order);
				}
			})
		})
	}
	
	function bindRow(tr, order){
		tr.empty();
		tr.click(function(){
			selectRow(tr, order)
		});
		var td1 = $('<td />').appendTo(tr);
		td1.text(order.name);
		var td4 = $('<td />').appendTo(tr);
		td4.text(order.sponsor.remarkName || order.sponsor.realName);
		var td2 = $('<td />').appendTo(tr);
		td2.text(order.createTime);
		var td3 = $('<td />').appendTo(tr);
		td3.text(status[order.status]);
		
		var td4 = $('<td />').appendTo(tr);
		if(identity.isAdmin||order.sponsor._id==identity._id){
			renderButtons(order, td4);
		}
		else{
			td4.text('非该订单发起人，无操作权限。')
		}
	}
	
	var orderDetailList = {};
	function getOrderDetail(odid, callback){
		var od = orderDetailList[odid];
		if(!od){
			$.getJSON('/order/Detail',{'id':odid}, function(data){
				orderDetailList[odid] = data;
				callback(data);
			})
		}else{
			callback(od);
		}
	}
	var menuDetailList = {};
	function getMenuDetail(menuId, callback){
		var menu = menuDetailList[menuId];
		if(!menu){
			$.getJSON('/menu/Detail',{'id':menuId}, function(data){
				menuDetailList[menuId] = data;
				callback(data);
			})
		}else{
			callback(menu);
		}
	}
	
	function renderButtons(order, td){
		td.empty();		
		var tr = td.parent();
		function _rebind(order){
			bindRow(tr, order);
			$.messagelabel.show('操作成功！');
			selectRow(tr, order);		
		}
		function _addButton(text, status){
			var btn1 = $('<a href="javascript:void(0)"  class="linkBtn1"/>').appendTo(td);
			btn1.text(text);
			btn1.click(function(){
				$.messager.confirm(text,'您确定要'+text+'？', function(answer){	
					if(answer){						
						$.postJSON('/order/changeStatus',{'id':order._id, 'status':status}, function(data){
							_rebind(data.order);
						})	
					}
				})
				return false;
			})
		}
		function _payButton(){
			var btn1 = $('<a href="javascript:void(0)"  class="linkBtn1"/>').appendTo(td);
			btn1.text('结单');
			btn1.click(function(){
				if(order.orderType==2){
					dlgPay.find('.view2').show();
				}else{
					dlgPay.find('.view2').hide();
					dlgPay.find('.txtAmount').val('');
				}
				if(identity.payment.byTurns){
					dlgPay.find('.view3').show();
				}else{
					dlgPay.find('.view3').hide();
					dlgPay.find('.payerId').val('');
				}
				dlgPay.show();
				dlgPay.dialog({
					'title':'结单',
					'modal':true
				})
			})
			
		}
		if(order.status==0){//正在点餐中
			if(order.orderType===2 || order.sum){				
				_addButton('停止点餐', 1);
				_payButton('结单', 2);
			}
			_addButton('取消订单', -1);
		}
		else if(order.status==1){//停止点餐
			_addButton('重新启用', 0);
			_payButton('结单', 2);
			_addButton('取消订单', -1);
		}		
		else if(order.status==-1){//已取消
			_addButton('重新启用', 0);
		}	
	}
	
	function pay(){
		$.postJSON('/order/changeStatus',{'id':curOrder._id, 'status':2, 
			'payerId':dlgPay.find('.payerId').val(), sum: dlgPay.find('.txtAmount').val()}, 
			function(data){
				bindRow(curTr, data.order);
				$.messagelabel.show('操作成功！');
				selectRow(curTr, data.order);
		})
		dlgPay.dialog('close');
	}
	
	function selectRow(tr, order){
		curOrder = order;
		curTr = tr;
		tbList.children('.selected').removeClass('selected');
		tr.addClass('selected');
		bindSlideInfo();
	}
	
	function bindPayerList(){
		var ddl = dlgPay.find('.payerId');
		var txtPayName = dlgPay.find('.payerName');
		ddl.change(function(){
			if(!ddl.val()){
				txtPayName.text('我');
			}
			else{
				txtPayName.text(ddl.find('option:selected').text());
			}
		})
		$.getJSON('/user/list',{}, function(data){
			$(data.rows).each(function(i, user){
				if(user._id!=identity._id){					
					var option = $('<option />').appendTo(ddl);
					option.val(user._id);
					option.text(user.remarkName);
				}
			})
		})
	}
	
	function bindSlideInfo(){
		_bindPayer();
		_bindOrderDetail();
		if(curOrder.orderType===1){
			_bindSum();
			_bindMenuDetail();		
		}else{
			pnlSum.hide();
			pnlMenu.hide();
		}
		
		function _bindPayer(){
			pnlPayer.hide();
			if(curOrder.payer){
				pnlPayer.show();
				pnlPayer.find('.name').text(curOrder.payer.user.remarkName);
				pnlPayer.find('.dateTime').text(curOrder.payer.dateTime);
			}
		}
		
		
		function _bindSum(){
			var sum = curOrder.sum;
			pnlSum.hide();
			if(sum){
				pnlSum.show();
				tbDishCount.empty();
				if(curOrder.orderType===1){
					dlgPay.find('.sumAmount').text(sum.amount);
					//
					$.each(sum.dishes, function(dishId, dish){
						var count = dish.count;
						if(count){
							var tr = $('<tr />').appendTo(tbDishCount);
							var td = $('<td />').appendTo(tr);
							td.text(dish.name);
							var td1 = $('<td />').appendTo(tr);
							td1.text(count + '份');
						}
					})
					pnlSum.find('.amount').text(sum.amount);
					pnlSum.find('.totalCount').text(sum.count);
				}
			}
		}
		function _bindOrderDetail(){
			var sum = curOrder.sum;
			pnlOrderDetail.hide();	
			tbOrderDetail.empty();
			pnlOrderDetail.find('.sum').text('');
			
			if(sum && sum.count){
				pnlOrderDetail.show();
				if(curOrder.orderType===2){
					getOrderDetail(curOrder._id, function(data){
						$(data.rows).each(function(i, od){
							var tr = $('<tr />').appendTo(tbOrderDetail);
							var td = $('<td />').appendTo(tr);
							td.text(od.user.remarkName);
							var td1 = $('<td />').appendTo(tr);
							td1.text('×'+od.sum.count);
						})
					});
					var txtSum = '共'+sum.count+'份';
					if(sum.amount){
						txtSum += '，总计:'+ sum.amount + '元';
					}
					pnlOrderDetail.find('.sum').text(txtSum);
				}
				else{
					getOrderDetail(curOrder._id, function(data){
						$(data.rows).each(function(i, od){
							$.each(od.sum.dishes, function(dishId, dish){
								var tr = $('<tr />').appendTo(tbOrderDetail);
								var td = $('<td />').appendTo(tr);
								td.text(od.user.remarkName);
								var td1 = $('<td />').appendTo(tr);
								td1.text(dish.name);
								var td2 = $('<td />').appendTo(tr);
								td2.text('×'+dish.count);
							});
						});
					});		
			 	}
		   }
		}
		
		
		function _bindMenuDetail(){
			pnlMenu.hide();
			getMenuDetail(curOrder.menuId, function(data){
				pnlMenu.show();
				pnlMenu.find('.name').text(data.menu.name);
				pnlMenu.find('.phone').text(data.menu.contact.phone);
				pnlMenu.find('.address').text(data.menu.contact.address);	
				
				tbDishes.empty();
				$(data.dishes).each(function(i, dish){				
					var tr = $('<tr />').appendTo(tbDishes);
					var td1 = $('<td />').appendTo(tr);
					td1.text(dish.name);
					var td2 = $('<td />').appendTo(tr);
					td2.text(dish.price);
				});
			});
		}
	}
	
	
	

})(jQuery);



















