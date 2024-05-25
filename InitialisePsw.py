import tkinter as tk
from tkinter import messagebox, filedialog
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email():
    sender_email = sender_email_entry.get()
    receiver_email = receiver_email_entry.get()
    subject = subject_entry.get()
    message = message_text.get('1.0', 'end')
    sender_password = ""  

    email = MIMEMultipart()
    email['From'] = sender_email
    email['To'] = receiver_email
    email['Subject'] = subject


    email.attach(MIMEText(message, 'plain'))

    for file_path in attachment_paths:
        attachment = open(file_path, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {file_path.split('/')[-1]}")
        email.attach(part)


    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, email.as_string())
        server.quit()
        messagebox.showinfo("Success", "Email sent successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def add_attachment():
    file_path = filedialog.askopenfilename()
    attachment_paths.append(file_path)
    attachment_label.config(text=f"Attachments: {', '.join(attachment_paths)}")

# Create main window
root = tk.Tk()
root.title("Email Sender")
root.geometry("500x400")

# Create style
font_style = ('Arial', 12)
bg_color = '#f0f0f0'
button_color = '#4CAF50'
button_fg_color = 'white'

# Create labels
sender_email_label = tk.Label(root, text="Sender Email:", font=font_style, bg=bg_color)
sender_email_label.grid(row=0, column=0, sticky='w', padx=10, pady=10)

receiver_email_label = tk.Label(root, text="Receiver Email:", font=font_style, bg=bg_color)
receiver_email_label.grid(row=1, column=0, sticky='w', padx=10, pady=10)

subject_label = tk.Label(root, text="Subject:", font=font_style, bg=bg_color)
subject_label.grid(row=2, column=0, sticky='w', padx=10, pady=10)

message_label = tk.Label(root, text="Message:", font=font_style, bg=bg_color)
message_label.grid(row=3, column=0, sticky='w', padx=10, pady=10)

attachment_label = tk.Label(root, text="Attachments: ", font=font_style, bg=bg_color)
attachment_label.grid(row=4, column=0, sticky='w', padx=10, pady=10)

# Create entry fields
sender_email_entry = tk.Entry(root, font=font_style, width=30)
sender_email_entry.grid(row=0, column=1, padx=10, pady=10)

receiver_email_entry = tk.Entry(root, font=font_style, width=30)
receiver_email_entry.grid(row=1, column=1, padx=10, pady=10)

subject_entry = tk.Entry(root, font=font_style, width=30)
subject_entry.grid(row=2, column=1, padx=10, pady=10)

message_text = tk.Text(root, height=10, width=40, font=font_style)
message_text.grid(row=3, column=1, padx=10, pady=10)


add_attachment_button = tk.Button(root, text="Add Attachment", font=font_style, bg=button_color, fg=button_fg_color, command=add_attachment)
add_attachment_button.grid(row=4, column=1, padx=10, pady=10)

send_button = tk.Button(root, text="Send Email", font=font_style, bg=button_color, fg=button_fg_color, command=send_email)
send_button.grid(row=5, column=0, columnspan=2, pady=10)

attachment_paths = []

root.mainloop()
