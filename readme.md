```python
sequencescape = connect_to_sequencescape("mysql://user:@host:3306/database")

sequencescape.sample.get_by_name(sample_name)
sequencescape.sample.get_by_name([sample_name, other_sample_name])

sequencescape.library.get_by_id(library_internal_id)
sequencescape.library.get_by_id([library_internal_id, other_library_internal_id])

sequencescape.study.get_by_accession_number(study_accession_number)
sequencescape.study.get_by_accession_number([study_accession_number, other_study_accession_number])

sequencescape.sample.get_by_property_value(property, property_value)
sequencescape.sample.get_by_property_value([(property, property_value), (other_property, property_value)])
sequencescape.sample.get_by_property_value(property, [property_value, other_property_value])
```