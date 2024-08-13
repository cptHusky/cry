"""Общие структуры"""
from dataclasses import dataclass


@dataclass
class QuoteData:
    """Общий формат полученной котировки"""
    symbol: str
    price: float
    volume: float
    timestamp: str
