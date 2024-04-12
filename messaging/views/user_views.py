from django.forms.models import model_to_dict
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView

from .views_utils import create_db_user, get_user


class DetailUserView(DetailView):
    def get(self, request: HttpRequest, user_id) -> JsonResponse:
        user_instance = get_user(user_id)
        if not user_instance:
            return JsonResponse(
                {"error": f"User with ID {user_id} does not exist..."}, status=404
            )
        return JsonResponse(model_to_dict(user_instance))


@method_decorator(csrf_exempt, name="dispatch")
class CreateUserView(CreateView):
    def post(
        self, request: HttpRequest, username, password, first_name, last_name, **kwargs
    ) -> JsonResponse:
        user_instance = create_db_user(
            username, password, first_name, last_name, **kwargs
        )
        return JsonResponse(model_to_dict(user_instance))
