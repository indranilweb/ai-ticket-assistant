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
        troubleshootingTips();
    })
    .catch(error => {
        document.getElementById("errorResponse").innerHTML = "<div class='response-content'>Error: " + error  + "</div>";
    });
}

function assignTicket() {
    const ticket = {
        subject: "", // document.getElementById('subject').value,
        description: document.getElementById('description').value //document.getElementById('issue').value // document.getElementById('description').value
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

        document.getElementById("response").innerText = data.support_group;
    })
    .catch(error => {
        document.getElementById("errorResponse").innerHTML = "<div class='response-content'>Error: " + error  + "</div>";
    });
}

function troubleshootingTips() {
    const issue = {
        text: document.getElementById('description').value
    };

    fetch("http://localhost:8000/troubleshooting-tips", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(issue)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("issueTroubleshoot").classList.remove("hidden");

        // Get the container element where tips will be displayed
        const troubleshootingListDiv = document.getElementById('troubleshootingList');

        let tipsInnerHtml = "";

        // Access the array of troubleshooting tips
        const tips = data?.troubleshooting_tips;

        // Loop through each tip and create HTML elements
        tips.forEach(tip => {
            // const tipItemDiv = document.createElement('div');
            // tipItemDiv.classList.add('tip-item'); // Add a class for styling

            // const titleElement = document.createElement('h5');
            // titleElement.textContent = tip.title;

            // const actionElement = document.createElement('p');
            // actionElement.textContent = tip.action;

            // tipItemDiv.appendChild(titleElement);
            // tipItemDiv.appendChild(actionElement);

            // troubleshootingListDiv.appendChild(tipItemDiv);

            tipsInnerHtml += `<div class="tip-item">
                    <h5>${tip.title}</h5>
                    <p>${tip.action}</p>
                </div>`
        });

        troubleshootingListDiv.innerHTML = tipsInnerHtml;
    })
    .catch(error => {
        document.getElementById("errorResponse").innerHTML = "<div class='response-content'>Error: " + error  + "</div>";
    });
}