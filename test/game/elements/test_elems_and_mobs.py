import unittest

from hybrid_cc.game.elements import instances
from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.game.elements.instances.elem_factory import ElemFactory
from hybrid_cc.game.elements.mob import Mob
from hybrid_cc.shared import Id, Layer, Direction
from hybrid_cc.shared.color import Color
from hybrid_cc.shared.kwargs import COLOR, DIRECTION, RULE, COUNT, CHANNEL, \
    SIDES


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

    def test_instantiate(self):
        ElemFactory.init_at_game_load()

        kwargs = {
            COLOR: Color.RED,
            DIRECTION: Direction.N,
            RULE: "test_rule",
            COUNT: 33,
            CHANNEL: 44,
            SIDES: "NEWS"
        }

        for _id in Id:
            if _id == Id.DEFAULT:
                continue
            result = ElemFactory.construct_at((0, 0, 0), _id, **kwargs)

            # Assert something was returned.
            self.assertIsNotNone(result)

            # Assert the instance has the correct id.
            self.assertEqual(_id, result.id)

            # Assert only the filtered kwargs remain
            in_filter = set(result.__class__.kwarg_filter)
            in_kwargs = set(result._kwargs)
            self.assertEqual(in_kwargs, in_filter)


if __name__ == '__main__':
    unittest.main()




