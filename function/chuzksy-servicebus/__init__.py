import logging
import azure.functions as func
import psycopg2
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import traceback

def main(msg: func.ServiceBusMessage):

    notification_id = int(msg.get_body().decode('utf-8'))
    logging.info('Python ServiceBus queue trigger processed message: %s',notification_id)

    # TODO: Get connection to database
    conn = psycopg2.connect(
        database="techconfdb",
        user='azureuser@chuzksy-server-pg',
        password='Password001001', 
        host='chuzksy-server-pg.postgres.database.azure.com',
    )
    cursor = conn.cursor()

    semdgridKey = "SENDGRID_API_KEY"
    

    try:
        # TODO: Get notification message and subject from database using the notification_id
        cursor.execute("SELECT message, subject FROM public.notification WHERE id = %s", (notification_id,))
        notification = cursor.fetchone()

        # TODO: Get attendees email and name
        cursor.execute("SELECT email, first_name, last_name FROM public.attendee")
        attendances = cursor.fetchall()

        # TODO: Loop through each attendee and send an email with a personalized subject
        for i, attendance in enumerate(attendances):
            message = Mail(
                from_email='info@techconf.com',
                to_emails=attendance[0],
                subject=notification[1] or 'Notification from TechConf',
                html_content=notification[0])
            sg = SendGridAPIClient(semdgridKey)
            response = sg.send(message)

        # TODO: Update the notification table by setting the completed date and updating the status with the total number of attendees notified
        numberOfAttendees = f'Notified {len(attendances)} attendees'
        cursor.execute("UPDATE public.notification SET completed_date = %s, status = %s WHERE id = %s",
                       (datetime.now(), numberOfAttendees, notification_id))
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
        traceback.print_exc()
        conn.rollback()
    finally:
        # TODO: Close connection
        conn.close()
        cursor.close()
