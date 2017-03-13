from django.shortcuts import render

from dal import autocomplete

from aspendb.models import Employee


class EmployeeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Employee.objects.none()

        qs = Employee.objects.all()

        if self.q:
            qs = qs.filter(first_name__istartswith=self.q)

        return qs

