# Чамкина Александра R3135 ISU-334638
# 8 вариант:	Вырезать область в 400 на 400 пикселей из центра и сохранить как файл
# Выведите на кадр вертикальную и горизонтальную прямые, пересечение которых совпадает с центром метки

import cv2
import time

# Преобразование изображения - Вырезать область в 400 на 400 пикселей из центра и сохранить как файл
#-----------------------------------------------------------------------------------------------------------------------

cat = cv2.imread("variant-8.jpg")  # Получения изображения
crop_cat = cat[int(cat.shape[0]/2-200):int(cat.shape[0]/2+200), int(cat.shape[1]/2-200):int(cat.shape[1]/2+200)]
cv2.imshow("result", crop_cat)   # Обрезание заданной области изображения
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite("variant-8-result.jpg", crop_cat)

# Отслеживание метки через камеру и вывод на кадр вертикальной и горизонтальной прямой, пересечение которых совпадает с центром метки
#-----------------------------------------------------------------------------------------------------------------------

cap = cv2.VideoCapture(0)         # Получение изображения с камеры
down_points = (640, 480)
i = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, down_points, interpolation=cv2.INTER_LINEAR)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    ret, thresh = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY_INV)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) > 0:                           # Поиск метки и построение контура
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        if i % 5 == 0:                              # Определение центра метки
            a = x + (w // 2)
            b = y + (h // 2)
            print(a, b)
        cv2.line(frame, (a, 500), (a, 0), (0, 0, 0), 5)     # Построение прямых, прощодящих через центр метки
        cv2.line(frame, (0, b), (1000, b), (0, 0, 0), 5)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(0.1)
    i += 1

cap.release()

