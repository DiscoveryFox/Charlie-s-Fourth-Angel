(function() {
    // Was soll passieren, wenn anhand das ID das Element dokumentiert ist
    var switchToDark = document.getElementById("switchToDark");
    if (switchToDark) {
        initTheme();
        switchToDark.addEventListener("change", function(event) {
            resetTheme();
        });
        // Was soll drin passieren, wenn das Schalter geklickt ist
        // Das localStorage speichert die Daten ohne Ablaufdatum. Das heißt, wenn du auf Dark Mode die Seite verlassen hast, dann wird die Dark Mode nicht weg und bleibt, sobald du das auf Light Mode zurücksetzt. Die Daten werden beim Schließen des Browsers nicht gelöscht und stehen am nächsten Tag, in der nächsten Woche oder im nächsten Jahr zur Verfügung.
        // Was soll zurückgesetzt werden, wenn unserer Schalter nicht mehr geprüft ist bzw. wenn man es nochmal geklickt hat.
        function initTheme() {
            var darkThemeClick =
                localStorage.getItem("switchToDark") !== null &&
                localStorage.getItem("switchToDark") === "dark";
            switchToDark.checked = darkThemeClick;
            darkThemeClick
                ?
                document.body.setAttribute("theme", "dark"):
                document.body.removeAttribute("theme");
            darkThemeClick
                ?
                $('#logo_img').attr("src", "https://raw.githubusercontent.com/DiscoveryFox/Charlie-s-Fourth-Angel/master/favicon_light.png"):
                null

        }
        function resetTheme() {
            if (switchToDark.checked) {
                document.body.setAttribute("theme", "dark");
                localStorage.setItem("switchToDark", "dark");
                document.getElementById("spanChange").innerHTML = "Dark Mode";
                $('#logo_img').attr("src", "https://raw.githubusercontent.com/DiscoveryFox/Charlie-s-Fourth-Angel/master/favicon_light.png");

            } else {
                document.body.removeAttribute("theme");
                localStorage.removeItem("switchToDark");
                document.getElementById("spanChange").innerHTML = "Light Mode";
                $('#logo_img').attr("src", "https://raw.githubusercontent.com/DiscoveryFox/Charlie-s-Fourth-Angel/master/favicon_dark.png");

            }
        }
    }
})();