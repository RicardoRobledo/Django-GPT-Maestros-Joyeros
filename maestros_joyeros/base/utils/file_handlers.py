import os

from maestros_joyeros.products.models import ProductModel
from maestros_joyeros.customers.models import CustomerModel
from maestros_joyeros.documents.models import TopicModel, DocumentModel


__author__ = 'Ricardo'
__version__ = '0.1'


def read_product_files(folder_path):
    """
    Read all files in a products folder and return a list of objects

    :param folder_path: str
    :param model: instance of custom django model
    :return: list of product objects
    """

    products = []
    files = os.listdir(folder_path)

    for file in files:

        with open(f'{folder_path}/{file}', 'r', encoding='utf-8') as file_instance:

            content = file_instance.read()
            file_name = file.replace('.txt', '')

            product_object = ProductModel(
                product_name=file_name, description=content)
            products.append(product_object)

    return products


def read_customer_files(folder_path):
    """
    Read all files in a customer folder and return a list of objects

    :param folder_path: str
    :return: list of document objects of the model
    """

    customers = []
    files = os.listdir(folder_path)

    for file in files:

        with open(f'{folder_path}/{file}', 'r', encoding='utf-8') as file_instance:

            content = file_instance.read()
            file_name = file.replace('.txt', '')

            customer_object = CustomerModel(
                customer_type=file_name, description=content)
            customers.append(customer_object)

    return customers


def read_document_files(folder_path, topic_name):
    """
    Read all files in a documents folder and return a list of objects

    :param folder_path: str of the folder path
    :param topic_name: str of the topic name
    :return: list of document objects of the model
    """

    documents = []
    files = os.listdir(folder_path)

    topic = TopicModel.objects.filter(topic_name=topic_name).first()

    for file in files:

        with open(f'{folder_path}/{file}', 'r', encoding='utf-8') as file_instance:

            content = file_instance.read()
            file_name = file.replace('.txt', '')

            document_object = DocumentModel(
                document_name=file_name, content=content, topic_id=topic)
            documents.append(document_object)

    return documents
