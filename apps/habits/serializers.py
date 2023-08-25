from rest_framework import serializers

from apps.habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if self.instance:
            if self.instance.related_habit and (data.get('reward') or data.get('related_habit')):
                raise serializers.ValidationError('Низзя выбрать вознаграждение и связанную с ним привычку для одной привычки.')
            elif self.instance.is_pleasant and (data.get('reward') or data.get('related_habit')):
                raise serializers.ValidationError('К приятным привычками низзя добавить награду или полезную привычку.')
            elif data.get('is_pleasant') and (self.instance.reward or self.instance.related_habit):
                raise serializers.ValidationError('К приятным привычками низзя добавить награду или полезную привычку.')
            elif data.get('related_habit'):
                if data.get('related_habit').is_pleasant is False:
                    raise serializers.ValidationError('Сопутствующая привычка должна быть приятной')
            elif data.get('execution_time'):
                if data.get('execution_time') > 120:
                    raise serializers.ValidationError('Время выполнения вашей привычки должно быть не более 120 секунд.')
            elif data.get('period'):
                if data.get('period') > 7:
                    raise serializers.ValidationError('Выполнять привычку нельзя реже, чем 1 раз в 7 дней.')

        return data

    class Meta:
        model = Habit
        fields = '__all__'








