Email Client Script
This Python script provides a simple interface for interacting with an email server using IMAP. It allows users to:

Connect to an IMAP server
List available mailboxes
Select a mailbox
Fetch and display emails from a mailbox
The script is designed to handle common errors gracefully and display email content in a readable format.

Features

IMAP Connection

Connect securely to an IMAP server using SSL.
Mailbox Management

List all mailboxes on the server.
Select specific mailboxes for email retrieval.
Email Fetching

Fetch emails using search criteria (default: ALL).
Display email subject, sender, and body.
Replace carriage returns (\r\n) with proper newlines for better readability.
Error Handling

Gracefully handle errors during mailbox selection and email fetching.
Continue processing other mailboxes or emails even if an error occurs.
Requirements

Python 3.8+
Modules:
imaplib
Installation

Clone the repository:

git clone https://github.com/josemlwdf/IMAP-Mail-Dumper.git
Navigate to the project directory:

cd IMAP-Mail-Dumper 
Run the script:

python3 IMAP_Client.py
Usage

Configuring the Script

Update the following variables in the script to match your email server and credentials:

server = "your.imap.server"
email/username = "your-email@example.com"
password = "your-password"
Running the Script

Simply execute the script:

python3 IMAP_Client.py mail.google.com myusername mypassword
The script will:

Connect to the IMAP server.
List available mailboxes.
Retrieve emails from each mailbox.
Display the subject, sender, and body of each email.


