import cv2
import os
import numpy
from PIL import Image as im
import json

def auth(digital):
    #Aquisição 1
    fingerprint_test = cv2.imread(f"static/temp/{digital}")
    # cv2.imshow("Original", cv2.resize(fingerprint_test, None, fx=1, fy=1))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    try:
        if os.listdir("static/saved").count() >= 1:
            for file in [file for file in os.listdir("./static/saved")]:
                # Aquisição 2
                fingerprint_database_image = cv2.imread("./static/saved/"+file)

                # Pré-Processamento
                fingerprint_test_gray = cv2.cvtColor(fingerprint_test, cv2.COLOR_BGR2GRAY)
                fingerprint_database_image_gray = cv2.cvtColor(fingerprint_database_image, cv2.COLOR_BGR2GRAY)
                fingerprint_test_blur = cv2.GaussianBlur(fingerprint_test_gray, (5, 5), 0)
                fingerprint_database_image_blur = cv2.GaussianBlur(fingerprint_database_image_gray, (5, 5), 0)
                fingerprint_test_enhanced = cv2.equalizeHist(fingerprint_test_blur)
                fingerprint_database_image_enhanced = cv2.equalizeHist(fingerprint_database_image_blur)

                # Segmentação
                fingerprint_test_segmented = cv2.adaptiveThreshold(
                    fingerprint_test_enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                    cv2.THRESH_BINARY_INV, 11, 2
                )
                fingerprint_database_image_segmented = cv2.adaptiveThreshold(
                    fingerprint_database_image_enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                    cv2.THRESH_BINARY_INV, 11, 2
                )

                # Extração de Características
                sift = cv2.SIFT_create()
                keypoints_1, descriptors_1 = sift.detectAndCompute(fingerprint_test_segmented, None)
                keypoints_2, descriptors_2 = sift.detectAndCompute(fingerprint_database_image_segmented, None)

                # Comparação de Características
                matches = cv2.FlannBasedMatcher(dict(algorithm=1, trees=10), dict()).knnMatch(descriptors_1, descriptors_2, k=2)
                match_points = []

                for p, q in matches:
                    if p.distance < 0.1 * q.distance:
                        match_points.append(p)

                # Interpretação dos Resultados
                keypoints = min(len(keypoints_1), len(keypoints_2))
                if keypoints > 0 and (len(match_points) / keypoints) > 0.95:
                    return True
                else:
                    return False
    except:
        return False


def authDirect(digital, nome):
    js = open("static/users.json", "r")
    usrs = json.loads(js.read())
    # print(usrs)
    js.close()
    # print(nome)
    try:
        for user in usrs["users"]:
            if user["nome"] == nome:
                # Aquisição
                fingerprint_test = cv2.imread(f"./static/temp/{digital}")
                fingerprint_database_image = cv2.imread(f"./static/saved/{user['digital']}")

                # Pré-Processamento
                fingerprint_test_gray = cv2.cvtColor(fingerprint_test, cv2.COLOR_BGR2GRAY)
                fingerprint_database_image_gray = cv2.cvtColor(fingerprint_database_image, cv2.COLOR_BGR2GRAY)
                fingerprint_test_blur = cv2.GaussianBlur(fingerprint_test_gray, (5, 5), 0)
                fingerprint_database_image_blur = cv2.GaussianBlur(fingerprint_database_image_gray, (5, 5), 0)
                fingerprint_test_enhanced = cv2.equalizeHist(fingerprint_test_blur)
                fingerprint_database_image_enhanced = cv2.equalizeHist(fingerprint_database_image_blur)

                # Segmentação
                fingerprint_test_segmented = cv2.adaptiveThreshold(
                    fingerprint_test_enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                    cv2.THRESH_BINARY_INV, 11, 2
                )
                fingerprint_database_image_segmented = cv2.adaptiveThreshold(
                    fingerprint_database_image_enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                    cv2.THRESH_BINARY_INV, 11, 2
                )

                # Extração de Características
                sift = cv2.SIFT_create()
                keypoints_1, descriptors_1 = sift.detectAndCompute(fingerprint_test_segmented, None)
                keypoints_2, descriptors_2 = sift.detectAndCompute(fingerprint_database_image_segmented, None)

                # Comparação de Características
                matches = cv2.FlannBasedMatcher(dict(algorithm=1, trees=10), dict()).knnMatch(descriptors_1, descriptors_2, k=2)
                match_points = []

                for p, q in matches:
                    if p.distance < 0.1 * q.distance:
                        match_points.append(p)

                # Interpretação dos Resultados
                keypoints = min(len(keypoints_1), len(keypoints_2))
                if keypoints > 0 and (len(match_points) / keypoints) > 0.95:
                    return True
                else:
                    return False

    except:
        return False


if __name__ == "__main__":
    authDirect("2__F_Left_index_finger.BMP", "babidi")