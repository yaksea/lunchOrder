(function($) {
	var rules = {
			url : {
				validator : function(value) {
					return /(((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:)*@)?(((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?)(:\d*)?)(\/((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)?)?(\?((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|[\uE000-\uF8FF]|\/|\?)*)?(\#((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|\/|\?)*)?$/i
							.test(value);
				},
				message : 'Please enter a valid URL.'
			},
			isLaterToday : {
				validator : function(value, params) {
					var date = $.fn.datebox.defaults.parser(value);
					return date > new Date();
				},
				message : 'The date is not later than today'
			},
	
			minLength : { // 判断最小长度
				validator : function(value, params) {
					value = $.trim(value); // 去空格
					
					return value.length >= params[0];
				},
				message : '最少输入 {0} 个字符。'
			},
			length : {
				validator : function(value, params) {
					var len = $.trim(value).length;
					return len >= params[0] && len <= params[1];
				},
				message : "输入内容长度必须介于{0}和{1}之间."
			},
			phone : {// 验证电话号码 支持手机号码
				validator : function(value) {				
					return /^[\+]?[0-9,-]+$/.test(value);
				},
				message : '格式不正确(例+86-021-88888888,12)'
			},
			mobile : {// 验证手机号码
				validator : function(value) {
					return /^(13|15|18|14|17)\d{9}$/i.test(value);
				},
				message : '请输入真实的手机号码'
			},
			idcard : {// 验证身份证
				validator : function(value) {
					return /^\d{15}(\d{2}[A-Za-z0-9])?$/i.test(value);
				},
				message : '身份证号码格式不正确'
			},
			intOrFloat : {// 验证整数或小数
				validator : function(value) {
					return /^\d+(\.\d+)?$/i.test(value);
				},
				message : '请输入数字，并确保格式正确'
			},
			currency : {// 验证货币
				validator : function(value) {
					return /^\d+(\.\d+)?$/i.test(value);
				},
				message : '货币格式不正确'
			},
			CHS : {
				validator : function(value, params) {
					return /^[\u0391-\uFFE5]+$/.test(value);
				},
				message : '请输入汉字'
			},
			qq : {// 验证QQ,从10000开始
				validator : function(value) {
					return /^[1-9]\d{4,9}$/i.test(value);
				},
				message : 'QQ号码格式不正确'
			},
			integer : {// 验证整数
				validator : function(value) {
					// alert(value)
					return /^[+]?[1-9]+\d*$/i.test(value);
				},
				message : '请输入整数'
			},
			chinese : {// 验证中文
				validator : function(value) {
					return /^[\u0391-\uFFE5]+$/i.test(value);
				},
				message : '请输入中文'
			},
			english : {// 验证英语
				validator : function(value) {
					return /^[A-Za-z]+$/i.test(value);
				},
				message : '请输入英文'
			},
			unnormal : {// 验证是否包含空格和非法字符
				validator : function(value) {
					return /.+/i.test(value);
				},
				message : '输入值不能为空和包含其他非法字符'
			},
			username : {// 验证用户名
				validator : function(value) {
					return /^[a-zA-Z][a-zA-Z0-9_]{5,15}$/i.test(value);
				},
				message : '请输入6-16个字符的字母、数字或下划线，以字母开头'
			},
			faxno : {// 验证传真
				validator : function(value) {
					// return /^[+]{0,1}(\d){1,3}[ ]?([-]?((\d)|[
					// ]){1,12})+$/i.test(value);
					return /^((\(\d{2,3}\))|(\d{3}\-))?(\(0\d{2,3}\)|0\d{2,3}-)?[1-9]\d{6,7}(\-\d{1,4})?$/i
							.test(value);
				},
				message : '传真号码不正确'
			},
			zip : {// 验证邮政编码
				validator : function(value) {
					return /^[1-9]\d{5}$/i.test(value);
				},
				message : '邮政编码格式不正确'
			},
			ip : {// 验证IP地址
				validator : function(value) {
					return /d+.d+.d+.d+/i.test(value);
				},
				message : 'IP地址格式不正确'
			},
			name : {// 验证姓名，可以是中文或英文
				validator : function(value) {
					return /^[\u0391-\uFFE5a-zA-Z0-9_]+$/i.test(value);
				},
				message : '请输入中文、英文或数字'
			},
			carNo : {
				validator : function(value) {
					return /^[\u4E00-\u9FA5][\da-zA-Z]{6}$/.test(value);
				},
				message : '车牌号码无效（如：粤J12350）'
			},
			carenergin : {
				validator : function(value) {
					return /^[a-zA-Z0-9]{16}$/.test(value);
				},
				message : '发动机型号无效(如：FG6H012345654584)'
			},
			email : {
				validator : function(value) {
					return /^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/
							.test(value);
				},
				message : '请输入有效的电子邮件账号(如：abc@126.com)'
			},
			msn : {
				validator : function(value) {
					return /^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/
							.test(value);
				},
				message : '请输入有效的msn账号(如：abc@hotnail(msn/live).com)'
			},
			same : {
				validator : function(value, params) {
					if ($(params[0]).val() != "" && value != "") {
						return $(params[0]).val() == value;
					} else {
						return true;
					}
				},
				message : '两次输入的密码不一致！'
			}
		};		
	var inputs = {};
	
	$.InputHint = function(target, options) {
		var options = $.extend({}, $.fn.inputHint.defaults, typeof options === 'string'?{}:options);
				
		var instance = this;

		var pnlInfo = $('<span class="yellowBlock" style="display:none;margin-left:5px;" />').insertAfter(target);
		$('<font style="font-family:icomoon;font-size:16px;color:#ccc;">&#xe8c7;&nbsp;</font>').appendTo(pnlInfo);
		var txtInfo = $('<span />').appendTo(pnlInfo);
		var pnlError = $('<span class="redBlock"  style="display:none;margin-left:5px;"/>').insertAfter(target);
		$('<font style="font-family:icomoon;font-size:14px;">&#xe8ca;&nbsp;</font>').appendTo(pnlError);
		var txtError = $('<span />').appendTo(pnlError);
		
		this.isError = false;
		var validators = [];
		
		this.validate = function(){
			pnlInfo.hide();
			pnlError.hide();
			this.isError = false;
			//
			var val = target.val().trim();
			if(options.isRequired && !val){
				this.isError = true;
				pnlError.show();
				txtError.text('必填字段');
			}else if(val){
				var errMsg = '';
				this.isError = false;
				$.each(validators, function(i, vali){
					var res = vali.validator(val, vali.params);
					if(res===false){
						instance.isError = true;
						errMsg = vali.message;
						return false;
					}
				});
				
				if(this.isError && errMsg){
					pnlError.show();
					txtError.text(errMsg);
				}
			}	
		}
		
		$.extend(options.rules, rules);
		$.each(options.validTypes, function(i, vt){
			var result = /([a-zA-Z_]+)(.*)/.exec(vt);
			var vali = options.rules[result[1]];
			if(vali){
				var params = eval(result[2]);
				var message = vali.message;
				if(params) {
					for ( var i = 0; i < params.length; i++) {
						message = message.replace(new RegExp("\\{" + i
								+ "\\}", "g"), params[i]);
					}
				}
				validators.push({validator:vali.validator, params: params, message:message})
			}
		});
		target.focus(function(e){
			if(!instance.isError && options.info){
				pnlInfo.show();
				txtInfo.text(options.info);
			}
		}).blur(function(e){
			instance.validate();
		});
		
		
		this.target = target; //jquery obj
		this.options = options;
		this.val = target.val;
		this.pnlInfo = pnlInfo;
		this.pnlError = pnlError;
		this.txtError = txtError;
		
		this.name = options.name;
		this.validators = validators;
		inputs[options.name] = this;
		target.data('inputHint-obj', this);
	};
	$.InputHint.inputs = inputs;
	$.InputHint.validate = function(){
		var pass = true;
		$.each(inputs, function(i, input){
			input.validate();
			if(input.isError){
				pass = false;
			}
		});
		return pass;
	}
	$.InputHint.val = function(){
		var value = {};
		$.each(inputs, function(i, input){
			value[input.name] = input.target.val();
		});
		return value;
	}
	
	$.InputHint.prototype = {

	};
	$.fn.inputHint  = function(options) {
		var target = $(this[0]);
		var obj = target.data('inputHint-obj');
		if(!obj){
			obj = new $.InputHint(target, options);
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
	$.fn.inputHint.defaults = {
		name : '',
		validTypes : [], //
		info : '',
		isRequired : false,
		rules :{}

	};
		
})(jQuery);
