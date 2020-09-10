"""
This type stub file was generated by pyright.
"""

from boto3.docs.base import BaseDocumenter

class CollectionDocumenter(BaseDocumenter):
    def document_collections(self, section):
        ...
    


def document_collection_object(section, collection_model, include_signature=...):
    """Documents a collection resource object

    :param section: The section to write to

    :param collection_model: The model of the collection

    :param include_signature: Whether or not to include the signature.
        It is useful for generating docstrings.
    """
    ...

def document_batch_action(section, resource_name, event_emitter, batch_action_model, service_model, collection_model, include_signature=...):
    """Documents a collection's batch action

    :param section: The section to write to

    :param resource_name: The name of the resource

    :param action_name: The name of collection action. Currently only
        can be all, filter, limit, or page_size

    :param event_emitter: The event emitter to use to emit events

    :param batch_action_model: The model of the batch action

    :param collection_model: The model of the collection

    :param service_model: The model of the service

    :param include_signature: Whether or not to include the signature.
        It is useful for generating docstrings.
    """
    ...

def document_collection_method(section, resource_name, action_name, event_emitter, collection_model, service_model, include_signature=...):
    """Documents a collection method

    :param section: The section to write to

    :param resource_name: The name of the resource

    :param action_name: The name of collection action. Currently only
        can be all, filter, limit, or page_size

    :param event_emitter: The event emitter to use to emit events

    :param collection_model: The model of the collection

    :param service_model: The model of the service

    :param include_signature: Whether or not to include the signature.
        It is useful for generating docstrings.
    """
    ...

