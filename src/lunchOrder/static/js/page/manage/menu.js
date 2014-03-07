(function($) {
	var menuList,btnSubmit,dlgCreateOrder,dlgEditMenu,dlgEditDish, cCreateMenu;
	var selectedMenuId, curDishData, curDishC, curMenuData, curMenuHead, curMenuId, curMenuDishList;
	
	$(function(){
		menuList = $('#menuList');
		dlgCreateOrder = $('#dlgCreateOrder');
		dlgEditMenu = $('#dlgEditMenu');
		dlgEditDish = $('#dlgEditDish');
		
		btnSubmit = $('#btnSubmit');		
		btnSubmit.click(submit);
		
		dlgCreateOrder.find('.save').click(createOrder);
		dlgCreateOrder.find('.cancel').click(function(){
			dlgCreateOrder.dialog('close');
		});
		dlgEditMenu.find('.save').click(editMenu);
		dlgEditMenu.find('.cancel').click(function(){
			dlgEditMenu.dialog('close');
		});
		dlgEditDish.find('.save').click(editDish);
		dlgEditDish.find('.cancel').click(function(){
			dlgEditDish.dialog('close');
		});
		
		bindMenus();
	})
	
	function bindMenus(){		
		cCreateMenu = $('<div class="menuBlock"/>').appendTo(menuList);
		var btnCreateMenu = $('<a href="javascript:void(0)" class="linkBtn1">新建菜单</a>').appendTo(cCreateMenu);
		btnCreateMenu.click(function(){
			dlgEditMenu.find('.name').val('');
			dlgEditMenu.find('.phone').val('');
			dlgEditMenu.find('.address').val('');
			curMenuData = null;			
			dlgEditMenu.show();
			dlgEditMenu.dialog({
				modal : true,
				title : "新建菜单"
			});	
		})
		if(!identity.isAdmin){
			cCreateMenu.hide();
		}
		
		$.getJSON('/menu/list',{}, function(data){			
			$(data.rows).each(function(i, menu){
				bindMenu(menu._id);
			})
		})
	}
	
	function bindMenu(menuId){
		var cMenu = $('<div class="menuBlock"/>').insertBefore(cCreateMenu);
		
		cMenu.click(function(){
			menuList.children('.selected').removeClass('selected');
			cMenu.addClass('selected');
			selectedMenuId = menuId;
		})
		
		$.getJSON('/menu/detail',{id:menuId}, function(data){
			var cMenuHead = $('<div class="block"/>').appendTo(cMenu);
			bindMenuHead(cMenuHead, data.menu);
			
			var divDishes = $('<div class="block"/>').appendTo(cMenu);
			var tableDishes = $('<table />').appendTo(divDishes);
			var cDishes = $('<tbody/>').appendTo(tableDishes);
			bindDishes(cDishes, data);	
		})	
	}
	
	function bindMenuHead(cMenuHead, dMenuHead){	
		cMenuHead.empty();
		var l1= $('<div />').appendTo(cMenuHead);
		l1.text('菜单名：'+dMenuHead.name);
		
		if(identity.isAdmin){
			var btns = $('<div style="float:right"/>').appendTo(l1);
			var btnEdit = $('<a href="javascript:void(0)" class="linkBtn1">编辑</a>').appendTo(btns);
			btnEdit.click(function(){
				dlgEditMenu.find('.name').val(dMenuHead.name);
				dlgEditMenu.find('.phone').val(dMenuHead.contact.phone);
				dlgEditMenu.find('.address').val(dMenuHead.contact.address);
				curMenuData = dMenuHead;	
				curMenuHead = cMenuHead;
				dlgEditMenu.show();
				dlgEditMenu.dialog({
					modal : true,
					title : "编辑菜单"
				});		
			})		
			var btnDel = $('<a href="javascript:void(0)" class="linkBtn1">删除</a>').appendTo(btns);
			btnDel.click(function(){
				$.messager.confirm('删除菜单','您确定要删除菜单['+dMenuHead.name+']？', function(answer){	
					if(answer){	
						cMenuHead.parent().remove();
						$.postJSON('/menu/delete',{'id':dMenuHead._id}, function(){
							$.messagelabel.show('已成功删除菜单');
						})	
					}
				})
				return false;
			})
		}
		var l2= $('<div />').appendTo(cMenuHead);
		l2.text('电话：'+dMenuHead.contact.phone);
		var l3= $('<div />').appendTo(cMenuHead);
		l3.text('地址：'+dMenuHead.contact.address);
	
		
	}
	
	function bindDishes(cDishes, dMenuDetail){
		$(dMenuDetail.dishes).each(function(i, dish){
			var tr = $('<tr />').appendTo(cDishes);
			bindDish(tr, dish);
		})	
		if(identity.isAdmin){
			var btnCreate = $('<a href="javascript:void(0)" class="linkBtn1">添加菜品</a>').insertAfter(cDishes);
			btnCreate.click(function(){
				dlgEditDish.find('.name').val('');
				dlgEditDish.find('.price').val('');
				curMenuId = dMenuDetail.menu._id;
				curMenuDishList = cDishes;
				curDishData = null;
				dlgEditDish.show();
				dlgEditDish.dialog({
					modal : true,
					title : "添加菜品"
				});			
			})
		}
	}
	
	function bindDish(cDish, dDish){
		cDish.empty();
		var td1 = $('<td />').appendTo(cDish);
		td1.text(dDish.name);
		var td2 = $('<td />').appendTo(cDish);
		td2.text(dDish.price);
		var td3 = $('<td />').appendTo(cDish);
		if(identity.isAdmin){
			var btnEdit = $('<a href="javascript:void(0)" class="linkBtn1">编辑</a>').appendTo(td3);
			btnEdit.click(function(){
				dlgEditDish.find('.name').val(dDish.name);
				dlgEditDish.find('.price').val(dDish.price);
				curDishData = dDish;
				curDishC = cDish;
				dlgEditDish.show();
				dlgEditDish.dialog({
					modal : true,
					title : "编辑菜品"
				});			
			})
			var btnDel = $('<a href="javascript:void(0)" class="linkBtn1">删除</a>').appendTo(td3);
			btnDel.click(function(){
				cDish.remove();
				$.postJSON('/dish/delete',{'id':dDish._id}, function(){
					$.messagelabel.show('已成功删除菜品')
				})	
			})
		}
		
	}
	
	
	function submit(){
		if(selectedMenuId){
			dlgCreateOrder.show();
			dlgCreateOrder.dialog({
				modal : true,
				title : "提交订单"
			});	
			
		}
		else{
			$.messager.alert('', '请选择菜单，然后再提交。');
		}
	}
	
	function createOrder(){
		dlgCreateOrder.dialog('close');
		$.postJSON('/order/create',{name:dlgCreateOrder.find('.name').val(), 
			note:dlgCreateOrder.find('.note').val(), 
			menuId:selectedMenuId},
			function(){
				$.messagelabel.show('成功提交！');
		})		
	}
	
	function editMenu(){
		dlgEditMenu.dialog('close');
		var menuData = {name:dlgEditMenu.find('.name').val(), 
			phone:dlgEditMenu.find('.phone').val(), 
			address:dlgEditMenu.find('.address').val()};
		
		if(curMenuData){
			$.extend(curMenuData, menuData, {id:curMenuData['_id']})
			$.postJSON('/menu/edit', curMenuData,
				function(){
					curMenuData.contact = {phone:menuData.phone, address:menuData.address};
					bindMenuHead(curMenuHead,curMenuData);
					$.messagelabel.show('成功提交！');
				})		
		}
		else{			
			$.postJSON('/menu/create', menuData,
				function(data){
					bindMenu(data.id);
					$.messagelabel.show('成功提交！');
				})
		}
	}
	function editDish(){
		dlgEditDish.dialog('close');
		if(curDishData){
			$.extend(curDishData, {name:dlgEditDish.find('.name').val(), 
				price:dlgEditDish.find('.price').val(), id:curDishData['_id']})
			$.postJSON('/dish/edit', curDishData,
				function(){
					bindDish(curDishC,curDishData);
						$.messagelabel.show('成功提交！');
				})		
		}
		else{
			curDishData = {}
			$.extend(curDishData, {name:dlgEditDish.find('.name').val(), 
				price:dlgEditDish.find('.price').val(), 'menuId': curMenuId});
			
			$.postJSON('/dish/create',curDishData,
				function(data){
					curDishData._id = data.id;
					var tr = $('<tr />').appendTo(curMenuDishList);
					bindDish(tr, curDishData);
					$.messagelabel.show('成功提交！');
				})
		}
	}
	
	

})(jQuery);



















