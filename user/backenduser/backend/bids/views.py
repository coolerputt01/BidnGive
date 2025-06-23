from rest_framework import viewsets, permissions, status , generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from .models import Bid
from .serializers import BidSerializer , BidPaymentConfirmSerializer
from django.utils import timezone

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enter_auction_room(request):
    user = request.user
    bids = Bid.objects.filter(user=user, status='pending', in_auction_room=False)
    if not bids.exists():
        return Response({"message": "No pending bids to enter."})
    bids.update(in_auction_room=True)
    return Response({"message": f"{bids.count()} bid(s) entered auction room."})

class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Bid.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        bid = self.get_object()
        if 'payment_proof' in request.data:
            bid.payment_proof = request.data['payment_proof']
            bid.status = 'paid'
            bid.save()
        return Response(BidSerializer(bid).data)

class UploadProofView(generics.UpdateAPIView):
    serializer_class = BidPaymentConfirmSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]

    def get_queryset(self):
        return Bid.objects.filter(user=self.request.user, status='merged')

class ConfirmReceiverView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, bid_id):
        try:
            bid = Bid.objects.get(id=bid_id, status='merged')
            if bid.user == request.user:
                return Response({"error": "You can't confirm your own bid as receiver."}, status=403)
            bid.receiver_confirmed = True
            bid.save()
            return Response({"message": "Payment confirmed by receiver."})
        except Bid.DoesNotExist:
            return Response({"error": "Bid not found."}, status=404)
