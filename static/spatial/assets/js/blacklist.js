(function($) {

  var formContainer = null;
  var flashMessageContainer = null;
  var blacklistedAddresses = [];

  var flashMessages = {
    info: 'p.info',
    warn: 'p.warn',
    error: 'p.error',
    all: 'p.info, p.warn, p.error'
  };

  var hideMessages = function() {
    var selector = $(flashMessages.all, flashMessageContainer);
    selector.text('');
    selector.hide();
  };

  var showMessage = function(type, msg) {
    hideMessages();
    var selector = $(flashMessages[type], flashMessageContainer);
    selector.text(msg);
    selector.show();
  };

  var getBlacklist = function() {
    if (blacklistedAddresses.length > 0) return blacklistedAddresses;
    var addressList = $('ul#blacklist li code').each(function() {
      blacklistedAddresses.push($(this).text().toLowerCase());
    });
    return blacklistedAddresses;
  };

  var normalizeInput = function(onion) {
    onion = onion.replace('.onion', '');
    onion = onion.replace('http:', '');
    onion = onion.replace('https:', '');
    return onion.replace('//', '').trim();
  };

  var checkAddress = function(evt) {
    hideMessages();
    evt.preventDefault();
    // get value from form
    getBlacklist();
    var plaintext = normalizeInput($('#blacklistInput').val()) + "\n";
    if (plaintext.length !== 12) {
      showMessage('warn', "This doesn't appear to be a valid onion.");
      return;
    }
    var md5 = window.md5(plaintext);
    var isBlacklisted = false;
    for (var i=0; i<blacklistedAddresses.length; i++) {
      if (md5 === blacklistedAddresses[i]) {
        isBlacklisted = true;
      }
    }
    if (isBlacklisted) {
      showMessage('error', "This .onion is on the Ahmia blacklist.");
    } else {
      showMessage('info', "This .onion is not blacklisted.");
    }
  };

  $(document).ready(function() {
    flashMessageContainer = $('#flashMessage');
    formContainer = $('#ahmiaFormContainer');
    if (formContainer && flashMessageContainer &&
      typeof window.md5 === 'function') {
      formContainer.removeClass('hidden');
    } else {
      return;
    }
    hideMessages();
    $('#checkBlacklist').on('submit', checkAddress);
  });

})(window.jQuery);
