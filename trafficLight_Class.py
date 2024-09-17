import cv2
import random
import numpy as np 

class TrafficLight: 
  trafficLight_list =  ['red', 'yellow', 'green']
  random_trafficLight = None
  hmin = None
  hmax = None
  
  def __init__(self):
    for color, traffic_light in enumerate(self.trafficLight_list):
      fileName = str('data2/' + traffic_light + '.jpg')
      # Convert the image to HSV color space
      img = cv2.imread(fileName)
      self.trafficLight_list[color] = tuple((fileName, img))
      #이미지들이 잘 들어 갔는지 확인하기
      # cv2.imshow(self.trafficLight_list[color][0], self.trafficLight_list[color][1])
      # cv2.waitKey()
      # cv2.destroyAllWindows()
  
  def get_random_trafficLight(self):
    self.random_trafficLight = random.choice(self.trafficLight_list)
    #이미지가 잘 전달 되었는지 확인
    # cv2.imshow('random', self.random_trafficLight[1])
    # cv2.waitKey()
    # cv2.destroyAllWindows()
    return self.random_trafficLight[1]
    
  def on_trackbar(self, pos):
    self.hmin = cv2.getTrackbarPos('H_min', 'Trackbar')
    self.hmax = cv2.getTrackbarPos('H_max', 'Trackbar')
    # 색상의 범위를 잘 지정하려면 bgr->hsv
    hsv = cv2.cvtColor(self.random_trafficLight[1], cv2.COLOR_BGR2HSV)
    # inRange함수에 적용
    dst = cv2.inRange(hsv, (self.hmin,150,0), (self.hmax,255,255))
    cv2.imshow('Trackbar', dst) # 트랙바 지정 된 값을 이미지에 적용
    
  def show_pic_with_trackbar(self, img):
    # 창에 트랙바를 넣기 위해서는 창을 먼저 생성
    cv2.namedWindow('Trackbar')
    cv2.imshow('Trackbar', img)

    # 트랙바 생성 : 'H_min' 트랙바의 이름, 범위 0~255,  
    # on_trackbar : 트랙바를 움직일때 호출되는 함수(콜백함수)
    cv2.createTrackbar('H_min', 'Trackbar', 0, 180, self.on_trackbar)
    cv2.createTrackbar('H_max', 'Trackbar', 0, 180, self.on_trackbar)
    self.on_trackbar(0) #창 위에 트랙바 띄우기
    
    while True:
     key = cv2.waitKey(1)
     if key == 27:  # Esc 키 누르면 종료
        cv2.destroyAllWindows()
        break
    
  def guess_trafficLight_color(self, img):
    #BGR에서 HSV 색상 공간으로 변환
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # 각 색상에 대한 HSV 임계값 정의
    red_lower1 = np.array([0, 100, 100])
    red_upper1 = np.array([10, 255, 255])
    red_lower2 = np.array([160, 100, 100])
    red_upper2 = np.array([180, 255, 255])

    yellow_lower = np.array([15, 100, 100])
    yellow_upper = np.array([35, 255, 255])

    green_lower = np.array([40, 50, 50])
    green_upper = np.array([80, 255, 255])

    # inRange 함수를 사용하여 각 색상 범위 내의 픽셀 마스크 생성
    red1_mask = cv2.inRange(hsv, red_lower1, red_upper1)
    red2_mask = cv2.inRange(hsv, red_lower2, red_upper2)
    red_mask = cv2.bitwise_or(red1_mask, red2_mask)
    yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
    green_mask = cv2.inRange(hsv, green_lower, green_upper)

    # 각 마스크의 흰색 픽셀 수 계산
    red_pixels = cv2.countNonZero(red_mask)
    yellow_pixels = cv2.countNonZero(yellow_mask)
    green_pixels = cv2.countNonZero(green_mask)

    # Find contours in each mask
    red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    yellow_contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
    green_contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 

    # Find the largest contour for each color
    largest_red_contour = None
    largest_yellow_contour = None
    largest_green_contour = None
    if len(red_contours)>0:
        largest_red_contour = max(red_contours, key=lambda c: cv2.contourArea(c), default=None)
    if len(yellow_contours)>0:
        largest_yellow_contour = max(yellow_contours, key=lambda c: cv2.contourArea(c), default=None)
    if len(green_contours)>0:
        largest_green_contour = max(green_contours, key=lambda c: cv2.contourArea(c), default=None)

    # Determine the color of the traffic light based on the largest contour
    if largest_red_contour is not None:
      return 'red'
    elif largest_yellow_contour is not None:
      return 'yellow'
    elif largest_green_contour is not None:
      return 'green'
    else:
      return None
                
    
new_trafficLight = TrafficLight()
random_trafficLight = new_trafficLight.get_random_trafficLight()
guess_color = new_trafficLight.guess_trafficLight_color(random_trafficLight)
new_trafficLight.show_pic_with_trackbar(random_trafficLight)
print(f'traffic light is : {guess_color}')
  