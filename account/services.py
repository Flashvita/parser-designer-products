from djoser import signals
from djoser.compat import get_user_email
from djoser.conf import settings
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action



class RegistrationMixin(viewsets.ModelViewSet):
    """
    Mixin for registration owner and worker
    with send email for activation account
    """
   
    def perform_create(self, serializer):
        user = serializer.save()
        signals.user_registered.send(
            sender=self.__class__, user=user, request=self.request
        )
        context = {"user": user}
        to = [get_user_email(user)]
        if settings.SEND_ACTIVATION_EMAIL:
            settings.EMAIL.activation(self.request, context).send(to)
        elif settings.SEND_CONFIRMATION_EMAIL:
            settings.EMAIL.confirmation(self.request, context).send(to)

    @action(["post"], detail=False)
    def activation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user.is_active = True
        user.save()
        signals.user_activated.send(
            sender=self.__class__, user=user, request=self.request
        )
        if settings.SEND_CONFIRMATION_EMAIL:
            context = {"user": user}
            to = [get_user_email(user)]
            settings.EMAIL.confirmation(self.request, context).send(to)

        return Response(status=status.HTTP_204_NO_CONTENT)

