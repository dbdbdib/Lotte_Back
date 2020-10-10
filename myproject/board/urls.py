from django.urls import path
from board.views import MainPageView, foodcompany

# for Media file전달
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', MainPageView.as_view(), name='mainpage'),
    path('식품', foodcompany, name = 'food'),
    # path('food/', food, name='food'),
    # path('retail/', retail, name='retail'),
    # path('chem/', chem, name='chem'),
    # path('tour/', tour, name='tour'),
    # path('food/post/<int:board_id>', index, name="food_post"),
    # path('retail/post/<int:board_id>', index, name="retail_post"),
    # path('chem/post/<int:board_id>', index, name="chem_post"),
    # path('tour/post/<int:board_id>', index, name="tour_post"),
]