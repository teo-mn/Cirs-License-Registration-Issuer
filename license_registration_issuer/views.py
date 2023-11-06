
from rest_framework import generics


class BasicView(generics.GenericAPIView):
    def post(self):
        pass


class RegisterView(BasicView):
    pass


class UpdateDurationView(BasicView):
    pass


class AddEmployeeView(BasicView):
    pass


class RemoveEmployeeView(BasicView):
    pass
