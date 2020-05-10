"use strict";

(function () {
  window.addEventListener(
    "load",
    function () {
      let form = document.getElementById("upload-form");
      form.addEventListener(
        "submit",
        function (event) {
          if (form.checkValidity() === false) {
            event.preventDefault();
            event.stopPropagation();
          }
          form.classList.add("was-validated");
        },
        false
      );
    },
    false
  );
})();
