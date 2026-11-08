"""Serializer DRF untuk bagian portofolio (Project dan Experience).

Tanggung jawab file ini hanya dua yaitu mengubah objek model menjadi data yang
dikirim ke klien, dan memvalidasi serta membersihkan input dari klien.
Hak akses ada di main/permissions.py, query ada di main/selectors.py.
"""

from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Experience, Project
from main.selectors import STARRED_USERS_ATTR

# Field hasil perhitungan dari relasi starred_by. Semuanya read-only.
STAR_FIELDS = ["star_count", "is_starred", "starred_by_names"]


def clean_text(value, empty_message=None):
    """Buang tag HTML dan spasi di tepi, setara clean_<field> pada Tugas 5.

    Jika empty_message diberikan dan hasilnya kosong (misalnya input hanya
    berisi tag HTML), input ditolak dengan pesan tersebut. strip_tags
    bukan sanitizer HTML penuh, jadi template tetap wajib melakukan escaping.
    """
    cleaned = strip_tags(value).strip()
    if empty_message and not cleaned:
        raise serializers.ValidationError(empty_message)
    return cleaned


class StarredModelSerializer(serializers.ModelSerializer):
    """Base serializer untuk model yang memiliki relasi starred_by ke User.

    class ini menyediakan tiga field hasil perhitungan yang tidak dapat ditulis klien.
    Ketiganya membaca daftar pemberi star dari _get_starred_users, yang
    mencari datanya dengan urutan berikut:

    1. Hasil Prefetch(to_attr=STARRED_USERS_ATTR) dari
       selectors.with_starred_users: satu query untuk seluruh daftar.
    2. Jika tidak ada (serializer dipakai tanpa prefetch), satu query per
       objek yang disimpan di cache serializer, jadi tiga field di atas tetap
       hanya memakai satu query per objek.

    Kedua jalur hanya memuat kolom id dan username; email dan hash
    password tidak pernah dibaca. Subclass wajib menyertakan STAR_FIELDS
    di Meta.fields.
    """

    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    def _get_starred_users(self, obj):
        prefetched = getattr(obj, STARRED_USERS_ATTR, None)
        if prefetched is not None:
            return prefetched

        cache = self.__dict__.setdefault("_starred_users_cache", {})
        if obj.pk not in cache:
            cache[obj.pk] = list(obj.starred_by.only("id", "username"))
        return cache[obj.pk]

    def get_star_count(self, obj):
        return len(self._get_starred_users(obj))

    def get_is_starred(self, obj):
        # True jika pengguna yang sedang melihat sudah memberi star.
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return any(user.pk == request.user.pk for user in self._get_starred_users(obj))

    def get_starred_by_names(self, obj):
        # Hanya username yang tampil; email dan data akun lain tidak pernah.
        return ", ".join(user.username for user in self._get_starred_users(obj))


class ProjectSerializer(StarredModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "subtitle", "image", "description", *STAR_FIELDS]
        read_only_fields = ["id"]

    def validate_title(self, value):
        return clean_text(value, "Title cannot be empty.")

    def validate_subtitle(self, value):
        return clean_text(value)

    def validate_description(self, value):
        return clean_text(value)


class ExperienceSerializer(StarredModelSerializer):
    """Representasi dan validasi Experience untuk /api/v1/experience/.

    category_display dan is_ongoing dihitung dari model dan bersifat
    read-only. Judul, deskripsi, dan peran dibersihkan dari tag HTML dan tidak
    boleh kosong setelahnya.
    """

    category_display = serializers.CharField(
        source="get_category_display", read_only=True,
    )
    is_ongoing = serializers.BooleanField(read_only=True)

    class Meta:
        model = Experience
        fields = [
            "id", "title", "description", "category", "category_display",
            "thumbnail", "started_at", "ended_at", "role",
            "is_featured", "display_order", "is_ongoing", *STAR_FIELDS,
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        return clean_text(value, "Nama pengalaman tidak boleh hanya berisi tag HTML.")

    def validate_description(self, value):
        return clean_text(value, "Deskripsi tidak boleh hanya berisi tag HTML.")

    def validate_role(self, value):
        return clean_text(value, "Peran tidak boleh hanya berisi tag HTML.")

    def validate(self, attrs):
        """Tanggal selesai tidak boleh lebih awal dari tanggal mulai.

        Pada PATCH, salah satu tanggal bisa tidak dikirim, jadi nilai yang
        tidak ada diambil dari instance yang sedang diubah.
        """
        started_at = attrs.get("started_at", getattr(self.instance, "started_at", None))
        ended_at = attrs.get("ended_at", getattr(self.instance, "ended_at", None))

        if started_at and ended_at and ended_at < started_at:
            raise serializers.ValidationError({
                "ended_at": "Tanggal selesai tidak boleh lebih awal dari tanggal mulai.",
            })
        return attrs