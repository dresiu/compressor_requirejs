requirejs.config({
    optimize: 'none',
    onBuildRead: function (moduleName, path, contents) {
        var pattern1 = /\{\%.*\%\}/g;
        var pattern2 = /\{\{.*\}\}/g;

        //Always return a value.]
        function toBase64(g1){
            return 'django_code:' + (new Buffer(g1).toString('base64'));
        }
        var content = contents.replace(pattern1, toBase64);
        content = content.replace(pattern2, toBase64);
        content = this._processCompileExclusion(content, function(line){
            return '// ' + line + '\n';
        });
        if(this._onBuildRead){
            content = this._onBuildRead(moduleName, path, content);
        }
        return content;
    },
    _processCompileExclusion: function(content, lineCallback){
        var patternUseExclusion = /(\/\/\>startExclusion[\n\s])([\s\S]*?)(?=\/\/\>endExclusion)/gm;
        function excludeText(g1, g2, g3){
            var comment = g2 + '\n';
            g3.split(/\n/).forEach(function(line){
                comment += lineCallback(line);
            });
            return comment;
        }
        return content.replace(patternUseExclusion, excludeText);
    },

    //A function that will be called for every write to an optimized bundle
    //of modules. This allows transforms of the content before serialization.
    onBuildWrite: function (moduleName, path, contents) {
        //Always return a value.
        var decodePattern = /django_code:((?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?)/g;
        var content = contents.replace(decodePattern, function(g1, g2){
            return (new Buffer(g2, 'base64').toString('utf8'));
        });
        content = this._processCompileExclusion(content, function(line){
            return line.replace(/\/\//, '') + '\n';
        });

        if(this._onBuildWrite){
            content = this._onBuildWrite(moduleName, path, content);
        }
        return content;
    },
    fileExclusionRegExp: null
});
