import unittest

from hybrid_cc.game.elements import instances
from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.game.elements.instances.elem_factory import ElemFactory
from hybrid_cc.game.elements.mob import Mob
from hybrid_cc.shared import Id, Layer


class TestElemsAndMobs(unittest.TestCase):
    def test_smoke_tests_per_element(self):
        instantiated = []
        for attribute_name in dir(instances):
            element_class = getattr(instances, attribute_name)
            if (isinstance(element_class, type)
                    and element_class is not ElemFactory):
                # Instantiate the class if it has a parameterless constructor
                try:
                    instance = element_class()  # Instantiate the class
                    self.assertTrue(isinstance(instance, Elem))

                    # Class name matches id
                    expected_id_name = attribute_name.lower()
                    actual_id_name = instance.id.name.replace('_', '').lower()
                    self.assertEqual(actual_id_name, expected_id_name)

                    if instance.layer == Layer.MOB:
                        self.assertTrue(isinstance(instance, Mob))
                    else:
                        self.assertFalse(isinstance(instance, Mob))

                    instantiated.append(attribute_name)
                except TypeError as e:
                    print(f'Cannot instantiate {attribute_name} without '
                          f'parameters')
                    print(e)
        print(f"Instantiated {len(instantiated)} elems: {instantiated}")
        print(f"Smoke tests for Mob & Non-Mob layer & parent classes pass.")
        print(f"No name mismatches between ids and class names.")

    def test_instantiate_from_parent(self):
        ElemFactory.initialize()
        for _id in Id:
            if _id == Id.DEFAULT:
                continue
            result = ElemFactory.construct_at(_id)
            self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()




