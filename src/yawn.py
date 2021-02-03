from imutils import face_utils
from scipy.spatial import distance as dist

class yawn(object):
    cv = None
    threshold = None

    def __init__(self, cv2, threshold=0.3):
        super(yawn, self).__init__()
        self.cv = cv2
        self.threshold = threshold

    def set_threshold(self, threshold):
        self.threshold = threshold
    
    def get_threshold(self, threshold):
        return self.threshold

    def mouth_aspect_ratio(self, mouth):
        # Points 49-60 found here https://www.pyimagesearch.com/wp-content/uploads/2017/04/facial_landmarks_68markup-768x619.jpg
        left = mouth[0]
        #left_middle_top = mouth[1]
        left_top = mouth[2]
        middle_top = mouth[3]
        right_top = mouth[4]
        #right_middle_top = mouth[5]
        right = mouth[6]
        #right_middle_bottom = mouth[7]
        right_bottom = mouth[8]
        middle_bottom = mouth[9]
        left_bottom = mouth[10]
        #left_middle_bottom = mouth[11]

        A = dist.euclidean(left_top, left_bottom)
        B = dist.euclidean(right_top, right_bottom)
        C = dist.euclidean(left, right)

        mar = (A + B) / (2.0 * C)
        return mar


    def detect(self, frame, shape):
        (mouth_start, mouth_end) = face_utils.FACIAL_LANDMARKS_68_IDXS["mouth"];
        (inner_mouth_start, inner_mouth_end) = face_utils.FACIAL_LANDMARKS_68_IDXS["inner_mouth"];

        mouth = shape[mouth_start:mouth_end]
        inner_mouth = shape[inner_mouth_start:inner_mouth_end]

        mouth_hull = cv2.convexHull(mouth)
        inner_mouth_hull = cv2.convexHull(inner_mouth)

        __draw_mouth(frame, cv2, (mouth_hull, inner_mouth_hull))

        mar = mouth_aspect_ratio(mouth)
        __draw_mar(frame, cv2, mar)
        return mar

    def __draw_mouth(self, frame, contours):
        cv2.drawContours(frame, [contours[0]], -1, (0, 0, 255), 1)
        cv2.drawContours(frame, [contours[1]], -1, (0, 255, 255), 1)

    def __draw_mar(self, frame, cv2, mar):
        cv2.putText(frame, "MAR: {:.2f}".format(mar), (300, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)