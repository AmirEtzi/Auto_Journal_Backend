from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Trade, StrategyTag, MistakeTag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name']
        read_only_fields = ['id']


class StrategyTagSerializer(TagSerializer):
    class Meta(TagSerializer.Meta):
        model = StrategyTag


class MistakeTagSerializer(TagSerializer):
    class Meta(TagSerializer.Meta):
        model = MistakeTag


class TradeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    strategy_tags = StrategyTagSerializer(many=True, required=False)
    mistake_tags = MistakeTagSerializer(many=True, required=False)

    class Meta:
        model = Trade
        fields = [
            'id', 'user', 'status', 'symbol', 'opened_at', 'direction', 'size', 'entry_price',
            'stop_loss', 'target', 'risk_percent', 'exit_price', 'close_reason', 'closed_at',
            'emotion_before', 'emotion_after', 'strategy_tags', 'mistake_tags', 'screenshot',
            'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def _upsert_tags(self, tag_model, user, items):
        instances = []
        for item in items:
            name = (item.get('name') or '').strip()
            if not name:
                continue
            instance, _ = tag_model.objects.get_or_create(user=user, name=name)
            instances.append(instance)
        return instances

    def create(self, validated_data):
        strategy_data = validated_data.pop('strategy_tags', [])
        mistake_data = validated_data.pop('mistake_tags', [])
        user = self.context['request'].user
        trade = Trade.objects.create(user=user, **validated_data)
        if strategy_data:
            trade.strategy_tags.set(self._upsert_tags(StrategyTag, user, strategy_data))
        if mistake_data:
            trade.mistake_tags.set(self._upsert_tags(MistakeTag, user, mistake_data))
        return trade

    def update(self, instance, validated_data):
        strategy_data = validated_data.pop('strategy_tags', None)
        mistake_data = validated_data.pop('mistake_tags', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        user = self.context['request'].user
        if strategy_data is not None:
            instance.strategy_tags.set(self._upsert_tags(StrategyTag, user, strategy_data))
        if mistake_data is not None:
            instance.mistake_tags.set(self._upsert_tags(MistakeTag, user, mistake_data))
        return instance

