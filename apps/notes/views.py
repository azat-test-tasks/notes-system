from django.utils.decorators import method_decorator

from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, permissions, viewsets

from apps.notes.models import Note
from apps.notes.serializers import NoteSerializer


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="The route is to view all roles.",
        operation_summary="View all notes",
        tags=["Notes"],
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_description="The route is to create a note",
        operation_summary="Create a note",
        tags=["Notes"],
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description="The route is to view detail note.",
        operation_summary="View detail notes",
        tags=["Notes"],
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_description="The route is to update notes.",
        operation_summary="Partial update notes",
        tags=["Notes"],
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_description="The route is to partial update note",
        operation_summary="Update notes",
        tags=["Notes"],
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_description="The route is to delete notes.",
        operation_summary="Delete notes",
        tags=["Notes"],
    ),
)
class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all().prefetch_related("user")
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    search_fields = ("title", "description")
    filterset_fields = ("title",)
    ordering_fields = ("created_at",)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Note.objects.filter(user=self.request.user)
        else:
            return Note.objects.none()
