define(['text!./../app/template.html'], function (template) {

	function print(str){
		document.getElementsByTagName('h1')[0].innerHTML = str + template;
	}
    return {
        print: print
    }
});