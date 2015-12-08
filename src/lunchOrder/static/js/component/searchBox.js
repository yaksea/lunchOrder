/**
 * panel - jQuery EasyUI
 * 
 * Licensed under the GPL: http://www.gnu.org/licenses/gpl.txt
 * 
 * Copyright 2010 stworthy [ stworthy@gmail.com ]
 * 
 */
(function($) {
	$.SearchBox = function(target, options){
		var options = $.extend({}, $.fn.searchBox.defaults,
				$.fn.searchBox.parseOptions(target), typeof options === 'string'?{}:options);
		this.target = target.hide(); //jquery obj
		var instance = this;
		this.target = target; //jquery obj
		this.target.click(function(){
			instance.target.val('');
			
		});
		this.options = options;
		this.label = $('<div class="searchBox-label" />').insertAfter(target);
		this.label.css('width', options.width);
		this.panel = $('<div class="searchBox-panel"/>').appendTo('body');
		this.panel.css('width', options.width);
		
		this.label.mousedown(function(){
			return false;
		});
		this.panel.mousedown(function(){
			return false;
		});
		
		this.status = 0; //0:collapsed 1: expanded
		this.label.click(function(){
			if(instance.status){
				instance.collapse();
			}else{
				instance.expand();
			}
			
		});
		
		this.pnlSearch = $('<div class="searchBox-pnlSearch" />').appendTo(this.panel);
		this.txtSearch = $('<input class="searchBox-txtSearch" placeholder="输入关键字进行查找" />').appendTo(this.pnlSearch);
		this.txtSearch.placeholder();
		this.txtSearch.css('width', options.width-20);
		
		this.btnClear = $('<div style="display:none" class="searchBox-btnClear" />').appendTo(this.pnlSearch);
		this.txtSearch.keyup(function(e){
			if((e.keyCode>=37&&e.keyCode<=40)){
				return false;
			}
			switch (e.keyCode) {
				case 13: // enter
					instance.selectRow();
					break;
				case 27: // esc
					instance.clear();
					break;					
				default:
					var $this = $(this);
					if($this.val().length){
						instance.btnClear.show();
					}
					else{
						instance.btnClear.hide();
					}
					instance.filter();
					break;
				}
				return false;			
		});
		this.txtSearch.keydown(function(e){
			switch (e.keyCode) {
				case 27: // esc
					if(!instance.txtSearch.val()){
						instance.collapse();
					}
					break;
				case 37: // left
					instance.selectPrev();
					break;
				case 38: // up
					instance.selectPrev();
					break;
				case 39: // right
					instance.selectNext();
					break;
				case 40: // down
					instance.selectNext();
					break;
			}
		});
		instance.btnClear.click(function(){
			instance.clear();
		});
		instance.filter();
		this.pnlList = $('<ul class="searchBox-pnlList" />').appendTo(this.panel);
		
		target.data('searchBox-obj', this);
		
		
		$(document).bind("mousedown.SearchBox", function(e) {
			instance.collapse();
		});;

		$(window).resize(function() {
			if(instance.status){
				instance.locatePanel();
			}
		});
	};
	$.SearchBox.prototype = {
		getValue: function(){
			return this.target.val();
		},
		getText: function(){
			return this.label.text();
		},
		setValue: function(value, text){
			this.target.val(value);
			if(text){
				this.label.text(text);
			}
		},
		setText: function(text){
			this.label.text(text);
		},
		expand : function(){
			this.locatePanel();
			this.txtSearch.focus();
			this.status = 1;
		},
		locatePanel : function(){
			var panel = this.panel;
			var label = this.label;
			var top = label.offset().top + label.outerHeight();
			panel.css({
				left : label.offset().left,
				top : top-4,
				display:'block'
			});	
		},
		collapse : function(){
			this.panel.hide();
			this.status = 0;
		},
		selectRow : function(){
			this.setValue(this.focusedRow.attr('val'), this.focusedRow.text());
			this.clear();
			this.collapse();			
		},
		selectPrev : function(){
			var prevRow = this.focusedRow.prev();
			if(prevRow.length){
				this.focusedRow.removeClass('selected');
				prevRow.addClass('selected');
				this.focusedRow = prevRow;
			}
			if(this.focusedRow.position().top<36){
				this.pnlList.scrollTop(this.pnlList.scrollTop()+this.focusedRow.position().top-36);
			}			
		},
		selectNext: function(){
			var nextRow = this.focusedRow.next();
			if(nextRow.length){
				this.focusedRow.removeClass('selected');
				nextRow.addClass('selected');
				this.focusedRow = nextRow;
			}
			if(this.focusedRow.position().top>200){
				this.pnlList.scrollTop(this.pnlList.scrollTop()+this.focusedRow.position().top-200);
			}
		},
		filter : function(){
			var instance = this;
			var kw = this.txtSearch.text();
			$.postJSON(this.options.dataUrl, {q:instance.txtSearch.val(), l:instance.options.rows}, function(data){
				instance.pnlList.empty();
				var rows = data[instance.options.dataList];
				instance.totalRows = rows.length;
				$(rows).each(function(i, row){
					var li = $('<li />').appendTo(instance.pnlList);
					if(i==0){
						instance.focusedRow = li;
						li.addClass('selected');
					}
					li.text(row[instance.options.textField]);
					li.attr('val', row[instance.options.valueField]);
					li.mouseover(function(){
						instance.focusedRow.removeClass('selected');
						li.addClass('selected');					
						instance.focusedRow = li;
					});
					li.click(function(){
						instance.selectRow();
					});
				});
				if(!rows){
					instance.focusedRow = null;
				}
				instance.pnlList.scrollTop(0);
			});
		},
		clear : function(){
			this.txtSearch.val('');
			this.txtSearch.focus();
			this.filter();
			this.btnClear.hide();
		}
	};
	
	$.fn.searchBox = function(options) {
		var target = $(this[0]);
		var obj = target.data('searchBox-obj');
		if(!obj){
			obj = new $.SearchBox(target, options);
		}
		
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
	$.fn.searchBox.parseOptions = function(target) {
		return {
			id : target.prop("id")
		};
	};
	$.fn.searchBox.defaults = {
		title : null,
		dataUrl : '',
		dataList : 'rows', //如为[]数组则不使用dataUrl，如为‘’字符串则表示dataUrl返回的字段名，比如"rows"
		textField : '',
		valueField : '',
		rows: 20,
		width: 200 //px
	};
})(jQuery);
