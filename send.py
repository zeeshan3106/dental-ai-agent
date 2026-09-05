import smtplib
import time
from email.message import EmailMessage
Email = "zeeshanalizafar53@gmail.com"

# recipents = [
#     {"email":"zeeshanalizafar032@gmail.com","name":"Zeeshan Ali Zafar"},
#     {"email":"zainhassan3106@gmail.com","name":"Zeeshan"
#     },
#     {"email":"zeeshanalizafar10@gmail.com","name":"Zeeshan"
#     }

# ]


def EmailSend(to_email, name,age,service,desc):
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>

<body style="margin:0; padding:0; background-color:#f5f7fa; font-family:Arial, sans-serif; color:#1f2937;">

    <div style="max-width:600px; margin:40px auto; background:#ffffff; border-radius:12px; overflow:hidden;">

        <!-- Header -->
        <div style="padding:30px 35px; background:#0f766e; color:white;">
            <h1 style="margin:0; font-size:24px; font-weight:600;">
                Melbourne Dentals
            </h1>
            <p style="margin:8px 0 0; font-size:14px; opacity:0.9;">
                Appointment Confirmation
            </p>
        </div>

        <!-- Content -->
        <div style="padding:35px;">

            <p style="font-size:16px; margin-top:0;">
                Hi {name},
            </p>

            <p style="font-size:15px; line-height:1.6; color:#4b5563;">
                Your appointment with Melbourne Dentals has been successfully confirmed.
            </p>

            <h2 style="font-size:17px; margin-top:30px; color:#111827;">
                Appointment Details
            </h2>

            <table style="width:100%; border-collapse:collapse; margin-top:15px;">

                <tr>
                    <td style="padding:12px 0; color:#6b7280; border-bottom:1px solid #e5e7eb;">
                        Patient Name
                    </td>
                    <td style="padding:12px 0; text-align:right; font-weight:600; border-bottom:1px solid #e5e7eb;">
                        {name}
                    </td>
                </tr>

                <tr>
                    <td style="padding:12px 0; color:#6b7280; border-bottom:1px solid #e5e7eb;">
                        Age
                    </td>
                    <td style="padding:12px 0; text-align:right; font-weight:600; border-bottom:1px solid #e5e7eb;">
                        {age}
                    </td>
                </tr>

                <tr>
                    <td style="padding:12px 0; color:#6b7280; border-bottom:1px solid #e5e7eb;">
                        Service
                    </td>
                    <td style="padding:12px 0; text-align:right; font-weight:600; border-bottom:1px solid #e5e7eb;">
                        {service}
                    </td>
                </tr>

                <tr>
                    <td style="padding:12px 0; color:#6b7280;">
                        Additional Information
                    </td>
                    <td style="padding:12px 0; text-align:right; font-weight:600;">
                        {desc}
                    </td>
                </tr>

            </table>

            <p style="font-size:15px; line-height:1.6; color:#4b5563; margin-top:30px;">
                Thank you for choosing Melbourne Dentals. We look forward to providing you with excellent dental care.
            </p>

            <p style="font-size:15px; line-height:1.6; color:#4b5563;">
                If you need to make any changes to your appointment, please contact our team.
            </p>

        </div>

        <!-- Footer -->
        <div style="padding:22px 35px; background:#f8fafc; border-top:1px solid #e5e7eb;">
            <p style="margin:0; font-size:13px; color:#6b7280;">
                Kind regards,<br>
                <strong style="color:#374151;">Melbourne Dentals</strong>
            </p>
        </div>

    </div>

</body>
</html>
"""
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
        smtp.login(Email,APP_Password)
        a = time.time()
        msg = EmailMessage()
        msg["From"] = f"Zeeshan Ali Zafar <{Email}>"
        msg["To"] = to_email
        msg["Subject"] = "Booked Succesfully..."

        body = f"""Hi {name},

    Hope you are doing well!
    Thanks for Booking in Melbouene Dentals
    You have booked Successfully with folloeing information:
    Name:{name}
    Age:{age}
    Service:{service}
    Additional:{desc}

    Kind Regards,
    Zeeshan Ali Zafar
    """
        msg.set_content(body)
        msg.add_alternative(html, subtype="html")
        smtp.send_message(msg)
        
       
        b = time.time()
        c = b-a
        minutes = int(c // 60)
        seconds = c % 60

        print(f"All Emails Sent in {minutes} min {seconds:.2f} sec")

