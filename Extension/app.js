document.addEventListener("DOMContentLoaded", function() {
    var btn = document.getElementById("Summarise");
    btn.addEventListener("click", function() {
        btn.disabled = true;
        btn.innerHTML = "Summarising...";
        chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
            var url = tabs[0].url;
            var xhr = new XMLHttpRequest();
            xhr.open("GET", "http://127.0.0.1:5000/summary?url=" + encodeURIComponent(url), true);
            xhr.onload = function() {
                var text = xhr.responseText;
                const p = document.getElementById("output");
                p.innerHTML = text;
                btn.disabled = false;
                btn.innerHTML = "Summarise";
            }
            xhr.send();
        });
    });

    // Function to copy text to clipboard
    function copyToClipboard() {
        var output = document.getElementById("output");
        var range = document.createRange();
        range.selectNode(output);
        window.getSelection().removeAllRanges();
        window.getSelection().addRange(range);

        try {
            // Attempt to copy the selected text
            var success = document.execCommand("copy");
            var message = success ? "Copied to clipboard!" : "Failed to copy to clipboard.";
            alert(message);
        } catch (err) {
            console.error("Error copying to clipboard:", err);
            alert("Error copying to clipboard. Please try again.");
        } finally {
            window.getSelection().removeAllRanges();
        }
    }

    // Add event listener to copy button
    document.getElementById("copyBtn").addEventListener("click", copyToClipboard);
});
