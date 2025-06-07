function submitTicket() {
    const ticket = {
        subject: document.getElementById('subject').value,
        description: document.getElementById('description').value
    };
    document.getElementById("response").innerHTML = "<div class='response-content response-loading'><span class='loader'></span><span class='loader-text'>Please wait while we assign your ticket to the correct support group.</span></div>";

    fetch("http://localhost:8000/assign-ticket", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(ticket)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("response").innerHTML = "<div class='response-content'><div>You ticket has been assigned to: </div><div class='support-group'>" + data.support_group + "</div></div>";
    })
    .catch(error => {
        document.getElementById("response").innerHTML = "<div class='response-content'>Error: " + error  + "</div>";
    });
}