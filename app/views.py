from collections import defaultdict

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import View
from django.views.generic.list import ListView
from bulk_update.helper import bulk_update

from app.models import Voivodeship, Powiat, Gmina, Constituency


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

    def _error(self, message):
        context = self.get_context_data()
        context["error"] = message
        return self.render_to_response(context)

    def post(self, *args, **kwargs):
        request, gmina_id = args
        gmina = get_object_or_404(Gmina, pk=gmina_id)
        post_data = dict(request.POST.iteritems())
        post_data.pop("csrfmiddlewaretoken", 0)
        form_version = int(post_data.pop("version", 0))
        if form_version < gmina.version:
            return self._error("modified")
        new_values = defaultdict(dict)
        for key, value in post_data.iteritems():
            id, field = key.split("_", 1)
            if field not in ["can_vote", "blanks_received"]:
                return self._error("unknown_field")
            new_values[int(id)].update({field: value})
        constituencies = []
        for key, value in new_values.iteritems():
            constituency = get_object_or_404(Constituency, pk=key)
            constituency.can_vote = value.pop("can_vote", constituency.can_vote)
            constituency.blanks_received = value.pop("blanks_received", constituency.blanks_received)
            constituencies.append(constituency)
        bulk_update(constituencies, update_fields=["can_vote", "blanks_received"])
        gmina.version += 1
        gmina.save()
        return redirect(gmina, permanent=True)


class ConstituencyView(View):
    def get(self, request, pk):
        constituency = get_object_or_404(Constituency, pk=pk)
        return JsonResponse({"blanks_received": constituency.blanks_received,
                             "can_vote": constituency.can_vote,
                             "version": constituency.version})

    def post(self, request, pk):
        constituency = get_object_or_404(Constituency, pk=pk)
        post_data = dict(self.request.POST.iteritems())
        post_data.pop("csrfmiddlewaretoken", 0)
        form_version = int(post_data.pop("version", 0))
        if form_version < constituency.version:
            raise ValueError("old version")
        can_vote = int(post_data.pop("can_vote", 0))
        if can_vote < 0:
            raise ValueError("can_vote < 0")
        blanks_received = int(post_data.pop("blanks_received", 0))
        if blanks_received < 0:
            raise ValueError("blanks_received < 0")
        constituency.can_vote = can_vote
        constituency.blanks_received = blanks_received
        constituency.version = constituency.version + 1
        constituency.save()
        return JsonResponse({"blanks_received": constituency.blanks_received,
                             "can_vote": constituency.can_vote,
                             "version": constituency.version})

