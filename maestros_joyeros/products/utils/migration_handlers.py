from maestros_joyeros.base.utils.file_handlers import read_product_files


__author__ = 'Ricardo'
__version__ = '0.1'


def insert_initial_data(apps, schema_editor):

    ProductModel = apps.get_model('products', 'ProductModel')

    products = read_product_files('Información/Productos')
    ProductModel.objects.bulk_create(products)
