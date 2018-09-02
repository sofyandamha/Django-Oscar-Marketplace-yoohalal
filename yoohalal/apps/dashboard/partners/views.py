from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views import generic

from oscar.apps.dashboard.partners.views import PartnerCreateView, PartnerDeleteView
from oscar.apps.dashboard.partners.forms import ExistingUserForm
from oscar.core.compat import get_user_model
from oscar.core.loading import get_model

from .forms import NewUserForm, PartnerCreateForm, PartnerAddressForm

User = get_user_model()
Partner = get_model('partner', 'Partner')


class PartnerCreateView(PartnerCreateView):
    form_class = PartnerCreateForm


class PartnerManageView(generic.UpdateView):
    template_name = 'dashboard/partners/partner_manage.html'
    form_class = PartnerAddressForm
    success_url = reverse_lazy('dashboard:partner-list')

    def get_object(self, queryset=None):
        self.partner = get_object_or_404(Partner, pk=self.kwargs['pk'])
        address = self.partner.primary_address
        if address is None:
            address = self.partner.addresses.model(partner=self.partner)
        return address

    def get_initial(self):
        return {'name': self.partner.name, 'is_active':self.partner.is_active}

    def get_context_data(self, **kwargs):
        ctx = super(PartnerManageView, self).get_context_data(**kwargs)
        ctx['partner'] = self.partner
        ctx['title'] = self.partner.name
        ctx['owner'] = self.partner.user
        return ctx

    def form_valid(self, form):
        messages.success(
            self.request, _("Partner '%s' was updated successfully.") %
            self.partner.name)
        self.partner.name = form.cleaned_data['name']
        self.partner.is_active = form.cleaned_data['is_active']
        self.partner.save()

        try:
            obj = User.objects.get(pk=self.partner.user_id)
        except User.DoesNotExist:
            obj = None

        if obj: 
            if not obj.is_staff and (self.partner.is_active == 'True'):
                dashboard_access_perm = Permission.objects.get(
                    codename='dashboard_access',
                    content_type__app_label='partner')
                obj.user_permissions.add(dashboard_access_perm)

            if not obj.is_staff and (self.partner.is_active == 'False'):
                dashboard_access_perm = Permission.objects.get(
                    codename='dashboard_access',
                    content_type__app_label='partner')
                obj.user_permissions.remove(dashboard_access_perm)

        return super(PartnerManageView, self).form_valid(form)


class PartnerDeleteView(PartnerDeleteView):

    def delete(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        success_url = self.get_success_url()
    
        try:
            obj = User.objects.get(pk=self.object.user_id)
        except User.DoesNotExist:
            obj = None

        if obj:
            if not obj.is_staff:
                dashboard_access_perm = Permission.objects.get(
                    codename='dashboard_access',
                    content_type__app_label='partner')
                obj.user_permissions.remove(dashboard_access_perm)

        self.object.delete()
        return HttpResponseRedirect(success_url)



class PartnerUserCreateView(generic.CreateView):
    model = User
    template_name = 'dashboard/partners/partner_user_form.html'
    form_class = NewUserForm

    def dispatch(self, request, *args, **kwargs):
        self.partner = get_object_or_404(
            Partner, pk=kwargs.get('partner_pk', None))
        return super(PartnerUserCreateView, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(PartnerUserCreateView, self).get_context_data(**kwargs)
        ctx['partner'] = self.partner
        ctx['title'] = _('Create user')
        return ctx

    def get_form_kwargs(self):
        kwargs = super(PartnerUserCreateView, self).get_form_kwargs()
        kwargs['partner'] = self.partner
        return kwargs

    def get_success_url(self):
        name = self.object.get_full_name() or self.object.email
        messages.success(self.request,
                         _("User '%s' was created successfully.") % name)
        return reverse('dashboard:partner-list')


class PartnerUserLinkView(generic.View):

    def get(self, request, user_pk, partner_pk):
        # need to allow GET to make Undo link in PartnerUserUnlinkView work
        return self.post(request, user_pk, partner_pk)

    def post(self, request, user_pk, partner_pk):
        user = get_object_or_404(User, pk=user_pk)
        name = user.get_full_name() or user.email
        partner = get_object_or_404(Partner, pk=partner_pk)
        oldpartner = Partner.objects.select_related().filter(user = user_pk)

        if oldpartner:
            messages.error(
                request,
                _("User '%(name)s' has been linked with '%(partner_name)s'") %
                {'name': name, 'partner_name': oldpartner[0].name})
            return redirect('dashboard:partner-manage', pk=partner_pk)

        if self.link_user(user, partner):
            messages.success(
                request,
                _("User '%(name)s' was linked to '%(partner_name)s'")
                % {'name': name, 'partner_name': partner.name})
        else:
            messages.info(
                request,
                _("User '%(name)s' is already linked to '%(partner_name)s'")
                % {'name': name, 'partner_name': partner.name})
        return redirect('dashboard:partner-manage', pk=partner_pk)

    def link_user(self, user, partner):
        """
        Links a user to a partner, and adds the dashboard permission if needed.

        Returns False if the user was linked already; True otherwise.
        """
        if partner.user:
            return False
        partner.user_id = user.id
        partner.save()
        if not user.is_staff and partner.is_active:
            dashboard_access_perm = Permission.objects.get(
                codename='dashboard_access',
                content_type__app_label='partner')
            user.user_permissions.add(dashboard_access_perm)
        return True


class PartnerUserUnlinkView(generic.View):

    def unlink_user(self, user, partner):
        """
        Unlinks a user from a partner, and removes the dashboard permission
        if they are not linked to any other partners.

        Returns False if the user was not linked to the partner; True
        otherwise.
        """
        if not partner.user:
            return False
        partner.user = None
        partner.save()
        if not user.is_staff:
            dashboard_access_perm = Permission.objects.get(
                codename='dashboard_access',
                content_type__app_label='partner')
            user.user_permissions.remove(dashboard_access_perm)
        return True

    def post(self, request, user_pk, partner_pk):
        user = get_object_or_404(User, pk=user_pk)
        name = user.get_full_name() or user.email
        partner = get_object_or_404(Partner, pk=partner_pk)
        if self.unlink_user(user, partner):
            msg = render_to_string(
                'dashboard/partners/messages/user_unlinked.html',
                {'user_name': name,
                 'partner_name': partner.name,
                 'user_pk': user_pk,
                 'partner_pk': partner_pk})
            messages.success(self.request, msg, extra_tags='safe noicon')
        else:
            messages.error(
                request,
                _("User '%(name)s' is not linked to '%(partner_name)s'") %
                {'name': name, 'partner_name': partner.name})
        return redirect('dashboard:partner-manage', pk=partner_pk)


class PartnerUserUpdateView(generic.UpdateView):
    template_name = 'dashboard/partners/partner_user_form.html'
    form_class = ExistingUserForm

    def get_object(self, queryset=None):
        self.partner = get_object_or_404(Partner, pk=self.kwargs['partner_pk'])
        return get_object_or_404(User, pk=self.kwargs['user_pk'])

    def get_context_data(self, **kwargs):
        ctx = super(PartnerUserUpdateView, self).get_context_data(**kwargs)
        name = self.object.get_full_name() or self.object.email
        ctx['partner'] = self.partner
        ctx['title'] = _("Edit user '%s'") % name
        return ctx

    def get_success_url(self):
        name = self.object.get_full_name() or self.object.email
        messages.success(self.request,
                         _("User '%s' was updated successfully.") % name)
        return reverse('dashboard:partner-list')