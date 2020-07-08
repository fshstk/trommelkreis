"use strict";

function replaceYoutubeTagWithEmbed() {
  // select any <youtube> tag inside challenge-description div
  $("div.challenge-description youtube").each(function () {
    let embedCode = $(this).text();
    let embedTag =
      "<div class='embed-container'><iframe src='https://www.youtube.com/embed/" +
      embedCode +
      "' frameborder='0' allowfullscreen></iframe></div>";
    $(this).replaceWith(embedTag);
  });
}

$(document).ready(function () {
  replaceYoutubeTagWithEmbed();
});
