var nursesApp = angular.module('NursesApp', ['ngResource'])
                .factory("Nurses", function($resource, $http) {
                  var nurse_resource = $resource("/api/v1/nurse/:id",
                                                 {id: "@id"});

                  nurse_resource.create = function (nurse, success, error) {
                    $http.post("/api/v1/nurse/", nurse);
                  };

                  return nurse_resource;
                })
                .controller("NurseCtrl", function($scope, $resource) {
                  $scope.newNurse = function() {
                    Nurses.create($scope.nurse);
                  }
                });