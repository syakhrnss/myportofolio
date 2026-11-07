"""
Permission adalah class DRF untuk otorisasi berdasarkan empat role dari Tugas 4.

Autentikasi (siapa pengirimnya) ditangani SessionAuthentication pada
view, file ini hanya memutuskan apa yang boleh dilakukan pengirim itu.

==================  =====  ====  ==========  ======
Peran               Baca   Star  PUT/PATCH   POST/DELETE
==================  =====  ====  ==========  ======
Pengunjung          ya     -     -           -
Pengguna biasa      ya     ya    -           -
Editor              ya     ya    ya          -
Pemilik (superuser) ya     ya    ya          ya
==================  =====  ====  ==========  ======

Hak star tidak diatur di sini karena endpoint star memakai IsAuthenticated.
"""

from rest_framework.permissions import SAFE_METHODS, BasePermission

EDITOR_GROUP_NAME = "Editor"
EDITOR_METHODS = ("PUT", "PATCH")


def is_editor(user):
    """True jika pengguna login dan tergabung dalam grup Editor."""
    return (
        user.is_authenticated
        and user.groups.filter(name=EDITOR_GROUP_NAME).exists()
    )


class IsPortfolioOwnerOrReadOnly(BasePermission):
    # Read bisa dilakukan semua orang, write hanya bisa dilakukan owner (superuser).

    message = "Only the portfolio owner can change projects."

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_superuser
        )


class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    # Read bisa untuk semua, PUT/PATCH untuk owner dan Editor; sisanya owner.
    # Dicek di has_permission (sebelum objek dicari), sehingga pengguna
    # tanpa hak mendapat 403 walaupun objek yang diminta tidak ada.

    message = (
        "Hanya pemilik portofolio yang dapat membuat atau menghapus data; "
        "Editor hanya dapat mengubah data."
    )

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return request.method in EDITOR_METHODS and is_editor(request.user)