import cv2
import os
import numpy
from PIL import Image as im
import json

def auth(digital):
    fingerprint_test = cv2.imread(f"static/temp/{digital}")
    a = True
    # cv2.imshow("Original", cv2.resize(fingerprint_test, None, fx=1, fy=1))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    try:
        if os.listdir("static/saved").count() >= 1:
            for file in [file for file in os.listdir("./static/saved")]:
                fingerprint_database_image = cv2.imread("./static/saved/"+file)
                sift = cv2.SIFT_create()
                keypoints_1, descriptors_1 = sift.detectAndCompute(fingerprint_test, None)
                keypoints_2, descriptors_2 = sift.detectAndCompute(fingerprint_database_image, None)

                
                matches = cv2.FlannBasedMatcher(dict(algorithm=1, trees=10), dict()).knnMatch(descriptors_1, descriptors_2, k=2)
                match_points = []
            
                for p, q in matches:
                    if p.distance < 0.1*q.distance:
                        match_points.append(p)
                keypoints = 0
                if len(keypoints_1) <= len(keypoints_2):
                    keypoints = len(keypoints_1)            
                else:
                    keypoints = len(keypoints_2)
                print(f"Keypoints: {keypoints}")
                print(f"match_points: {match_points}")
                if (len(match_points) / keypoints)>0.95:
                    print("% match: ", len(match_points) / keypoints * 100)
                    print("Figerprint ID: " + str(file)) 
                    result = cv2.drawMatches(fingerprint_test, keypoints_1, fingerprint_database_image, keypoints_2, match_points, None) 
                    result = cv2.resize(result, None, fx=2.5, fy=2.5)
                    # print(f"Result: {result}")
                    img = im.fromarray(result, 'RGB')
                    img.save('img.BMP')
                    # cv2.imshow("result", result)
                    # cv2.waitKey(0)
                    # cv2.destroyAllWindows()
                    a = True
                    break;
                else:
                    a = False
            return a
    except:
        return False


def authDirect(digital, nome):
    js = open("static/users.json", "r")
    usrs = json.loads(js.read())
    js.close()
    for user in usrs["users"]:
        try:
            if user["nome"] == nome:
                fingerprint_test = cv2.imread(f"./static/temp/{digital}")
                fingerprint_database_image = cv2.imread(f"./static/saved/{user['digital']}")
                sift = cv2.SIFT_create()
                keypoints_1, descriptors_1 = sift.detectAndCompute(fingerprint_test, None)
                keypoints_2, descriptors_2 = sift.detectAndCompute(fingerprint_database_image, None)

                matches = cv2.FlannBasedMatcher(dict(algorithm=1, trees=10), dict()).knnMatch(descriptors_1, descriptors_2, k=2)
                match_points = []
            
                for p, q in matches:
                    if p.distance < 0.1*q.distance:
                        match_points.append(p)
                keypoints = 0
                if len(keypoints_1) <= len(keypoints_2):
                    keypoints = len(keypoints_1)            
                else:
                    keypoints = len(keypoints_2)
                # print(f"Keypoints: {keypoints}")
                # print(f"match_points: {match_points}")
                if (len(match_points) / keypoints)>0.95:
                    # result = cv2.drawMatches(fingerprint_test, keypoints_1, fingerprint_database_image, keypoints_2, match_points, None) 
                    # result = cv2.resize(result, None, fx=2.5, fy=2.5)
                    # img = im.fromarray(result, 'RGB')
                    # img.save('img.BMP')
                    return True
        except:
            pass
            # print("CUTUVELO")
        return False


if __name__ == "__main__":
    authDirect("2__F_Left_index_finger.BMP", "babidi")