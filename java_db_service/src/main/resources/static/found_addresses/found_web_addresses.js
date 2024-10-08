
angular.module('crypto-osint-front').controller('found_addressesController', function ($scope, $http, $location, $localStorage) {
    const contextPath = 'http://localhost:8190/OSINT/';

    $scope.loadFoundAddresses = function (pageIndex = 1) {
        $http({
            url: contextPath + 'api/v1/found_addresses',
            method: 'GET',
            params: {
                p: pageIndex,
                address: $scope.filter ? $scope.filter.address : null,
                // min_price: $scope.filter ? $scope.filter.min_price : null,
                // max_price: $scope.filter ? $scope.filter.max_price : null,
                // min_square_meters: $scope.filter ? $scope.filter.min_square_meters : null,
                // max_square_meters: $scope.filter ? $scope.filter.max_square_meters : null,
                // number_of_guests: $scope.filter ? $scope.filter.number_of_guests : null,
                // number_of_rooms: $scope.filter ? $scope.filter.number_of_rooms : null,
                // number_of_beds: $scope.filter ? $scope.filter.number_of_beds : null,
                // title_part: $scope.filter ? $scope.filter.title_part : null,
                // category_part: $scope.filter ? $scope.filter.category_part : null,
                // start_date: $scope.filter ? $scope.filter.start_date : null,
                // finish_date: $scope.filter ? $scope.filter.finish_date : null
            }
        }).then(function (response) {
            $localStorage.filter_storage = $scope.filter;
            $scope.FoundAddressesPage = response.data;
            console.log( response.data)
            $scope.paginationArray = $scope.generatePagesIndexes(1, $scope.FoundAddressesPage.totalPages);
        });
    };

    $scope.generatePagesIndexes = function (startPage, endPage) {
        let arr = [];
        for (let i = startPage; i < endPage + 1; i++) {
            arr.push(i);
        }
        return arr;
    }

    $scope.loadFoundAddresses();
});