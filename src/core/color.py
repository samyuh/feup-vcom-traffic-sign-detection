import cv2
import numpy as np

class ColorDetector:
    def __init__(self, image) -> None:
        self.image = image
        pass

    def find_color(self):
        hslimage  = cv2.cvtColor(self.image, cv2.COLOR_BGR2HLS)
        Lchannel = hslimage[:,:,1]
        lvalue =cv2.mean(Lchannel)[0]
        print(f' VALORRRR: {lvalue}')

        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

        # split HSV
        h,s,v = cv2.split(hsv)

        # Increasing Contrast with CLAHE in saturation and value
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        swithCLAHE = clahe.apply(s)
        vwithCLAHE = clahe.apply(v)

        hsv = cv2.merge([h, swithCLAHE, vwithCLAHE])

        # Generate lower mask (0-10) and upper mask (170-180) of red
        red_mask1 = cv2.inRange(hsv, (0,100,50), (20,255,255)) # funcionam no road54.png
        red_mask2 = cv2.inRange(hsv, (160,100,50), (180,255,255)) # funcionam no road54.png
        red_mask1 = cv2.inRange(hsv, (0,90,50), (10,255,255)) # deteta tudo no road56.png
        red_mask2 = cv2.inRange(hsv, (170,90,50), (180,255,255)) # deteta tudo no road56.png

        # Merge the mask and crop the red regions
        red_mask = cv2.bitwise_or(red_mask1, red_mask2)

        # Generate mask (90-130) of blue
        blue_mask = cv2.inRange(hsv, (90,30,50), (130,255,255)) # valores originais

        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
        # red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_DILATE, np.ones((3,3),np.uint8))

        blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
        # blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_GRADIENT, np.ones((3,3),np.uint8))

        red = cv2.bitwise_and(self.image, self.image, mask=red_mask)
        blue = cv2.bitwise_and(self.image, self.image, mask=blue_mask)

        # Show red tracing
        cv2.imshow('ANTES DO SEGUNDO THRESHOLD', red)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        red_hslimage  = cv2.cvtColor(red, cv2.COLOR_BGR2HLS)
        red_Lchannel = red_hslimage[:,:,1]
        red_lvalue =cv2.mean(red_Lchannel)[0]
        print(f' VALORRRR DO RED: {red_lvalue}')

        blue_hslimage  = cv2.cvtColor(blue, cv2.COLOR_BGR2HLS)
        blue_Lchannel = blue_hslimage[:,:,1]
        blue_lvalue =cv2.mean(blue_Lchannel)[0]
        print(f' VALORRRR DO BLUE: {blue_lvalue}')

        red_hsv = cv2.cvtColor(red, cv2.COLOR_BGR2HSV)
        average_hsv = cv2.mean(red_hsv,  red_mask)[:3]
        print(f' AVERAGGEEEEEE: {average_hsv}')
        min_value_saturation = red_hsv[np.where(red_hsv[:,:,1]>0)][:,1].min()
        print(f' MINIMUMMM: {min_value_saturation}')
        red_threshold = (average_hsv[1] + min_value_saturation) / 50
        print(f' THRESHOLD A PARTIR DE: {red_threshold}')

        # Show red tracing
        show_hsv = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        cv2.imshow('EFEITO DO CLAHE', show_hsv)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        red_mask1 = cv2.inRange(hsv, (0, red_threshold, 50), (10, 255, 255))
        red_mask2 = cv2.inRange(hsv, (170, red_threshold, 50), (180, 255, 255))
        
        # Merge the mask and crop the red regions
        red_mask = cv2.bitwise_or(red_mask1, red_mask2)

        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))

        red = cv2.bitwise_and(self.image, self.image, mask=red_mask)

        # Show red tracing
        cv2.imshow('Red Color', red)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Show blue tracing
        cv2.imshow('Blue Color', blue)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        mask = cv2.bitwise_or(red, blue)

        result = cv2.bitwise_and(self.image, mask)

        # Show blue and red tracing
        cv2.imshow('Red Color Detection', red)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return ("gray", red, blue, result)