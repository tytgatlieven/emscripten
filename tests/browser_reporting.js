var hasModule = typeof Module === 'object' && Module;

/** @param {boolean=} sync
    @param {number=} port */
function reportResultToServer(result, sync, port) {
  port = port || 8888;
  if (reportResultToServer.reported) {
    // Only report one result per test, even if the test misbehaves and tries to report more.
    reportErrorToServer("excessive reported results, sending " + result + ", test will fail");
  }
  reportResultToServer.reported = true;
  var xhr = new XMLHttpRequest();
  if (hasModule && Module['pageThrewException']) {
    result = 'pageThrewException';
  }
  xhr.open('GET', 'http://localhost:' + port + '/report_result?' + result, !sync);
  xhr.send();
  if (typeof window === 'object' && window && hasModule && !Module['pageThrewException'] /* for easy debugging, don't close window on failure */) setTimeout(function() { window.close() }, 1000);
}

/** @param {boolean=} sync
    @param {number=} port */
function maybeReportResultToServer(result, sync, port) {
  if (reportResultToServer.reported) return;
  reportResultToServer(result, sync, port);
}

function reportErrorToServer(message) {
  var xhr = new XMLHttpRequest();
  xhr.open('GET', encodeURI('http://localhost:8888?stderr=' + message));
  xhr.send();
}

if (typeof window === 'object' && window) {
  function onerror(e) {
    // MINIMAL_RUNTIME doesn't handle exit or call the below onExit handler
    // so we detect the exit by parsing the uncaught exception message.
    var message = e.message || e;
    console.error("got top level error: " + message);
    var offset = message.indexOf('exit(');
    if (offset != -1) {
      var status = message.substring(offset + 5);
      offset = status.indexOf(')')
      status = status.substr(0, offset)
      console.error(status);
      maybeReportResultToServer('exit:' + status);
    } else {
      var xhr = new XMLHttpRequest();
      xhr.open('GET', encodeURI('http://localhost:8888?exception=' + e.message + ' / ' + e.stack));
      xhr.send();
    }
  }
  window.addEventListener('error', onerror);
  window.addEventListener('unhandledrejection', event => onerror(event.reason));
}

if (hasModule) {
  Module['onExit'] = function(status) {
    maybeReportResultToServer('exit:' + status);
  }

  Module['onAbort'] = function(reason) {
    maybeReportResultToServer('abort:' + reason);
  }
}
