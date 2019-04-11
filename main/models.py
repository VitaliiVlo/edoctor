from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValidationError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if extra_fields.get('role') == UserProfile.DOCTOR and not extra_fields.get('hospital'):
            raise ValidationError(_('The Hospital must be set for doctor'))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class Hospital(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=20)
    street = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=5)
    phone_number = models.CharField(max_length=20)


class UserProfile(AbstractUser):
    PATIENT = 0
    DOCTOR = 1
    NURSE = 2
    ROLES = (
        (PATIENT, "Patient"),
        (DOCTOR, "Doctor"),
        (NURSE, "Nurse")
    )
    MALE = 0
    FEMALE = 1
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )

    email = models.EmailField('email address', unique=True)
    gender = models.IntegerField(choices=GENDER_CHOICES)
    role = models.IntegerField(choices=ROLES)
    phone_number = models.CharField(max_length=20)
    birthday = models.DateField()
    city = models.CharField(max_length=20)
    street = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=5)

    # only for doctors
    hospital = models.ForeignKey(Hospital, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['gender', 'role', 'phone_number', 'birthday', 'city', 'street', 'zip_code']
    objects = CustomUserManager()

    def is_admin(self):
        return self.is_superuser or self.is_staff

    def can_change_visit(self):
        return self.role == self.DOCTOR or self.role == self.NURSE or self.is_admin()


class Visit(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    patient = models.ForeignKey(UserProfile, related_name="visits_patient", null=True, blank=True)
    doctor = models.ForeignKey(UserProfile, related_name="visits_doctor")

    class Meta:
        unique_together = (('start_date', 'doctor'),
                           ('end_date', 'doctor'))

    def save(self, *args, **kwargs):
        visits = Visit.objects.filter(Q(start_date__gte=self.start_date) & Q(start_date__lt=self.end_date) |
                                      Q(end_date__gt=self.start_date) & Q(end_date__lte=self.end_date))
        if visits.exists():
            return
        super(Visit, self).save(*args, **kwargs)
