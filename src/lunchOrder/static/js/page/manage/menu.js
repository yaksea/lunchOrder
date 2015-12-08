(function($) {
	var menuList, noSelected, pnlSelected, btnSubmit;
	var selectedMenus = {};
	
	$(function(){
		menuList = $('#menuList');
		noSelected = $('#noSelected');
		pnlSelected = $('#pnlSelected');
		btnSubmit = $('#btnSubmit');
		bindMenus();
		
		btnSubmit.click(function(){
			btnSubmit.prop('disabled', true);
			$.postJSON('/menu/copy', {'ids':Object.keys(selectedMenus)}, function(){
				btnSubmit.prop('disabled', false);
				window.opener.refreshMenuList();
				$.messagelabel.show('已复制完成，将要关闭窗口...');
				setTimeout(function(){
					window.close();
				}, 2000);
			});
		});
	})
	
	function bindMenus(){		
		$.getJSON('/menu/alllist',{}, function(data){		
			countMenu = data.rows.length;
			$(data.rows).each(function(i, menu){
				bindMenu(i, menu._id);
			});
		});
	}
	function bindMenu(i, menuId){
		var cMenu = $('<div class="menuBlock"/>').appendTo(menuList.children().get(i%3));
		
		cMenu.click(function(e){
			if(e.target.tagName!='A'){
				if(selectedMenus[menuId]){
					cMenu.removeClass('selected');
					delete selectedMenus[menuId];
				}else{
					selectedMenus[menuId] = 1;
					cMenu.addClass('selected');
				}
				bindCount();
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
	}
	
	function bindDish(cDish, dDish){
		cDish.empty();
		var td1 = $('<td />').appendTo(cDish);
		td1.text(dDish.name);
		var td2 = $('<td />').appendTo(cDish);
		td2.text(dDish.price);
		var td3 = $('<td />').appendTo(cDish);
	}
	
	function bindCount(){
		var count = Object.keys(selectedMenus).length;
		if(!count){
			noSelected.show();
			pnlSelected.hide();
		}else{
			noSelected.hide();
			pnlSelected.show();
			$('#countSelected').text(count);
		}
	}
	

})(jQuery);



















