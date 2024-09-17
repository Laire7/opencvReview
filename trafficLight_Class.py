import cv2
import random 

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
                
    
trafficLights = TrafficLight()
random_trafficLight = trafficLights.get_random_trafficLight()
trafficLights.show_pic_with_trackbar(random_trafficLight)
  