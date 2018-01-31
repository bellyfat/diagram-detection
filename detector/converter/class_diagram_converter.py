from detector import util
from detector.primitives.shape import Shape
from detector.util import log
from detector.util import ShapeType
from detector.converter.diagram_converter import DiagramConverter
from detector.primitives.generic_entity import GenericEntity


class ClassDiagramTypes:
    CLASS_ENTITY = 0
    ASSOCIATION_ENTITY = 1


class ClassDiagramConverter(DiagramConverter):
    CONVERTER_TYPE = "class_diagram"

    def convert(self):
        log("transform to class primitives")
        extracted_classes = self._extract_classes()
        extracted_associations = self._extract_associations()

        self.generic_entities = extracted_classes + extracted_associations
        return self.generic_entities

    def _extract_classes(self):
        log(f"Extract classes from {len(self.shape_detector.shapes)} shapes")

        found_classes = []
        sorted_contours = self.shape_detector.sort_contours_by_parent()
        for k, v in sorted_contours.items():
            contour_groups = util.group_contours_by_x_pos(v)

            for group_key, group_value in contour_groups.items():
                # Create class entities
                if len(group_value) == 3:
                    new_class = GenericEntity(ClassDiagramTypes.CLASS_ENTITY)

                    # Add shapes to class
                    new_class.add_shape(Shape(group_value[0]))
                    new_class.add_shape(Shape(group_value[1]))
                    new_class.add_shape(Shape(group_value[2]))

                    # new_class.set("name_contour", group_value[0])
                    # new_class.set("attribute_contour", group_value[1])
                    # new_class.set("method_contour", group_value[2])

                    found_classes.append(new_class)

        log(f"{len(found_classes)} class entities found")
        return found_classes

    def _extract_associations(self):
        # Remove class entitites in order to find associations
        img = util.remove_generic_entities_in_image(self.shape_detector.image, self.generic_entities, ClassDiagramTypes.CLASS_ENTITY)
        shapes, _, _ = self.shape_detector.find_shapes_in_image(img)
        log(f"Extract associations from {len(shapes)} shapes")

        found_associations = []
        for s in shapes:
            new_assoc = GenericEntity(ClassDiagramTypes.ASSOCIATION_ENTITY)
            new_assoc.add_shape(s)

            found_associations.append(new_assoc)

        log(f"{len(found_associations)} associations entities found")
        return found_associations

    @classmethod
    def is_diagram(cls, shape_detector):
        return True

    def get_attributes(self):
        attributes = util.get_contour_children_for(self.shape.contour_index, self.shape_detector.hierarchy)
        return attributes

    def draw_class_entities_on_img(self, entities):
        entities = filter(lambda x: x.type == ClassDiagramTypes.CLASS_ENTITY, entities)
        return util.draw_entities_on_image(self.shape_detector.image, entities)
