from django.conf import settings
from django.db import models


class Source(models.Model):
    SOURCE_TYPE_CHOICES = [
        ("bible", "Bible"),
        ("historical", "Historical"),
        ("research", "Research"),
        ("technology", "Technology"),
    ]

    title = models.CharField(max_length=255)
    source_type = models.CharField(max_length=30, choices=SOURCE_TYPE_CHOICES, default="bible")
    language = models.CharField(max_length=10, default="sw")
    citation = models.CharField(max_length=255, blank=True)
    url = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True)
    trust_level = models.CharField(max_length=20, default="medium")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class BibleVerse(models.Model):
    book = models.CharField(max_length=100)
    book_en = models.CharField(max_length=100, blank=True)
    chapter = models.PositiveIntegerField()
    verse = models.PositiveIntegerField()
    text = models.TextField()
    keywords = models.JSONField(default=list, blank=True)
    topics = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("book", "chapter", "verse")

    def __str__(self):
        return f"{self.book} {self.chapter}:{self.verse}"


class Claim(models.Model):
    CATEGORY_CHOICES = [
        ("prophecy", "Prophecy"),
        ("doctrine", "Doctrine"),
        ("history", "History"),
        ("technology", "Technology"),
        ("other", "Other"),
    ]
    STATUS_CHOICES = [
        ("fact", "Fact"),
        ("interpretation", "Interpretation"),
        ("speculation", "Speculation"),
        ("unknown", "Unknown"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="claims", null=True, blank=True)
    claim = models.TextField()
    language = models.CharField(max_length=10, default="sw")
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default="other")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="interpretation")
    confidence = models.FloatField(default=0.0)
    related_verses = models.ManyToManyField(BibleVerse, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.claim[:80]


class Evidence(models.Model):
    CLASSIFICATION_CHOICES = [
        ("FACT", "Fact"),
        ("INTERPRETATION", "Interpretation"),
        ("SPECULATION", "Speculation"),
        ("UNKNOWN", "Unknown"),
    ]

    claim = models.ForeignKey(Claim, related_name="evidence_items", on_delete=models.CASCADE)
    classification = models.CharField(max_length=20, choices=CLASSIFICATION_CHOICES, default="UNKNOWN")
    content = models.TextField()
    source = models.ForeignKey(Source, null=True, blank=True, on_delete=models.SET_NULL)
    support_strength = models.FloatField(default=0.0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.claim.claim[:30]} - {self.classification}"


class HistoricalInterpretation(models.Model):
    topic = models.CharField(max_length=255)
    era = models.CharField(max_length=100, blank=True)
    summary = models.TextField()
    classification = models.CharField(max_length=20, default="INTERPRETATION")
    source = models.ForeignKey(Source, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.topic


class TechnologyTopic(models.Model):
    name = models.CharField(max_length=255)
    aliases = models.JSONField(default=list, blank=True)
    summary = models.TextField(blank=True)
    category = models.CharField(max_length=50, default="technology")

    def __str__(self):
        return self.name
