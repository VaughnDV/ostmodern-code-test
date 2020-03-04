from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from shiptrader.models import Starship, Listing
from shiptrader.serializers import (
    StarshipSerializer,
    ListingSerializer,
    ManageListingSerializer,
)
from rest_framework import filters, generics, status


class StarshipView(generics.ListAPIView):
    """
        A View for retrieving all Starships
    """

    queryset = Starship.objects.all()
    serializer_class = StarshipSerializer


class ListingView(generics.ListCreateAPIView):
    """
        CREATE: To list a Starship as for sale, the user should supply the Starship name and list price
        GET: A potential buyer can browse all the listings for a given starship_class
        GET: A potential buyer can order listings by price or time of listing
    """

    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ("price", "created_at")
    search_fields = ("ship_type__starship_class",)


class ManageListingView(generics.UpdateAPIView):
    """

        UPDATE: A seller can deactivate and reactivate their listing
    """

    queryset = Listing.objects.all()

    def patch(self, request, *args, **kwargs):
        listing = get_object_or_404(Listing, pk=kwargs["listing_id"])
        keep = ["active"]
        data = {k: request.data[k] for k in keep if k in request.data}
        serializer = ListingSerializer(listing, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
