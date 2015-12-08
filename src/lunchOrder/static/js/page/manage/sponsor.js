(function($) {
	var menuList,navPath,btnSubmit,dlgCreateOrder,dlgEditMenu,dlgEditDish;
	var selectedMenuId, curDishData, curDishC, curMenuData, curMenuHead, curMenuId, curMenuDishList, curStep=1;
	var view1, view2;
	var orderType;
	var isCopy;
	
	$(function(){
		navPath = $('#navPath');
		view1 =	$('#view1');
		view2 =	$('#view2');
		navPath.find('a').click(function(){
			view1.show();
			view2.hide();
			navPath.hide();			
		})
		
		$('#orderType1').click(function(){
			orderType = 1;
			view1.hide();
			view2.show();	
			navPath.show();
			bindMenus();
		});
		$('#orderType2').click(function(){
			orderType = 2;
			submit();
		});
		
		menuList = $('#menuList');
		
		
		
		dlgCreateOrder = $('#dlgCreateOrder');
		dlgEditMenu = $('#dlgEditMenu');
		dlgEditDish = $('#dlgEditDish');
		
		dlgCreateOrder.find('.save').click(createOrder);
		dlgCreateOrder.find('.cancel').click(function(){
			dlgCreateOrder.dialog('close');
		});
		dlgEditMenu.find('.save').click(editMenu);
		dlgEditMenu.find('.cancel').click(function(){
			dlgEditMenu.dialog('close');
		});
		dlgEditDish.find('.save').click(function(){
			editDish(false);
		});
		dlgEditDish.find('.continue').click(function(){
			editDish(true);
		});
		dlgEditDish.find('.cancel').click(function(){
			dlgEditDish.dialog('close');
		});
		dlgEditDish.find('.price, .name').keypress(function(e){
			if (e.keyCode === 13){
				editDish(e.ctrlKey);
			}
		})
		
		var btnCreateMenu = $('#btnCreateMenu');
		btnCreateMenu.show();
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
		});	
	})
	
	function bindMenus(){		
		$.getJSON('/menu/list',{}, function(data){	
			menuList.children().empty();
			$(data.rows).each(function(i, menu){
				bindMenu(i, menu._id);
			});
		});
	}
	function bindMenu(i, menuId){
		var cMenu = $('<div class="menuBlock"/>').appendTo(menuList.children().get(i%3));
		
		cMenu.click(function(e){
			if(e.target.tagName!='A'){
				$('.menuBlock').removeClass('selected');
				cMenu.addClass('selected');
				selectedMenuId = menuId;
				submit();
			}
		});
		
		$.getJSON('/menu/detail',{id:menuId}, function(data){
			var cMenuHead = $('<div class="head"/>').appendTo(cMenu);
			bindMenuHead(cMenuHead, data.menu);
			
			var divDishes = $('<div class="list"/>').appendTo(cMenu);
			var tableDishes = $('<table />').appendTo(divDishes);
			var cDishes = $('<tbody/>').appendTo(tableDishes);
			bindDishes(cDishes, data);	
		});	
	}
	function bindMenuHead(cMenuHead, dMenuHead){	
		cMenuHead.empty();
		var l1= $('<div />').appendTo(cMenuHead);
		l1.text('菜单名：'+dMenuHead.name);
		
		var btns = $('<div style="float:right"/>').appendTo(l1);
		var btnEdit = $('<a href="javascript:void(0)" class="linkBtn1">编辑</a>').appendTo(btns);
		btnEdit.click(function(){
			isCopy = false;
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
		});
		var btnCopy = $('<a href="javascript:void(0)" class="linkBtn1">复制</a>').appendTo(btns);
		btnCopy.click(function(){
			isCopy = true;
			dlgEditMenu.find('.name').val(dMenuHead.name).select();
			dlgEditMenu.find('.phone').val(dMenuHead.contact.phone);
			dlgEditMenu.find('.address').val(dMenuHead.contact.address);
			curMenuData = dMenuHead;	
			dlgEditMenu.show();
			dlgEditMenu.dialog({
				modal : true,
				title : "复制菜单"
			});		
		});
		if(identity.isAdmin){
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
			});
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
		});
		
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
		});
	}
	
	function bindDish(cDish, dDish){
		cDish.empty();
		var td1 = $('<td />').appendTo(cDish);
		td1.text(dDish.name);
		var td2 = $('<td />').appendTo(cDish);
		td2.text(dDish.price);
		var td3 = $('<td />').appendTo(cDish);
		
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
		});
		var btnDel = $('<a href="javascript:void(0)" class="linkBtn1">删除</a>').appendTo(td3);
		btnDel.click(function(){
			cDish.remove();
			$.postJSON('/dish/delete',{'id':dDish._id}, function(){
				$.messagelabel.show('已成功删除菜品')
			});	
		});
		
	}
	
	
	function submit(){
		if(orderType===2 || selectedMenuId){
			var name = $.getDateString();
			if(orderType===1){
				name += '快餐';
			}else{
				name += '小炒AA';
			}
			dlgCreateOrder.find('.name').val(name);
			dlgCreateOrder.show();
			dlgCreateOrder.dialog({
				modal : true,
				title : "发起饭事"
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
			orderType:orderType,
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
			if(isCopy){
				menuData['ids'] = [curMenuData._id];
				$.postJSON('/menu/copy', menuData,
					function(){
						bindMenus();
						$.messagelabel.show('成功提交！');
					});
				isCopy = false;
			}else{
				$.extend(curMenuData, menuData, {id:curMenuData['_id']})
				$.postJSON('/menu/edit', curMenuData,
					function(){
						curMenuData.contact = {phone:menuData.phone, address:menuData.address};
						bindMenuHead(curMenuHead,curMenuData);
						$.messagelabel.show('成功提交！');
					});
			}
		}
		else{			
			$.postJSON('/menu/create', menuData,
				function(data){
					bindMenus();
					$.messagelabel.show('成功提交！');
				})
		}
	}
	function editDish(conti){
		if(!conti){
			dlgEditDish.dialog('close');
		}
		if(curDishData){
			$.extend(curDishData, {name:dlgEditDish.find('.name').val(), 
				price:dlgEditDish.find('.price').val(), id:curDishData['_id']})
			$.postJSON('/dish/edit', curDishData,
				function(data){
					bindDish(curDishC,data);
					$.messagelabel.show('成功提交！');
				})		
		}
		else{
			var dd = {name:dlgEditDish.find('.name').val(), 
				price:dlgEditDish.find('.price').val(), 'menuId': curMenuId};
			
			$.postJSON('/dish/create',dd,
				function(data){
					var tr = $('<tr />').appendTo(curMenuDishList);
					bindDish(tr, data);
					$.messagelabel.show('成功提交！');
				})
		}
		dlgEditDish.find('.name').val('').focus();
		dlgEditDish.find('.price').val('');
	}
	
	window.refreshMenuList = function(){
		bindMenus();
	}
	
	

})(jQuery);



















