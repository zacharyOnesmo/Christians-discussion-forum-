from django.core.management.base import BaseCommand

from dashboard.models import BibleVerse, Source


class Command(BaseCommand):
    help = "Seed the NENO LENS sample data with Bible and evidence references."

    def handle(self, *args, **options):
        if BibleVerse.objects.exists():
            self.stdout.write(self.style.SUCCESS("Sample data already exists. Skipping seed."))
            return

        Source.objects.create(
            title="Ufunuo 13:16-18 (mfano)",
            source_type="bible",
            language="sw",
            citation="Ufunuo 13:16-18",
            trust_level="high",
            notes="Mfano wa data ya Biblia kwa majaribio ya mfumo.",
        )

        Source.objects.create(
            title="Historia ya tafsiri ya 666",
            source_type="historical",
            language="sw",
            citation="Historia ya ufasiri",
            trust_level="medium",
            notes="Mifano ya tafsiri ya kihistoria, si uthibitisho wa kweli ya Biblia.",
        )

        Source.objects.create(
            title="Mfano wa teknolojia ya BCI",
            source_type="technology",
            language="sw",
            citation="Mfano wa teknolojia",
            trust_level="medium",
            notes="Kwa madhumuni ya maendeleo ya mfumo wa utafiti wa teknolojia.",
        )

        BibleVerse.objects.create(
            book="Ufunuo",
            book_en="Revelation",
            chapter=13,
            verse=16,
            text="Na alifanya watu wote, wadogo na wakubwa, matajiri na maskini, huru na watumwa, wapatie alama katika mkono wa kushoto au kwenye paji la uso wao.",
            keywords=["alama", "mnyama", "mkono", "uso"],
            topics=["alama", "mnyama", "ukoloni", "ubaguzi"],
        )

        BibleVerse.objects.create(
            book="Ufunuo",
            book_en="Revelation",
            chapter=13,
            verse=18,
            text="Hapa kuna hekima. Aweza kujua nambari ya mnyama, maana ni nambari ya mtu; na nambari yake ni mia sita na sitini na sita.",
            keywords=["666", "mnyama", "nambari", "alama"],
            topics=["666", "mnyama", "nambari", "alama"],
        )

        self.stdout.write(self.style.SUCCESS("Seed data created successfully."))
