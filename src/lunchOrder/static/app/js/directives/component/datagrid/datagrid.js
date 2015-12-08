(function($) {
	$.DataGrid = function(target, options) {
		var options = $.extend({}, $.fn.dataGrid.defaults, typeof options === 'string'?{}:options);
		
		var self = this;
		var columns = [];
		var columnSettings = {};
		var thead = target.find('thead');
		var tbody = $('<tbody />').appendTo(target);
		var sort, order=-1;//order:-1降，1升
		options.onSort && target.bind('sort.datagrid', options.onSort);
		options.onSelected && target.bind('selected.datagrid', options.onSelected);
		options.rowSelectable && options.singleSelect && (options.checkbox=false);
		
		this.parseColumnSettings = function(){
			thead.find('th').each(function(i, th){
				var th = $(th);
				var opts = th.data();
				var fieldName = opts.field||('NONAME_'+i);
				columns.push(fieldName);
				columnSettings[fieldName] = opts;
				if(opts.width){
					th.css('width',opts.width);
				}
				if(opts.sortable){
					th.click(function(e){
						if(fieldName==sort){
							order = order==-1? 1: 
								order==1?0:-1;
							if(order===0){
								sort='';
							}
						}
						else{
							sort = fieldName;
							order = -1;
						}
						thead.removeClass('sortAsc').removeClass('sortDesc');
						if(order==1){
							th.addClass('sortAsc');
						}
						else if(order==-1){
							th.addClass('sortDesc');
						}
						target.trigger('sort.datagrid', [sort, order]);
					});
				}
			});
		};
		this.parseColumnSettings();
		if(options.checkbox){
			var th = $('<th style="width:20px;"  />').insertBefore(thead.find('th:first'));
			var cb = $('<input type="checkbox" class="dataGrid-checkbox" />').appendTo(th);
			cb.click(function(){
					if($(this).prop('checked')){
						tbody.find('tr').addClass('selected');
						tbody.find('.dataGrid-checkbox').prop('checked', true);
					}else{
						tbody.find('tr').removeClass('selected');
						tbody.find('.dataGrid-checkbox').prop('checked', false);
					}				
			});
		}
		
		this.bind = function(rows){
			if(rows){
				tbody.empty();
				tbody.hide();
				thead.find('.dataGrid-checkbox').prop('checked', false);
				$.each(rows, function(i,row){
					self.addRow(row);
				});
				tbody.show();
			}
		};
		this.addRow = function(row, insert){
			var tr = $('<tr />');
			insert ? tr.prependTo(tbody) : tr.appendTo(tbody);
			tr.attr('id', 'tr_'+row._id);
			buildTr(tr, row);
		};
		this.updateRow = function(row){
			var tr = $('#tr_'+row._id);
			tr.empty();
			buildTr(tr, row);
		};
		this.delRows = function(ids){
			$.each(ids, function(i, id){
				$('#tr_'+id).remove();
			});
		};
		this.hideRows = function(ids, delay){
			$.each(ids, function(i, id){
				$('#tr_'+id).hide(delay || 'slow');
			});
		};
		
		this.rowsLen = function(){
			return tbody.children().length;
		};
		this.getSelectedIds = function(){
			var ids = [];
			tbody.find('tr.selected').each(function(i, tr){
				ids.push(tr.id.substr(3));
			});
			return ids;
		};
		this.sort = function(eventHandler){
			eventHandler && target.bind('sort.datagrid', eventHandler);
		};
		this.rowSelected = function(eventHandler){
			eventHandler && target.bind('rowSelected.datagrid', eventHandler);
		};
		function buildTr(tr, row){
			if(options.checkbox){
				var td = $('<td style="text-align:center;padding:0px;" />').appendTo(tr);
				var cb = $('<input type="checkbox" class="dataGrid-checkbox" />').appendTo(td);
				function check(){
					if(cb.prop('checked')){
						tr.addClass('selected');
					}else{
						tr.removeClass('selected');
						thead.find('.dataGrid-checkbox').prop('checked', false);
					}
				}
				cb.click(function(e){
					check();
					e.stopPropagation();
				});
				if(options.rowCheckable){
					tr.click(function(){
						cb.prop('checked', !cb.prop('checked'));
						check();
						return false;
					});
				}
			}
			if(options.rowSelectable){
				tr.click(function(){
					if(options.singleSelect){
						tbody.find('tr.selected').removeClass('selected');
						tr.addClass('selected');
					}else{
						if(tr.hasClass('selected')){
							tr.removeClass('selected');
						}else{
							tr.addClass('selected');
						}
					}
					if(options.singleSelect){
						console.info(tr[0].id.substr(3))
						target.trigger('rowSelected.datagrid', [tr[0].id.substr(3), row]);
						
					}else{
						target.trigger('rowSelected.datagrid', [this.getSelectedIds()]);
					}
					return false;
				});
			}
			$.each(columns, function(i, fn){
				var td = $('<td />').appendTo(tr);
				var opts = columnSettings[fn];
				if(opts.width){
					td =  $('<div />').appendTo(td);
					td.css('width', opts.width);
					td.addClass('datagrid-ellipsis');
				}
				if(opts.align){
					td.css('textAlign', opts.align);
				}
				
				var parser = options.parsers[opts.parser];
				if((options.checkbox && options.rowCheckable)||options.rowSelectable){
					td.on('click', ':nth-child(n)', function(e){
						e.stopPropagation();
					});
				}				
				if(fn.indexOf('NONAME_')===0){
					parser && parser(tr, td, row);
					return true;
				}
				var fieldValue = row[fn];
				if(fieldValue===undefined && fn.indexOf('.')>0){
					var na = fn.split('.');
					var xv = row;
					$.each(na, function(i, ns){
						if(i===na.length-1){
							fieldValue = xv[ns];
							return false;
						}
						xv = xv[ns];
						if(xv===undefined){
							fieldValue = undefined;
							return false;
						}
					});						
				}
				parser ? parser(tr, td, row, fieldValue) : td.text((fieldValue===undefined||fieldValue===null)?
																(columnSettings[fn]['default']||'') : fieldValue);
			});		
		}
		options.dataRows && this.bind(options.dataRows);
		
		this.target = target; //jquery obj
		this.options = options;
		
	};
	
	
	$.DataGrid.prototype = {

	};
	$.fn.dataGrid  = function(options) {
		var target = $(this[0]);
		var obj = target.data('dataGrid-obj');
		if(!obj){
			obj = new $.DataGrid(target, options);
		}
		target.data('dataGrid-obj', this);
		if (typeof options === 'string') {
			var attr = obj[options];
			if(attr){
				if(typeof(attr)==='function'){
					return attr.apply(obj, Array.prototype.slice.call(arguments, 1));
				}
				return attr;
			}
		}
		else{
			
			return obj;
		}

	};
	$.fn.dataGrid.defaults = {
		parsers : {}, //parser格式：  function(tr, td, rowData, fieldValue)
		dataRows : [],
		checkbox: true,
		rowCheckable: true, //点行时选中checkbox
		rowSelectable: true, //点行时选中行
		singleSelect: true, //单选选中行
		onSort:function(e, sort, order){},
		onRowSelected:function(e, rowIds){}
	};
		
})(jQuery);
