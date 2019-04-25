function askLocalStorage(cb) {
  chrome.fileSystem.chooseEntry({
    type: 'openDirectory'
  },
  function(entry, entries) {
    if (entry) {
      chrome.storage.local.set({'directory': chrome.fileSystem.retainEntry(entry)});
    }
    cb(entry);
  })
}

function ensureLocalStorage(cb) {
  chrome.storage.local.get('directory', function(items) {
    var directory = items['directory'];
    if (!directory) {
      askLocalStorage(cb);
      return;
    }
    chrome.fileSystem.restoreEntry(directory, function(entry) {
      if (!entry) {
        askLocalStorage(cb);
        return;
      }
      cb(entry);
    })
  });
}
