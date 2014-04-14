require(["./util/util", 'app/api'], function (util, api) {
    console.log(api);
    util.print('require js supported');
    function ffff(longParameter){
        var longerParameter = 'fsdfagdfgs';
        return longParameter + longerParameter;
    }

    require(['this.api', '{{ STATIC_URL }}mainapp/js/app/async.js'], function (api2, async) {
        console.log(api2);
    });

});