import cv2
import imutils
from imutils import contours
from detector.util import *
import numpy as np
from detector.diagram.shape import Shape
from detector.shape_type import ShapeType
import detector.util as util


class DiagramConverter(object):
    CONVERTER_TYPE = None

    def __init__(self, shape_detector):
        self.shape_detector = shape_detector
        """ Shape detector, that contains all detected shapes, the contours and the contour hierarchy. """

    def transform_shapes_to_diagram(self):
        raise NotImplementedError()
