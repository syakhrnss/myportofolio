# Operasi yang mengubah data dan dipakai bersama oleh beberapa view.


def toggle_star(instance, user):
    # Beri star jika user belum memberinya, jika sudah maka unstar.
    # Operasi ini bekerja untuk model apa pun yang punya relasi starred_by ke User.
    # Akun pemberi star selalu berasal dari request.user yang dikirim oleh
    # view, tidak pernah dari input klien. Return True jika setelah
    # pemanggilan user berstatus memberi star.
    
    if instance.starred_by.filter(pk=user.pk).exists():
        instance.starred_by.remove(user)
        return False
    instance.starred_by.add(user)
    return True