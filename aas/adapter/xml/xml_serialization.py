# Copyright 2019 PyI40AAS Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
"""
Module for serializing Asset Administration Shell data to the official XML format


"""

import xml.etree.ElementTree as ET
from typing import List

from aas import model


# ##############################################################
# transformation functions to serialize abstract classes from model.base
# ##############################################################


MODELING_KIND: Dict[model.ModelingKind, str] = {
    model.ModelingKind.TEMPLATE: 'Template',
    model.ModelingKind.INSTANCE: 'Instance'}

ASSET_KIND: Dict[model.AssetKind, str] = {
    model.AssetKind.TYPE: 'Type',
    model.AssetKind.INSTANCE: 'Instance'}

KEY_ELEMENTS: Dict[model.KeyElements, str] = {
    model.KeyElements.ASSET: 'Asset',
    model.KeyElements.ASSET_ADMINISTRATION_SHELL: 'AssetAdministrationShell',
    model.KeyElements.CONCEPT_DESCRIPTION: 'ConceptDescription',
    model.KeyElements.SUBMODEL: 'Submodel',
    model.KeyElements.ANNOTATED_RELATIONSHIP_ELEMENT: 'AnnotatedRelationshipElement',
    model.KeyElements.BASIC_EVENT: 'BasicEvent',
    model.KeyElements.BLOB: 'Blob',
    model.KeyElements.CAPABILITY: 'Capability',
    model.KeyElements.CONCEPT_DICTIONARY: 'ConceptDictionary',
    model.KeyElements.DATA_ELEMENT: 'DataElement',
    model.KeyElements.ENTITY: 'Entity',
    model.KeyElements.EVENT: 'Event',
    model.KeyElements.FILE: 'File',
    model.KeyElements.MULTI_LANGUAGE_PROPERTY: 'MultiLanguageProperty',
    model.KeyElements.OPERATION: 'Operation',
    model.KeyElements.PROPERTY: 'Property',
    model.KeyElements.RANGE: 'Range',
    model.KeyElements.REFERENCE_ELEMENT: 'ReferenceElement',
    model.KeyElements.RELATIONSHIP_ELEMENT: 'RelationshipElement',
    model.KeyElements.SUBMODEL_ELEMENT: 'SubmodelElement',
    model.KeyElements.SUBMODEL_ELEMENT_COLLECTION: 'SubmodelElementCollection',
    model.KeyElements.VIEW: 'View',
    model.KeyElements.GLOBAL_REFERENCE: 'GlobalReference',
    model.KeyElements.FRAGMENT_REFERENCE: 'FragmentReference'}

KEY_TYPES: Dict[model.KeyType, str] = {
    model.KeyType.CUSTOM: 'Custom',
    model.KeyType.IRDI: 'IRDI',
    model.KeyType.IRI: 'IRI',
    model.KeyType.IDSHORT: 'IdShort',
    model.KeyType.FRAGMENT_ID: 'FragmentId'}

IDENTIFIER_TYPES: Dict[model.IdentifierType, str] = {
    model.IdentifierType.CUSTOM: 'Custom',
    model.IdentifierType.IRDI: 'IRDI',
    model.IdentifierType.IRI: 'IRI'}

ENTITY_TYPES: Dict[model.EntityType, str] = {
    model.EntityType.CO_MANAGED_ENTITY: 'CoManagedEntity',
    model.EntityType.SELF_MANAGED_ENTITY: 'SelfManagedEntity'}



def abstract_classes_to_xml(obj: object) -> List[ET.Element]:
    """
    transformation function to serialize abstract classes from model.base which are inherited by many classes.

    :param obj: an object of the AAS
    :return: a list of et.Elements to be inserted into the parent Element of the object
    """
    elements = []
    if isinstance(obj, model.Referable):
        #todo NOT CORRECT
        et_id_short = ET.Element("aas:idShort")
        et_id_short.text(obj.id_short)
        elements += [et_id_short]
        if obj.category:
            et_category = ET.Element("aas:category")
            et_category.text(obj.category)
            elements += [et_category]
        if obj.description:
            et_description = ET.Element("description")
            et_description.text(obj.description)
            elements += [et_description]
        try:
            ref_type = next(iter(t for t in inspect.getmro(type(obj)) if t in model.KEY_ELEMENTS_CLASSES))
        except StopIteration as e:
            raise TypeError("Object of type {} is Referable but does not inherit from a known AAS type"
                            .format(obj.__class__.__name__)) from e
        et_model_type = ET.Element("aas:modelType")
        et_model_type.text = {'name': ref_type.__name__}
        elements += [et_model_type]

    if isinstance(obj, model.Identifiable):
        et_identifiable = ET.Element("aas:identification")
        et_identifiable.set("idType", obj.identification.id_type)
        et_identifiable.text(obj.identification.id)
        elements += [et_identifiable]
        if obj.administration:
            et_administration = ET.Element("aas:administration")
            et_administration_version = ET.Element("aas:version")
            et_administration_version.text(obj.administration.version)
            et_administration_revision = ET.Element("aas:revision")
            et_administration_revision.text(obj.administration.revision)
            et_administration.insert(0, et_administration_version)
            et_administration.insert(1, et_administration_revision)
            elements += [et_administration]

    if isinstance(obj, model.HasDataSpecification):
        if obj.data_specification:
            et_has_data_specification = ET.Element("aas:embeddedDataSpecification")
            et_has_data_specification.text(obj.data_specification)
            elements += [et_has_data_specification]

    if isinstance(obj, model.HasSemantics):
        if obj.semantic_id:
            et_semantics = ET.Element("aas:semanticId")
            et_semantics.text(obj.semantic_id)
            elements += [et_semantics]

    if isinstance(obj, model.HasKind):
        if obj.kind is model.ModelingKind.TEMPLATE:
            et_modeling_kind = ET.Element("aas:modelingKind")
            et_modeling_kind.text(obj.kind)
            elements += [et_modeling_kind]

    if isinstance(obj, model.Qualifiable):
        if obj.qualifier:
            et_qualifiers = ET.Element("aas:qualifier")
            et_qualifiers.text(obj.qualifier)
            elements += [et_qualifiers]

    return elements


# ###############################################################
# transformation functions to serialize classes from model.submodel
# ###############################################################


def submodel_to_xml(obj: submodel.Submodel):
    """
    serialization of an object from class Submodel to XML

    :param obj: object of class Submodel
    :return:  et.Element object with serialized attributes of this object
    """

    return
