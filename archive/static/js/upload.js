"use strict";

function passwordValid() {
  return false;
}

function validatePassword() {
  let field = $("#id_password")[0];
  let password = $("#id_password").val();

  $.post(
    "/upload/checkpassword/",
    { password: password },
    function (response) {
      if (response.valid) {
        // Password correct :)
        console.log("yay");
        field.setCustomValidity("");
      } else {
        // Password incorrect :(
        console.log("boo");
        field.setCustomValidity("Passwort falsch");
      }
    },
    "json"
  );
}

// Validate form when clicking submit:
$("form").submit(function (event) {
  validatePassword();

  if ($("form")[0].checkValidity() === false) {
    event.preventDefault();
    event.stopPropagation();
  }
  $("form").addClass("was-validated");
});

$(".custom-file-input").on("change", function () {
  let file = $(this).prop("files")[0];

  if (file.name.match(/\.[^/.]+$/) == ".mp3") {
    this.setCustomValidity("");
  } else {
    this.setCustomValidity("Datei endet nicht in .mp3");
  }

  ID3.loadTags(
    file.name,
    function () {
      let tags = ID3.getAllTags(file.name);
      if (tags.title) {
        var title = tags.title;
      } else {
        // Strip file suffix:
        var title = file.name.replace(/\.[^/.]+$/, "");
        // Underscores to spaces:
        title = title.replace(/_/g, " ");
      }
      // Populate title/artist fields with ID3 tags of selected file:
      $("#id_name").val(title);
      console.log(title);
      $("#id_artist").val(tags.artist);
      // Display the file name in input field if one is selected:
      $(".custom-file-label").html(title);
    },
    { dataReader: ID3.FileAPIReader(file) }
  );
});
