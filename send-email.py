import smtplib
import traceback
import sys
import configparser
import ast
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from os import path


def check_args():
    arg_length = len(sys.argv)

    if (arg_length <= 1) or (arg_length >= 3):
        print("Illegal number of parameters ")
        print("Usage: python3 send-email.py path/to/git/results/text/file")
        exit(1)


def check_file_exists(filename):
    if path.exists(filename) and path.isfile(filename):
        return True
    else:
        print("File does not exist. Please enter a valid file path name")
        exit(1)


def main(filename):
    configParser = configparser.RawConfigParser()
    configFilePath = r'config.ini'
    configParser.read(configFilePath)

    gmail_user = configParser.get('gmail-config', 'gmail_user')
    gmail_password = configParser.get('gmail-config', 'gmail_password')

    sent_from = gmail_user
    receiver = configParser.get('gmail-config', 'receiver')
    for email in ast.literal_eval(receiver):
        subject = '<SUBJECT>'
        body = '<EMAIL BODY>'

        message = MIMEMultipart()
        message['From'] = sent_from
        message['To'] = email
        message['Subject'] = subject

        attach_file_name = filename
        attach_file = open(attach_file_name, 'rb')
        payload = MIMEBase('application', 'octet-stream')
        payload.set_payload(attach_file.read())
        encoders.encode_base64(payload)
        payload.add_header('Content-Disposition', "attachment; filename= %s" % attach_file_name)

        message.attach(payload)
        message.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(gmail_user, gmail_password)
            text = message.as_string()
            server.sendmail(sent_from, email, text)
            server.close()

            print('Email sent successfully!')

        except Exception:
            print('Something went wrong...')
            print(traceback.format_exc())


if __name__ == "__main__":
    check_args()

    file = sys.argv[1]
    if check_file_exists(file):
        main(file)
