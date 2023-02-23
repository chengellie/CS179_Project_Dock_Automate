//Check Off Specific Todos By Clicking
$("header").on("click", "h2", function () {
    // $(this).toggleClass("completed");
    // alert("Handler for .click() called.");
    $(this).fadeToggle();
});