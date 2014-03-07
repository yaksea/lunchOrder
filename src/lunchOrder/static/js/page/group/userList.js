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
		td4.text(order.sponsor.name);
		var td2 = $('<td />').appendTo(tr);
		td2.text(order.createTime);
		var td3 = $('<td />').appendTo(tr);
		td3.text(status[order.status]);
		
		var td4 = $('<td />').appendTo(tr);
		if(identity.isAdmin||order.sponsor._id==identity.userId){
			renderButtons(order, td4);
		}
		else{
			td4.text('非该订单发起人，无操作权限。')
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
				dlgPay.show();
				dlgPay.dialog({
					'title':'结单',
					'modal':true
				})
			})
			
		}
		if(order.status==0){//正在点餐中
			if(order.sum){				
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
			'payerId':dlgPay.find('.payerId').val()}, function(data){
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
		bindSum();
		bindOrderDetail();
		bindPayer();
		bindMenuDetail();		
	}
	
	function bindPayerList(){
		var ddl = dlgPay.find('.payerId');
		var txtPayName = dlgPay.find('.payerName');
		ddl.change(function(){
			if(!ddl.val()){
				txtPayName.text('您');
			}
			else{
				txtPayName.text(ddl.find('option:selected').text());
			}
		})
		$.getJSON('/user/list',{}, function(data){
			$(data.rows).each(function(i, user){
				if(user._id!=identity.userId){					
					var option = $('<option />').appendTo(ddl);
					option.val(user._id);
					option.text(user.name);
				}
			})
		})
	}
	
	function bindSum(){
		var sum = curOrder.sum;
		pnlSum.hide();
		if(sum){
			dlgPay.find('.sumAmount').text(sum.amount);
			//
			pnlSum.show();
			tbDishCount.empty();
			var totalCount = 0;
			$(sum.dishes).each(function(i, dish){
				var count = sum.dishCount[dish._id];
				if(count){
					var tr = $('<tr />').appendTo(tbDishCount);
					var td = $('<td />').appendTo(tr);
					td.text(dish.name);
					var td1 = $('<td />').appendTo(tr);
					td1.text(count + '份');
					totalCount += count;
//					td1.text(dish.price + ' * ' + count + '份');
				}
			})
			pnlSum.find('.amount').text(sum.amount);
			pnlSum.find('.totalCount').text(totalCount);
		}
	}
	function bindOrderDetail(){
		var sum = curOrder.sum;
		pnlOrderDetail.hide();	
		
		if(sum){
			$.getJSON('/order/Detail',{'id':curOrder._id}, function(data){
				pnlOrderDetail.show();
				tbOrderDetail.empty();
				$(data.rows).each(function(i, od){
					var tr = $('<tr />').appendTo(tbOrderDetail);
					var td = $('<td />').appendTo(tr);
					td.text(od.user.name);
					var td1 = $('<td />').appendTo(tr);
					td1.text(od.dish.name);
					var td2 = $('<td />').appendTo(tr);
					td2.text(od.dish.price+'元');
				})
			})			
		}
	}
	
	
	function bindPayer(){
		pnlPayer.hide();
		if(curOrder.payer){
			pnlPayer.show();
			pnlPayer.find('.name').text(curOrder.payer.user.name);
			pnlPayer.find('.dateTime').text(curOrder.payer.dateTime);
		}
	}
	
	function bindMenuDetail(){
		pnlMenu.hide();
		$.getJSON('/menu/Detail',{'id':curOrder.menuId}, function(data){
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
			})
		})
	}
	
	
	

})(jQuery);



















