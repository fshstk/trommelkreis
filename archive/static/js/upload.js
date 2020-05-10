"use strict";

// Validate form when clicking submit:
$("form").submit(function (event) {
  if ($("form")[0].checkValidity() === false) {
    event.preventDefault();
    event.stopPropagation();
  }
  if (true) {
    $("#id_password");
  }
  $("form").addClass("was-validated");
});

$(".custom-file-input").on("change", function () {
  let file = $(this).prop("files")[0];

  // Populate title/artist fields with ID3 tags of selected file:
  ID3.loadTags(
    file.name,
    function () {
      let tags = ID3.getAllTags(file.name);
      console.log("Artist: " + tags.artist);
      console.log("Title: " + tags.title);
      if (tags.title) {
        var title = tags.title;
      } else {
        // Strip file suffix:
        var title = file.name.replace(/\.[^/.]+$/, "");
        // Underscores to spaces:
        title = file.name.replace(/_/, " ");
      }
      $("#id_name").val(title);
      $("#id_artist").val(tags.artist);
    },
    { dataReader: ID3.FileAPIReader(file) }
  );

  // Display the file name in input field if one is selected:
  $(this).next(".custom-file-label").html(file.name);
});
