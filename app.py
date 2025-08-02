from flask import Flask, render_template, request, jsonify
from supabase import create_client, Client
import os
import smtplib

app = Flask(__name__)

# Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')
    
@app.route('/Services')
def services():
    return render_template('Services.html')

@app.route('/projects')
def get_projects():
    return render_template("projects.html")


@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    subject = f"New Contact from {name}"
    body = f"From: {name}\nEmail: {email}\n\nMessage:\n{message}"

    try:
        send_email(subject, body)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def send_email(subject, body):
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.zoho.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))

    from_addr = smtp_user
    to_addr = smtp_user  # send to yourself

    message = f"Subject: {subject}\n\n{body}"

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(from_addr, to_addr, message)

@app.route('/health')
def health_check():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)



