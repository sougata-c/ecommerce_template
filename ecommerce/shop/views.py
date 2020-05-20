"""

    Tunnel
    ------

        checkout > shipment > payment > success
"""

from django import http
from django.core import paginator
from django.core import serializers as core_serializers
from django.shortcuts import render, reverse, redirect
from django.utils.decorators import method_decorator
from django.views import generic

from shop import models, serializers


def no_cart_router(request, current_path, debug=False):
    if not debug:
        try:
            request.session['cart_id']
        except:
            return redirect(reverse('no_cart'))
        return redirect(reverse(current_path))
    else:
        return render

class IndexView(generic.View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'pages/shop.html', context)

class ProductsView(generic.ListView):
    model = models.Product
    queryset = models.Product.objects.all()
    template_name = 'pages/collections.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        klass = super().get_paginator(self.queryset, self.paginate_by)
        serialized_products = serializers.ProductSerializer(instance=klass.object_list, many=True)
        context['vue_products'] = serialized_products.data
        return context

class ProductView(generic.DetailView):
    model = models.Product
    queryset = models.Product.objects.all()
    template_name = 'pages/product.html'
    context_object_name = 'product'

    def post(self, request, *args, **kwargs):
        product = super().get_object()
        serialiazed_product = core_serializers.serialize('json', product)
        return http.JsonResponse(data={'success': 'success'})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = super().get_object()
        serialized_product = serializers.ProductSerializer(instance=product)
        context['vue_product'] = serialized_product.data
        return context

class CheckoutView(generic.ListView):
    model = models.Cart
    template_name = 'pages/cart.html'
    context_object_name = 'products'
    
    def get_queryset(self, **kwargs):
        return models.Cart.cart_manager.cart_products('eino')

class CartSuccessView(generic.TemplateView):
    template_name = 'pages/success.html'

    def get(self, request, *args, **kwargs):
        return no_cart_router(request, reverse('success'), debug=True)(request, self.template_name)

class ShipmentView(generic.ListView):
    model = models.Cart
    template_name = 'pages/shipment.html'
    context_object_name = 'products'

    def get_queryset(self, **kwargs):
        return models.Cart.cart_manager.cart_products('eino')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_total'] = self.model.cart_manager.cart_total('zef')['product__price_ht__sum']
        return context


class PaymentView(generic.ListView):
    model = models.Cart
    template_name = 'pages/payment.html'
    context_object_name = 'products'

    def get_queryset(self, **kwargs):
        return models.Cart.cart_manager.cart_products('eino')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_total'] = self.model.cart_manager.cart_total('zef')['product__price_ht__sum']
        return context

class EmptyCartView(generic.TemplateView):
    template_name = 'pages/no_cart.html'