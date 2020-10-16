# from django.urls import path
# from post.views import index, create, detail, update, delete, create_comment, comment_delete
# # for Media file전달
# from django.conf import settings
# from django.conf.urls.static import static
# urlpatterns = [
#     path('post/', index, name="post"),
#     path('create/', create, name="create"),
#     path('detail/<int:post_id>', detail, name="detail"),
#     path('update/<int:post_id>', update, name="update"),
#     path('delete/<int:post_id>', delete, name="delete"),
#     path('create_comment/<int:post_id>', create_comment, name="create_comment"),
#     path('comment_delete/<int:post_id>/<int:com_id>',
#          comment_delete, name="comment_delete"),
# ] 
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)