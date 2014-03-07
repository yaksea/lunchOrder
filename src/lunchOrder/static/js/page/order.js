(function($) {
	var tbOrders, pnlMenu, tbDishes,pnlBalance,btnSubmit;
	var curOrder, curOrderTr;
	var selectedDishId;
	
	$(function(){
		tbOrders = $('#tbOrders');
		pnlMenu = $('#pnlMenu');
		tbDishes = $('#tbDishes');
		pnlBalance = $('#pnlBalance');
		btnSubmit = $('#btnSubmit');
		
		bindBalance();
		bindOrders();
		btnSubmit.click(submit);
	})
	
	function bindBalance(){
		$.getJSON('/account/balance',{}, function(data){
			pnlBalance.text(data.balance);
		})
	}
	
	function bindOrders(){
		$.getJSON('/order/AvailableOrders',{}, function(data){
			if(data.rows.length){				
				$('.hasOrder').show();
				$('.noOrder').hide();
				$(data.rows).each(function(i, order){
					var tr = $('<tr />').appendTo(tbOrders);
					var td1 = $('<td />').appendTo(tr);
					td1.text(order.name);
					var td2 = $('<td />').appendTo(tr);
					td2.text(order.sponsor.name);
					var td3 = $('<td />').appendTo(tr);
					td3.text(order.createTime);
					var td4 = $('<td />').appendTo(tr);
					td4.text(order.note);
					var td5 = $('<td />').appendTo(tr);
					td5.text('未选择');
					
					if(i==0){
						selectOrder(tr, order);
					}
					
					tr.click(function(){
						if(curOrder._id != order._id){	
							selectOrder(tr, order);
						}
					})				
				})
			}
			else{
				$('.hasOrder').hide();
				$('.noOrder').show();
			}
			
		})
	}
	
	function selectOrder(tr, order){
		tbOrders.children('.selected').removeClass('selected');
		tr.addClass('selected');
		curOrder = order;
		curOrderTr = tr;
		selectedDishId = null;
		bindMenu();	
		bindBook(tr);
	}
	
	function bindMenu(){
		pnlMenu.find('.orderName').text(curOrder.name);
		pnlMenu.find('.menuName').text('');
		tbDishes.empty();
		$.getJSON('/menu/detail',{id:curOrder.menuId}, function(data){
			pnlMenu.find('.menuName').text(data.menu.name);
			$(data.dishes).each(function(i, dish){
				var tr = $('<tr />').appendTo(tbDishes);
				tr.prop('id', dish._id);
				var td1 = $('<td />').appendTo(tr);
				td1.text(dish.name);
				var td2 = $('<td />').appendTo(tr);
				td2.text(dish.price);
				
				tr.click(function(){
					tbDishes.children('.selected').removeClass('selected');
					tr.addClass('selected');
					selectedDishId = dish._id;
				})				
			})
			
		})
	}
	
	//绑定所选
	function bindBook(){
		$.getJSON('/order/MyOrderDetail',{id:curOrder._id}, function(data){
			if(data.dish){
				var td = curOrderTr.find("td:last-child");
				td.empty();
				var span = $('<span />').appendTo(td);
				span.text(data.dish.name);
				var btnClean = $('<a href="javascript:void(0)"  class="linkBtn1">取消</a>').appendTo(td);
				btnClean.click(function(){
					td.text('未选择');
					$.postJSON('/order/recallBook',{id:curOrder._id}, function(data){
						$.messagelabel.show('取消成功。')
					})
				})
				//
				var dishTr = tbDishes.children('#'+data.dish._id);
				if(dishTr){					
					tbDishes.children('.selected').removeClass('selected');
					dishTr.addClass('selected');
					selectedDishId = data.dish._id;
				}
			}
			
		})		
	}
	
	
	function submit(){
		if(selectedDishId){
			$.postJSON('/order/book',{orderId:curOrder._id,dishId:selectedDishId},function(){
				bindBook();
				$.messagelabel.show('成功提交！');
			})
		}
		else{
			$.messager.alert('', '请选择菜品，然后再提交。');
		}
	}
	
	

})(jQuery);



















