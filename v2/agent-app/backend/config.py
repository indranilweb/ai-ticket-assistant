# Define available support groups and their roles
SUPPORT_GROUPS = {
    "Hardware Support": "For issues related to physical devices like laptops, keyboards, and mice.",
    "Software Support": "For problems with applications, operating systems, and software licenses.",
    "Network Support": "For connectivity issues, including Wi-Fi, VPN, and internet access problems.",
    "User Access Management": "For requests related to password resets, account lockouts, and permissions."
}

SUPPORT_GROUPS_1 = {
    "Hardware Support": (
        "Handles all issues related to the physical components of IT infrastructure. "
        "This includes diagnostics, repair, replacement, and lifecycle management of physical devices."
        "\n\t- Responsibilities: Laptops, desktops, monitors, keyboards, mice, printers, scanners, desk phones, and other peripherals."
        "\n\t- Common Tasks: Fixing broken hardware, setting up new workstations, managing inventory, and handling warranty claims."
    ),
    "Software Support": (
        "Manages issues concerning applications, operating systems, and productivity tools. "
        "This team ensures that all software is correctly installed, configured, licensed, and functional."
        "\n\t- Responsibilities: Operating Systems (Windows, macOS), Microsoft Office 365, Adobe Creative Suite, CRM/ERP systems, and other business-specific applications."
        "\n\t- Common Tasks: Installing software, troubleshooting application errors, managing software licenses, and applying updates and patches."
    ),
    "Network Support": (
        "Focuses on all aspects of network connectivity to ensure reliable access to internal and external resources. "
        "They troubleshoot and maintain the infrastructure that connects our organization."
        "\n\t- Responsibilities: Wi-Fi, Local Area Network (LAN), Wide Area Network (WAN), Virtual Private Network (VPN), and general internet connectivity."
        "\n\t- Common Tasks: Resolving Wi-Fi connection issues, diagnosing slow network speeds, configuring VPN access, and managing firewall rules."
    ),
    "User Access Management": (
        "Controls user identity and access to company resources. "
        "This is a critical security function focused on ensuring users have the appropriate level of access—no more, no less."
        "\n\t- Responsibilities: User account lifecycle, security groups, and access permissions for files, folders, and applications."
        "\n\t- Common Tasks: Creating new user accounts, performing password resets, unlocking accounts, modifying user permissions, and conducting access audits."
    ),
    "Data & Database Services": (
        "Manages the organization's data infrastructure, including databases and data storage systems. "
        "This team handles data integrity, security, and availability."
        "\n\t- Responsibilities: SQL/NoSQL databases, data warehousing, storage area networks (SAN), and data backup and recovery systems."
        "\n\t- Common Tasks: Running data queries, troubleshooting database connection issues, managing data backups, and restoring lost data."
    ),
    "Security & Compliance": (
        "Oversees all information security operations to protect the organization from cyber threats and ensure regulatory compliance. "
        "They manage security tools and respond to security incidents."
        "\n\t- Responsibilities: Antivirus/antimalware software, intrusion detection systems, email filtering, and data loss prevention (DLP)."
        "\n\t- Common Tasks: Investigating phishing attempts, managing security alerts, performing vulnerability scans, and ensuring compliance with standards like GDPR or ISO 27001."
    ),
    "Unclassified": (
        "A temporary holding queue for tickets that are ambiguous, poorly defined, or do not clearly fit into any other category. "
        "A support lead typically reviews and reassigns these tickets to the appropriate team."
    )
}

# Define prompt templates
REVISE_DETAIL_PROMPT = """
You are an expert at creating concise and clear support ticket descriptions and subjects.
Your task is to take a given "rough text" about a technical issue and transform it into a professional, well-structured support ticket and return a JSON output.

**Here are the rules:**

1. **If the "rough text" is already a clear, concise, and complete description of a technical issue, including necessary details and a clear problem statement, then simply output the text as is, without any changes.** In this case, you should still attempt to extract a short, appropriate subject line.

2. **If the "rough text" is vague, contains grammatical errors, is too brief, or uses informal language, then rewrite it.**

* **Subject Line:** Create a **short, descriptive subject line** (under 10 words) that summarizes the core issue.

* **Paragraph Description:** Frame the main issue into a **single, clear, and properly structured paragraph**.
* Start by stating the problem directly.
* Briefly mention any troubleshooting steps already attempted.
* Do not add any information that is not mentioned by the user
* Keep it professional and easy to understand for a support agent.

**Output in JSON Format:**
subject: [Your Generated or Extracted Subject]
description: [Your Generated or Original Paragraph]

---

**Example Rough Input:**
"laptop not starting... plugged and unplugged charger... still not working.. pls help"

**Example Well-Formed Input:**
"My workstation's primary monitor is not displaying any output. I have verified all cable connections and restarted the system, but the issue persists. All other peripherals are functioning correctly."

---

Now, process the following rough text:
{rough_text}
"""

SUGGEST_SUPPORT_PROMPT = """
You are an intelligent IT support ticket assignment agent. Your task is to analyze a new support ticket and assign it to the correct support group.

Here are the available support groups and their responsibilities:
{group_definitions}

Analyze the following ticket and determine the most appropriate support group.

Ticket Subject: {subject}
Ticket Description: {description}

Provide only the name of the correct support group as your answer. Do not add any other text. Do not add anything after your answer.
"""