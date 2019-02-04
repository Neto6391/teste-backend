from rest_framework import serializers
from api.models import *


class StudentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Students
        fields = ('regional',)


class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = ('id', 'description')


class AlternativesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alternatives
        fields = ('id', 'description')


class AnswersSerializer(serializers.ModelSerializer):
    average_answers = serializers.SerializerMethodField()
    sum_answers = 0

    class Meta:
        model = Answers

    def get_average_answers(self, obj1, obj2, obj3):
        total = len(obj3['regionals'])
        total_national = sum(
            [obj1['regionals'][i]['average']
                for i in range(len(obj1['regionals']))]
        )

        for i in range(len(obj1['regionals'])):
            obj1['regionals'][i]['average'] = round(
                (
                    obj1['regionals'][i]['average'] /
                    obj2['regionals'][i]['average']
                ) * 100, 4
            )

        average_national = round((total_national/total) * 100, 4)
        obj1['national'] = average_national

        return(obj1)
