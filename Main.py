import glob
from datetime import datetime
import face_recognition
import cv2
import smtplib

sender = 'silvio.papa92@gmail.com.com'
receivers = ['silvio.papa92@gmail.com']


def main():
    filenames = glob.glob("access/*.*")
    access = []
    for img in filenames:
        image1 = face_recognition.load_image_file(img);
        image1_location = face_recognition.face_locations(image1)
        image1_encodings = face_recognition.face_encodings(image1, image1_location)
        access = access + image1_encodings
    video_capture = cv2.VideoCapture(0)
    while True:
        check = True
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb_small_frame = small_frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        for face in face_encodings:
            results = face_recognition.compare_faces(access, face)
            if not results[0]:
                send_alert(frame)


def send_alert(frame):
    print("Alert")
    time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    cv2.imwrite("alert/" + time + ".png", frame)
    pass


def send_mail():
    message = """From: No Reply <no_reply@mydomain.com>
    To: Person <person@otherdomain.com>
    Subject: Test Email

    This is a test e-mail message.
    """
    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receivers, message)
        print("Successfully sent email")
    except smtplib.SMTPException:
        print("Error: unable to send email")


if __name__ == "__main__":
    main()
