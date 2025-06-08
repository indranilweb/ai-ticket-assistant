function reviewTicket() {
    // document.getElementById("issueDraft").classList.add("hidden");
    document.getElementById("analyzing").classList.remove("hidden");
    const issue = {
        text: document.getElementById('issue').value
    };
    // document.getElementById("response").innerHTML = "<div class='response-content response-loading'><span class='loader'></span><span class='loader-text'>Please wait while we assign your ticket to the correct support group.</span></div>";

    fetch("http://localhost:8000/review-ticket", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(issue)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("subject").value = data.ticket.subject;
        document.getElementById("description").value = data.ticket.description;

        assignTicket();
    })
    .catch(error => {
        document.getElementById("response").innerHTML = "<div class='response-content'>Error: " + error  + "</div>";
    });
}

// function backToDraft() {
//     document.getElementById("issueReview").classList.add("hidden");
//     // document.getElementById("issueDraft").classList.remove("hidden");
// }

function assignTicket() {
    const ticket = {
        subject: "", // document.getElementById('subject').value,
        description: document.getElementById('issue').value // document.getElementById('description').value
    };
    // document.getElementById("response").innerHTML = "<div class='response-content response-loading'><span class='loader'></span><span class='loader-text'>Please wait while we assign your ticket to the correct support group.</span></div>";

    fetch("http://localhost:8000/assign-ticket", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(ticket)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("analyzing").classList.add("hidden");
        document.getElementById("issueReview").classList.remove("hidden");
        document.getElementById("issueTroubleshoot").classList.remove("hidden");

        document.getElementById("response").innerText = data.support_group;
    })
    .catch(error => {
        document.getElementById("response").innerHTML = "<div class='response-content'>Error: " + error  + "</div>";
    });
}