import cv2
import pytesseract

# Grayscale, Gaussian blur, Otsu's threshold
image = cv2.imread('msg1.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imwrite('gray.jpg', gray)

blur = cv2.GaussianBlur(gray, (3,3), 0)
thresh = cv2.threshold(blur, 115, 255, cv2.THRESH_BINARY_INV)[1]

# Morph open to remove noise and invert image
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
invert = 255 - thresh

# Perform text extraction
data = pytesseract.image_to_string(invert, lang='eng', config='--psm 6')
print(data)

# Save images instead of displaying them
cv2.imwrite('thresh.jpg', thresh)
cv2.imwrite('opening.jpg', opening)
cv2.imwrite('invert.jpg', invert)