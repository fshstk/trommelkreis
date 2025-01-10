$(() => $("#id_password")[0].setCustomValidity("Kein Passwort"));

$("#id_password").typeWatch({
  callback: str => $.post(
    "/upload/checkpassword/",
    { password: str },
    res => $("#id_password")[0].setCustomValidity(res.valid ? "" : "Passwort falsch"),
    "json"
  ),
  wait: 200,
});

$("form").submit(evt => {
  if (!$("form")[0].checkValidity())
    evt.preventDefault();
  else
    $("#upload-button").addClass("disabled loading").attr("disabled", true).text("Dein Track lädt hoch…");
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
