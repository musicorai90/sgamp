from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from . import models

class GroupRequiredMixin(object):
    """
    group_required - list of strings, required param
    """

    group_required = None

    def dispatch(self, request, *args, **kwargs):
        user_groups = []
        for group in request.user.groups.values_list('name', flat=True):
            user_groups.append(group)
        if len(set(user_groups).intersection(self.group_required)) <= 0:
            return redirect('principal:index')
        return super(GroupRequiredMixin, self).dispatch(request, *args, **kwargs)

class ControlAccess():

    def dispatch(self, *args, **kwargs):
        objeto = self.get_object()
        try:
            if str(self.request.user.groups.get()) == 'GE' or str(self.request.user.groups.get()) == 'SE' and str(objeto.status) != "E" or objeto.nucleo_id == models.Coordinador.objects.get(usuario_id=int(self.request.user.id)).nucleo_id:
                return super().dispatch(*args, **kwargs)
        except ObjectDoesNotExist:
            pass
        return redirect('principal:index')

class ControlAccess2():

    def dispatch(self, *args, **kwargs):
        objeto = self.get_object()
        if str(self.request.user.groups.get()) == 'GE' or objeto.nombre.nucleo_id == models.Coordinador.objects.get(usuario_id=int(self.request.user.id)).nucleo_id:
            return super().dispatch(*args, **kwargs)
        return redirect('principal:index')

class ControlAccess3():

    def dispatch(self, *args, **kwargs):
        objeto = self.get_object()
        if str(self.request.user.groups.get()) == 'GE' or str(self.request.user.groups.get()) == 'SE' or str(self.request.user.groups.get()) == 'CB' or objeto.nucleo_id == models.Coordinador.objects.get(usuario_id=int(self.request.user.id)).nucleo_id:
            return super().dispatch(*args, **kwargs)
        return redirect('principal:index')

def get_nucleo(self):
    nucleo = models.Coordinador.objects.get(usuario_id=int(self.request.user.id)).nucleo_id
    return int(nucleo)

def get_group(self):
    grupo = self.request.user.groups.get()
    return str(grupo)