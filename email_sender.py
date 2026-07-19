import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()


class EmailSender:

    def __init__(self):

        self.username = os.getenv("EMAIL_USER")
        self.password = os.getenv("EMAIL_PASSWORD")
        self.receiver = os.getenv("EMAIL_TO")

    def send(self, screener_name, stocks):

        if not stocks:
            print("No stocks to email.")
            return

        html = f"""
        <html>
        <body>

        <h2>{screener_name}</h2>

        <p>Total Stocks : <b>{len(stocks)}</b></p>

        <table border="1" cellpadding="5" cellspacing="0">
            <tr>
                <th>Symbol</th>
                <th>Close</th>
                <th>Volume</th>
            </tr>
        """

        for stock in stocks:

            html += f"""
            <tr>
                <td>{stock['symbol']}</td>
                <td>{stock['close']}</td>
                <td>{stock['volume']}</td>
            </tr>
            """

        html += """
        </table>

        </body>
        </html>
        """

        msg = MIMEMultipart("alternative")

        msg["Subject"] = f"{screener_name} Alert"

        msg["From"] = self.username

        msg["To"] = self.receiver

        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:

            smtp.starttls()

            smtp.login(self.username, self.password)

            smtp.send_message(msg)

        print("Email sent successfully.")