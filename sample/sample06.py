from format_flex import GData
import cv2

img = cv2.imread("Lenna.png", cv2.IMREAD_GRAYSCALE)

item = [
    {"this": "is", "random": "object"},
    {"prime", 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37},
    {"image": img},
    {
        "text": "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    }
]
# Gdata can store any type of data.
gdata = GData(item)

print(gdata.to.pickle("output/output").summary)
print(gdata.to.joblib("output/output").summary)
print(gdata.to.cloudpickle("output/output").summary)
print(gdata.to.dill("output/output").summary)
