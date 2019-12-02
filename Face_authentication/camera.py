import cv2

cascPath = 'haarcascade_frontalface_dataset.xml'  # dataset
faceCascade = cv2.CascadeClassifier(cascPath)
import os
import face_recognition
import cv2
import numpy as np
new_face_encodings=[]
new_face_names=[]
for filename in os.listdir('datasets'):
    if(filename!='.ipynb_checkpoints' and filename!='.DS_Store'):
            test = face_recognition.load_image_file(os.path.join('datasets',filename))
            test_encoding = face_recognition.face_encodings(test)[0]
            new_face_encodings.append(test_encoding)
            face_name = filename.split('.')[0][:-1]
            new_face_names.append(face_name)
known_face_encodings = new_face_encodings
known_face_names = new_face_names
video_capture = cv2.VideoCapture(0)  # 0 for web camera live stream
#  for cctv camera'rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp'
#  example of cctv or rtsp: 'rtsp://mamun:123456@101.134.16.117:554/user=mamun_password=123456_channel=1_stream=0.sdp'




def camera_stream():
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        rgb_small_frame = small_frame[:, :, ::-1]

        if process_this_frame:

            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                name = "Unknown"
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if (min(face_distances) > 0.5):
                    name = "Unknown"
                elif matches[best_match_index]:
                    name = known_face_names[best_match_index]
                face_names.append(name)

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Display the resulting frame in browser
        return cv2.imencode('.jpg', frame)[1].tobytes()
def person_name():
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        rgb_small_frame = small_frame[:, :, ::-1]

        if process_this_frame:

            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                name = "Unknown"
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if (min(face_distances) > 0.5):
                    name = "Unknown"
                elif matches[best_match_index]:
                    name = known_face_names[best_match_index]
                face_names.append(name)

        process_this_frame = not process_this_frame


        return  face_names[0]