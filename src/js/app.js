var app = angular.module('TNT', [
    'ngAnimate',
    'ngSanitize',
    'ngRoute',
    'ui.bootstrap'
])



.config(function ($routeProvider, $locationProvider) {

        $routeProvider.when('/', {
            templateUrl: 'views/main.html',
            controller: 'TrackerCtrl'
        });

        $routeProvider.when('/thing/:thingId', {
            templateUrl: "views/thing/view.html",
            controller: "ThingCtrl"
        });

        $locationProvider.html5Mode(false);

    })

    .controller('AppCtrl', ['$scope', '$timeout', '$http', '$rootScope', function ($scope, $timeout, $http, $rootScope) {

        if ($scope.things == undefined) {
            $scope.thingsSummary = [];


            $http({
                method: 'get',
                url: 'tracker.json'
            }).then(function (response) {
                console.log(response, 'got tracker.json');
                data = response.data;
                $scope.things = {};

                for (var i = 0; i < data.things.length; i++) {
                    var thing = data.things[i];
                    $scope.things[thing.id] = thing;
                    $scope.thingsSummary.push({
                        id: thing.id,
                        avatar: thing.avatar,
                        title: thing.title,
                        created: thing.created,
                        creator:thing.authors[0].name,
                        description: thing.description,
                        like: thing.like,
                        collect: thing.collect,
                        made: thing.made,
                        watch: thing.watch,
                        remix: thing.remix,
                        thumbnailURL: (thing.thumbnailUrls && thing.thumbnailUrls[0]) || undefined
                    });
                    console.log($scope.thingsSummary);
                }
                ;

            }, function (error) {
                console.log(error, 'can not get tracker.json data.');
            });
        }
    }])

    .controller('TrackerCtrl', ['$rootScope', function ($rootScope) {
        $rootScope.appTitle = "ThingsBox"
    }])




    .controller('DocumentReady', [function() {
        angular.element(document).ready(function () {

            console.log("docready");
        });
    }])


    .controller('ThingCtrl', ['$scope', '$location', '$routeParams', '$http', '$rootScope', function ($scope, $location, $routeParams, $http, $rootScope) {

        $scope.thingId = $routeParams.thingId;

        if ($scope.thingId === undefined) {
            console.error("No Thing ID given.");
            $location.path("/");
        }
        ;

        $scope.thing = $scope.things[$scope.thingId];

        $rootScope.appTitle = "ThingsBox : " + $scope.thing.title

    }])

    .controller('CarouselCtrl', function ($scope) {
        $scope.myInterval = 5000;
        $scope.noWrapSlides = false;
        $scope.active = 0;
        var slides = $scope.slides = [];
        var currIndex = 0;

        $scope.addSlide = function(slide) {
            slides.push({
                image: slide,
                id: currIndex++
            });
        };

        for (var i = 0; i < $scope.thing.thumbnailUrls.length; i++) {
            $scope.addSlide($scope.thing.thumbnailUrls[i]);
        }

    })

    .filter('reverse', function () {
        return function (items) {
            return items.slice().reverse();
        };
    })
    .filter('nl2br', function () {
        return function (text) {
            if (text == undefined) {
                return undefined;
            }
            return text.replace(/\\n/g, '<br>');
        }
    })
    .filter('stripUrlProtocol', function () {
        return function (text) {
            if (text == undefined) {
                return undefined;
            }
            return text.replace(/^(?:(ht|f)tp(s?)\:\/\/)?/, '');
        }
    })
    .filter('truncate', function () {
        return function (text, length, end) {
            if (text == undefined) {
                return undefined;
            }
            if (isNaN(length))
                length = 10;

            if (end === undefined)
                end = "...";

            if (text.length <= length || text.length - end.length <= length) {
                return text;
            }
            else {
                return String(text).substring(0, length - end.length) + end;
            }
        };
    });