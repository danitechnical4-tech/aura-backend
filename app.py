from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
CORS(app)

# Aapki Email aur App Password
SENDER_EMAIL = "danitechnical4@gmail.com"
EMAIL_PASSWORD = "igvu irxn axjd rtgp"

@app.route('/submit-order', methods=['POST'])
def submit_order():
    try:
        data = request.json
        if not data:
            return jsonify({"status": "error", "message": "No data received"}), 400

        customer_name = data.get('name', 'N/A')
        customer_phone = data.get('phone', 'N/A')
        customer_address = data.get('address', 'N/A')
        product_details = data.get('product_details', 'N/A')

        # Email Message Setup
        subject = f"New Order Received from {customer_name}!"
        body = f"""Naya Order Aaya Hai!

Customer Name: {customer_name}
Phone Number: {customer_phone}
Delivery Address: {customer_address}

Order Details:
{product_details}
"""

        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = SENDER_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Gmail SMTP Connection & Sending Email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, EMAIL_PASSWORD)
        server.sendmail(SENDER_EMAIL, SENDER_EMAIL, msg.as_string())
        server.quit()

        return jsonify({"status": "success", "message": "Order placed and email sent successfully!"}), 200

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)