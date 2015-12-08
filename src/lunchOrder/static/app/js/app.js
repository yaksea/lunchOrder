var shops = [{
    _id:0,
    name:'枯国佣兵国',
    address:'莆田市'
},{
    _id:1,
    name:'玩具百无一用的',
    address:'福州市'
},{
    _id:2,
    name:'基材摇篮脾仍',
    address:'厦门市'
}];

var mCommon;

if($.browser.msie){
    mCommon = angular.module('mCommon', ['component.directives']);
}else{
    mCommon = angular.module('mCommon', ['ngRoute','component.directives']);
}

var mApp = angular.module('mApp', ['mCommon']);

mApp.config(['$compileProvider', '$routeProvider', '$locationProvider', function ($compileProvider, $routeProvider, $locationProvider) {
    $routeProvider.when('/', {controller:  'cList', templateUrl: 'list.html'}).
        when('/shops/:id', {controller: 'cDetail', templateUrl: 'detail.html'}).
        otherwise({redirectTo:'/'});
    //$compileProvider.debugInfoEnabled(false);
    //$locationProvider.hashPrefix('!');//;.html5Mode(true)
    //$compileProvider.urlSanitizationWhitelist(/^\s*(https?|ftp|mailto|file):/);
}]);

mApp.controller('cList', ['$scope', function ($scope) {
    $scope.shops = shops;
    $scope.ddlChange = function(e){
        console.info(e);
        return 'dsaf'
    }
}]);
mApp.controller('ctlMain', ['$scope', function ($scope) {
    //$scope.ddlChange = function(e){
    //    console.info(e);
    //    return 'dsaf'
    //}
    $scope.shops = ['asdf','sdafds', 'fdgfdgf'];
    $scope.ddlVal = 'fdgfdgf';
    $scope.ddlChange = function(value, oldValue){
        console.info(value, oldValue);
    };
    $scope.changeVal = function(){
        console.info(arguments);
        $scope.shops[2] = 'vcxxcvb';
    }
    //$scope.$watch('ddlVal', function(){
    //    console.info($scope.ddlVal)
    //})
}]);


mApp.controller('cDetail', ['$scope','$routeParams', function ($scope,$routeParams) {
    console.info(shops[$routeParams.id])
    $scope.shop = shops[$routeParams.id];
}]);

