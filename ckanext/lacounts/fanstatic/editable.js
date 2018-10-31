$(document).ready(function() {

  // Exit if nothing is editable
  if ($('*[data-editable]').length === 0) return;

  // Create editor
  var editor = ContentTools.EditorApp.get();
  editor.init('*[data-editable]', 'data-name');

  // Save edited regions
  editor.addEventListener('saved', function (ev) {
      var name, payload, regions, xhr, data;

      // Check that something changed
      regions = ev.detail().regions;
      if (Object.keys(regions).length == 0) {
          return;
      }

      // Set the editor as busy while we save our changes
      this.busy(true);

      // Collect the contents of each region into a FormData instance
      data = Object.assign({}, regions, {is_patch: true});
      payload = new FormData();
      payload.append('ckanext.lacounts.editable_regions', JSON.stringify(data))

      // Send the update content to the server to be saved
      function onStateChange(ev) {
          // Check if the request is finished
          if (ev.target.readyState == 4) {
              editor.busy(false);
              if (ev.target.status == '200') {
                  // Save was successful, notify the user with a flash
                  new ContentTools.FlashUI('ok');
              } else {
                  // Save failed, notify the user with a flash
                  new ContentTools.FlashUI('no');
              }
          }
      };

      xhr = new XMLHttpRequest();
      xhr.addEventListener('readystatechange', onStateChange);
      xhr.open('POST', '/api/action/config_option_update');
      xhr.send(payload);
  });

});
