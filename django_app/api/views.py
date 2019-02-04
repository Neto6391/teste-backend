from django.core import serializers
from api.models import Answers
from api.serializers import *

from rest_framework import generics
from rest_framework.response import Response


class ApiList(generics.ListCreateAPIView):
    serializer_class = AnswersSerializer

    def get_queryset(self):
        qs = Answers.objects.filter(
            alternative__description='Sim').values(description=models.F('student__regional')).annotate(average=models.Count('student__regional')).order_by('student__regional')
        return qs

    def list(self, request):
        total = Answers.objects.all()
        group_region = Answers.objects.values(description=models.F('student__regional')).annotate(
            average=models.Count('student__regional')).order_by('student__regional')

        queryset = AnswersSerializer.get_average_answers(
            self, {'regionals': self.get_queryset()}, {'regionals': group_region}, {
                'regionals': total}
        )

        return Response(queryset)
