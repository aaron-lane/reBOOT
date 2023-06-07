# -*- coding: utf-8 -*-
import simplejson as json

from base64 import urlsafe_b64decode
from binascii import Error

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse, QueryDict
from django.views import View
from django.utils import timezone
from django.utils.decorators import method_decorator

from app.models import Donor, Donation, Item


class DonorView(View):
    """DonorView
    - GET: Return JSON serialized Donor object
    - POST: Insert and return that Donor object
    - PUT: Update and return that Donor object
    - DELETE: Delete and return HTTP status code
    """

    def get(self, request):
        try:
            donor = Donor.objects.get(id=request.GET["id"])
            return JsonResponse(donor.camel_serialize(), status=200)
        except ValidationError as e:
            return _error_response(e)
        except Exception as e:
            print(e.args)
            return HttpResponseBadRequest()

    @method_decorator(permission_required("app.can_add_donor"))
    def post(self, request):
        try:
            donor = Donor.objects.create(
                donor_name=request.POST["donorName"],
                email=request.POST["email"],
                want_receipt="wantReceipt" in request.POST,
                telephone_number=request.POST["telephoneNumber"],
                mobile_number=request.POST["mobileNumber"],
                address_line=request.POST["addressLine"],
                city=request.POST["city"],
                province=request.POST["province"],
                postal_code=request.POST["postalCode"],
                customer_ref=request.POST["customerRef"],
                verified="verified" in request.POST
            )
            return JsonResponse(donor.camel_serialize(), status=201)
        except ValidationError as e:
            return _error_response(e)
        except Exception as e:
            print(e.args)
            return HttpResponseBadRequest()

    @method_decorator(permission_required("app.can_change_donor"))
    def put(self, request):
        try:
            request.PUT = QueryDict(request.body)
            donor = Donor.objects.get(id=request.PUT["id"])
            donor.donor_name = request.PUT["donorName"]
            donor.email = request.PUT["email"]
            donor.want_receipt = "wantReceipt" in request.PUT
            donor.telephone_number = request.PUT["telephoneNumber"]
            donor.mobile_number = request.PUT["mobileNumber"]
            donor.address_line = request.PUT["addressLine"]
            donor.city = request.PUT["city"]
            donor.province = request.PUT["province"]
            donor.postal_code = request.PUT["postalCode"]
            donor.customer_ref = request.PUT["customerRef"]
            donor.verified = "verified" in request.PUT
            donor.save()
            return JsonResponse(donor.camel_serialize(), status=200)
        except ValidationError as e:
            return _error_response(e)
        except Exception as e:
            print(e.args)
            return HttpResponseBadRequest()

    @method_decorator(permission_required("app.can_delete_donor"))
    def delete(self, request):
        try:
            request.DELETE = QueryDict(request.body)
            donor = Donor.objects.get(id=request.DELETE["id"])
            donor.delete()
            return JsonResponse({}, status=200)
        except ValidationError as e:
            return _error_response(e)
        except Exception as e:
            print(e.args)
            return HttpResponseBadRequest()


class DonateView(View):
    """DonateView
    - POST: Insert a Donation object based on a Formidable request.
    """
    def post(self, request):
        if "Authorization" not in request.headers:
            print("Authorization header not found in donate request")

            return HttpResponseForbidden()
        
        username_and_password_b64 = request.headers["Authorization"].partition("Basic ")[2]
        if username_and_password_b64 == "":
            print("Base64 encoded basic access authentication credentials not found in donate request")

            return HttpResponseForbidden()
        
        username_and_password = ""
        try:
            username_and_password = urlsafe_b64decode(username_and_password_b64).decode("UTF-8")
        except Error as e:
            print("Invalid Base64 encoding of basic access authentication credentials in donate request", e.args)

            return HttpResponseForbidden()
        
        username, separator, password = username_and_password.partition(":")
        if separator == "":
            print("Invalid basic authentication credentials format in donate request")

        user = authenticate(username=username, password=password)
        if user is None:
            print("Failed to authenticate user '" + username_and_password[0] + "' in donate request")

            return HttpResponseForbidden()
        
        # TODO: determine how to identify a new donor
        donor_id = "1"
        try:
            donation = Donation.objects.create(
                donor=Donor.objects.get(id=donor_id),
                donate_date=timezone.localtime().strptime(
                    request.POST["created_at"], "%Y-%m-%d").date(),
                verified=False,
                # 4jst2 is the key of the postal code field
                pick_up=request.POST["4jst2"]
            )

            return HttpResponse()
        except ValidationError as e:
            print("Invalid donation in donate request", e.args)

            return HttpResponseBadRequest()
        except Exception as e:
            print(e.args)
            return HttpResponseBadRequest()


class DonationView(View):
    """DonationView
    - GET: Return Donation object based on tax_receipt_no
    - GET: Return JSON serialized Donation objects based on donor id
    - POST: Insert and return that Donation object
    - PUT: Update and return that Donation object
    - DELETE: Delete and return HTTP status code
    """

    def get(self, request):
        try:
            donation = Donation.objects.get(
                tax_receipt_no=request.GET["taxReceiptNo"]
            )
            return JsonResponse(donation.camel_serialize(), status=200)
        except ValidationError as e:
            return _error_response(e)
        except Exception as e:
            print(e.args)
            return HttpResponseBadRequest()

    @method_decorator(permission_required("app.can_add_donation"))
    def post(self, request):
        try:
            donation = Donation.objects.create(
                donor=Donor.objects.get(id=request.POST["donorId"]),
                donate_date=timezone.localtime().strptime(
                    request.POST["donateDate"], "%Y-%m-%d").date(),
                verified="verified" in request.POST,
                pick_up=request.POST["pickUp"]
            )
            return JsonResponse(donation.camel_serialize(), status=200)
        except ValidationError as e:
            return _error_response(e)
        except Exception as e:
            print(e.args)
            return HttpResponseBadRequest()

    @method_decorator(permission_required("app.can_change_donation"))
    def put(self, request):
        try:
            request.PUT = QueryDict(request.body)
            donation = Donation.objects.get(
                tax_receipt_no=request.PUT["taxReceiptNo"])
            donation.donate_date = request.PUT["donateDate"]
            donation.verified = "verified" in request.PUT
            donation.pick_up = request.PUT["pickUp"]
            donation.save()
            return JsonResponse(donation.camel_serialize(), status=200)
        except ValidationError as e:
            return _error_response(e)
        except Exception as e:
            print(e.args)
            return HttpResponseBadRequest()

    @method_decorator(permission_required("app.can_delete_donation"))
    def delete(self, request):
        try:
            request.DELETE = QueryDict(request.body)
            donation = Donation.objects.get(
                tax_receipt_no=request.DELETE["taxReceiptNo"])
            donation.delete()
            return JsonResponse({}, status=200)
        except ValidationError as e:
            return _error_response(e)
        except Exception as e:
            print(e.args)
            return HttpResponseBadRequest()


class ItemView(View):
    """ItemView
    - GET: Return JSON serialized Item objects based on donation id
    - POST: Insert and return Item object
    - PUT: Update and return Item object
    - DELETE: Delete and return HTTP status code
    """

    def get(self, request):
        try:
            item = Item.objects.get(id=request.GET["id"])
            return JsonResponse(item.camel_serialize(), status=200)
        except ValidationError as e:
            return _error_response(e)
        except Exception as e:
            print(e.args)
            return HttpResponseBadRequest()

    @method_decorator(permission_required("app.can_add_item"))
    def post(self, request):
        try:
            item = Item.objects.create(
                donation=Donation.objects.get(
                    tax_receipt_no=request.POST["taxReceiptNo"]),
                description=request.POST["description"],
                particulars=request.POST["particulars"],
                manufacturer=request.POST["manufacturer"],
                model=request.POST["model"],
                quantity=_safe_cast(request.POST["quantity"], float, 0),
                working="working" in request.POST,
                condition=request.POST["condition"],
                quality=request.POST["quality"],
                status=request.POST["status"],
                batch=request.POST["batch"],
                value=_safe_cast(request.POST["value"], float, 0.0),
                verified="verified" in request.POST
            )
            return JsonResponse(item.camel_serialize(), status=200)
        except ValidationError as e:
            return _error_response(e)
        except Exception as e:
            print(e.args)
            return HttpResponseBadRequest()

    @method_decorator(permission_required("app.can_change_item"))
    def put(self, request):
        try:
            request.PUT = QueryDict(request.body)
            item = Item.objects.get(id=request.PUT["id"])
            item.description = request.PUT["description"]
            item.particulars = request.PUT["particulars"]
            item.manufacturer = request.PUT["manufacturer"]
            item.model = request.PUT["model"]
            item.quantity = _safe_cast(request.PUT["quantity"], float, 0)
            item.working = "working" in request.PUT
            item.condition = request.PUT["condition"]
            item.quality = request.PUT["quality"]
            item.status = request.PUT["status"],
            item.batch = request.PUT["batch"]
            item.value = _safe_cast(request.PUT["value"], float, 0.0)
            item.verified = "verified" in request.PUT
            item.save()
            return JsonResponse(item.camel_serialize(), status=200)
        except ValidationError as e:
            return _error_response(e)
        except Exception as e:
            print(e.args)
            return HttpResponseBadRequest()

    @method_decorator(permission_required("app.can_delete_item"))
    def delete(self, request):
        try:
            request.DELETE = QueryDict(request.body)
            item = Item.objects.get(id=request.DELETE["id"])
            item.delete()
            return JsonResponse({}, status=200)
        except ValidationError as e:
            return _error_response(e)
        except Exception as e:
            print(e.args)
            return HttpResponseBadRequest()


"""
Private Methods
"""


def _safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default


def _error_response(err):
    return JsonResponse({"errors": err.messages}, status=400)
