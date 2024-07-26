from rest_framework import serializers

from apps.products.models import ProductModel


class ProductListSerializer(serializers.ModelSerializer):
    """
    This class serialize our Product model to list all products
    """

    class Meta:
        """
        This inner class define our fields to show and our model to use
        
        Attributes:
            model (ProductModel): User instance to make reference
            field tuple(str): fields to show
        """
        
        model: ProductModel = ProductModel
        fields: tuple = ('product_name',)


class ProductDetailSerializer(serializers.ModelSerializer):
    """
    This class serialize our Product model to get a product
    """

    class Meta:
        """
        This inner class define our fields to show and our model to use
        
        Attributes:
            model (ProductModel): User instance to make reference
            field tuple(str): fields to show
        """
        
        model: ProductModel = ProductModel
        fields: tuple = ('product_name', 'description')
