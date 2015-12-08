(function($) {
	var tbOrders, pnlMenu, tbDishes,pnlBalance,btnSubmit1, btnSubmit2, btnDel1, btnDel2, tbDetails,
	pnlOrderDetails, pnlParty, pnlOrderList, pnlSteps;
	var curOrder, curOrderTr;
	var details;
	var orderIds;
	var pnlNoChoice, pnlMyChoice;
	var partyPieces;
	
	$(function(){
		tbOrders = $('#tbOrders');
		pnlMenu = $('#pnlMenu');
		tbDishes = $('#tbDishes');
		tbDetails = $('#tbDetails');
		pnlBalance = $('#pnlBalance');
		btnSubmit1 = $('#btnSubmit1');
		btnSubmit2 = $('#btnSubmit2');
		btnDel1 = $('#btnDel1');
		btnDel2 = $('#btnDel2');
		pnlOrderDetails = $('#pnlOrderDetails');
		pnlParty = $('#pnlParty');
		partyPieces = pnlParty.find('.pieces').numberAdjust({showAlways:true});
		
		pnlOrderList = $('#pnlOrderList');
		pnlSteps = $('#pnlSteps');
		pnlNoChoice = $('#pnlNoChoice');
		pnlMyChoice = $('#pnlMyChoice');
		
		bindBalance();
		bindPage();
		btnSubmit2.click(function(){
			btnSubmit2.prop('disabled', true);
			btnSubmit2.text('正在提交...');
			$.postJSON('/order/book', {count:partyPieces.getValue(), orderId:curOrder._id}, function(){
				btnSubmit2.prop('disabled', false);
				btnSubmit2.text('提交订单')
				bindDetail(true);
				$.messagelabel.show('提交订单成功。')
			});
		})
	})
	
	function bindBalance(){
		$.getJSON('/account/mybalance',{}, function(data){
			pnlBalance.text(Math.toMoney(data.balance));
		})
	}
	
	function bindPage(){
		$.getJSON('/order/AvailableOrders',{}, function(data){
			if(data.rows.length){				
				$('.hasOrder').show();
				$('.noOrder').hide();
				orderIds = $.map(data.rows, function(ord){
				  return ord['_id'];
				});
				$.postJSON('/order/MyOrderDetails',{ids:orderIds}, function(ddd){
					details = ddd.details;
					bindDetail();
					bindOrders(data.rows);
				});
			}
			else{
				$('.hasOrder').hide();
				$('.noOrder').show();
			}
			
		})
	}
	
	function bindOrders(orders){
 		$(orders).each(function(i, order){
			var tr = $('<tr />').appendTo(tbOrders);
			var td0 = $('<td />').appendTo(tr);
			td0.text(order.orderType===1?'快餐':'小炒AA');
			var td1 = $('<td />').appendTo(tr);
			td1.text(order.name);
			var td2 = $('<td />').appendTo(tr);
			td2.text(order.sponsor.remarkName);
			var td3 = $('<td />').appendTo(tr);
			td3.text(order.createTime);
			var td4 = $('<td />').appendTo(tr);
			td4.text(order.note);
			
			tr.click(function(){
				if(!curOrder || curOrder._id != order._id){	
					selectOrder(tr, order);
				}
			})
			if(i==0){
				tr.click();
			}
		})		
	}
	
	function selectOrder(tr, order){
		tbOrders.children('.selected').removeClass('selected');
		tr.addClass('selected');
		curOrder = order;
		curOrderTr = tr;
		if(curOrder.orderType===1){
			bindMenu();
		}else{
			bindParty();
		}
	}
	
	function bindMenu(){
		pnlMenu.show();
		pnlParty.hide();
		pnlMenu.find('.orderName').text(curOrder.name);
		pnlMenu.find('.menuName').text('');
		tbDishes.empty();
		var tbSum = pnlMenu.find('.tbSum');
		var dishCount = {};
		var sumDishes = details[curOrder._id] && details[curOrder._id]['sum'] &&
			details[curOrder._id]['sum']['dishes'];
		if(sumDishes){
			$.each(sumDishes, function(dishId, dish){
				dishCount[dishId] = dish['count'];
			});
		}
		var dishes = {}
		function _bindDetail(){
			var amount = 0;
			var totalCount = 0;
			tbDishes.children().removeClass('selected');
			if(!Object.keys(dishCount).length){
				pnlNoChoice.show();
				pnlMyChoice.hide();
				return;
			}
			pnlNoChoice.hide();
			pnlMyChoice.show();
			tbSum.empty();
			
			$.each(dishCount, function(dishId, count){
				var dish = dishes[dishId];
				var tr = $('<tr />').appendTo(tbSum);
				var td1 = $('<td />').appendTo(tr);
				td1.text(dish.name);
				var td2 = $('<td />').appendTo(tr);
				td2.text(dish.price);
				var td3 = $('<td style="text-align:center; vertical-align: middle;padding:0px;" />').appendTo(tr);	
				var txtCount = $('<input type="text" />').appendTo(td3);
				var numCount = txtCount.numberAdjust({value:count, change:function(value){
					dishCount[dish._id] = value;
					if(value===0){
						delete dishCount[dish._id];
					}
					_bindDetail();
					tbDishes.find('#'+dish._id).trigger('dataChanged');
				}});
				
				var td4 = $('<td />').appendTo(tr);				
				td4.text(dish.price*count);
				
				amount += (dish.price*count);
				totalCount += count;
				var dishTr = tbDishes.children('#'+dishId);
				dishTr.addClass('selected');
				tr.mouseover(function(){
					numCount.hover();
				}).mouseout(function(){
					numCount.out();
				})
			})
			pnlMenu.find('.totalCount').text(totalCount);
			pnlMenu.find('.amount').text(amount);
		}
		
		$.getJSON('/menu/detail',{id:curOrder.menuId}, function(data){
			pnlMenu.find('.menuName').text(data.menu.name);
			
			$(data.dishes).each(function(i, dish){
				dishes[dish._id] = dish;
				var tr = $('<tr />').appendTo(tbDishes);
				tr.prop('id', dish._id);
				var td1 = $('<td />').appendTo(tr);
				td1.text(dish.name);
				var td2 = $('<td />').appendTo(tr);
				td2.text(dish.price);
				var td3 = $('<td style="text-align:center;" />').appendTo(tr);
				var btnAdd = $('<a href="javascript:void(0)" class="cart">&#xe636;</a>').appendTo(td3);
//				btnAdd.hide();
				btnAdd.click(function(){
					dishCount[dish._id] = dishCount[dish._id] || 0;
					dishCount[dish._id] += 1;
					_dataBind();
					_bindDetail();
				});
				var txtCount = $('<input type="text" />').appendTo(td3);
				var numCount = txtCount.numberAdjust({value:dishCount[dish._id], noBorder:true, change:function(value){
					dishCount[dish._id] = value;
					if(value===0){
						delete dishCount[dish._id];
					}					
					_dataBind();
					_bindDetail();
				}});		
				tr.bind('dataChanged', _dataBind);
				
				function _dataBind(){
					numCount.setValue(dishCount[dish._id]);
					if(dishCount[dish._id]){
						numCount.show();
						btnAdd.hide();
					}else{
						numCount.hide();
						btnAdd.show();
					}
				}
				_dataBind();
				tr.mouseover(function(){
					if(dishCount[dish._id]){
						numCount.hover();
					}else{
//						btnAdd.show();
					}
				}).mouseout(function(){
					if(dishCount[dish._id]){
						numCount.out();
					}else{
//						btnAdd.hide();
					}
				});
				
				btnSubmit1.unbind('click').click(function(){
					if(Object.keys(dishCount).length){
						btnSubmit1.prop('disabled', true);
						btnSubmit1.text('正在提交...');
						$.postJSON('/order/book', {dishCount:dishCount, orderId:curOrder._id}, function(){
							btnSubmit1.text('提交订单');
							btnSubmit1.prop('disabled', false);
							bindDetail(true);
							$.messagelabel.show('提交订单成功。');
						})
					}else{
						alert('请先选择菜品。');
					}
				})
				btnDel1.unbind('click').click(function(){
					$.postJSON('/order/book', {dishCount:{}, orderId:curOrder._id}, function(){
						delete details[curOrder._id];
						bindDetail();
						$.messagelabel.show('取消订单成功。');
						bindMenu();
					})
				})
			})
			_bindDetail();
		}, true);
	}
	
	//绑定所选
	function bindParty(){
		pnlParty.show();
		pnlMenu.hide();
		pnlParty.find('.orderName').text(curOrder.name);
		
		var count = details[curOrder._id] && details[curOrder._id]['sum'] &&
			details[curOrder._id]['sum']['count'] || 1;
		
		partyPieces.setValue(count);
	}
	
	function bindDetail(request){
		if(request){
			$.postJSON('/order/MyOrderDetails',{ids:orderIds}, function(ddd){
				details = ddd.details;
				_bind();
			})
		}else{
				_bind();
		}
		function _bind(){
			if(Object.keys(details).length===0){
				pnlSteps.show();
				pnlOrderList.hide();
				return;
			}
			pnlSteps.hide();
			pnlOrderList.show();
			tbDetails.empty();
			$.each(details, function(orderId, ods){
				if(ods.order.orderType===1){
					$.each(ods.sum.dishes, function(dishId, dish){
						var count = dish.count;
						var tr = $('<tr />').appendTo(tbDetails);
						var td00 = $('<td />').appendTo(tr);
						td00.text('快餐');
						var td0 = $('<td />').appendTo(tr);
						td0.text(ods.order.name);
						var td1 = $('<td />').appendTo(tr);
						td1.text(dish.name);
						var td2 = $('<td />').appendTo(tr);
						td2.text(dish.price);
						var td3 = $('<td />').appendTo(tr);				
						td3.text(count);
						var td4 = $('<td />').appendTo(tr);				
						td4.text(dish.price*count);				
					})
				}else{
					var tr = $('<tr />').appendTo(tbDetails);
					var td00 = $('<td />').appendTo(tr);
					td00.text('小炒AA');
					var td0 = $('<td />').appendTo(tr);
					td0.text(ods.order.name);
					var td1 = $('<td />').appendTo(tr);
					td1.text('-');
					td1.css('text-align','center');
					var td2 = $('<td />').appendTo(tr);
					td2.text('-');
					td2.css('textAlign','center');
					var td3 = $('<td />').appendTo(tr);				
					td3.text(ods.sum.count);
					var td4 = $('<td />').appendTo(tr);				
					td4.text('-');
					td4.css('text-align','center');
					
				}
			});
		}
	}
	
	

})(jQuery);



















