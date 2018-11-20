'use strict';

var fs = require('fs');
var cp = require('child_process');

function genericInvoke(event, context, callback) {
  let dataFile = `/tmp/invoke-data-${Date.now()}.json`;
  let data = JSON.stringify(event);

  fs.writeFile(dataFile, data, function (err) {
    cp.execFile('sls', ['invoke', 'local', '--function', 'resolve_blacklist', '--path', dataFile], {
      cwd: '/bounties_api',
    }, (error, stdout, stderr) => {
      if (error) {
        console.log("INVOKE_ERROR", error)
        console.log(stderr)
        return callback(error);
      }
      console.log("INVOKE_OUT", stdout);
      callback();
    });
  });
}

module.exports.resolve_blacklist = genericInvoke;