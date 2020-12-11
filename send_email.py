import smtplib
import ssl

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "backenddatabase4185@gmail.com"  # Enter your address
password = "dbuserdbuser"


def send_email(data):
    receiver_email = data["buyer_uni"]+"@columbia.edu"  # Enter receiver address
    receiver_email2 = data["seller_uni"]+"@columbia.edu"
    message = """Subject: Order confirmation # {} \n
    \n
    Buyer: {}
    Seller: {}
    Amount: {}
    Status: {}
    """.format(data["order_id"], data["buyer_uni"], data["seller_uni"], data["transaction_amt"],  data["status"])
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        server.sendmail(sender_email, receiver_email2, message)
        print("Successfully sent email")
