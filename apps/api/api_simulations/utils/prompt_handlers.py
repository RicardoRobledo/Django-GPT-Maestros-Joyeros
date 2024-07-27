import random
from string import Template

from ...api_documents.utils.document_handlers import get_context_documents


__author__ = 'Ricardo'
__version__ = '1.0'
__all__ = ['format_output',]


def format_prompt(prompt_path:str, product, customer=None, documents=None):
    """
    Give us a formatted string with the information of the documents and the product

    :param prompt_path: str of the path of the prompt file
    :param product: ProductModel instance
    :param customer: CustomerModel instance
    """

    with open(prompt_path, 'r', encoding='utf-8') as file:
        template = file.read()

    context_documents = list(documents)
    context_documents_content = [doc.content for doc in context_documents]

    customer_states = {
        'comprar': ['feliz', 'relajado', 'emocionado', 'agradecido', 'esperanzado', 'aburrido', 'no amigable', 'serio'],
        'quejarse': ['enojado', 'triste', 'ansioso', 'frustrado', 'confundido', 'miedoso', 'serio']
    }

    customer_intention = random.choice(list(customer_states.keys()))
    customer_humor = random.choice(customer_states[customer_intention])

    formatted_template = None

    if customer:

        formatted_template = Template(template).substitute(
            product_name=product.product_name,
            product_description=product.description,
            customer_type=customer.customer_type,
            customer_description=customer.description,
            customer_intention=customer_intention,
            customer_humor=customer_humor,
            context_documents=str.join('\n\n', context_documents_content),
        )
    
    else:

        formatted_template = Template(template).substitute(
            product_name=product.product_name,
            product_description=product.description,
            context_documents=str.join('\n\n', context_documents_content),
        )

    return formatted_template
