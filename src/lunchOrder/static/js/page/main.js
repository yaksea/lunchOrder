(function($) {
	var phGroupList;
	
	$(function(){
		if(identity.groupId){
			bindGroupList();
		}
	});
	
	function bindGroupList(){
		phGroupList = $('#phGroupList');
		phGroupList.show();
		var container = $('<div class="menu_dropdown" />').appendTo(phGroupList);
		var aCur = $('<a />').appendTo(container);
		aCur.text('当前群组:'+identity.groupName);
		var ul = $('<ul />').appendTo(container);
		var lastLi = null;
		
		$.getJSON('/group/MyGroups',{'cached':true}, function(data){
			$.each(data.rows, function(i, row){
				if(row.groupId===identity.groupId){
					return true;
				}
				var li = $('<li />');
				if(!lastLi){
					li.prependTo(ul);
				}else{
					li.insertAfter(lastLi);
				}
				lastLi = li;
				var a =  $('<a />').appendTo(li);
				a.text(row.groupName);
				a.click(function(){
					$.postJSON('/user/SwitchGroup',{'groupId':row.groupId},function(){
						$.messagelabel.show('切换身份成功。正在刷新页面...');
						location.href = location.href;
					});
				});
			});
			if(lastLi){
				lastLi.addClass('breakdown');
			}
		});
		var li1 =  $('<li />').appendTo(ul);
		var a1 = $('<a />').appendTo(li1);
		a1.attr('href', '/group/join');
		a1.text('查看更多群');
		var li2 =  $('<li />').appendTo(ul);
		var a2 = $('<a />').appendTo(li2);
		a2.attr('href', '/group/create');
		a2.text('自己创建一个群');
		
		
	}

})(jQuery);



















