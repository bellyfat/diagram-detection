import argparse
import cv2
from detector.detector import *
from detector import util
from detector.detector.line_detector import LineDetector
from detector.util import log

ap = argparse.ArgumentParser()
output_file = "./output/found_shapes.xml"

if __name__ == '__main__':

    img_path = "img/class_diagram_notation.jpeg"
    #img_path = "img/class_pencil.jpeg"

    #img_path = "img/class.jpeg"
    #img_path = "img/class_many.jpeg"
    #img_path = "img/class2.jpeg"
    #img_path = "img/usecase.jpeg"
    #img_path = "img/circles.jpeg"
    #img_path = "img/ocr_test.jpeg"
    #img_path = "img/ocr_test2.jpeg"

    # ap.add_argument("-i", "--image", required=True, help="Path to the image you want to detect")
    # args = vars(ap.parse_args())
    # print(args["image"])

    #   Detect all shapes
    shape_detector = ShapeDetector(img_path)
    shapes = shape_detector.find_shapes()
    log(f"{len(shapes)} shapes in image found")

    #   Detect type of diagram
    diagram_converter = DiagramTypeDetector.find_converter(shape_detector)

    #   Convert shapes into diagram
    class_entities = diagram_converter._extract_classes()
    assoc_entities = diagram_converter._extract_associations()

    # contours = [c.get("name_contour") for c in entities] +\
    #            [c.get("attribute_contour") for c in entities] +\
    #            [c.get("method_contour") for c in entities]

    #img = shape_detector.get_image_remove_shape_type(ShapeType.RECTANGLE)

    # Draw class contours
    #shape_detector.image = util.remove_generic_entities_in_image(shape_detector.image, entities)
    #shape_detector.image = diagram_converter.draw_class_entities_on_img(class_entities)
    #shape_detector.image = util.draw_entities_on_image(shape_detector.image, assoc_entities)
    #shape_detector.image = util.label_entities_in_image(assoc_entities, shape_detector.image)

    line_detector = LineDetector()
    line_detector.init_with_image(shape_detector.image)
    line_detector.find_lines()
    lines = line_detector.filter_lines(min_length=100, max_length=110)
    log(f"{len(lines)} lines found")
    util.draw_labeled_lines(shape_detector.image, lines, color=(0, 255, 0), toggle_label_drawing=False)


    # Label contours
    #shape_detector.label_contours()

    # Open result in window
    cv2.namedWindow("Image", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("Image", shape_detector.image)
    cv2.waitKey()
    cv2.destroyAllWindows()
