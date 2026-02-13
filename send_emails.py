import csv
import smtplib
import time
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ============ CONFIGURATION ============
GMAIL_ADDRESS = "contact.xray123@gmail.com"       # <-- Ton adresse Gmail
GMAIL_APP_PASSWORD = "zlpt ojvo grcc npzh"  # <-- App Password (pas ton vrai mdp)
CSV_FILE = "X-Ray waitlist - Feuille 1.csv"  # <-- Fichier CSV exporté de Google Sheets
EMAIL_COLUMN = "Email"                       # <-- Nom de la colonne avec les emails (ou index 0)
DELAY_SECONDS = 2                           # <-- Délai entre chaque envoi (évite le spam)

SUBJECT = "X-RAY — Early Access Launch"

HTML_BODY = """\
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="color-scheme" content="dark">
  <meta name="supported-color-schemes" content="dark">
  <style>
    :root { color-scheme: dark; supported-color-schemes: dark; }
    @media (prefers-color-scheme: light) {
      .dark-bg { background-color: #0d0b14 !important; }
      .card-bg { background-color: #13101e !important; }
    }
    u + .body .gscreen { background: #000; mix-blend-mode: screen; }
    u + .body .gdiff { background: #000; mix-blend-mode: difference; }
  </style>
</head>
<body class="body" style="margin: 0; padding: 0; background-color: #0d0b14; background-image: linear-gradient(#0d0b14, #0d0b14); font-family: 'Courier New', Courier, monospace;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color: #0d0b14; background-image: linear-gradient(#0d0b14, #0d0b14);">
    <tr>
      <td align="center" style="padding: 40px 16px;">
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width: 560px; background-color: #13101e; background-image: linear-gradient(#13101e, #13101e); border: 1px solid #2a2438; border-radius: 12px;">

          <!-- Logo -->
          <tr>
            <td align="center" style="padding: 40px 0 20px 0;">
              <img src="https://raw.githubusercontent.com/X-Ray-dot-One/backend-connected-programs/main/front/public/private-logo.png" alt="X-RAY" width="120" style="display: block;" />
            </td>
          </tr>

          <!-- Tag -->
          <tr>
            <td align="center" style="padding: 0 40px 12px 40px;">
              <table role="presentation" cellpadding="0" cellspacing="0">
                <tr>
                  <td style="background-color: #8b5cf6; border-radius: 4px; padding: 4px 14px;">
                    <span style="color: #ffffff; font-size: 11px; font-family: 'Courier New', Courier, monospace; letter-spacing: 2px; text-transform: uppercase;"><span class="gscreen"><span class="gdiff">// EARLY_ACCESS</span></span></span>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Headline -->
          <tr>
            <td align="center" style="padding: 16px 40px 8px 40px;">
              <h1 style="margin: 0; color: #ffffff; font-size: 36px; font-family: 'Courier New', Courier, monospace; font-weight: 700; letter-spacing: -0.5px; line-height: 1.2;">
                <span class="gscreen"><span class="gdiff">It's happening.</span></span>
              </h1>
            </td>
          </tr>

          <!-- Divider -->
          <tr>
            <td align="center" style="padding: 16px 60px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
                <tr><td style="border-top: 1px solid #2a2438;"></td></tr>
              </table>
            </td>
          </tr>

          <!-- Body -->
          <tr>
            <td style="padding: 8px 40px 0 40px;">
              <p style="margin: 0 0 18px 0; color: #ffffff; font-size: 18px; line-height: 1.7; font-family: 'Courier New', Courier, monospace;">
                <span class="gscreen"><span class="gdiff">The first early version of <strong>X-RAY</strong> is now live.</span></span>
              </p>
              <p style="margin: 0 0 24px 0; color: #ffffff; font-size: 18px; line-height: 1.7; font-family: 'Courier New', Courier, monospace;">
                <span class="gscreen"><span class="gdiff">First ones in. First ones to test true anonymity.</span></span>
              </p>
            </td>
          </tr>

          <!-- CTA -->
          <tr>
            <td align="center" style="padding: 0 40px 28px 40px;">
              <table role="presentation" cellpadding="0" cellspacing="0">
                <tr>
                  <td align="center" style="background-color: #8b5cf6; border-radius: 8px;">
                    <a href="https://alpha.x-ray.one/" target="_blank" style="display: inline-block; padding: 14px 36px; color: #ffffff; font-size: 14px; font-family: 'Courier New', Courier, monospace; font-weight: 700; text-decoration: none; letter-spacing: 1px;">
                      ENTER X-RAY &rarr;
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Divider -->
          <tr>
            <td align="center" style="padding: 0 60px 20px 60px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
                <tr><td style="border-top: 1px solid #2a2438;"></td></tr>
              </table>
            </td>
          </tr>

          <!-- Instructions -->
          <tr>
            <td style="padding: 0 40px 8px 40px;">
              <p style="margin: 0 0 6px 0; color: #8b5cf6; font-size: 14px; font-family: 'Courier New', Courier, monospace; letter-spacing: 1px; text-transform: uppercase;">
                &gt; get ready now
              </p>
            </td>
          </tr>
          <tr>
            <td style="padding: 0 40px 28px 40px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color: #1a1628; background-image: linear-gradient(#1a1628, #1a1628); border: 1px solid #2a2438; border-radius: 8px;">
                <tr>
                  <td style="padding: 18px 20px;">
                    <p style="margin: 0 0 10px 0; color: #ffffff; font-size: 16px; font-family: 'Courier New', Courier, monospace; line-height: 1.7;">
                      <span style="color: #8b5cf6;">&rarr;</span>&nbsp; <span class="gscreen"><span class="gdiff">Switch your wallet to <strong>Devnet</strong></span></span>
                    </p>
                    <p style="margin: 0 0 10px 0; color: #ffffff; font-size: 16px; font-family: 'Courier New', Courier, monospace; line-height: 1.7;">
                      <span style="color: #8b5cf6;">&rarr;</span>&nbsp; <span class="gscreen"><span class="gdiff">Connect with <strong>your</strong> wallet</span></span>
                    </p>
                    <p style="margin: 0; color: #ffffff; font-size: 16px; font-family: 'Courier New', Courier, monospace; line-height: 1.7;">
                      <span style="color: #8b5cf6;">&rarr;</span>&nbsp; <span class="gscreen"><span class="gdiff">Unlock <strong>Shadow Mode</strong></span></span>
                    </p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Closing -->
          <tr>
            <td align="center" style="padding: 0 40px 32px 40px;">
              <p style="margin: 0; color: #ffffff; font-size: 15px; font-family: 'Courier New', Courier, monospace;">
                <span class="gscreen"><span class="gdiff">See you on the other side.</span></span>
              </p>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background-color: #0d0b14; background-image: linear-gradient(#0d0b14, #0d0b14); border-radius: 0 0 12px 12px; padding: 24px 40px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td style="color: #4a4460; font-size: 11px; font-family: 'Courier New', Courier, monospace;">
                    &copy; 2026 X-RAY
                  </td>
                  <td align="right">
                    <a href="https://linktr.ee/xrayone" target="_blank" style="color: #8b5cf6; font-size: 11px; font-family: 'Courier New', Courier, monospace; text-decoration: none;">Socials</a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""
# =======================================


def load_emails(csv_path):
    emails = []
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            email = row.get(EMAIL_COLUMN, "").strip()
            if email and "@" in email:
                emails.append(email)
    return emails


def send_email(smtp, to_address):
    msg = MIMEMultipart("alternative")
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = SUBJECT
    msg.attach(MIMEText(HTML_BODY, "html"))
    smtp.sendmail(GMAIL_ADDRESS, to_address, msg.as_string())


def main():
    emails = load_emails(CSV_FILE)
    if not emails:
        print("Aucun email trouvé dans le CSV.")
        sys.exit(1)

    print(f"{len(emails)} emails trouvés.")
    print(f"Sujet: {SUBJECT}")
    print()

    confirm = input(f"Envoyer à {len(emails)} destinataires ? (oui/non): ")
    if confirm.lower() not in ("oui", "o", "yes", "y"):
        print("Annulé.")
        sys.exit(0)

    sent = 0
    failed = []

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        print("Connecté à Gmail SMTP.\n")

        for i, email in enumerate(emails, 1):
            try:
                send_email(smtp, email)
                sent += 1
                print(f"[{i}/{len(emails)}] OK  → {email}")
            except Exception as e:
                failed.append((email, str(e)))
                print(f"[{i}/{len(emails)}] FAIL → {email} ({e})")

            if i < len(emails):
                time.sleep(DELAY_SECONDS)

    print(f"\nTerminé: {sent} envoyés, {len(failed)} échoués.")
    if failed:
        print("\nÉchecs:")
        for email, err in failed:
            print(f"  - {email}: {err}")


if __name__ == "__main__":
    main()
