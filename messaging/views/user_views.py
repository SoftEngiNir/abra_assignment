from django.forms.models import model_to_dict
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView

from .views_utils import create_db_user, decode_bytes, get_user


class DetailUserView(DetailView):
    def get(self, request: HttpRequest) -> JsonResponse:
        user_id = request.user.id
        user_instance = get_user(user_id)
        if not user_instance:
            return JsonResponse(
                {"error": f"User with ID {user_id} does not exist..."}, status=404
            )
        return JsonResponse(model_to_dict(user_instance))


@method_decorator(csrf_exempt, name="dispatch")
class CreateUserView(CreateView):
    def post(self, request: HttpRequest) -> JsonResponse:
        body_json = decode_bytes(request.body)

        user_instance = create_db_user(**body_json)
        return JsonResponse(model_to_dict(user_instance))
