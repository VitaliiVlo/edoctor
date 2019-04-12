from datetime import date

from rest_framework import serializers

from main.models import UserProfile, Hospital, Visit


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ['pk', 'first_name', 'last_name', 'email', 'gender', 'role', 'phone_number', 'birthday', 'city',
                  'street', 'zip_code', 'hospital', 'password']

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class BaseDoctorPatientSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField(read_only=True)
    gender = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['pk', 'first_name', 'last_name', 'gender', 'age']

    @staticmethod
    def get_age(instance):
        today = date.today()
        return today.year - instance.birthday.year - ((today.month, today.day) < (instance.birthday.month,
                                                                                  instance.birthday.day))

    @staticmethod
    def get_gender(instance):
        return dict(UserProfile.GENDER_CHOICES)[instance.gender]


class PatientSerializer(BaseDoctorPatientSerializer):
    class Meta:
        model = UserProfile
        fields = ['pk', 'first_name', 'last_name', 'gender', 'age',
                  'email', 'phone_number', 'city', 'street', 'zip_code']


class DoctorSerializer(BaseDoctorPatientSerializer):
    class Meta:
        model = UserProfile
        fields = ['pk', 'first_name', 'last_name', 'gender', 'age']


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['pk', 'name', 'city', 'street', 'zip_code', 'phone_number']


class VisitSerializer(serializers.ModelSerializer):
    patient_details = serializers.SerializerMethodField(read_only=True)
    doctor_details = serializers.SerializerMethodField(read_only=True)
    time = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Visit
        fields = ['pk', 'start_date', 'end_date', 'patient', 'doctor',
                  'patient_details', 'doctor_details', 'time']

    def update(self, instance, validated_data):
        instance.patient = validated_data.get('patient', instance.patient)
        instance.save()
        return instance

    def get_patient_details(self, instance):
        user = self.context.get('user')
        if not user.can_change_visit() and instance.patient != user:
            return {"first_name": "Patient"}
        return PatientSerializer(instance.patient).data

    @staticmethod
    def get_doctor_details(instance):
        return DoctorSerializer(instance.patient).data

    @staticmethod
    def get_time(instance):
        return "%s - %s" % (instance.start_date.strftime('%H:%M'), instance.end_date.strftime('%H:%M'))
