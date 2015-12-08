var app = angular.module('myApp', ['myApp.directives']);

app.controller('MainCtrl', function($scope) {
  $scope.myText = 'Not Selected';
  $scope.currentDate = '12/17/2014';
  var ii = 'sdaf';
  $scope.updateMyText = function(date) {
    $scope.myText = 'Selected';
    console.info(date);
  };
});
