import imaplib
import sys
from email import policy
from email.parser import BytesParser


class EmailClient:
    def __init__(self, server, email, password):
        print("Initializing EmailClient")
        self.server = server
        self.email = email
        self.password = password
        self.imap_connection = None

    def connect_imap(self):
        print(f"Connecting securely to IMAP server: {self.server}")

        try:
            self.imap_connection = imaplib.IMAP4_SSL(
                self.server,
                993
            )

            print("Logging in to IMAP")
            status, response = self.imap_connection.login(
                self.email,
                self.password
            )

            if status == "OK":
                print("IMAP login successful")
                return True

            print(f"IMAP login failed: {response}")
            return False

        except Exception as e:
            print(f"Error connecting to IMAP: {e}")
            self.imap_connection = None
            return False

    def list_mailboxes(self):
        if not self.imap_connection:
            return []

        print("Listing IMAP mailboxes")

        try:
            status, mailboxes = self.imap_connection.list()

            if status != "OK":
                print("Unable to list mailboxes")
                return []

            mailbox_list = []

            for mailbox in mailboxes:
                if not mailbox:
                    continue

                decoded = mailbox.decode("utf-8", errors="replace")
                print(f"Mailbox: {decoded}")

                parts = decoded.split(' "/" ')
                mailbox_name = parts[-1].strip('"')

                if "\\Noselect" not in decoded:
                    mailbox_list.append(mailbox_name)

            return mailbox_list

        except Exception as e:
            print(f"Error listing mailboxes: {e}")
            return []

    def select_mailbox(self, mailbox="INBOX"):
        if not self.imap_connection:
            return False

        print(f"Selecting IMAP mailbox: {mailbox}")

        try:
            status, _ = self.imap_connection.select(
                f'"{mailbox}"'
            )

            if status != "OK":
                print(f"Failed to select mailbox: {mailbox}")
                return False

            return True

        except Exception as e:
            print(f"Error selecting mailbox {mailbox}: {e}")
            return False

    def fetch_imap_emails(self, search_criterion="ALL"):
        if not self.imap_connection:
            return []

        print(
            f"Fetching IMAP emails with criterion: "
            f"{search_criterion}"
        )

        try:
            status, messages = self.imap_connection.search(
                None,
                search_criterion
            )

            print(
                f"IMAP Search status: {status}, "
                f"Messages: {messages}"
            )

            if status == "OK" and messages:
                email_ids = messages[0].split()
                print(f"Found {len(email_ids)} email(s)")
                return email_ids

        except Exception as e:
            print(f"Error fetching emails: {e}")

        return []

    def get_imap_email(self, email_id):
        if not self.imap_connection:
            return None

        print(f"Fetching IMAP email ID: {email_id}")

        try:
            status, msg_data = self.imap_connection.fetch(
                email_id,
                "(RFC822)"
            )

            print(f"IMAP Fetch status: {status}")

            if status != "OK":
                return None

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    raw_email = response_part[1]

                    email_message = BytesParser(
                        policy=policy.default
                    ).parsebytes(raw_email)

                    print("IMAP Email fetched successfully")
                    return email_message

        except Exception as e:
            print(f"Error fetching email ID {email_id}: {e}")

        return None

    def parse_email(self, email_message):
        print("Parsing email")

        subject = email_message.get(
            "Subject",
            "(No Subject)"
        )

        sender = email_message.get(
            "From",
            "(Unknown Sender)"
        )

        receiver = email_message.get(
            "To",
            "(Unknown Recipient)"
        )

        print("\n" + "=" * 60)
        print(f"From: {sender}")
        print(f"To: {receiver}")
        print(f"Subject: {subject}")

        print("Body:")

        body = ""

        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                disposition = str(
                    part.get("Content-Disposition", "")
                )

                if (
                    content_type == "text/plain"
                    and "attachment" not in disposition
                ):
                    try:
                        body = part.get_content()
                    except Exception:
                        body = part.get_payload(
                            decode=True
                        ).decode(
                            "utf-8",
                            errors="replace"
                        )

                    break
        else:
            try:
                body = email_message.get_content()
            except Exception:
                payload = email_message.get_payload(
                    decode=True
                )

                if payload:
                    body = payload.decode(
                        "utf-8",
                        errors="replace"
                    )

        print(body)
        print("=" * 60 + "\n")

        return subject, sender, receiver, body

    def close_imap(self):
        if self.imap_connection:
            print("Closing IMAP connection")

            try:
                self.imap_connection.logout()
                print("IMAP Logout successful")
            except Exception as e:
                print(f"Error during logout: {e}")

            self.imap_connection = None


def display_usage():
    print(
        "Usage: python3 IMAP_Client.py "
        "<server> <username> <password>"
    )


if __name__ == "__main__":

    if len(sys.argv) != 4:
        display_usage()
        sys.exit(1)

    server = sys.argv[1]
    email = sys.argv[2]
    password = sys.argv[3]

    print("Creating EmailClient instance")

    client = EmailClient(
        server,
        email,
        password
    )

    print("Connecting to the IMAP server")

    if not client.connect_imap():
        print("Could not connect to the IMAP server.")
        sys.exit(1)

    print("Listing IMAP mailboxes")

    mailboxes = client.list_mailboxes()

    for mailbox in mailboxes:

        print(f"Selecting IMAP mailbox: {mailbox}")

        if not client.select_mailbox(mailbox):
            continue

        email_ids = client.fetch_imap_emails()

        for email_id in email_ids:

            print(
                f"Processing IMAP email ID: "
                f"{email_id.decode(errors='replace')}"
            )

            email_message = client.get_imap_email(
                email_id
            )

            if email_message:
                client.parse_email(email_message)

    client.close_imap()