from flask import Flask, render_template, request, jsonify, flash
import mysql.connector as c1234
import random
import webbrowser
import random
import language_tool_python  
import os 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#from gtts import gTTS
import os
import spam_model

app = Flask(__name__)

class Global:
    c = ""
    name = ""
    length = 0
    regName = ''
    regPass = ''
    regEmail = ''
    regPhone = ''
    otp = ''
    message = ''
    msgs = ''

g = Global()
con = c1234.connect(host="localhost", user="root",
                        passwd="hari@9RUSHI", database="vmail")
cursor = con.cursor()

def spam_filter(email):
    # Vectorize the email text
    vectorizer, model = spam_model.load_data()
    vectorized_email = vectorizer.transform([email])

    # Make a prediction on the email
    prediction = model.predict(vectorized_email)

    if prediction[0] == 1:
        return 1
    else:
        return 0


def registration_sucessful(reciever):
    sender_email = '20b01a05c6@svecw.edu.in'
    sender_password = 'hari@9RUSHI'  # Your email account password
    recipient_email = reciever
    smtp_server = 'smtp.gmail.com'  # SMTP server for Gmail
    # Create an email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = "Vmail : Registration Sucessfull" 
    body = "Your account have been created please login"
    message.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP(smtp_server, 587) # Creating an SMTP (Simple Mail Transfer Protocol) server instance
        server.starttls() # Initiating a secure connection using Transport Layer Security (TLS)
        server.login(sender_email, sender_password) # Logging into the email account on the SMTP server
        text = message.as_string() # Converting the email message to a string
        server.sendmail(sender_email, recipient_email, text) # Sending the email
        server.quit() # Closing the connection to the SMTP server
        print("Email sent successfully!")
    except Exception as e:
        return render_template('error_page.html',  error_message="An error occured" + str(e))
    
def sendOtpMail(reciever):
    sender_email = '20b01a05c6@svecw.edu.in'
    sender_password = 'hari@9RUSHI'  # Your email account password
    recipient_email = reciever
    smtp_server = 'smtp.gmail.com'  # SMTP server for Gmail
    # Create an email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = "Vmail : Thanks for your interest in Vmail" 
    otp = ''
    for i in range(6):
        otp += str(random.randint(1, 9))
    g.otp = otp
    body = "Please use this otp to complete registration process" + g.otp
    message.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP(smtp_server, 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = message.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        return render_template('error_page.html',  error_message="An error occured" + str(e))

def send_mail(sender, reciever, subject, msg, name):
    sender_email = '20b01a05c6@svecw.edu.in'
    sender_password = 'hari@9RUSHI'  
    recipient_email = reciever
    smtp_server = 'smtp.gmail.com' 
    msg = msg.split(' ')[:2]
    msg = ' '.join(msg)
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = "Vmail : Message from " + name
    body = "You have got an msg from " + sender + "  message : " + msg + " View in vmail app"
    message.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP(smtp_server, 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = message.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        return render_template('error_page.html', error_message=str(e))

def grammarCorrection(text):
    my_tool = language_tool_python.LanguageTool('en-US')  
    my_text = text
    my_matches = my_tool.check(my_text)  
    myMistakes = []  
    myCorrections = []  
    startPositions = []  
    endPositions = []  
    for rules in my_matches:  
        if len(rules.replacements) > 0:  
            startPositions.append(rules.offset)  
            endPositions.append(rules.errorLength + rules.offset)  
            myMistakes.append(my_text[rules.offset : rules.errorLength + rules.offset])  
            myCorrections.append(rules.replacements[0])  
    my_NewText = list(my_text)   
    for n in range(len(startPositions)):  
        for i in range(len(my_text)):  
            my_NewText[startPositions[n]] = myCorrections[n]  
            if (i > startPositions[n] and i < endPositions[n]):  
                my_NewText[i] = ""  
    
    my_NewText = "".join(my_NewText)  
    return my_NewText

@app.route('/')
def index():
    return render_template('registration.html')

def get_email_suggestions(prefix):
    con = c1234.connect(host="localhost", user="root",
                        passwd="hari@9RUSHI", database="vmail")
    cursor = con.cursor()
    cursor.execute("SELECT email FROM logindetails WHERE email LIKE '{}' LIMIT 5".format(prefix + '%',))
    suggestions = [row[0] for row in cursor.fetchall()]
    con.close()
    return suggestions

# Endpoint for autocomplete suggestions
@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    prefix = request.args.get('prefix', '')
    suggestions = get_email_suggestions(prefix)
    return jsonify(suggestions=suggestions)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/composeMail')
def composeMail():
    return render_template('compose.html', message = g.length)


@app.route('/ValidateAdmin', methods=['POST'])
def ValidateAdmin():
    con = c1234.connect(host="localhost", user="root",
                        passwd="hari@9RUSHI", database="vmail")
    query = "select * from admin2"
    image_dir = 'temp_images'
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    cursor = con.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    text = []
    subject = []
    send = []
    key = []
    to = []
    
    for i in records:
        subject.append(i[1])
        text.append(i[2])
        key.append(i[3])
        send.append(i[0])
        to.append(i[4])

    actualSub = []
    actualTxt = []
    for i in range(len(subject)):
        sub = ''
        txt = ''
        subjectDecrypt = subject[i].split()
        textDecrypt = text[i].split()
        k = key[i]
        for i in subjectDecrypt:
            for j in i:
                sub += chr((k.index(j) + 65))
            sub += ' '
        for i in textDecrypt:
            for j in i:
                txt += chr((k.index(j) + 65))
            txt += ' '
        actualSub.append(sub)
        actualTxt.append(txt)

    table = '<table border="1"><tr><th>Sender</th><th>Subject</th><th>Text</th><th>Receiver</th><th>Image</th></tr>'
    
    answer = []
    tbl = "<tr><td>To</td><td>Subject</td><td>Text</td><td>From</td><td>image</td></tr>"
    answer1 = [0] * (len(text) + 1)
    answer1[0] = tbl
    for i in range(len(text)):
        answer = []
        a = "<tr><td>%s</td>" % to[i]
        answer.append(a)
        a1 = "<td>%s</td>" % actualSub[i]
        answer.append(a1)
        a2 = "<td>%s</td>" % actualTxt[i]
        answer.append(a2)
        a3 = "<td>%s</td></tr>" % send[i]
        answer.append(a3)
        a4 = ''
        image_data = records[i][6]
        image_name = records[i][5]
        if image_data != '' and image_name != '':
            image_path = os.path.join(image_dir, image_name)
            with open(image_path, 'wb') as img_file:
                img_file.write(image_data)
                
            a4 = f'<td><img src="C://Users/Harshita/vmail/temp_images/{image_name}" alt="{image_name}" width="100" height="100"></td></tr>'
        answer.append(a4)
        answer1[i + 1] = answer


    if len(answer1) == 1:
        contents = '''<!DOCTYPE html>
            <html>
            <head>
            <meta content = "text/html; charset = UTF-8"
            http-equip = "content-type">
            </head>
            <body>
            <center>
            <h3> No Recieved items found </h3>
            </center>
            </body>
            </html>
            '''
    else:
        contents = '''<!DOCTYPE html>
                <html>
                <head>
                <meta content = "text/html; charset = UTF-8"
                http-equip = "content-type">
                <style>
                td {
                    padding :0 15px;
                }
                </style>
                <title>Time Table</title>
                </head>
                <body>
                    <div class="card" id="generatePDF">

                <br><br>
                <center>
                <table border = 1>
                %s
                </table>
                <br><br>
                
                <button id="pdfButton"><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTzxA1IZaV_fN96xiySAwgY5iZiM-pIg9W9ig&usqp=CAU" style="height:30px;width:30px;"><b style="padding-bottom:5px;" class="text"> <center>&nbsp; &nbsp Download</center></b></button>
    
    </div>
    </center>
        <script>
        var button = document.getElementById("pdfButton");
        var makepdf = document.getElementById("generatePDF");
        button.addEventListener("click", function () {
            var mywindow = window.open("", "PRINT", "height=600,width=600");
            mywindow.document.write(makepdf.innerHTML);
            mywindow.document.close();
            mywindow.focus();
            mywindow.print();
            return true;
        });
    </script>

                </body>
                </html>
                ''' % (answer1)
    filename = 'demo39.html'

    def main(contents, filename):
        output = open(filename, "w")
        output.write(contents)
        output.close()
    main(contents, filename)
    webbrowser.open(filename)
    return render_template('demo3.html')

@app.route('/Spam')
def Spam():
    query = "SELECT id, subject, text, sender, kys, timestamp_value FROM admin2 WHERE receiver = '{}' AND spam = 1 ORDER BY timestamp_value DESC".format(g.c)
    cursor.execute(query)
    message = cursor.fetchall()
    subject = []
    text = []
    keys = []
    for i in message:
        subject.append(i[1])
        text.append(i[2])
        keys.append(i[4])
    actualText = []
    actualSub = []
    
    for i in range(len(subject)):
        sub = ''
        txt = ''
        subjectDecrypt = subject[i].split()
        textDecrypt = text[i].split()
        k = keys[i]
        for i in subjectDecrypt:
            for j in i:
                try:
                    sub += chr((k.index(j) + 65))
                except:
                    sub += j
            sub += ' '
        for i in textDecrypt:
            for j in i:
                try:
                    txt += chr((k.index(j) + 65))
                except:
                    txt += j
            txt += ' '
        actualSub.append(sub)
        actualText.append(txt)
    messages = []
    for i in range(len(message)):
        a = []
        a.append(message[i][0])
        a.append(actualSub[i])
        a.append(actualText[i][:5])
        x = message[i][3].split('@')[0]
        x = x + (' ' * (100 - len(x) if len(x) < 100 else 0))
        a.append(x)
        a.append(message[i][5])
        messages.append(a)
    g.length = len(message)

    return render_template('spam.html', messages=messages, length = len(message))

@app.route('/inbox')
def inbox():
    query = "SELECT id, subject, text, sender, kys, timestamp_value FROM admin2 WHERE receiver = '{}' ORDER BY timestamp_value DESC".format(g.c)
    cursor.execute(query)
    message = cursor.fetchall()
    subject = []
    text = []
    keys = []
    for i in message:
        subject.append(i[1])
        text.append(i[2])
        keys.append(i[4])
    actualText = []
    actualSub = []
    
    for i in range(len(subject)):
        sub = ''
        txt = ''
        subjectDecrypt = subject[i].split()
        textDecrypt = text[i].split()
        k = keys[i]
        for i in subjectDecrypt:
            for j in i:
                try:
                    sub += chr((k.index(j) + 65))
                except:
                    sub += j
            sub += ' '
        for i in textDecrypt:
            for j in i:
                try:
                    txt += chr((k.index(j) + 65))
                except:
                    txt += j
            txt += ' '
        actualSub.append(sub)
        actualText.append(txt)
    messages = []
    for i in range(len(message)):
        a = []
        a.append(message[i][0])
        a.append(actualSub[i])
        a.append(actualText[i][:5])
        x = message[i][3].split('@')[0]
        x = x + (' ' * (100 - len(x) if len(x) < 100 else 0))
        a.append(x)
        a.append(message[i][5])
        messages.append(a)
    g.length = len(message)

    return render_template('userDash.html', messages=messages, length = len(message))

@app.route('/ValidateUser', methods=['POST'])
def ValidateUser():
    name1 = request.form['uname']
    passw = request.form['password']
    con = c1234.connect(host="localhost", user="root",
                        passwd="hari@9RUSHI", database="vmail")
    query = "select * from logindetails"
    cursor = con.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    print(records)
    for i in records:
        if i[0] == name1 and i[1] == passw:
            g.c = i[2]
            g.name = i[0]
            query = "SELECT id, subject, text, sender, kys, timestamp_value FROM admin2 WHERE receiver = '{}' ORDER BY timestamp_value DESC".format(g.c)
            cursor.execute(query)
            message = cursor.fetchall()
            subject = []
            text = []
            keys = []
            for i in message:
                subject.append(i[1])
                text.append(i[2])
                keys.append(i[4])
            actualText = []
            actualSub = []
           
            for i in range(len(subject)):
                sub = ''
                txt = ''
                subjectDecrypt = subject[i].split()
                textDecrypt = text[i].split()
                k = keys[i]
                for i in subjectDecrypt:
                    for j in i:
                        try:
                            sub += chr((k.index(j) + 65))
                        except:
                            sub += j
                    sub += ' '
                for i in textDecrypt:
                    for j in i:
                        try:
                            txt += chr((k.index(j) + 65))
                        except:
                            txt += j
                    txt += ' '
                actualSub.append(sub)
                actualText.append(txt)
            messages = []
            for i in range(len(message)):
                a = []
                a.append(message[i][0])
                a.append(actualSub[i])
                a.append(actualText[i][:10])
                a.append(message[i][3]) 
                a.append(message[i][5])
                messages.append(a)

            g.length = len(message)
            return render_template('userDash.html', messages=messages, length = len(message))
    

@app.route('/message/<int:message_id>')
def message(message_id):
    # Fetch the selected message from the database 
    cursor.execute("SELECT subject, text, sender, receiver, timestamp_value, kys, name, image_data FROM admin2 WHERE id = %s", (message_id,))
    message = cursor.fetchone()
    print(message)
    message = list(message)
    name = message[6]
    image_data = message[7]
    image_dir = 'static'
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    key = message[5]
    sub = ''
    txt = ''
    subjectDecrypt = message[0].split()
    textDecrypt = message[1].split()
    k = key
    for i in subjectDecrypt:
        for j in i:
            try:
                sub += chr((k.index(j) + 65))
            except:
                sub += j
        sub += ' '
    for i in textDecrypt:
        for j in i:
            try:
                txt += chr((k.index(j) + 65))
            except:
                txt += j
        txt += ' '
    a4 = ''
    if image_data != '' and name != '':
        image_path = os.path.join(image_dir, name)
        with open(image_path, 'wb') as img_file:
            img_file.write(image_data)
            
        a4 = name
        
    message[0] = sub 
    message[1] = txt
    message[6] = a4
    print(message[:len(message) - 1])
    g.message = txt
    g.msgs = message 
    return render_template('message.html', message=message, length = g.length)

def text_to_speech(text, language='en', output_file='static/output.mp3'):
    # Create a gTTS object
    tts = gTTS(text=text, lang=language, slow=False)

    # Save the audio file
    tts.save(output_file)

    return output_file

@app.route('/convert', methods=['POST'])
def convert():
    if request.method == 'POST':
        text = g.message
        output_file = text_to_speech(text)
        return render_template('message.html', message=g.msgs, length = g.length, audio_file=output_file)

@app.route('/Registration')
def Registration():
    return render_template('registration.html')


@app.route('/otp', methods=['POST'])
def otp():
    otp = request.form['otp']
    print(otp, g.otp)
    if otp == g.otp:
        con = c1234.connect(host="localhost", user="root",
                        passwd="hari@9RUSHI", database="vmail")
        cursor = con.cursor()
        registration_sucessful(g.regEmail)
        mySql_insert_query = "INSERT INTO logindetails VALUES ('{}', '{}', '{}', '{}')".format(
            g.regName, g.regPass, g.regEmail, g.regPhone)
        cursor = con.cursor()
        cursor.execute(mySql_insert_query)
        con.commit()
        return render_template('RegistrationSucess.html')
    return render_template('invalidOtp.html')


@app.route('/registerUser', methods=['POST'])
def registerUser():
    name1 = request.form['uname']
    email1 = request.form['email']
    passw = request.form['password']
    phonenum = request.form['phonenum']
    g.regName = name1 
    g.regEmail = email1 
    g.regPass = passw 
    g.regPhone = phonenum
    con = c1234.connect(host="localhost", user="root",
                        passwd="hari@9RUSHI", database="vmail")
    query = "select * from logindetails where uname = '{}' or password = '{}' or email = '{}' or mobilenum = '{}'".format(name1, passw, email1, phonenum)
    cursor = con.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    if len(records) >= 1:
        return render_template('error_page.html', error_message= "An error occured" + "user name or password exist") 
    sendOtpMail(email1)
    return render_template('otp.html')

@app.route('/correct', methods=['POST'])
def correct_text():
    text = request.form['text']
    # Perform grammar and error correction here
    tool = language_tool_python.LanguageTool('en-US')
    corrected_text = tool.correct(text)
    return jsonify({'corrected_text': corrected_text})

@app.route('/email', methods=['POST'])
def email():
    reciever = request.form['reciever']
    subject = request.form['subject']
    message = request.form['message']
    sender = g.c
    image = request.files['image']
    con = c1234.connect(host="localhost", user="root",
                        passwd="hari@9RUSHI", database="vmail")
    query = "select * from logindetails where email = '{}'".format(reciever)
    cursor = con.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    print(len(records))
    if len(records) == 0:
        return render_template('error_page.html', error_message=  "An error occured" + "Please check the mail id")
    
    con = c1234.connect(host="localhost", user="root",
                        passwd="hari@9RUSHI", database="vmail")
    subject = grammarCorrection(subject)
    message = grammarCorrection(message)
    spam = spam_filter(message)
    send_mail(sender, reciever, subject, message, g.name)
    subject = subject.upper()
    message = message.upper()
    hm = {}
    key = ''
    alpha = [i for i in range(26)]
    for i in range(26):
        x = random.randint(0, len(alpha) - 1)
        x = alpha[x]
        hm[chr(i + ord('A'))] = chr(x + ord('A'))
        key += chr(x + ord('A'))
        alpha.remove(x)
    subject.upper()
    message.upper()
    subject = subject.split()
    encryptedSub = ''
    for i in subject:
        for j in i:
            if j in key:
                encryptedSub += hm[j]
            else:
                encryptedSub += j

        encryptedSub += " "
    encryptedMessage = ''
    message = message.split()
    for i in message:
        for j in i:
            try:
                encryptedMessage += hm[j]
            except:
                encryptedMessage += j
        encryptedMessage += " "
    image_data, image_name = '', ''
    if image:
        # Read image data
        image_data = image.read()
        image_name = image.filename

    mySql_insert_query = "INSERT INTO admin2 (sender, subject, text, kys, receiver, name, image_data, spam) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    values = (sender, encryptedSub, encryptedMessage, key, reciever, image_name, image_data, spam)

    cursor = con.cursor()
    cursor.execute(mySql_insert_query, values)
    con.commit()


    return render_template('login.html')
   

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if request.method == 'POST':
        image = request.files['image']
        if image:
            # Read image data
            image_data = image.read()
            image_name = image.filename

            # Insert image data into the database
            con = c1234.connect(host="localhost", user="root",
                        passwd="hari@9RUSHI", database="vmail")
            cursor = con.cursor()
            cursor.execute("INSERT INTO images (name, image_data) VALUES (%s, %s)", (image_name, image_data))
            con.commit()

    return render_template('login.html')

@app.route('/SendMail')
def SendMail():
    query = "SELECT id, subject, text, receiver, kys, timestamp_value FROM admin2 WHERE sender = '{}' ORDER BY timestamp_value DESC".format(g.c)
    cursor.execute(query)
    message = cursor.fetchall()
    subject = []
    text = []
    keys = []
    for i in message:
        subject.append(i[1])
        text.append(i[2])
        keys.append(i[4])
    actualText = []
    actualSub = []
    
    for i in range(len(subject)):
        sub = ''
        txt = ''
        subjectDecrypt = subject[i].split()
        textDecrypt = text[i].split()
        k = keys[i]
        for i in subjectDecrypt:
            for j in i:
                try:
                    sub += chr((k.index(j) + 65))
                except:
                    sub += j
            sub += ' '
        for i in textDecrypt:
            for j in i:
                try:
                    txt += chr((k.index(j) + 65))
                except:
                    txt += j
            txt += ' '
        actualSub.append(sub)
        actualText.append(txt)
    messages = []
    for i in range(len(message)):
        a = []
        a.append(message[i][0])
        a.append(actualSub[i])
        a.append(actualText[i][:5])
        x = message[i][3].split('@')[0]
        x = x + (' ' * (100 - len(x) if len(x) < 100 else 0))
        a.append(x)
        a.append(message[i][5])
        messages.append(a)

    return render_template('sentMail.html', messages=messages, length = g.length)

@app.route('/RecievedMail')
def RecievedMail():
    con = c1234.connect(host="localhost", user="root",
                        passwd="hari@9RUSHI", database="vmail")
    query = "select sender, subject, text, kys, receiver, name, image_data from admin2 ORDER BY timestamp_value DESC"
    cursor = con.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    image_dir = 'temp_images'
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    text = []
    subject = []
    send = []
    key = []
    imageName = []
    imageData = []
    for i in records:
        if i[4] == g.c:
            subject.append(i[1])
            text.append(i[2])
            key.append(i[3])
            send.append(i[0])
            imageName.append(i[5])
            imageData.append(i[6])

    actualSub = []
    actualTxt = []
    for i in range(len(subject)):
        sub = ''
        txt = ''
        subjectDecrypt = subject[i].split()
        textDecrypt = text[i].split()
        k = key[i]
        for i in subjectDecrypt:
            for j in i:
                sub += chr((k.index(j) + 65))
            sub += ' '
        for i in textDecrypt:
            for j in i:
                txt += chr((k.index(j) + 65))
            txt += ' '
        actualSub.append(sub)
        actualTxt.append(txt)
    answer = []
    tbl = "<tr><td>To</td><td>Subject</td><td>Text</td><td>From</td><td>image</td></tr>"
    answer1 = [0] * (len(text) + 1)
    answer1[0] = tbl
    for i in range(len(text)):
        answer = []
        a = "<tr><td>%s</td>" % g.c
        answer.append(a)
        a1 = "<td>%s</td>" % actualSub[i]
        answer.append(a1)
        a2 = "<td>%s</td>" % actualTxt[i]
        answer.append(a2)
        a3 = "<td>%s</td></tr>" % send[i]
        answer.append(a3)
        a4 = ''
        image_data = imageData[i]
        image_name = imageName[i]
        if image_data != '' and image_name != '':
            image_path = os.path.join(image_dir, image_name)
            with open(image_path, 'wb') as img_file:
                img_file.write(image_data)
                
            a4 = f'<td><img src="C://Users/Harshita/vmail/temp_images/{image_name}" alt="{image_name}" width="100" height="100"></td></tr>'
        answer.append(a4)
        answer1[i + 1] = answer
    if answer1 == []:
        contents = '''<!DOCTYPE html>
            <html>
            <head>
            <meta content = "text/html; charset = UTF-8"
            http-equip = "content-type">
            </head>
            <body>
            <center>
            <h3> No Recieved items found </h3>
            </center>
            </body>
            </html>
            '''
    else:
        contents = '''<!DOCTYPE html>
                <html>
                <head>
                <meta content = "text/html; charset = UTF-8"
                http-equip = "content-type">
                <style>
                td {
                    padding :0 15px;
                }
                </style>
                <title>Time Table</title>
                </head>
                <body>
                    <div class="card" id="generatePDF">

                <br><br>
                <center>
                <table border = 1>
                %s
                </table>
                <br><br>
                
                <button id="pdfButton"><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTzxA1IZaV_fN96xiySAwgY5iZiM-pIg9W9ig&usqp=CAU" style="height:30px;width:30px;"><b style="padding-bottom:5px;" class="text"> <center>&nbsp; &nbsp Download</center></b></button>
    
    </div>
    </center>
        <script>
        var button = document.getElementById("pdfButton");
        var makepdf = document.getElementById("generatePDF");
        button.addEventListener("click", function () {
            var mywindow = window.open("", "PRINT", "height=600,width=600");
            mywindow.document.write(makepdf.innerHTML);
            mywindow.document.close();
            mywindow.focus();
            mywindow.print();
            return true;
        });
    </script>

                </body>
                </html>
                ''' % (answer1)
    filename = 'demo37.html'

    def main(contents, filename):
        output = open(filename, "w")
        output.write(contents)
        output.close()
    main(contents, filename)
    webbrowser.open(filename)
    return render_template('demo3.html')

app.secret_key = 'secret123'
app.run(debug=True)