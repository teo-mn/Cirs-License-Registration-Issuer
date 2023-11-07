import logging
import json

from rest_framework.exceptions import ValidationError as ValidationErrorDjango
from django.http import HttpResponse
from jsonschema import ValidationError
from rest_framework import generics

from license_registration_issuer.models import Request, RequestType
from license_registration_issuer.schemas.register import RegisterSchema
from license_registration_issuer.validate import parse_error_message, CustomValidator
from license_registration_issuer.tasks import register_task


class BasicView(generics.GenericAPIView):
    JSONSchema = RegisterSchema
    defaultType = RequestType.REGISTER

    def post(self, request):
        self.validate()
        instance = self.save_instance()
        self.add_to_queue(str(instance.id))
        return HttpResponse(status=201)

    def validate(self):
        """
        :return:
        """
        try:
            CustomValidator(self.JSONSchema).validate(self.request.data)
        except ValidationError as e:
            msg = parse_error_message(e)
            raise ValidationErrorDjango({"error_msg": msg})
        except Exception as e:
            logging.error(e)
            raise RuntimeError(str(e))

    def save_instance(self):
        data = self.request.data
        # TODO:
        # if Request.objects.filter(id=data['request_id']).count() > 0:
        #     raise ValidationErrorDjango({"error_msg": '[request_id] already exists'})
        instance = Request.objects.create(
            # id=data['request_id'],
            request_type=self.defaultType,
            callback_url=data['callback_url'],
            data=json.dumps(data['payload'])
        )
        instance.save()
        return instance

    def add_to_queue(self, request_id):
        pass


class RegisterView(BasicView):
    JSONSchema = RegisterSchema

    def add_to_queue(self, request_id):
        register_task.delay(request_id)


class UpdateDurationView(BasicView):

    def add_to_queue(self, request_id):
        pass


class AddEmployeeView(BasicView):

    def add_to_queue(self, request_id):
        pass


class RemoveEmployeeView(BasicView):

    def add_to_queue(self, request_id):
        pass
