import logging
import json

from rest_framework.exceptions import ValidationError as ValidationErrorDjango
from django.http import HttpResponse
from jsonschema import ValidationError
from rest_framework import generics

from license_registration_issuer.models import Request, RequestType
from license_registration_issuer.schemas.add_employee import AddEmployeeSchema
from license_registration_issuer.schemas.add_requirement import AddRequirementSchema
from license_registration_issuer.schemas.register import RegisterSchema
from license_registration_issuer.schemas.remove_employee import RemoveEmployeeSchema
from license_registration_issuer.schemas.remove_requirement import RemoveRequirementSchema
from license_registration_issuer.schemas.revoke import RevokeSchema
from license_registration_issuer.schemas.update import UpdateSchema
from license_registration_issuer.validate import parse_error_message, CustomValidator
from license_registration_issuer.tasks.register import register_task
from license_registration_issuer.tasks.add_employee import add_employee_task
from license_registration_issuer.tasks.remove_employee import remove_employee_task
from license_registration_issuer.tasks.update import update_task
from license_registration_issuer.tasks.revoke import revoke_task
from license_registration_issuer.tasks.add_requirement import add_requirement_task
from license_registration_issuer.tasks.remove_requirement import remove_requirement_task


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


class UpdateView(BasicView):
    JSONSchema = UpdateSchema
    defaultType = RequestType.UPDATE_DURATION

    def add_to_queue(self, request_id):
        update_task.delay(request_id)


class AddEmployeeView(BasicView):
    JSONSchema = AddEmployeeSchema
    defaultType = RequestType.ADD_EMPLOYEE

    def add_to_queue(self, request_id):
        add_employee_task.delay(request_id)


class RemoveEmployeeView(BasicView):
    JSONSchema = RemoveEmployeeSchema
    defaultType = RequestType.REMOVE_EMPLOYEE

    def add_to_queue(self, request_id):
        remove_employee_task.delay(request_id)


class RevokeView(BasicView):
    JSONSchema = RevokeSchema
    defaultType = RequestType.REVOKE

    def add_to_queue(self, request_id):
        revoke_task.delay(request_id)


class AddRequirementView(BasicView):
    JSONSchema = AddRequirementSchema
    defaultType = RequestType.ADD_REQUIREMENT

    def add_to_queue(self, request_id):
        add_requirement_task.delay(request_id)


class RemoveRequirementView(BasicView):
    JSONSchema = RemoveRequirementSchema
    defaultType = RequestType.REMOVE_REQUIREMENT

    def add_to_queue(self, request_id):
        remove_requirement_task.delay(request_id)
