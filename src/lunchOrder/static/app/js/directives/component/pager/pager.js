(function($) {
	$.Pager = function(target, options) {
		var options = $.extend({}, $.fn.pager.defaults, typeof options === 'string'?{}:options);
		
		var self = this;
		this.pageIndex = 0;
		this.total = 0;
		this.pages = 0;
		
		target.addClass('pager');
		var controls =  $('<div class="pager-controls" />').appendTo(target)
		var btnPrev = $('<button class="pager-prev pager-block" />').appendTo(controls).text('上一页');
		var pl = $('<div class="pager-list pager-block" />').appendTo(controls);
		var btnNext = $('<button class="pager-next  pager-block" />').appendTo(controls).text('下一页');
		var ps = $('<div class="pager-split  pager-block" />').appendTo(controls);
		var txtGo = $('<input type="text" />').appendTo(ps);
		var txtPages =  $('<span  />').appendTo(ps.append('/'));
		
		var pt = $('<div class="pager-total pager-block" />').appendTo(target);
		
		txtGo.keypress(function(e){
			if(e.which===13){
				var pi = parseInt($(this).val());
				if(pi>self.pages){
					pi = self.pages;
				}else if(pi<1){
					pi = 1;
				}
				self.pageIndex = pi-1;
				options.onChange(self.pageIndex);
				self.render(self.pageIndex);	
				this.select();
			}
		}).click(function(){
			this.select();
		});
		
		btnNext.click(function(){
			self.pageIndex++;
			options.onChange(self.pageIndex);
			self.render(self.pageIndex);			
		});
		btnPrev.click(function(){
			self.pageIndex--;
			options.onChange(self.pageIndex);
			self.render(self.pageIndex);			
		});
		
		this.render = function(pageIndex, total){ //total可选
			pl.empty();
			if(typeof(total)==='number'){
				this.total = total;
			}
			var total = this.total;
			if(total===9999){
				pt.text('共9999+条记录');
			}else{
				pt.text('共'+total+'条记录');
			}
			this.pageIndex = pageIndex = pageIndex||0;
			var pages = Math.ceil(total/options.pageSize);
			this.pages = pages;
			if(pages<=1){
				controls.hide();
				return;
			}
			controls.show();
			txtPages.text(pages);
			txtGo.numberbox({min:1,max:pages});
			txtGo.val(self.pageIndex+1)
			var multi = pages>10;
			
			if(multi){
				if(pageIndex<10){
					for(var i=0;i<10;i++){
						_renderButton(i);
					}
					_renderButton(10, '...');
					_renderButton(pages-1);
					
				}else if(pageIndex>=pages-10){
					_renderButton(0);
					_renderButton(pages-11, '...');
					for(var i=0;i<10;i++){
						_renderButton(pages-10+i);
					}
				}else{
					_renderButton(0);
					_renderButton(pageIndex-4, '...');
					for(var i=0;i<8;i++){
						_renderButton(pageIndex-3+i);
					}
					_renderButton(pageIndex+5, '...');
					_renderButton(pages-1);
				}
			}else{
				for(var i=0;i<pages;i++){
					_renderButton(i);
				}
			}
			btnPrev.removeProp('disabled');
			btnPrev.removeClass('disabled');
			btnNext.removeProp('disabled');
			btnNext.removeClass('disabled');
			if(pageIndex===0){
				btnPrev.attr('disabled', 'disabled');
			}else if(pageIndex===pages-1){
				btnNext.attr('disabled', 'disabled');
			}
			function _renderButton(index, text){
				var li = $('<div />').appendTo(pl);
				if(text){
					li.text(text);
				}else{
					li.text(index+1);
				}
				if(index===pageIndex){
					li.addClass('selected');
				}
				li.click(function(){
					pl.find('.selected').removeClass('selected');
					li.addClass('selected');
					self.pageIndex = index;
					options.onChange(index);
					self.render(index, total);
				});
				
			}
			
		}
		
		target.data('pager-obj', this);
		this.target = target; //jquery obj
		this.options = options;
		
	};
	
	$.fn.pager  = function(options) {
		var target = $(this[0]);
		var obj = target.data('pager-obj');
		if(!obj){
			obj = new $.Pager(target, options);
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
	$.fn.pager.defaults = {
		onChange :function(pageIndex){},//pageIndex: 0起始 
		pageSize : 20
	};
		
})(jQuery);
