from django.db import models
from django.contrib.auth.models import User
from lib.base_classes import BaseModel
import random
from lib.validators import pin_validator
from django.core.exceptions import ValidationError
from api.config import States


def validate_pin(value):
    if not pin_validator(value):
        raise ValidationError(
            _('Invalid Pin Code')
        )

class BaseOTPModel(BaseModel):
    is_verified = models.BooleanField(blank=False, default=False)
    request_id = models.CharField(max_length=50, unique=True)
    otp = models.CharField(max_length=6)
    attempts = models.IntegerField(default=0)
    expiry_time = models.DateTimeField(null=True, blank=True)
    white_listed = models.BooleanField(
        default=False,
    )
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    @classmethod
    def white_list(cls, otp, username):
        try:
            otp_verification = cls.objects.get(username=username)
        except cls.DoesNotExist:
            otp_verification = cls(username=username)

        otp_verification.otp = otp
        otp_verification.requestId = str(uuid.uuid4())
        otp_verification.white_listed = True
        otp_verification.full_clean()
        otp_verification.save()

    @classmethod
    def unwhite_list(cls, username):
        otp_verification = cls.objects.get(
            username=username,
            white_listed=True
        )
        otp_verification.white_listed = False
        otp_verification.full_clean()
        otp_verification.save()

    def generateOTP(self) :
        digits = "0123456789"
        otp = "".join(random.choices(digits, k=6))
        return otp

    class Meta:
        abstract = True


class MobileOTP(BaseOTPModel):
    username = models.CharField(max_length=10)
    # mode = models.CharField(
    #     max_length=10,
    #     choices=[(tag.name, tag.value) for tag in OtpModes],
    #     default=OtpModes.SMS.name
    # )

class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=15, null=True, blank=True)
    email = models.CharField(max_length=40, default='', blank=True)

    def __str__(self):
        return f"{self.name}"


class Address(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    address = models.CharField(max_length=60)
    city = models.CharField(max_length=255)
    state = models.CharField(
        max_length=2,
        choices=[(x.name, x.value) for x in States]
    )
    pin = models.CharField(
        max_length=6,
        validators=[validate_pin],
    )
    landmark = models.TextField(max_length=1023, default='', blank=True, null=True)
    # location = PointField(null=True, blank=True)
