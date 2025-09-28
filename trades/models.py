from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class StrategyTag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='strategy_tags')
    name = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'name')
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class MistakeTag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mistake_tags')
    name = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'name')
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Trade(models.Model):
    STATUS_OPEN = 'open'
    STATUS_CLOSED = 'closed'
    STATUS_CHOICES = [
        (STATUS_OPEN, 'Open'),
        (STATUS_CLOSED, 'Closed'),
    ]

    BUY = 'buy'
    SELL = 'sell'
    DIRECTION_CHOICES = [
        (BUY, 'Buy'),
        (SELL, 'Sell'),
    ]

    EMOTION_NEGATIVE = 'negative'
    EMOTION_NEUTRAL = 'neutral'
    EMOTION_POSITIVE = 'positive'
    EMOTION_CHOICES = [
        (EMOTION_NEGATIVE, 'Negative'),
        (EMOTION_NEUTRAL, 'Neutral'),
        (EMOTION_POSITIVE, 'Positive'),
    ]

    CLOSE_MANUAL = 'manual'
    CLOSE_TAKE_PROFIT = 'tp'
    CLOSE_STOP_LOSS = 'sl'
    CLOSE_BREAKEVEN = 'breakeven'
    CLOSE_TIME = 'time'
    CLOSE_OTHER = 'other'
    CLOSE_REASON_CHOICES = [
        (CLOSE_MANUAL, 'Closed Manually'),
        (CLOSE_TAKE_PROFIT, 'Take Profit'),
        (CLOSE_STOP_LOSS, 'Stop Loss'),
        (CLOSE_BREAKEVEN, 'Breakeven'),
        (CLOSE_TIME, 'Time-based'),
        (CLOSE_OTHER, 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trades')
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default=STATUS_OPEN)
    symbol = models.CharField(max_length=20)
    opened_at = models.DateTimeField(null=True, blank=True)
    direction = models.CharField(max_length=4, choices=DIRECTION_CHOICES, null=True, blank=True)

    size = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    entry_price = models.DecimalField(max_digits=20, decimal_places=8)
    stop_loss = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    target = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    # Kept for migration compatibility; replaced by target/exit_price in UI
    take_profit = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    risk_percent = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    # Closed trade fields
    exit_price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    close_reason = models.CharField(max_length=16, choices=CLOSE_REASON_CHOICES, null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    emotion_before = models.CharField(max_length=8, choices=EMOTION_CHOICES, default=EMOTION_NEUTRAL)
    emotion_after = models.CharField(max_length=8, choices=EMOTION_CHOICES, null=True, blank=True)

    notes = models.TextField(blank=True)
    screenshot = models.FileField(upload_to='screenshots/', null=True, blank=True)

    strategy_tags = models.ManyToManyField(StrategyTag, blank=True, related_name='trades')
    mistake_tags = models.ManyToManyField(MistakeTag, blank=True, related_name='trades')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-opened_at', '-created_at']

    def __str__(self) -> str:
        return f"{self.user.username} {self.symbol} {self.direction} @ {self.entry_price}"


