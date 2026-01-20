from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from email.message import EmailMessage
from topsis import topsis
import smtplib, ssl
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULT_FOLDER'] = 'results'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        weights = request.form['weights']
        impacts = request.form['impacts']
        email = request.form['email']

        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        output_path = os.path.join(app.config['RESULT_FOLDER'], 'result.csv')

        file.save(input_path)

        # Run TOPSIS
        topsis(input_path, weights, impacts, output_path)

        # Send email
        send_email(email, output_path)

        return "Result sent successfully to your email!"
    
    return render_template('index.html')

def send_email(receiver, file_path):
    sender = "pritish3473@gmail.com"
    password = "quoe ewfj xgtc khid"

    msg = EmailMessage()
    msg['Subject'] = "TOPSIS Result"
    msg['From'] = sender
    msg['To'] = receiver
    msg.set_content("Please find attached the result file.")

    abs_path = os.path.abspath(file_path)

    with open(abs_path, 'rb') as f:
        content = f.read()
        msg.add_attachment(content, maintype='text', subtype='csv', filename='result.csv')

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('results', exist_ok=True)
    app.run(debug=True)
