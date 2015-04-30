from django.http.response import HttpResponseForbidden

from django.shortcuts import get_object_or_404

from django.views.generic.list import ListView

from crawlers.models import Voivodeship, Powiat, Gmina, Constituency


class AdminPartListView(ListView):
    template_name = "admin_part_list.html"

    def get_queryset(self):
        parent_model = self.model.get_parent_model()
        if parent_model:
            return self.model.objects.filter(
                **{parent_model.get_name().lower(): get_object_or_404(parent_model, pk=self.args[0])})
        else:
            return super(AdminPartListView, self).get_queryset()

    def get_context_data(self, **kwargs):
        self.object_list = self.get_queryset()
        context = super(AdminPartListView, self).get_context_data(**kwargs)
        child_model = self.model.get_child_model()
        parent_model = self.model.get_parent_model()
        context["this_view_name"] = self.model.get_name_plural().lower()
        if child_model:
            context["part_view_name"] = child_model.get_name_plural().lower()
        context["path"] = [{"view_name": "voivodeships",
                            "name": "Polska"}]
        if parent_model:
            context["object"] = get_object_or_404(parent_model, pk=self.args[0])
            context["path"] += context["object"].get_path()
        return context


class Voivodeships(AdminPartListView):
    model = Voivodeship


class Powiats(AdminPartListView):
    model = Powiat


class Gminas(AdminPartListView):
    model = Gmina


class Constituencies(AdminPartListView):
    model = Constituency

    def post(self, *args, **kwargs):
        request, gmina_id = args
        gmina = get_object_or_404(Gmina, pk=gmina_id)
        form_version = int(request.POST.get("version"))
        if form_version < gmina.version:
            context = self.get_context_data()
            context["error"] = "Modified"
            return self.render_to_response(context)
        for key, value in request.POST.iteritems():
            if key == "csrfmiddlewaretoken" or key == "version":
                continue
            id, field = key.split("_", 1)
            constituency = get_object_or_404(Constituency, pk=id)
            if field == "blanks_received":
                constituency.blanks_received = int(value)
            elif field == "can_vote":
                constituency.can_vote = int(value)
            else:
                return HttpResponseForbidden()
            constituency.save()
        gmina.version += 1
        gmina.save()
        return self.get(*args, **kwargs)
