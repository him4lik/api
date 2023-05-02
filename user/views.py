from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import MobileOTP, Profile, Address
import uuid
from datetime import datetime, timedelta
from rest_framework.response import Response
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction

def get_user(mobile, is_active):
    try:
        user = User.objects.get(username=mobile)
        if is_active and not user.is_active:
            user.is_active = is_active
            user.save()

    except User.DoesNotExist:
        with transaction.atomic():
            user = User.objects.create_user(username=mobile)
            user.is_active = is_active
            user.save()
            profile = Profile(user=user)
            profile.save()
    return user

class WhiteListUser(APIView):
    def get(self, request):
        wl_mobiles = list(MobileOTP.objects.filter(
            white_listed=True
        ).values_list('mobile', flat=True))
        return Response(wl_mobiles)

    def post(self, request):
        phone = str(request.data['phone'])
        otp = str(request.data['otp'])
        MobileOTP.white_list(phone, otp)
        return Response(status=200)

class RemoveWhiteListedUser(APIView):
    def post(self, request):
        phone = request.data['phone']
        MobileOTP.unwhite_list(phone)
        return Response(status=200)

def send_mobile_msg(phone, name):
    validate_phone_number(phone)
    user = get_user(phone, False)
    notification_type = NotificationType.PAYMENT_REMINDER_1
    obj = Notification.create_sms_notification(
            user, notification_type,
            LanguageChoices(language)
        )
    obj.send(name)

def verify_otp(request_id, user_otp):
    msg = None
    try:
        otp = MobileOTP.objects.get(request_id=request_id)
    except MobileOTP.DoesNotExist:
        msg =  {"text":"requestId does not exist", "status":404}
        return msg

    if not otp.white_listed:
        if otp.expiry_time is None or otp.expiry_time <= timezone.now() or otp.attempts > 3:
            if otp.attempts > 3:
                msg = {"text":"Max number of attempts reached", "status":400}
            else:
                msg = {"text":"OTP is expired", "status":400}
            otp.attempts = 0
            otp.expiry_time = None
            otp.full_clean()
            otp.save()
            return msg

    if otp.otp != user_otp:
        otp.attempts += 1
        otp.full_clean()
        otp.save()
        msg = {"text":"OTP is wrong", "status":400}
        return msg

    otp.is_verified = True
    otp.expiry_time = None
    otp.attempts = 0
    otp.full_clean()
    otp.save()

# def send_mobile_otp(phone, otp):
#     validate_phone_number(phone)
#     user = get_user(phone, False)
#     notification_type = NotificationType.OTP_GENERATED
#     obj = Notification.create_sms_notification(
#             user, notification_type,
#             LanguageChoices(language)
#         )
#     obj.send(otp.otp)

class LoginOTPView(APIView):
    permission_classes=[AllowAny]

    def get(self, request):
        phone = request.query_params.get('phone')
        try:
            otp = MobileOTP.objects.get(username=phone)
        except MobileOTP.DoesNotExist:
            otp = MobileOTP(username=phone)

        request_id = str(uuid.uuid4())
        otp.request_id = request_id
        if otp.white_listed:
            otp.full_clean()
            otp.save()
            return Response({'requestId': request_id})

        if otp.expiry_time is None or otp.expiry_time < timezone.now():
            otp.expiry_time = datetime.now() + timedelta(seconds=900)
            otp.otp = otp.generateOTP()
        print(otp.otp)
        otp.full_clean()
        otp.save()
        # send_mobile_otp(phone, otp)

        return Response({"request_id": request_id})

    def post(self, request):
        request_id = request.data['request_id']
        otp = request.data['otp']
        res = verify_otp(request_id, otp)
        if res:
            return Response(res['text'], status=res['status'])

        otp = MobileOTP.objects.get(request_id=request_id)
        flag = False
        user_obj = get_user(otp.username, True)
        refresh = RefreshToken.for_user(user_obj)
        print(refresh)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

class GetUserView(APIView):
    permission_classes=[AllowAny]

    def get(self, request):
        user = request.user
        print(user)
        if user.is_authenticated:
            profile = user.profile
            data = {
                "is_authenticated":True,
                "username":user.username,
                "name":profile.name,
                }
        else:
            data={"is_authenticated":False}
        return Response(data)