import json
import unittest
from typing import Iterable, Callable

from sequencescape.models import Model


class _TestJSONEncoder(unittest.TestCase):
    """
    Tests for custom JSON encoders.
    """
    def __init__(self, model_factory: Callable[[], Model], expected_json_properties: Iterable[str], encoder_type: type,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_factory = model_factory
        self.expected_json_properties = expected_json_properties
        self.encoder_type = encoder_type

    def setUp(self):
        self.model = self.model_factory()

    def test_default(self):
        encoded_as_dict = self.encoder_type().default(self.model)
        for property in self.expected_json_properties:
            self.assertIn(property, encoded_as_dict)

    def test_with_json_dumps(self):
        encoded_as_string = json.dumps(self.model, cls=self.encoder_type)
        encoded_as_dict = json.loads(encoded_as_string)
        for property in self.expected_json_properties:
            self.assertIn(property, encoded_as_dict)


class _TestJSONDecoder(unittest.TestCase):
    """
    Tests for custom JSON decoders.
    """
    def __init__(self, model_factory: Callable[[], Model], encoder_type: type, decoder_type: type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_factory = model_factory
        self.encoder_type = encoder_type
        self.decoder_type = decoder_type

    def setUp(self):
        self.model = self.model_factory()

    def test_decode(self):
        encoded_as_string = json.dumps(self.model, cls=self.encoder_type)
        decoded = self.decoder_type().decode(encoded_as_string)
        self.assertEqual(decoded, self.model)

    def test_decode_parsed(self):
        encoded_as_dict = self.encoder_type().default(self.model)
        decoded = self.decoder_type().decode_parsed(encoded_as_dict)
        self.assertEqual(decoded, self.model)

    def test_with_json_loads(self):
        encoded_as_string = json.dumps(self.model, cls=self.encoder_type)
        decoded = json.loads(encoded_as_string, cls=self.decoder_type)
        self.assertEqual(decoded, self.model)


def create_json_converter_test(model_factory: Callable[[], Model], expected_json_properties: Iterable[str], encoder_type: type,
                               decoder_type: type):
    encoder_test_class_name = "Test%s" % encoder_type
    decoder_test_class_name = "Test%s" % decoder_type

    def init(self, *args, **kwargs):
        super(type(self), self).__init__(*self._SETUP, *args, **kwargs)

    globals()[encoder_test_class_name] = type(
        encoder_test_class_name,
        (_TestJSONEncoder, ),
        {
            "_SETUP": (model_factory, expected_json_properties, encoder_type),
            "__init__": init
        }
    )
    globals()[decoder_test_class_name] = type(
        decoder_test_class_name,
        (_TestJSONDecoder, ),
        {
            "_SETUP": (model_factory, encoder_type, decoder_type),
            "__init__": init
        }
    )
