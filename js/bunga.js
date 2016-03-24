var DUPLICATES = [];
$(document).ready(function () {
  console.log('yep');
  $(document).keypress(function (event) {
    if (event.which == 13 ) {
      var values = $('input:checked').map(function() {
	var t = $(this);
	var result = t.parent("label").text();
	t.attr('checked', false);
	t.closest('div.holder').remove();
	return result;
      }).get();
      DUPLICATES.push(values);
      var text = JSON.stringify(DUPLICATES, null, 2);
      clipboard.copy(text).then(
	function(){console.log("successfully copied '" + text + "'");},
	function(err){console.log("failed to copy '" + text + "'", err);}
      );
    }
  });
});
