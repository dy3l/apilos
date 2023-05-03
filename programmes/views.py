from http.client import BAD_REQUEST

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from conventions.models import Convention
from conventions.services.conventions import ConventionListService
from programmes.services import get_or_create_conventions_from_operation_number
from siap.siap_client.utils import IncompleteBailleurDataException


@login_required
def operation_conventions(request, numero_operation):

    # Décorator ?
    if not request.user.is_cerbere_user():
        raise PermissionError("this function is available only for CERBERE user")

    try:
        (programme, _, _) = get_or_create_conventions_from_operation_number(
            request, numero_operation
        )
    except IncompleteBailleurDataException as e:
        return render(
            "400.html",
            {
                "message": f"Impossible de créer la convention de l'opération {numero_operation}: {e}"
            },
            status=BAD_REQUEST,
        )

    service = ConventionListService(
        order_by=request.GET.get("order_by", "programme__date_achevement_compile"),
        page=request.GET.get("page", 1),
        user=request.user,
        my_convention_list=Convention.objects.filter(programme=programme)
        .prefetch_related("programme")
        .prefetch_related("programme__administration")
        .prefetch_related("lot"),
    )
    service.paginate()

    return render(
        request,
        "operations/conventions.html",
        {
            "numero_operation": numero_operation,
            "programme": programme,
            #            "lots": lots,
            "conventions": service,
        },
    )
