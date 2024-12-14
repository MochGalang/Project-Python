import cv2
import mediapipe as mp
import pyautogui


cam = cv2.VideoCapture(0)
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

try:
    while True:
        
        ret, frame = cam.read()
        if not ret:
            print("Gagal membaca frame!")
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = face_mesh.process(rgb_frame)

        frame_h, frame_w, _ = frame.shape
        if output.multi_face_landmarks:
            landmarks = output.multi_face_landmarks[0].landmark

           
            for id, landmark in enumerate(landmarks[474:478]):
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)
                if id == 1:  
                    screen_x = screen_w / frame_w * x
                    screen_y = screen_h / frame_h * y
                    pyautogui.moveTo(screen_x, screen_y)

            
            left = [landmarks[145], landmarks[159]]
            for landmark in left:
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)
            if (left[0].y - left[1].y) < 0.004:
                pyautogui.click()
                pyautogui.sleep(1)

        
        cv2.imshow('Eye Controlled Mouse', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Keluar dari program.")
            break

finally:
    cam.release()
    cv2.destroyAllWindows()
    print("Kamera dan jendela ditutup dengan benar.")
