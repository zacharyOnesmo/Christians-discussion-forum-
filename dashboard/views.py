from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ClaimInputForm, LoginForm, RegisterForm
from .models import BibleVerse, Claim, Evidence, Source, HistoricalInterpretation, TechnologyTopic


UI_TEXT = {
    "sw": {
        "site_title": "NenoLens | Dashibodi ya Uchunguzi",
        "nav_dashboard": "Dashibodi",
        "nav_claims": "Dai",
        "nav_evidence": "Ushahidi",
        "nav_reports": "Ripoti",
        "sidebar_intro": "Uchunguzi wa ushahidi",
        "sidebar_desc": "Hii ni mfumo wa kukagua dai, maandiko, historia na teknolojia kwa uangalifu.",
        "eyebrow": "NenoLens AI / Research",
        "page_title": "Dashibodi ya uchunguzi",
        "status": "FACT • INTERPRETATION • SPECULATION • UNKNOWN",
        "stat_bible": "Maandiko",
        "stat_history": "Historia",
        "stat_tech": "Teknolojia",
        "stat_sources": "Vyanzo",
        "stat_evidence": "Ushahidi",
        "hero_badge": "Evidence-first",
        "hero_title": "Chunguza madai kwa uwazi, muktadha, na uelewa wa vyanzo.",
        "hero_desc": "Tenganisha maandiko ya Biblia, tafsiri ya kihistoria, madai ya teknolojia, na uvumi usio na msingi kabla ya kutoa hitimisho.",
        "feature_scripture": "Maandiko",
        "feature_context": "Historia",
        "feature_tech": "Teknolojia",
        "feature_evidence": "Ushahidi",
        "feature_scripture_title": "Maandishi na muktadha",
        "feature_history_title": "Tafsiri",
        "feature_tech_title": "Uhakiki wa teknolojia",
        "feature_evidence_title": "Uwazi na hitimisho",
        "cta_label": "NenoLens",
        "cta_title": "Fanyia utafiti madai ya Kikristo kwa ushahidi, si uvumi.",
        "cta_desc": "Tunalinganisha maandiko, tafsiri ya kihistoria, ukweli wa teknolojia, na hoja wazi ili watumiaji waweze kutathmini madai kwa uwajibikaji.",
        "cta_primary": "Chunguza dai",
        "cta_secondary": "Angalia ushahidi",
        "process_title_1": "Wasilisha dai",
        "process_desc_1": "Watumiaji wanaweka taarifa au dai kwa lugha ya kawaida.",
        "process_title_2": "Tenga tabaka",
        "process_desc_2": "Tunalinganisha maandiko, tafsiri, muktadha, na madai ya teknolojia ya kisasa.",
        "process_title_3": "Toa hitimisho",
        "process_desc_3": "Kila ripoti inaonyesha kinachokuwa cha kweli, cha tafsiri, cha uvumi, au kisichothibitishwa.",
        "why_title": "Kwa nini NenoLens",
        "why_subtitle": "Imejengwa kwa ajili ya uchunguzi wa ushahidi na uwazi.",
        "trust_bible": "Uwazi wa Biblia",
        "trust_bible_desc": "Maandishi yanatenganishwa na tafsiri ili watumiaji waweze kutathmini madai kwa uaminifu zaidi.",
        "trust_history": "Uelewa wa kihistoria",
        "trust_history_desc": "Muktadha husaidia kuelewa maana ya kifungu katika mazingira ya kihistoria.",
        "trust_tech": "Ufahamu wa teknolojia",
        "trust_tech_desc": "Dai za kisasa zinatathminiwa kwa kutenganisha ukweli kutoka kwa uvumi.",
        "trust_verdict": "Hitimisho la uwazi",
        "trust_verdict_desc": "Kila ripoti inasisitiza kama ushahidi unaunga mkono dai au la.",
        "research_layers_label": "Tabaka za utafiti",
        "research_layers_title": "Dai moja, tabaka nyingi za ushahidi.",
        "research_layers_desc": "Tunatenganisha maneno halisi ya Biblia kutoka tafsiri ya kihistoria, madai ya teknolojia, na uvumi usio na msingi.",
        "research_layer_1": "Maandiko ya Biblia",
        "research_layer_2": "Muktadha wa kihistoria",
        "research_layer_3": "Ukweli wa teknolojia",
        "research_layer_4": "Hitimisho",
        "methodology_label": "Jinsi NenoLens inavyofanya kazi",
        "methodology_title": "Uchunguzi wa uwazi na mipaka ya ushahidi.",
        "methodology_1": "Text",
        "methodology_1_desc": "Tunaanza kwa maneno yenyewe na kile kifungu kinachosema kwa kweli.",
        "methodology_2": "Context",
        "methodology_2_desc": "Muktadha wa kihistoria, kitamaduni, na kifasihi husaidia kueleza maana ya taarifa.",
        "methodology_3": "Evidence",
        "methodology_3_desc": "Dai za kisasa na ukweli wa sasa zinatathminiwa kando na tafsiri na imani.",
        "methodology_4": "Verdict",
        "methodology_4_desc": "Ripoti ya mwisho hutofautisha ukweli, tafsiri, uvumi, na kinachobaki kisichowekwa wazi.",
        "assistant_title": "Muulizaji",
        "assistant_prompt": "Uliza swali lako",
        "online": "Online",
        "assistant_greeting_1": "Habari! Nimewekwa kukusadia kuchunguza dai la Kikiristo, maandiko, na teknolojia kwa usawaziko wa ushahidi.",
        "assistant_greeting_2": "Uliza swali kama: “666 ni chip ya ubongo?” au “AI ni mnyama wa Ufunuo?”",
        "analyze": "Chunguza",
        "clear": "Futa",
        "quick_title": "Maswali ya haraka",
        "rules_title": "Kanuni ya mfumo",
        "rules": [
            "Tofauti kati ya maandiko ya Biblia na tafsiri.",
            "Tambua historia, teknolojia na ushahidi wa utafiti.",
            "Usisitize uvumi kama ukweli wa Biblia.",
            "Ushahidi ukikosekana, sema wazi: “Ushahidi hautoshi kuthibitisha dai hili.”",
        ],
        "strategy_title": "Mikakati",
        "report_title": "Ripoti ya uchunguzi",
        "brief_answer": "Jibu la ufupi",
        "classification": "Uainishaji",
        "confidence": "Uhakika",
        "claim_dna": "Claim DNA",
        "claim_subject": "Hasa",
        "biblical_concepts": "Dhahania za Biblia",
        "tech_concepts": "Dhahania za teknolojia",
        "relationship": "Uhusiano",
        "claim_type": "Aina ya dai",
        "related_scripture": "Maandiko yanayohusiana",
        "evidence_label": "Ushahidi",
        "recent_title": "Hivi karibuni",
        "claim_label": "Dai au madai",
        "placeholder": "Mfano: 666 ni chip ya ubongo",
        "language_switch": "Lugha",
        "english": "ENG",
        "swahili": "SW",
        "submit_success": "Uchambuzi umechangwa kwa kanuni ya ushahidi.",
        "welcome": "Karibu,",
        "logged_in_text": "Umeingia kwenye akaunti yako na unaweza kutuma madai.",
        "login": "Ingia",
        "logout": "Ondoka",
        "register": "Jisajili",
        "login_title": "Ingia kwenye akaunti yako",
        "login_subtitle": "Endelea kuchunguza madai kwa ushahidi, muktadha, na uwazi.",
        "login_cta": "Ingia",
        "login_prompt": "Huna akaunti?",
        "login_link": "Unda akaunti",
        "register_title": "Unda akaunti yako",
        "register_subtitle": "Anza dashibodi yako ya uchunguzi ya ushahidi binafsi.",
        "register_cta": "Unda akaunti",
        "register_prompt": "Tayari una akaunti?",
        "register_link": "Ingia",
        "username_label": "Jina la mtumiaji",
        "email_label": "Barua pepe",
        "password_label": "Nywila",
        "password_repeat_label": "Rudia nywila",
        "profile_title": "Profaili yangu",
        "profile_subtitle": "Maboresho ya akaunti yako na historia ya uchunguzi.",
        "profile_greeting": "Habari,",
        "profile_stats": "Takwimu za akaunti",
        "profile_total_claims": "Jumla ya dai",
        "profile_recent_activity": "Shughuli ya hivi karibuni",
        "profile_empty": "Huna dai lililorekodiwa bado. Anza kuchunguza kwa kutuma dai lako la kwanza.",
        "profile_dashboard_link": "Nenda kwenye dashibodi",
        "profile_analyze_link": "Chunguza dai",
        "claim_detail_title": "Maelezo ya dai",
        "claim_detail_status": "Hali",
        "claim_detail_confidence": "Uhakika",
        "claim_detail_category": "Kategoria",
        "claim_detail_related": "Maandiko yanayohusiana",
        "claim_detail_evidence": "Ushahidi",
        "claim_detail_back": "Rudi kwenye profaili",
    },
    "en": {
        "site_title": "NenoLens | Investigation Dashboard",
        "nav_dashboard": "Dashboard",
        "nav_claims": "Claims",
        "nav_evidence": "Evidence",
        "nav_reports": "Reports",
        "sidebar_intro": "Evidence investigation",
        "sidebar_desc": "This system evaluates claims using biblical text, historical context, and technology evidence with care and transparency.",
        "eyebrow": "NenoLens AI / Research",
        "page_title": "Investigation dashboard",
        "status": "FACT • INTERPRETATION • SPECULATION • UNKNOWN",
        "stat_bible": "Scripture",
        "stat_history": "History",
        "stat_tech": "Technology",
        "stat_sources": "Sources",
        "stat_evidence": "Evidence",
        "hero_badge": "Evidence-first",
        "hero_title": "Investigate claims with transparency, context, and source awareness.",
        "hero_desc": "Separate biblical text, historical interpretation, technology claims, and unsupported speculation before drawing a conclusion.",
        "feature_scripture": "Scripture",
        "feature_context": "History",
        "feature_tech": "Technology",
        "feature_evidence": "Evidence",
        "feature_scripture_title": "Text & context",
        "feature_history_title": "Interpretation",
        "feature_tech_title": "Modern fact-check",
        "feature_evidence_title": "Clarity & verdict",
        "cta_label": "NenoLens",
        "cta_title": "Research Christian claims with evidence, not guesswork.",
        "cta_desc": "We compare biblical text, historical interpretation, technology facts, and clear reasoning so users can evaluate claims responsibly.",
        "cta_primary": "Analyze a claim",
        "cta_secondary": "Explore evidence",
        "process_title_1": "Submit the claim",
        "process_desc_1": "Users enter a statement or claim for review in plain language.",
        "process_title_2": "Separate the layers",
        "process_desc_2": "We compare scripture, interpretation, context, and modern technology claims.",
        "process_title_3": "Deliver a verdict",
        "process_desc_3": "Each result shows what is factual, interpretive, speculative, or unproven.",
        "why_title": "Why NenoLens",
        "why_subtitle": "Built for careful, evidence-first exploration.",
        "trust_bible": "Biblical clarity",
        "trust_bible_desc": "Text stays distinct from interpretation, so users can evaluate claims more honestly.",
        "trust_history": "Historical depth",
        "trust_history_desc": "Context helps users understand what a passage meant in its historical setting.",
        "trust_tech": "Technology awareness",
        "trust_tech_desc": "Modern claims are assessed with careful distinction between facts and speculation.",
        "trust_verdict": "Transparent conclusion",
        "trust_verdict_desc": "Every report emphasizes whether evidence supports the claim or not.",
        "research_layers_label": "Research layers",
        "research_layers_title": "One claim, multiple evidence layers.",
        "research_layers_desc": "We separate the actual biblical wording from historical interpretation, technology claims, and unsupported speculation.",
        "research_layer_1": "Biblical text",
        "research_layer_2": "Historical context",
        "research_layer_3": "Technology facts",
        "research_layer_4": "Verdict",
        "methodology_label": "How NenoLens works",
        "methodology_title": "Transparent investigation with clear evidence boundaries.",
        "methodology_1": "Text",
        "methodology_1_desc": "We begin with the wording itself and what the passage actually says.",
        "methodology_2": "Context",
        "methodology_2_desc": "Historical, cultural, and literary context helps explain the meaning behind the statement.",
        "methodology_3": "Evidence",
        "methodology_3_desc": "Modern claims and facts are checked separately from interpretation and belief-driven conclusions.",
        "methodology_4": "Verdict",
        "methodology_4_desc": "The final report distinguishes fact, interpretation, speculation, and what remains uncertain.",
        "assistant_title": "Researcher",
        "assistant_prompt": "Ask your question",
        "online": "Online",
        "assistant_greeting_1": "Hello! I am here to help investigate claims by separating scripture, history, and technology with evidence-driven analysis.",
        "assistant_greeting_2": "Ask a question like: “666 is a brain chip?” or “Is AI the beast of Revelation?”",
        "analyze": "Analyze",
        "clear": "Clear",
        "quick_title": "Quick questions",
        "rules_title": "System principles",
        "rules": [
            "Separate biblical text from interpretation.",
            "Identify historical and technological context.",
            "Do not treat speculation as biblical fact.",
            "If evidence is insufficient, state it clearly: “The evidence is insufficient to support this claim.”",
        ],
        "strategy_title": "Strategies",
        "report_title": "Investigation report",
        "brief_answer": "Short answer",
        "classification": "Classification",
        "confidence": "Confidence",
        "claim_dna": "Claim DNA",
        "claim_subject": "Subject",
        "biblical_concepts": "Biblical concepts",
        "tech_concepts": "Technology concepts",
        "relationship": "Relationship",
        "claim_type": "Claim type",
        "related_scripture": "Related passages",
        "evidence_label": "Evidence",
        "recent_title": "Recent claims",
        "claim_label": "Claim or statement",
        "placeholder": "Example: 666 is a brain chip",
        "language_switch": "Language",
        "english": "ENG",
        "swahili": "SW",
        "submit_success": "The analysis was generated using evidence-based principles.",
        "welcome": "Welcome,",
        "logged_in_text": "You are logged in and can submit claims.",
        "login": "Login",
        "logout": "Logout",
        "register": "Register",
        "login_title": "Login to your account",
        "login_subtitle": "Continue investigating claims with evidence, context, and clarity.",
        "login_cta": "Login",
        "login_prompt": "New here?",
        "login_link": "Create account",
        "register_title": "Create your account",
        "register_subtitle": "Start your personal evidence-based investigation dashboard.",
        "register_cta": "Create account",
        "register_prompt": "Already have an account?",
        "register_link": "Login",
        "username_label": "Username",
        "email_label": "Email",
        "password_label": "Password",
        "password_repeat_label": "Repeat password",
        "profile_title": "My profile",
        "profile_subtitle": "Your account overview and investigation history.",
        "profile_greeting": "Hello,",
        "profile_stats": "Account stats",
        "profile_total_claims": "Total claims",
        "profile_recent_activity": "Recent activity",
        "profile_empty": "You have no saved investigations yet. Start by submitting your first claim.",
        "profile_dashboard_link": "Go to dashboard",
        "profile_analyze_link": "Analyze a claim",
        "claim_detail_title": "Claim details",
        "claim_detail_status": "Status",
        "claim_detail_confidence": "Confidence",
        "claim_detail_category": "Category",
        "claim_detail_related": "Related scripture",
        "claim_detail_evidence": "Evidence",
        "claim_detail_back": "Back to profile",
    },
}


def get_user_language(request):
    selected = request.GET.get("lang") or request.POST.get("lang") or request.session.get("lang", "sw")
    if selected not in UI_TEXT:
        selected = "sw"
    request.session["lang"] = selected
    return selected


def ensure_demo_data():
    if BibleVerse.objects.exists():
        return

    source = Source.objects.create(
        title="Ufunuo 13:16-18 (mfano)",
        source_type="bible",
        language="sw",
        citation="Ufunuo 13:16-18",
        trust_level="high",
        notes="Mfano wa data ya Biblia kwa majaribio ya mfumo.",
    )

    BibleVerse.objects.create(
        book="Ufunuo",
        book_en="Revelation",
        chapter=13,
        verse=16,
        text="Na alifanya watu wote, wadogo na wakubwa, matajiri na maskini, huru na watumwa, wapatie alama katika mkono wa kushoto au kwenye paji la uso wao.",
        keywords=["alama", "mnyama", "mkono", "uso"],
        topics=["alama", "mnyama", "ukoloni", "ubaguzi"]
    )
    BibleVerse.objects.create(
        book="Ufunuo",
        book_en="Revelation",
        chapter=13,
        verse=18,
        text="Hapa kuna hekima. Aweza kujua nambari ya mnyama, maana ni nambari ya mtu; na nambari yake ni mia sita na sitini na sita.",
        keywords=["666", "mnyama", "nambari", "alama"],
        topics=["666", "mnyama", "nambari", "alama"]
    )

    source_tech = Source.objects.create(
        title="Mfano wa teknolojia ya BCI",
        source_type="technology",
        language="sw",
        citation="Mfano wa teknolojia",
        trust_level="medium",
        notes="Kwa madhumuni ya majaribio ya kutumia istilahi za teknolojia.",
    )

    Source.objects.create(
        title="Historia ya tafsiri ya 666",
        source_type="historical",
        language="sw",
        citation="Historia ya ufasiri",
        trust_level="medium",
        notes="Hilo ni mfano wa tafsiri ya kihistoria, si uthibitisho wa kweli ya Biblia.",
    )

    demo_claim = Claim.objects.create(
        claim="666 ni chip ya ubongo",
        language="sw",
        category="prophecy",
        status="interpretation",
        confidence=0.18,
    )
    demo_claim.related_verses.set(BibleVerse.objects.filter(book="Ufunuo"))
    Evidence.objects.create(
        claim=demo_claim,
        classification="FACT",
        content="Ufunuo 13:16-18 inataja alama na nambari ya mnyama, na 666 ni nambari inayorejelewa katika maandiko.",
        source=source,
        support_strength=0.75,
        notes="Hii ni taarifa ya maandiko; haihusiani moja kwa moja na chip ya ubongo."
    )
    Evidence.objects.create(
        claim=demo_claim,
        classification="INTERPRETATION",
        content="Wengine wanatafsiri 666 kama mfano wa utambuzi wa kidijitali au mfumo wa teknolojia ya kisasa.",
        source=source_tech,
        support_strength=0.42,
        notes="Hii ni tafsiri, si ukweli uliothibitishwa moja kwa moja kwenye maandiko."
    )
    Evidence.objects.create(
        claim=demo_claim,
        classification="SPECULATION",
        content="Hili ni dai la kutabiri kwamba 666 ni chip ya ubongo kwa uhakika na bila ushahidi wa kutosha.",
        source=source_tech,
        support_strength=0.12,
        notes="Ushahidi hauwezi kuthibitisha madai hayo bila uhusiano wa kitaalamu unaoeleweka."
    )


def classify_claim(text):
    lower_text = text.lower()
    biblical_concepts = []
    technology_concepts = []

    if "666" in lower_text or "mia sita na sitini na sita" in lower_text:
        biblical_concepts.append("666")
    if "mnyama" in lower_text:
        biblical_concepts.append("mnyama")
    if "alama" in lower_text:
        biblical_concepts.append("alama")

    tech_keywords = ["chip", "ubongo", "brain", "bci", "computer", "digital", "interface", "chip ya ubongo"]
    for word in tech_keywords:
        if word in lower_text:
            technology_concepts.append(word)

    if not technology_concepts and any(item in lower_text for item in ["ai", "robotiki", "digital id", "id ya kidijitali"]):
        technology_concepts.append("teknolojia")

    relationship = "" 
    if biblical_concepts and technology_concepts:
        relationship = "666 = brain chip / teknolojia ya ubongo"
    elif biblical_concepts:
        relationship = "dhana ya Biblia inatambulishwa bila uhusiano wa moja kwa moja na teknolojia"
    else:
        relationship = "dai halijafafanuliwa vizuri"

    claim_type = "interpretive_claim" if biblical_concepts and technology_concepts else "biblical_or_technical_claim"
    status = "interpretation"
    confidence = 0.18 if technology_concepts else 0.12

    return {
        "claim": text,
        "biblical_concepts": biblical_concepts,
        "technology_concepts": technology_concepts,
        "relationship": relationship,
        "claim_type": claim_type,
        "status": status,
        "confidence": confidence,
    }


def brief_answer_for_claim(claim_text, analysis):
    if analysis["technology_concepts"] and analysis["biblical_concepts"]:
        return (
            "Dai hili lina kigezo cha Biblia na teknolojia, lakini uhusiano wake ni tafsiri, si uthibitisho wa moja kwa moja. "
            "Ushahidi wa maandiko unaonyesha alama na 666, lakini hauelezi chip ya ubongo."
        )
    if analysis["biblical_concepts"]:
        return (
            "Dai hili linaelekezwa kwenye msingi wa Biblia, lakini taarifa za moja kwa moja zimebaki wazi na zinahitaji tafsiri zaidi. "
            "Ushahidi wa maandiko ni wa kijamii na wa kihistoria, si uthibitisho wa kisayansi."
        )
    return (
        "Dai hili halijajengwa vizuri kwa msingi wa ushahidi. Tafadhali toa taarifa zaidi au uweke rejeleo la maandiko/lugha inayohusiana."
    )


def login_view(request):
    lang = get_user_language(request)
    ui = UI_TEXT[lang]
    form = LoginForm(request.POST or None, lang=lang)

    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Karibu, {user.username}!")
            return redirect("dashboard")
        messages.error(request, "Jina la mtumiaji au nywila si sahihi.")

    return render(request, "dashboard/login.html", {"form": form, "lang": lang, "ui": ui})


def register_view(request):
    lang = get_user_language(request)
    ui = UI_TEXT[lang]
    form = RegisterForm(request.POST or None, lang=lang)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f"Akaunti imeundwa kwa mafanikio. Karibu, {user.username}!")
        return redirect("dashboard")

    return render(request, "dashboard/register.html", {"form": form, "lang": lang, "ui": ui})


def logout_view(request):
    logout(request)
    messages.info(request, "Umeondoka kwenye akaunti yako.")
    return redirect("login")


@login_required(login_url="login")
def profile_view(request):
    lang = get_user_language(request)
    ui = UI_TEXT[lang]
    user_claims = Claim.objects.filter(user=request.user).order_by("-created_at")

    context = {
        "lang": lang,
        "ui": ui,
        "user": request.user,
        "claim_count": user_claims.count(),
        "claims": user_claims[:8],
    }
    return render(request, "dashboard/profile.html", context)


@login_required(login_url="login")
def claim_detail_view(request, claim_id):
    lang = get_user_language(request)
    ui = UI_TEXT[lang]
    claim = Claim.objects.filter(user=request.user).get(pk=claim_id)

    context = {
        "lang": lang,
        "ui": ui,
        "user": request.user,
        "claim_obj": claim,
        "related_verses": claim.related_verses.all(),
        "evidence_items": claim.evidence_items.all(),
    }
    return render(request, "dashboard/claim_detail.html", context)


@login_required(login_url="login")
def dashboard_view(request):
    ensure_demo_data()
    lang = get_user_language(request)
    ui = UI_TEXT[lang]

    form = ClaimInputForm(request.POST or None)
    form.fields["claim"].label = ui["claim_label"]
    form.fields["claim"].widget.attrs["placeholder"] = ui["placeholder"]

    claim_report = None
    recent_claims = Claim.objects.filter(user=request.user).order_by("-created_at")[:5]
    if not recent_claims.exists():
        recent_claims = Claim.objects.filter(user__isnull=True).order_by("-created_at")[:5]
    bible_count = BibleVerse.objects.count()
    history_count = HistoricalInterpretation.objects.count()
    tech_count = TechnologyTopic.objects.count()
    source_count = Source.objects.count()
    evidence_count = Evidence.objects.count()

    sample_questions = [
        "666 ni chip ya ubongo?" if lang == "sw" else "666 is a brain chip?",
        "AI ni mnyama wa Ufunuo?" if lang == "sw" else "Is AI the beast of Revelation?",
        "Digital ID ni alama ya mnyama?" if lang == "sw" else "Is digital ID the mark of the beast?",
        "Yesu ni Mungu?" if lang == "sw" else "Is Jesus God?",
        "Biblia inasema AI itatawala dunia?" if lang == "sw" else "Does the Bible say AI will rule the world?",
    ]

    if request.method == "POST" and form.is_valid():
        claim_text = form.cleaned_data["claim"]
        analysis = classify_claim(claim_text)
        claim = Claim.objects.create(
            user=request.user,
            claim=claim_text,
            language=lang,
            category="prophecy",
            status=analysis["status"],
            confidence=analysis["confidence"],
        )

        related = BibleVerse.objects.filter(book="Ufunuo")[:2]
        claim.related_verses.set(related)

        Evidence.objects.create(
            claim=claim,
            classification="FACT",
            content="Ufunuo 13:16-18 inataja alama na nambari ya mnyama, lakini haielezi chip ya ubongo." if lang == "sw" else "Revelation 13:16-18 mentions a mark and the number of the beast, but it does not explicitly describe a brain chip.",
            source=Source.objects.filter(source_type="bible").first(),
            support_strength=0.72,
            notes="Hili ni maandiko ya msingi." if lang == "sw" else "This is the main biblical reference."
        )

        Evidence.objects.create(
            claim=claim,
            classification="INTERPRETATION",
            content="Wakati mwingine watu hutafsiri alama ya mnyama kwa njia ya teknolojia ya kisasa, lakini hiyo ni tafsiri ya binadamu, si maelezo ya moja kwa moja ya Biblia." if lang == "sw" else "Some people interpret the mark of the beast through modern technology, but this is human interpretation rather than a direct biblical statement.",
            source=Source.objects.filter(source_type="historical").first(),
            support_strength=0.38,
            notes="Interpretation inafaa kuonyesha kama dhana ya kiufasaha, si ukweli uliowekwa wazi." if lang == "sw" else "This shows interpretation rather than direct certainty."
        )

        Evidence.objects.create(
            claim=claim,
            classification="SPECULATION",
            content="Dai kwamba 666 ni chip ya ubongo bila evidence thabiti ni uvumi au tafsiri isiyothibitishwa." if lang == "sw" else "Claiming that 666 is definitely a brain chip without sufficient evidence is speculation or unsupported interpretation.",
            source=Source.objects.filter(source_type="technology").first(),
            support_strength=0.10,
            notes="Ushahidi hautoshi kuthibitisha dai hili." if lang == "sw" else "The evidence is insufficient to support this claim."
        )

        brief_answer = brief_answer_for_claim(claim_text, analysis)
        if lang == "en":
            brief_answer = (
                "This claim mixes biblical and technological language, but the connection is interpretive rather than direct proof. "
                "Scripture mentions the mark and 666, yet it does not explicitly identify a brain chip."
            ) if analysis["technology_concepts"] and analysis["biblical_concepts"] else (
                "This claim is related to biblical language, but it remains interpretive and needs clearer evidence. "
                "The biblical material is not the same as scientific proof."
            ) if analysis["biblical_concepts"] else (
                "This claim is not well supported by evidence. More context or direct scriptural references are needed."
            )

        claim_report = {
            "claim": claim_text,
            "analysis": analysis,
            "related_verses": claim.related_verses.all(),
            "evidence": claim.evidence_items.all(),
            "classification": "INTERPRETATION",
            "confidence": analysis["confidence"],
            "conclusion": brief_answer,
            "brief_answer": brief_answer,
        }
        messages.success(request, ui["submit_success"])
        context = {
            "form": form,
            "report": claim_report,
            "recent_claims": recent_claims,
            "bible_count": bible_count,
            "history_count": history_count,
            "tech_count": tech_count,
            "source_count": source_count,
            "evidence_count": evidence_count,
            "sample_questions": sample_questions,
            "lang": lang,
            "ui": ui,
        }
        return render(request, "dashboard/dashboard.html", context)

    context = {
        "form": form,
        "report": claim_report,
        "recent_claims": recent_claims,
        "bible_count": bible_count,
        "history_count": history_count,
        "tech_count": tech_count,
        "source_count": source_count,
        "evidence_count": evidence_count,
        "sample_questions": sample_questions,
        "lang": lang,
        "ui": ui,
    }
    return render(request, "dashboard/dashboard.html", context)
