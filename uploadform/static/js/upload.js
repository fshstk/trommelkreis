"use strict";

function validatePassword() {
  let field = $("#id_password")[0];
  let password = $("#id_password").val();

  $.post(
    "/upload/checkpassword/",
    { password: password },
    function (response) {
      if (response.valid) {
        // Password correct :)
        field.setCustomValidity("");
      } else {
        // Password incorrect :(
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
  } else {
    $("#upload-button").addClass("disabled loading").attr("disabled", true)
    $("#upload-button").text("Dein Track lädt hoch…");
  }
  $("form").addClass("was-validated");
});

$("#id_data").on("change", function () {
  let file = $(this).prop("files")[0];
  if (!file.name.endsWith(".mp3")) {
    this.setCustomValidity("Datei endet nicht in .mp3");
    return;
  }
  this.setCustomValidity("");
  const setFormValues = (title, artist) => {
    const stripSuffix = str => str.substring(0, file.name.lastIndexOf("."));
    title = title || stripSuffix(file.name).replace("_", " ");
    $("#id_name").val(title);
    $("#track-name").html(title);
    if(artist)
      $("#id_artist").val(artist);
  };
  jsmediatags.read(file, {
    onSuccess: res => setFormValues(res.tags.title, res.tags.artist),
    onError: _ => setFormValues("", ""),
  });
});
