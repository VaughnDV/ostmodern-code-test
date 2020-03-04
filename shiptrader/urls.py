from django.conf.urls import url
from shiptrader import views

urlpatterns = [
    url(r"^starships/$", views.StarshipView.as_view(), name="starships"),
    url(r"^listings/$", views.ListingView.as_view(), name="listings"),
    url(
        r"^listings/(?P<listing_id>\d+)$",
        views.ManageListingView.as_view(),
        name="manage-listing",
    ),
]
