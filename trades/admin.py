from django.contrib import admin
from .models import Trade, StrategyTag, MistakeTag


@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'status', 'symbol', 'direction', 'entry_price', 'exit_price', 'opened_at', 'closed_at'
    )
    list_filter = ('status', 'direction', 'opened_at', 'closed_at', 'created_at')
    search_fields = ('symbol', 'user__username', 'notes')
    autocomplete_fields = ('strategy_tags', 'mistake_tags')


@admin.register(StrategyTag)
class StrategyTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'created_at')
    search_fields = ('name', 'user__username')
    list_filter = ('created_at',)


@admin.register(MistakeTag)
class MistakeTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'created_at')
    search_fields = ('name', 'user__username')
    list_filter = ('created_at',)
