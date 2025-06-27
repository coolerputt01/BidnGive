from rest_framework import viewsets, permissions, status , generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from .models import Bid
from .serializers import BidSerializer , BidPaymentConfirmSerializer
from django.utils import timezone
from django.core.management import call_command

@api_view(['GET'])
@permission_classes([AllowAny])
def run_auto_merge(request):
    if request.GET.get('key') != 'biddedkey':
        return Response({'error': 'Unauthorized'}, status=403)
    
    call_command('auto_merge')
    return Response({'status': 'Auto merge ran successfully'})

@api_view(['GET'])
@permission_classes([AllowAny])
def auto_block(request):
    if request.GET.get('key') != 'expiredkey':
        return Response({'error': 'Unauthorized'}, status=403)

    call_command('auto_block_expired')
    return Response({'status': 'Auto Block sent'})

class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Bid.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        has_pending = Bid.objects.filter(user=user).exclude(status='paid').exists()

        if has_pending:
            raise ValidationError("You already have a pending bid.")
        serializer.save(user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        bid = self.get_object()
        if 'payment_proof' in request.data:
            bid.payment_proof = request.data['payment_proof']
            bid.status = 'paid'
            bid.save()
        return Response(BidSerializer(bid).data)

        def destroy(self, request, *args, **kwargs):
            bid = self.get_object()
            if bid.status != 'pending':
                return Response({'error': 'Only pending bids can be cancelled.'}, status=status.HTTP_400_BAD_REQUEST)
            bid.delete()
            return Response({'message': 'Bid cancelled.'}, status=status.HTTP_204_NO_CONTENT)

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
