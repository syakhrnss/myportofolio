"""
API view portofolio di bawah /api/v1/ (function-based, @api_view).

Pembagian tugas:

* main/permissions.py  siapa yang boleh melakukan apa (403),
* main/serializers.py  bentuk data, validasi, dan pembersihan input (400),
* main/selectors.py    pencarian, filter, dan pengurutan,
* main/services.py     operasi write yang bisa digunakan bersama (toggle star),
* main/api_views.py    hanya HTTP, memilih method, status, dan response.

Urutan satu request: autentikasi -> permission -> pemeriksaan method ->
isi view (cari objek, serializer) -> response.
"""

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Experience, Project
from main.permissions import (
    IsPortfolioOwnerOrEditorOrReadOnly, IsPortfolioOwnerOrReadOnly,
)
from main.selectors import search_experiences, search_projects, with_starred_users
from main.serializers import ExperienceSerializer, ProjectSerializer
from main.services import toggle_star


# helpers

def _context(request):
    # Konteks serializer, is_starred bergantung pada pengguna request.
    return {"request": request}


def _list_response(serializer_class, queryset, request):
    serializer = serializer_class(queryset, many=True, context=_context(request))
    return Response(serializer.data)


def _save_response(serializer_class, request, instance=None):
    # Validasi lalu simpan; dipakai untuk POST, PUT, dan PATCH.
    # instance=None berarti membuat data baru (201). Dengan instance,
    # PATCH bersifat parsial (field yang tidak dikirim tetap), sedangkan PUT
    # mewajibkan semua field. Input salah menghasilkan 400 beserta error per field.
    
    serializer = serializer_class(
        instance, data=request.data,
        partial=request.method == "PATCH", context=_context(request),
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    code = status.HTTP_201_CREATED if instance is None else status.HTTP_200_OK
    return Response(serializer.data, status=code)


def _get_object(model, pk, request):
    # Ambil satu objek atau 404. Relasi star hanya di-prefetch jika respons akan memuatnya
    # DELETE tidak membutuhkannya.
    queryset = model.objects.all()
    if request.method != "DELETE":
        queryset = with_starred_users(queryset)
    return get_object_or_404(queryset, pk=pk)


def _detail_response(model, serializer_class, pk, request):
    # GET untuk detail, PUT/PATCH untuk ubah, DELETE untuk hapus (204).
    instance = _get_object(model, pk, request)
    if request.method == "DELETE":
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    if request.method in ("PUT", "PATCH"):
        return _save_response(serializer_class, request, instance)
    return Response(serializer_class(instance, context=_context(request)).data)


def _star_response(model, serializer_class, pk, request):
    # Toggle star lalu return data terbaru agar frontend dapat memperbaruinya.
    # Objek sengaja tidak di-prefetch karena cache lama akan tidak valid setelah star diubah.
    instance = get_object_or_404(model, pk=pk)
    toggle_star(instance, request.user)
    return Response(serializer_class(instance, context=_context(request)).data)


# Projects

@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def project_list(request):
    # GET: daftar (?title=, ?sort=stars). POST: create (hanya owner)
    if request.method == "POST":
        return _save_response(ProjectSerializer, request)
    return _list_response(ProjectSerializer, search_projects(request.query_params), request)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def project_detail(request, project_id):
    # GET: detail. PUT/PATCH: ubah (Owner/Editor). DELETE: hapus (owner).
    return _detail_response(Project, ProjectSerializer, project_id, request)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def project_star(request, project_id):
    # Beri atau batalkan star hanya untuk akun yang sudah login.
    return _star_response(Project, ProjectSerializer, project_id, request)


# Experience

@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_list(request):
    # GET: daftar (?title=, ?category=, ?sort=stars). POST: create (hanya owner).
    if request.method == "POST":
        return _save_response(ExperienceSerializer, request)
    return _list_response(
        ExperienceSerializer, search_experiences(request.query_params), request,
    )


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_detail(request, experience_id):
    # GET: detail. PUT/PATCH: ubah (Owner/Editor). DELETE: hapus (owner).
    return _detail_response(Experience, ExperienceSerializer, experience_id, request)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def experience_star(request, experience_id):
    # Beri atau batalkan star hanya untuk akun yang sudah login.
    return _star_response(Experience, ExperienceSerializer, experience_id, request)