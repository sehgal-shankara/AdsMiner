var page = require('webpage').create(),
	fs = require('fs'),
	system = require('system'),
	address, file;

if (system.args.length === 1) {
  console.log('Usage: save.js <some URL> <file name>');
  phantom.exit();
}	

address = system.args[1];
page.settings.resourceTimeout = system.args[2];
page.settings.userAgent = 'Mozilla/5.0 (Windows NT 5.1; rv:27.0) Gecko/20100101 Firefox/27.0';
page.settings.loadImages = false;
page.viewportSize = { width: 1024, height: 768 };


page.open(address, function (status) {
  if (status !== 'success') {
    console.log('FAIL to load the address');
  } else {

	 console.log('URL: ' + page.evaluate(function () {
                return document.location.href;
            }));
  }
    phantom.exit();
});
