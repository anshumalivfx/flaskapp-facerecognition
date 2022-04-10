import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime


class FaceRecognition:
    def __init__(self):
        self.path = "Training_images"
        self.images = []
        self.classNames = []
        self.myList = os.listdir(self.path)
        for cl in self.myList:
            curImg = cv2.imread(f'{self.path}/{cl}')
            self.images.append(curImg)
            self.classNames.append(os.path.splitext(cl)[0])
        print(self.classNames)
        
    def findEncodings(self):
        encodeList = []
        for img in self.images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            try:
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)
            except:
                encodeList.append('Unknown')
        return encodeList
    
    def markAttendance(self, name):
        with open('Attendance.csv', 'r+') as f:
            myDataList = f.readlines()
            nameList = []
            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])
                if name not in nameList:
                    now = datetime.now()
                    f.writelines(f'\n{name},{now}')
                if name in nameList:
                    print('already marked')
                    break
    
    
    
    def start(self, img):
        encodeListKnown = self.findEncodings()
        print('Encoding Complete')
        attendance = ""
    
        img = cv2.imread(img)
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print(faceDis)
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                name = self.classNames[matchIndex].upper()
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (255, 0, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                nameFile = open('Attendance.csv', 'r+')
                nameList = nameFile.readlines()
                for line in nameList:
                    entry = line.split(',')
                    if name in entry:
                        attendance = "Already Marked"
                else:
                   
                    self.markAttendance(name)
                    attendance = "Marked"
            
            else:
                name = "Unknown"
                attendance = "Not Marked"
            return f'{name} {attendance}'