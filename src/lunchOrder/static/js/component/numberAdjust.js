(function($) {
	
	$.NumberAdjust = function(target, options) {
		var options = $.extend({}, $.fn.numberAdjust.defaults, typeof options === 'string'?{}:options);
				
		var instance = this;
		this.target = target; //jquery obj
		this.options = options;
		this.value = options.value;

		var container = $('<div class="numberAdjust" />').insertAfter(target);
		var btnMinus = $('<a href="javascript:void(0)" class="minus">-</a>').appendTo(container);
		target.addClass("numCount").appendTo(container);
		target.val(this.value);
		if(options.noBorder){
			target.addClass("noBorder");
		}
		var btnAdd = $('<a href="javascript:void(0)" class="plus">+</a>').appendTo(container);
		btnMinus.click(function(){
			instance.value --;
			if(instance.value<0){
				instance.value = 0;
			}
			target.val(instance.value);
			options.change(instance.value);
		});
		btnAdd.click(function(){
			instance.value ++;
			target.val(instance.value);
			options.change(instance.value);
		});
		target.focus(function(){
			target.select();
		})
		target.change(function(){
			instance.value =  parseInt(target.val()) || 0;
			if(instance.value<0){
				instance.value = 0;
			}			
			target.val(instance.value);
			options.change(instance.value);
		});
		target.keypress(function(e){
			if((e.which >= 48 && e.which <= 57) || e.which == 0 || e.which == 8){
				return true;
			}
			return false;
		});
	
		this.btnAdd = btnAdd;
		this.btnMinus = btnMinus;
		this.container = container;
		if(options.showAlways){
			this.hover();
		}
		
		target.data('numberAdjust-obj', this);
	};
	$.NumberAdjust.prototype = {
		setValue:function(value){
			this.value =  parseInt(value) || 0;
			this.target.val(this.value);			
		},
		getValue : function() {			
			return this.value;
		},
		hover : function(){
			this.btnAdd.css({display:'inline-block'});
			this.btnMinus.css({display:'inline-block'});
			if(this.options.noBorder){
				this.target.removeClass("noBorder");
			}
		},
		out : function(){
			this.btnAdd.hide();
			this.btnMinus.hide();
			if(this.options.noBorder){
				this.target.addClass("noBorder");
			}
		},
		show : function(){
			this.container.show();
		},
		hide : function(){
			this.container.hide();
		}
	};

	$.fn.numberAdjust  = function(options) {
		var target = $(this[0]);
		var obj = target.data('numberAdjust-obj');
		if(!obj){
			obj = new $.NumberAdjust(target, options);
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
	$.fn.numberAdjust.defaults = {
		change : function(value){},
		value : 0,
		noBorder : false,
		showAlways : false
	};
})(jQuery);
