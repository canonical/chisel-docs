document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("input[type='checkbox'][disabled]").forEach(cb => {
        cb.removeAttribute("disabled");
    });
});
