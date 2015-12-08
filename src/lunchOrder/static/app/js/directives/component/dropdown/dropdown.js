/* ========================================================================
 * Bootstrap: dropdown.js v3.2.0
 * http://getbootstrap.com/javascript/#dropdowns
 * ========================================================================
 * Copyright 2011-2014 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * ======================================================================== */


+function ($) {
    var Dropdown = function (target, options) {
        if(!target){
            return;
        }

        var options = $.extend({}, $.fn.dropdown.defaults, $.fn.dropdown.parseOptions(target),
            typeof(options)==='string'?{}:options);

        options.onBound && target.bind('bound.dropdown', options.onBound);
        options.onChange && target.bind('change.dropdown', options.onChange);
        options.onVal && target.bind('val.dropdown', options.onVal);

        if(target.prop('tagName')==='SELECT' && !options.data){
            var data = {};
            target.children().each(function(i, option){
                var op = $(option);
                var txt = op.text();
                var v = op.prop('value') || txt;
                data[v] = txt;
                if(op.prop('checked')){
                    options.value = v;
                }
            });
            options.data = data;
        }
        target.hide();
        var self = this;
        this.target = target;
        var orgValue, curValue;
        var openVal;
        var textField = options.textField;
        var valField = options.valField;

        var label = this.label = $('<div class="dropdown" />').insertBefore(target);
        label.css('width', options.width);
        var labelText = this.labelText = $('<div class="dropdown-labelText" />').appendTo(label);
        var caret = this.caret = $('<span class="dropdown-caret" />').appendTo(label);
        var panel = this.panel = $('<div class="dropdown-panel"/>').appendTo('body');
        panel.css('width', options.width+4);
        var pnlList = this.pnlList = $('<ul class="dropdown-pnlList" />').appendTo(panel);

        this.status = 0; //0:collapsed 1: expanded
        this.selectedRow = null;

        this.label.mousedown(function(){
            return false;
        });
        this.panel.mousedown(function(){
            return false;
        });

        this.toggle = function(){
            if(self.status){
                self.collapse();
            }else{
                self.expand();
            }
        }
        this.label.click(function(){
            self.toggle();
//		return false;
        });
        this.getObj = function(){
            return self;
        }
        this.locatePanel = function(){
            var top = label.offset().top + label.outerHeight();
            panel.css({
                left : label.offset().left,
                top : top,
                display:'block'
            });
        }
        this.collapse = function(){
            label.removeClass('focus');
            self.panel.hide();
            self.status = 0;
            if(curValue!=openVal){
                target.trigger('change_apply.dropdown', [curValue, openVal]);
                openVal = curValue;
            }
        }
        this.expand = function(){
            label.addClass('focus');
            self.locatePanel();
            this.focusRow(self.selectedRow);
            self.status = 1;
            openVal = curValue;
        }
        this.applyChange = function(eventHandler){
            eventHandler && target.bind('change_apply.dropdown', eventHandler);
        }
        this.bind = function(data){
            options.data = data = data || options.data;
            self.pnlList.empty();
            self.selectedRow = null;
            if(!data){
                return;
            }
            $.each(data, function(i, item){
                var li = $('<li />').appendTo(self.pnlList);
//			var v = i;
                var text = textField? item[textField] : item;
                var v = valField?item[valField]:
                    typeof(i)==='number' ? text: i;

                li.text(text);
                li.attr('val', v);
                li.mouseover(function(){
                    self.focusRow(li);
                });
                li.click(function(){
                    self.val(li);
                    self.collapse();
                    return false;
                });
            });
            this.val(options.value);
        }
        this.focusRow = function(li){
            self.pnlList.children().removeClass('selected');
            li && li.addClass('selected');
        }
        this.selectNext = function(){
            var nextRow = this.selectedRow.next();
            if(nextRow.length){
                this.focusRow(nextRow);
                this.val(nextRow);
            }
        }
        this.selectPrev = function(){
            var prevRow = this.selectedRow.prev();
            if(prevRow.length){
                this.focusRow(prevRow);
                this.val(prevRow);
            }
        }
        this.change = function(eventHandler){
            eventHandler && target.bind('change.dropdown', eventHandler);
        }
        this.val = function(value){
            if(typeof(value)==='undefined'){
                return curValue;
            }else{
                if(typeof(value)==='object'){
                    self.selectedRow = value;
                }else{
                    var row = self.pnlList.children('[val='+value+']');
                    if(row.length){
                        self.selectedRow = row.eq(0);
                    }
                }
                if(!self.selectedRow){
                    self.selectedRow = self.pnlList.children(':first');
                }
                curValue = self.selectedRow.attr('val');
                if(orgValue!=curValue){
                    if(typeof(orgValue)==='undefined'){
                        target.trigger('bound.dropdown', curValue);
                    }else{
                        target.trigger('change.dropdown', [curValue, orgValue]);
                    }
                    target.trigger('val.dropdown', [curValue, orgValue]);
                    orgValue = curValue;
                    //
                    var text;
                    if(valField){
                        text = $.grep(options.data, function(item, i){
                            return item[valField]==curValue;
                        });
                        text = text.length ? text[0] : null;
                    }else{
                        text = options.data[curValue] || curValue;
                    }
                    this.text(textField? text[textField] : text);
                }
            }
        }
        function triggerChange(){
        }
        this.text = function(text){
            if(typeof(text)==='undefined'){
                return this.labelText.text();
            }else{
                this.labelText.text(text);
            }
        },

            $(window).resize(function() {
                if(self.status){
                    self.locatePanel();
                }
            });
        $(document).bind('keydown.dropdown', function(e){
            if(!self.status){
                return;
            }
            switch (e.which) {
                case 27: // esc
                    self.collapse();
                    return false;
                    break;
                case 37: // left
                    self.selectPrev();
                    return false;
                    break;
                case 38: // up
                    self.selectPrev();
                    return false;
                    break;
                case 39: // right
                    self.selectNext();
                    return false;
                    break;
                case 40: // down
                    self.selectNext();
                    return false;
                    break;
                case 13: // enter
                    self.collapse();
                    return false;
                    break;
            }
        }).bind('click.dropdown', function(e){
            if($(e.target).closest(label).length){
                return;
            }
            self.status && self.collapse();
        });

        target.data('dropdown-obj', this);
        this.bind();
    }

    $.fn.dropdown =  function(options) {
        var target = $(this[0]);
        var obj  = target.data('dropdown-obj');

        if (!obj) {
            obj = new Dropdown(target, options);
        }
        if (typeof options === 'string') {
            var attr = obj[options];
            if(attr && typeof(attr)==='function'){
                return attr.apply(obj, Array.prototype.slice.call(arguments, 1));
            }
        }
        return obj;
    }
    $.fn.dropdown.defaults = {
        data : null, //[] or {}
        value : null,
        textField : '',
        valField : '',
        width: 200, //px
        onBound: function(){}, //初始化绑定数据后
        onChange: function(){}, //值变后
        onVal: function(){} //值设置后，=onBound+onChange
    };
    $.fn.dropdown.parseOptions = function(target){
        var width = target.width()||200;
        return {width:width};
    }
}(jQuery);
