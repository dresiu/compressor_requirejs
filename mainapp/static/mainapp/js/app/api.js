//>startExclusion
{% load tags %}
//>endExclusion

define('this.api', [], function () {
    return {
        //>startExclusion
        jsonObj: {{ JSON_OBJECT|to_json }},
        //>endExclusion
        version: '1.0'
    }
});
