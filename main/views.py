import datetime
from io import BytesIO

from django.db.models import Q
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from weasyprint import HTML

from main.decorators import parse_json
from main.http import json_error
from main.models import Hospital, Visit, UserProfile
from main.permissions import IsAdminOrReadOnly, IsDoctor
from main.serializers import UserSerializer, HospitalSerializer, VisitSerializer
from main.utils import create_visit_for_doctor


class UserView(APIView):
    @method_decorator(csrf_exempt)
    @method_decorator(parse_json)
    def dispatch(self, *args, **kwargs):
        return super(UserView, self).dispatch(*args, **kwargs)

    @staticmethod
    @permission_classes((IsDoctor,))
    def get(request):
        name = request.GET.get('name', '')
        role = request.GET.get('role', UserProfile.PATIENT)
        users = UserProfile.objects.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name), role=role)
        user_serializer = UserSerializer(users, many=True)
        return JsonResponse(user_serializer.data, safe=False)

    @staticmethod
    def post(request):
        user_serializer = UserSerializer(data=request.json)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse({})
        return json_error(user_serializer.errors)


class UserDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    @method_decorator(csrf_exempt)
    @method_decorator(parse_json)
    def dispatch(self, *args, **kwargs):
        return super(UserDetailView, self).dispatch(*args, **kwargs)

    @staticmethod
    def get(request):
        user_serializer = UserSerializer(request.user)
        return JsonResponse(user_serializer.data)

    @staticmethod
    def patch(request):
        user_serializer = UserSerializer(request.user, data=request.json, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse(user_serializer.data)
        return json_error(user_serializer.errors)


class HospitalListView(APIView):
    permission_classes = (IsAdminOrReadOnly,)

    @method_decorator(csrf_exempt)
    @method_decorator(parse_json)
    def dispatch(self, *args, **kwargs):
        return super(HospitalListView, self).dispatch(*args, **kwargs)

    @staticmethod
    def get(request):
        name = request.GET.get('name', '')
        hospitals = Hospital.objects.filter(name__icontains=name)
        hospital_serializer = HospitalSerializer(hospitals, many=True)
        return JsonResponse(hospital_serializer.data, safe=False)

    @staticmethod
    def post(request):
        hospital_serializer = HospitalSerializer(data=request.json)
        if hospital_serializer.is_valid():
            hospital_serializer.save()
            return JsonResponse({})
        return json_error(hospital_serializer.errors)


class HospitalDetailView(APIView):
    permission_classes = (IsAdminOrReadOnly,)

    @method_decorator(csrf_exempt)
    @method_decorator(parse_json)
    def dispatch(self, *args, **kwargs):
        kwargs['hospital'] = get_object_or_404(Hospital, pk=kwargs.get('pk'))
        return super(HospitalDetailView, self).dispatch(*args, **kwargs)

    @staticmethod
    def get(request, pk, hospital):
        hospital_serializer = HospitalSerializer(hospital)
        return JsonResponse(hospital_serializer.data)

    @staticmethod
    def patch(request, pk, hospital):
        hospital_serializer = HospitalSerializer(hospital, data=request.json, partial=True)
        if hospital_serializer.is_valid():
            hospital_serializer.save()
            return JsonResponse(hospital_serializer.data)
        return json_error(hospital_serializer.errors)

    @staticmethod
    def delete(request, pk, hospital):
        hospital.delete()
        return JsonResponse({})


class VisitListView(APIView):
    permission_classes = (IsAuthenticated,)

    @method_decorator(csrf_exempt)
    @method_decorator(parse_json)
    def dispatch(self, *args, **kwargs):
        return super(VisitListView, self).dispatch(*args, **kwargs)

    @staticmethod
    def get(request):
        date = request.GET.get('date')
        if not date:
            return json_error('You must specify date')
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        doctor_id = request.GET.get('doctor')
        if not doctor_id:
            return json_error('You must specify doctor')
        try:
            doctor = UserProfile.objects.get(pk=doctor_id)
        except UserProfile.DoesNotExist:
            return json_error('You must specify id of existing doctor')
        create_visit_for_doctor(doctor, date)
        visits = Visit.objects.filter(doctor=doctor, start_date__date=date).order_by('start_date')
        visit_serializer = VisitSerializer(visits, many=True, context={'user': request.user})

        if request.GET.get('export', False):
            context = {
                'visits': visit_serializer.data,
                'doctor': doctor,
                'date': date
            }
            html = render_to_string('export.html', context=context)
            html_document = HTML(string=html)
            pdf_buffer = BytesIO()
            html_document.write_pdf(pdf_buffer)
            response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="report_%s_%s.pdf"' % (doctor.get_full_name(),
                                                                                           date.strftime("%d %b %Y"))
            return response
        return JsonResponse(visit_serializer.data, safe=False)

    # @staticmethod
    # def post(request):
    #     if not request.user.can_change_visit() and request.user.pk != request.json.get('patient'):
    #         return json_error("You don't have permission to add visit for another user")
    #     visit_serializer = VisitSerializer(data=request.json, context={'user': request.user})
    #     if visit_serializer.is_valid():
    #         visit_serializer.save()
    #         return JsonResponse({})
    #     return json_error(visit_serializer.errors)


class VisitDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    @method_decorator(csrf_exempt)
    @method_decorator(parse_json)
    def dispatch(self, *args, **kwargs):
        kwargs['visit'] = get_object_or_404(Visit, pk=kwargs.get('pk'))
        return super(VisitDetailView, self).dispatch(*args, **kwargs)

    @staticmethod
    def patch(request, pk, visit):
        if not request.user.can_change_visit() and visit.patient and (visit.patient != request.user or
                                                                      visit.patient.pk != request.json.get('patient')):
            return json_error("You don't have permission to change visit for another user")
        visit_serializer = VisitSerializer(visit, data=request.json, partial=True, context={'user': request.user})
        if visit_serializer.is_valid():
            visit_serializer.save()
            return JsonResponse(visit_serializer.data)
        return json_error(visit_serializer.errors)

    @staticmethod
    def delete(request, pk, visit):
        if not request.user.can_change_visit() and visit.patient != request.user:
            return json_error("You don't have permission to remove visit for another user")
        visit.patient = None
        visit.save()
        return JsonResponse({})
