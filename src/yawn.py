from imutils import face_utils
from scipy.spatial import distance as dist
from dataclasses import dataclass
from datetime import datetime
import math
from collections import defaultdict

'''
Data class for an instance of a yawn
To be used for aggregated analysis of yawning frequency
'''
@dataclass
class yawn_instance:
    timestamp: datetime
    mar: float

'''
Class to detect yawning
'''
class yawn(object):
    cv = None
    threshold = None
    yawns = []
    is_yawning = False

    def __init__(self, cv2, threshold=0.4):
        super(yawn, self).__init__()
        self.cv = cv2
        self.threshold = threshold

    def set_threshold(self, threshold):
        self.threshold = threshold
    
    def get_threshold(self, threshold):
        return self.threshold

    '''
    Function to calculate the mouth aspect ratio
    A measurement on how open the mouth is
    '''
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

    '''
    The mathematical sigmoid function
    '''
    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))

    '''
    A mathematical function that calculates the yawning score based on
    the amount of yawns per hour
    '''
    def yawning_score(self, x):
        return self.sigmoid(x - 1.5) - 0.18 * math.exp(-math.pow(x, 3))

    '''
    source: https://pubmed.ncbi.nlm.nih.gov/20357461/
    yawns per hour:
        0: awake
        1: starting to get tired
        1-2: somewhat tired
        2-3: tired
        3-3+: Danger
    '''
    def yawn_frequency(self):
        timestamps = list(map(lambda x: x.timestamp, self.yawns))
        occurences_per_hour = defaultdict(int)
        for occurrence in timestamps:
            occurences_per_hour[occurrence.strftime('%Y-%m-%d %H')] += 1
        if (len(occurences_per_hour) > 0):
            return sum(occurences_per_hour.values())/len(occurences_per_hour)
        else:
            return 0


    '''
    '''
    def detect(self, frame, shape):
        # Get the start and end point for outer and inner mouth
        (mouth_start, mouth_end) = face_utils.FACIAL_LANDMARKS_68_IDXS["mouth"];
        (inner_mouth_start, inner_mouth_end) = face_utils.FACIAL_LANDMARKS_68_IDXS["inner_mouth"];

        # Get the shape of the inner and outer mouth
        mouth = shape[mouth_start:mouth_end]
        inner_mouth = shape[inner_mouth_start:inner_mouth_end]

        # Create a convex hull shape with open cv that can be used to draw onto the face
        mouth_hull = self.cv.convexHull(mouth)
        inner_mouth_hull = self.cv.convexHull(inner_mouth)

        # Draw the convex hull of the mouth onto the face
        self.__draw_mouth(frame, (mouth_hull, inner_mouth_hull))

        # Get the MAR of the yawn
        mar = self.mouth_aspect_ratio(mouth)
        # Draw the MAR value onto the screen
        self.__draw_mar(frame, mar)

        # Add the yawn to the list of yawns if it's over the threshold
        if (not self.is_yawning and mar > self.threshold):
            self.is_yawning = True
            new_yawn = yawn_instance(datetime.now(), mar)
            self.yawns.append(new_yawn)
            self.yawn_frequency()
        elif (self.is_yawning and mar > self.threshold):
            if (self.yawns[-1].mar < mar):
                setattr(self.yawns[-1], 'mar', mar)
        elif (self.is_yawning and mar < self.threshold):
            self.is_yawning = False
        return self.yawning_score(self.yawn_frequency())

    '''
    Private method to draw the mouth – both inner and outer – onto the face
    '''
    def __draw_mouth(self, frame, contours):
        self.cv.drawContours(frame, [contours[0]], -1, (0, 0, 255), 1)
        self.cv.drawContours(frame, [contours[1]], -1, (0, 255, 255), 1)

    '''
    Private method to draw mar value to screen
    '''
    def __draw_mar(self, frame, mar):
        self.cv.putText(frame, "MAR: {:.2f}".format(mar), (300, 60),
               self.cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)