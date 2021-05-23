import cv2
import numpy as np


# https://becominghuman.ai/sudoku-and-cell-extraction-sudokuai-opencv-38b603066066
# https://github.com/Joy2469/Sudoku_AI
def display_image(image):
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def image_preprocessing(image):
    gray = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray.copy(), (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    max_area = 0
    c = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 1000:
            if area > max_area:
                max_area = area
                best_cnt = i
                image = cv2.drawContours(thresh, contours, c, (0, 255, 0), 3)
        c += 1
    mask = np.zeros((image.shape), np.uint8)
    cv2.drawContours(mask, [best_cnt], 0, 255, -1)
    cv2.drawContours(mask, [best_cnt], 0, 0, 2)
    display_image(mask)



if __name__ == "__main__":
    img = cv2.imread('1.png')

    thresh = image_preprocessing(img)
