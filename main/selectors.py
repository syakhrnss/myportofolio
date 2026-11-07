"""
Query read untuk API search, filter, dan sorting.

Dipisah dari view agar view hanya mengurus HTTP (method, status, response)
dan aturan query bisa dibaca serta diuji tersendiri. Fungsi search_*
menerima params (request.query_params) dan mengembalikan queryset.
"""

from django.contrib.auth.models import User
from django.db.models import Count, Prefetch, Q

from main.models import Experience, Project

SORT_BY_STARS = "stars"

# Nama atribut tempat hasil prefetch pemberi star disimpan pada setiap objek.
# Dibaca oleh StarredModelSerializer di main/serializers.py.
STARRED_USERS_ATTR = "_prefetched_starred_users"


def with_starred_users(queryset):
    """Prefetch pemberi star ke atribut STARRED_USERS_ATTR (satu query).

    to_attr menyimpan hasilnya sebagai list biasa, dan only("id",
    "username") membuat kolom lain (email, hash password) tidak pernah
    dimuat. Serializer memakai list ini untuk jumlah star, status star, dan
    daftar nama sekaligus, sehingga tidak ada query tambahan per baris.
    """
    return queryset.prefetch_related(
        Prefetch(
            "starred_by",
            queryset=User.objects.only("id", "username"),
            to_attr=STARRED_USERS_ATTR,
        )
    )


def _with_star_total(queryset):
    """Tambahkan star_total (jumlah star) sebagai kolom hasil query.

    distinct=True dapat menjaga hitungan tetap benar ketika queryset sudah
    di-join ke relasi lain.
    """
    return queryset.annotate(star_total=Count("starred_by", distinct=True))


def search_projects(params):
    # Project, dengan ?title= dan ?sort=stars.
    projects = with_starred_users(Project.objects.all())

    title = params.get("title", "").strip()
    if title:
        projects = projects.filter(title__icontains=title)

    if params.get("sort") == SORT_BY_STARS:
        return _with_star_total(projects).order_by("-star_total", "title", "id")
    return projects.order_by("title", "id")


def search_experiences(params):
    # Experience, dengan ?title= (judul atau peran), ?category=, ?sort=stars
    experiences = with_starred_users(Experience.objects.all())

    title = params.get("title", "").strip()
    if title:
        experiences = experiences.filter(
            Q(title__icontains=title) | Q(role__icontains=title)
        )

    category = params.get("category", "").strip()
    if category in {value for value, _ in Experience.EXPERIENCE_CHOICES}:
        experiences = experiences.filter(category=category)

    if params.get("sort") == SORT_BY_STARS:
        return _with_star_total(experiences).order_by("-star_total", "-started_at", "id")
    return experiences.order_by("-started_at", "id")