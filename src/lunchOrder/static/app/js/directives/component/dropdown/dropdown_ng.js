/**
 * Created by Administrator on 2014/12/8.
 */
mComponent.directive('daDropdown', function() {
    return {
        restrict: "AE",
        //transclude:true,
        template: '<span class="phComponent"></span>',
        //templateUrl: "dropdown.html",
        //replace: true,
        scope: {
            options: '=', //[] or {val:text}
            value: '=',
            width: '=',
            change: '&'//-change="handler(value, oldValue)"
        },
        //compile: function(tElement, tAttrs, transclude){
        //    return{
        //    //console.info($(document.body));
        //    //console.info('compile')
        //    //console.info(tElement.html())
        //    pre: function(scope, iElement, iAttrs, controller, transclude){
        //            console.info('pre');
        //        console.info(scope.xx);
        //
        //        //console.info(iElement.html());
        //            //console.info(iAttrs['kkk']);
        //            //console.info(transclude);
        //        },
        //        post: function(scope, iElement, iAttrs, controller, transclude){
        //            //console.info('post');
        //            //console.info(iElement.html());
        //            //console.info(iAttrs['kkk']);
        //            //console.info(transclude);
        //        }
        //    }
        //},
        link: function(scope, iElement, iAttrs, controller, transclude){
            //console.info(scope)
            var options =  {
                data : scope.options,
                value : scope.value,
                width : scope.width,
                onChange : function(e, newVal, oldValue){
                    scope.value = newVal;
                    scope.change({value:newVal, oldValue:oldValue});
                    scope.$apply();
                }
            };
            scope._obj =jQuery(iElement.children()[0]).dropdown(options);
            //scope._obj.change(function(e, newVal){
            //    scope.value = newVal.value;
            //    scope.onChange(newVal);
            //    //scope.xx(newVal)
            //    //console.info(scope.value)
            //    //$parse(iAttrs['ngModel']).assign(scope, data);
            //    scope.$apply();
            //});
            //console.info(iElement.html());
            //$(document.body).click(function(e){
            //    //console.inf
            //    scope.xx(e);
            //});
            //console.info(iAttrs['kkk']);
            //console.info(transclude);
        }//,
        //controller: function()
    };
});
mComponent.run(["$templateCache", function($templateCache) {
    $templateCache.put('dropdown.html', '<div class="phComponent"></div>');
}]);