from hgijson.json.builders import MappingJSONEncoderClassBuilder, MappingJSONDecoderClassBuilder
from hgijson.json.models import JsonPropertyMapping
from sequencescape.models import Sample, InternalIdModel, NamedModel

JSON_NAME_PROPERTY = "name"

JSON_INTERNAL_ID_PROPERTY = "internal_id"

JSON_ACCESSION_NUMBER_PROPERTY = "accession_number"

JSON_ORGANISM_PROPERTY = "organism"
JSON_COMMON_NAME_PROPERTY = "common_name"
JSON_TAXON_ID_PROPERTY = "taxon_id"
JSON_GENDER_PROPERTY = "gender"
JSON_ETHNICITY_PROPERTY = "ethnicity"
JSON_COHORT_PROPERTY = "cohort"
JSON_COUNTRY_OF_ORIGIN_PROPERTY = "country_of_origin"
JSON_GEOGRAPHICAL_REGION_PROPERTY = "geographical_region"


_named_json_mapping = [
    JsonPropertyMapping(JSON_NAME_PROPERTY, "name")
]
_NamedModelJSONEncoder = MappingJSONEncoderClassBuilder(NamedModel, _named_json_mapping).build()
_NamedModelJSONDecoder = MappingJSONDecoderClassBuilder(NamedModel, _named_json_mapping).build()


_internal_id_json_mapping = [
    JsonPropertyMapping(JSON_INTERNAL_ID_PROPERTY, "internal_id")
]
_InternalIdModelJSONEncoder = MappingJSONEncoderClassBuilder(InternalIdModel, _internal_id_json_mapping).build()
_InternalIdModelJSONDecoder = MappingJSONDecoderClassBuilder(InternalIdModel, _internal_id_json_mapping).build()


_accession_number_json_mapping = [
    JsonPropertyMapping(JSON_ACCESSION_NUMBER_PROPERTY, "accession_number")
]
_AccessionNumberModelJSONEncoder = MappingJSONEncoderClassBuilder(InternalIdModel, _accession_number_json_mapping).build()
_AccessionNumberModelJSONDecoder = MappingJSONDecoderClassBuilder(InternalIdModel, _accession_number_json_mapping).build()


_sample_json_mapping = [
    JsonPropertyMapping(JSON_ORGANISM_PROPERTY, "organism"),
    JsonPropertyMapping(JSON_COMMON_NAME_PROPERTY, "common_name"),
    JsonPropertyMapping(JSON_TAXON_ID_PROPERTY, "taxon_id"),
    JsonPropertyMapping(JSON_GENDER_PROPERTY, "gender"),
    JsonPropertyMapping(JSON_ETHNICITY_PROPERTY, "ethnicity"),
    JsonPropertyMapping(JSON_COHORT_PROPERTY, "cohort"),
    JsonPropertyMapping(JSON_COUNTRY_OF_ORIGIN_PROPERTY, "country_of_origin"),
    JsonPropertyMapping(JSON_GEOGRAPHICAL_REGION_PROPERTY, "geographical_region")
]
SampleJSONEncoder = MappingJSONEncoderClassBuilder(
    Sample,
    _sample_json_mapping,
    (_NamedModelJSONEncoder, _AccessionNumberModelJSONEncoder, _InternalIdModelJSONEncoder)
).build()
SampleJSONDecoder = MappingJSONDecoderClassBuilder(
    Sample,
    _sample_json_mapping,
    (_NamedModelJSONDecoder, _AccessionNumberModelJSONDecoder, _InternalIdModelJSONDecoder)
).build()