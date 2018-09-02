from decimal import Decimal as D

from django.db.models import Count, Q, Sum, fields
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect

from oscar.core.loading import get_class, get_model
from oscar.apps.dashboard.orders.views import (OrderStatsView, OrderListView, OrderDetailView,
                                                LineDetailView, ShippingAddressUpdateView)


Partner = get_model('partner', 'Partner')
Order = get_model('order', 'Order')
Line = get_model('order', 'Line')


def queryset_orders_for_user(user):
    queryset = Order._default_manager.select_related(
        'billing_address', 'billing_address__country',
        'shipping_address', 'shipping_address__country',
        'user'
    ).prefetch_related('lines')
    if user.is_staff:
        return queryset
    else:
        partners = Partner._default_manager.filter(user_id=user.id)
        return queryset.filter(lines__partner__in=partners).distinct()


def get_order_for_user_or_404(user, number):
    try:
        return queryset_orders_for_user(user).get(number=number)
    except ObjectDoesNotExist:
        raise Http404()


class OrderStatsView(OrderStatsView):
    
    def get_stats(self, filters):
        orders = queryset_orders_for_user(self.request.user).filter(**filters)
        stats = {
            'total_orders': orders.count(),
            'total_lines': Line.objects.filter(order__in=orders).count(),
            'total_revenue': orders.aggregate(
                Sum('total_incl_tax'))['total_incl_tax__sum'] or D('0.00'),
            'order_status_breakdown': orders.order_by('status').values(
                'status').annotate(freq=Count('id'))
        }
        return stats


class OrderListView(OrderListView):

    def dispatch(self, request, *args, **kwargs):
        # base_queryset is equal to all orders the user is allowed to access
        self.base_queryset = queryset_orders_for_user(
            request.user).order_by('-date_placed')

        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)


class OrderDetailView(OrderDetailView):

    def get_object(self, queryset=None):
        return get_order_for_user_or_404(
            self.request.user, self.kwargs['number'])


class LineDetailView(LineDetailView):

    def get_object(self, queryset=None):
        order = get_order_for_user_or_404(self.request.user,
                                          self.kwargs['number'])
        try:
            return order.lines.get(pk=self.kwargs['line_id'])
        except self.model.DoesNotExist:
            raise Http404()


class ShippingAddressUpdateView(ShippingAddressUpdateView):

    def get_object(self, queryset=None):
        order = get_order_for_user_or_404(self.request.user,
                                          self.kwargs['number'])
        return get_object_or_404(self.model, order=order)