var ___getJSONCache = {};
$.extend($,{
	postJSON: function( url, data, callback, failure, settings ) {
		if ( jQuery.isFunction( data ) ) {
			settings = failure;
			failure = callback;
			callback = data;
			data = undefined;
		}

		return jQuery.ajax($.extend({
			type: 'post',
			url: url,
			data: JSON.stringify(data),
			dataType: 'json',
			contentType: "application/json; charset=UTF-8",
			success: function(data){
				if(data.statusCode!=200 && failure){
					failure(data);
				}else if (data.statusCode!=200 && data.statusCode!=404){
					alert(data.message);
				}
				else if(callback){
					(callback)(data);	
				}					
			}
		},settings||{}));
	},
	//增加了 statusCode的校验,pageCache:页面缓存
	getJSON: function( url, params, callback, pageCache ) {
		if ( jQuery.isFunction( params ) ) {
			pageCache = callback;
			callback = params;
			data = undefined;
		}		
		
		function _callback(data){
			if (data.statusCode!=200 && data.statusCode!=404){
				alert(data.message);
			}
			else if(callback){
				(callback)(data);	
			}	
		}
		if(pageCache){
			var key = JSON.stringify(params);
			if(!___getJSONCache[url]){
				___getJSONCache[url] = {};
			}
			var data = ___getJSONCache[url][key];
			if(data){
				return _callback(data);
			}else{
				return jQuery.get(url, params, function(data){
					___getJSONCache[url][key] = data;
					_callback(data);
				},"json");
			}
		}
		else{
			return jQuery.get(url, params, function(data){
				_callback(data);
			},"json");
		}
	},
	initEvent : function(e){
		//firefox 下 绑定 srcElement=target
		//简写srcElement 
		if(e.target)
			e.srcElement=e.target;	
		if(e.which)
			e.keyCode=e.which;
		e.src=e.srcElement;
	},
	stringFormat : function(str) {
		for ( var i = 0; i < arguments.length - 1; i++) {
			str = str.replace("{" + i + "}", arguments[i + 1]);
		}
		return str;
	},
	getDateString : function(str) {
		if (str) {
			var date = new Date(parseInt(str.substr(6)));
			var str = date.getFullYear() + "-" + (date.getMonth() + 1) + "-"
					+ date.getDate();
		}else{
			var date = new Date();
			var str = date.getFullYear() + "-" + (date.getMonth() + 1) + "-"
					+ date.getDate();
		}
		return str;
	},
	getDateObj : function(str) {
		return new Date(parseInt(str.substr(6)));
	},
	getFormValues : function($form) {
		values = {};
		$folunchOrder.find(":input").each(function(index, elm) {
			if (elm.name && elm.name.indexOf('__') < 0) {
				values[elm.name] = $(elm).val();
			}
		});
		return values;
	},
	getUrl : function() {
		return location.href.split('?')[0];
	},
	getUrlParams : function() {
		var vars = [], hash;
		var hashes = window.location.href.slice(
				window.location.href.indexOf('?') + 1).split('&');
		for ( var i = 0; i < hashes.length; i++) {
			hash = hashes[i].split('=');
			vars.push(hash[0]);
			vars[hash[0]] = hash[1];
		}
		return vars;
	},
	getUrlParam : function(name) {
		return $.getUrlParams()[name];
	},
	getUrlAnchors : function() {
		var vars = [], hash;
		var hashes = window.location.href.slice(
				window.location.href.indexOf('#') + 1).split('&');
		for ( var i = 0; i < hashes.length; i++) {
			hash = hashes[i].split('=');
			vars.push(hash[0]);
			vars[hash[0]] = hash[1];
		}
		return vars;
	},
	getUrlAnchor : function(name) {
		return $.getUrlAnchors()[name];
	},
	removeFromArray : function(array, removeItem) {
		return jQuery.grep(array, function(value) {
			return value != removeItem;
		})
	},
	uniqueArray : function(array) {
		var ret = [], done = {};
		try {
			for ( var i = 0, length = array.length; i < length; i++) {
				var tmp = array[i]; // jQuery native code : var id =
				// jQuery.data(array[i]);
				if (!done[tmp]) {
					done[tmp] = true;
					ret.push(tmp);
				}
			}
		} catch (e) {
			ret = array;
		}
		return ret;
	},
	// 写入cookies
	setCookie : function(name, value, expiresDays) {
		var Days = expiresDays||30;
		var d = new Date();
		var exp = new Date(d.getFullYear(), d.getMonth(), d.getDate());
		exp.setTime(exp.getTime() + Days * 24 * 60 * 60 * 1000);
		document.cookie = name + "=" + escape(value) + ";domain=.17j38.com;path=/;expires="
				+ exp.toGMTString();
	},
	// 读取cookies
	getCookie : function(name) {
		var arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");
		if (arr = document.cookie.match(reg))
			return unescape(arr[2]);
		else
			return null;
	},
	// 删除cookies
	delCookie : function(name) {
		var exp = new Date();
		exp.setTime(exp.getTime() - 1);
		var cval = this.getCookie(name);
		if (cval != null)
			document.cookie = name + "=" + cval + ";expires="
					+ exp.toGMTString();
	},
	getUUID : function(){
//		var str = new Date(); 
//		str = str.getTime();
//		return str;
	    var d = new Date().getTime();
	    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
	        var r = (d + Math.random()*16)%16 | 0;
	        d = Math.floor(d/16);
	        return (c=='x' ? r : (r&0x7|0x8)).toString(16);
	    });
	    return uuid;		
	},
	urlEncode: function(str){
	   var ret="";
	   var strSpecial="!\"#$%&'()*+,/:;<=>?[]^`{|}~%";
	   for(var i=0;i<str.length;i++){
	   var chr = str.charAt(i);
	     var c=str2asc(chr);
	     if(parseInt("0x"+c) > 0x7f){
	       ret+="%"+c.slice(0,2)+"%"+c.slice(-2);
	     }else{
	       if(chr==" ")
	         ret+="+";
	       else if(strSpecial.indexOf(chr)!=-1)
	         ret+="%"+c.toString(16);
	       else
	         ret+=chr;
	     }
	   }
	   return ret;
	},
	urlDecode: function(zipStr){ 
	    var uzipStr=""; 
	    function _asciiToString(asccode){ 
	    	return String.fromCharCode(asccode); 
	    }
	    for(var i=0;i<zipStr.length;i++){ 
	        var chr = zipStr.charAt(i); 
	        if(chr == "+"){ 
	            uzipStr+=" "; 
	        }else if(chr=="%"){ 
	            var asc = zipStr.substring(i+1,i+3); 
	            if(parseInt("0x"+asc)>0x7f){ 
	                uzipStr+=decodeURI("%"+asc.toString()+zipStr.substring(i+3,i+9).toString()); 
	                i+=8; 
	            }else{ 
	                uzipStr+=_asciiToString(parseInt("0x"+asc)); 
	                i+=2; 
	            } 
	        }else{ 
	            uzipStr+= chr; 
	        } 
	    } 
	 
	    return uzipStr; 
	},
	returnBack: function(defaultUrl){
//		console.info(document.referrer);
//		console.info($.urlDecode($.getUrlParam('returnUrl') || defaultUrl || document.referrer || '/'));
		location.href = $.urlDecode($.getUrlParam('returnUrl') || defaultUrl || document.referrer || '/');
	}
	 
});



(function($) {
	if(!Object.keys)
	{
	  Object.keys = function(obj)
	  {
	    return $.map(obj, function(v, k)
	    {
	      return k;
	    });
	  };
	 }
	$.fn.findParent = function(expr) {
		var parents = this.parentsUntil(expr);
		return $(parents[parents.length - 1]).parent();
	}	
})(jQuery);
