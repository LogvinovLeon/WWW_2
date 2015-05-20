from django.db.models import Model
from django.db.models.fields import TextField, IntegerField
from django.db.models.fields.related import ForeignKey


class PolishAdminPart(Model):
    url = TextField(max_length=100, null=True)
    name = TextField(max_length=100)

    class Meta:
        abstract = True

    @classmethod
    def get_child_model(cls):
        index = PARTS_ORDER.index(cls)
        if index + 1 < len(PARTS_ORDER):
            return PARTS_ORDER[index + 1]
        else:
            return None

    @classmethod
    def get_parent_model(cls):
        index = PARTS_ORDER.index(cls)
        if index:
            return PARTS_ORDER[index - 1]
        else:
            return None

    @classmethod
    def get_name(cls):
        return cls._meta.verbose_name

    @classmethod
    def get_name_plural(cls):
        return cls._meta.verbose_name_plural

    def get_description(self):
        view_name = self.get_child_model().get_name_plural().lower()
        return {"view_name": view_name,
                "name": self.name,
                "id": self.pk}

    def get_path(self):
        parent_model = self.get_parent_model()
        if parent_model:
            parent_field_name = parent_model.get_name().lower()
            return getattr(self, parent_field_name).get_path() + [self.get_description()]
        else:
            return [self.get_description()]

    def __unicode__(self):
        return u"{}: {}".format(self.__class__.__name__, self.name)


class Voivodeship(PolishAdminPart):
    class Meta:
        verbose_name_plural = "Voivodeships"


class Powiat(PolishAdminPart):
    voivodeship = ForeignKey(Voivodeship)

    class Meta:
        verbose_name_plural = "Powiats"


class Gmina(PolishAdminPart):
    powiat = ForeignKey(Powiat)
    version = IntegerField(default=1)

    class Meta:
        verbose_name_plural = "Gminas"

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse

        return reverse('constituencies', args=[str(self.id)])


class Constituency(PolishAdminPart):
    gmina = ForeignKey(Gmina)
    blanks_received = IntegerField(default=0)
    can_vote = IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Constituencies"

    def __unicode__(self):
        return u"{} : {} : {}\n".format(super(Constituency, self).__unicode__(), self.blanks_received, self.can_vote)


PARTS_ORDER = [Voivodeship, Powiat, Gmina, Constituency]