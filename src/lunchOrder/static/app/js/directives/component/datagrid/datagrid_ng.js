/**
 * Created by Administrator on 2014/12/8.
 */
mComponent.directive('daDatagrid', function() {
    return {
        restrict: "AE",
        scope: {
            parsers : '=', //parser格式：  function(tr, td, rowData, fieldValue)
            dataRows : '=',
            checkbox: '@',
            rowCheckable:  '@',//点行时选中checkbox
            rowSelectable:  '@', //点行时选中行
            singleSelect:  '@', //单选选中行
            sort:'&',//{sort:sort, order:order}
            value:'='
        },
        link: function(scope, iElement, iAttrs, controller, transclude){
            var options =  {
                parsers : scope.parsers,
                dataRows : scope.dataRows,
                checkbox : scope.checkbox,
                rowCheckable : scope.rowCheckable,
                rowSelectable : scope.rowSelectable,
                singleSelect : scope.singleSelect,
                onSort : function(e, sort, order){
                    scope.sort({sort:sort, order:order});
                },
                onRowSelected:function(e, rowIds){
                    scope.value = rowIds;
                    scope.$apply();
                }
            };
            scope.$watch('dataRows', function(newValue, oldValue){
                console.info('dataRows');
            });
            scope._obj =jQuery(iElement).datagrid(options);
        }//,
    };
});