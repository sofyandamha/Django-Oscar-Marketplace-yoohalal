import os

from django.utils.translation import ugettext_lazy as _
from django.core.files.storage import FileSystemStorage
from django.db.models.fields.files import FileField
from django.core.files.storage import default_storage


def file_cleanup(sender, **kwargs):
    for fieldname in [f.name for f in sender._meta.get_fields()]:
        try:
            field = sender._meta.get_field(fieldname)
        except:
            field = None
        if field and isinstance(field, FileField):
            inst = kwargs['instance']
            f = getattr(inst, fieldname)
            m = inst.__class__._default_manager
            if hasattr(f, 'path') and os.path.exists(f.path) \
                and not m.filter(**{'%s__exact' % fieldname: getattr(inst, fieldname)})\
                .exclude(pk=inst._get_pk_val()):
                    try:
                        #os.remove(f.path)
                        default_storage.delete(f.path)
                    except:
                        pass