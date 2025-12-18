document.addEventListener("DOMContentLoaded", function () {
  document
    .querySelectorAll('li input[type="checkbox"]')
    .forEach((checkbox) => {
      checkbox.disabled = false;
    });
});
