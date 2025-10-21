from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from .models import Translation


# Core normalization maps
TO_TURKMEN = {
    'a': 'ä', 'u': 'ü', 'c': 'ç', 'y': 'ý',
    's': 'ş', 'n': 'ň', 'z': 'ž',
}
TO_BASIC = {v: k for k, v in TO_TURKMEN.items()}


def generate_variants(text: str) -> set[str]:
    """
    Generate all reasonable Turkmen/Latin variants of a given word.
    Example: 'saska' -> {'saska', 'şaska', 'şaşka', 'şäşkä'}
    """
    text = text.lower().strip()
    variants = {text}

    # Replace all possible characters one-by-one
    for i, ch in enumerate(text):
        if ch in TO_TURKMEN:
            for base in list(variants):
                variants.add(base[:i] + TO_TURKMEN[ch] + base[i+1:])
        if ch in TO_BASIC:
            for base in list(variants):
                variants.add(base[:i] + TO_BASIC[ch] + base[i+1:])

    return variants


def translator_view(request):
    result = ""
    query = request.GET.get('query')
    direction = request.GET.get('direction', 'en_to_tm')

    if query:
        query = query.strip().lower()
        variants = generate_variants(query)

        try:
            if direction == 'en_to_tm':
                # English → Turkmen
                matches = Translation.objects.filter(english__iexact=query)
                if matches.exists():
                    result = ", ".join([m.turkmen for m in matches])
                else:
                    result = "Tapylmady."
            else:
                # Turkmen → English
                # Only translate if exact or normalized variant exists
                q_obj = Q()
                for v in variants:
                    q_obj |= Q(turkmen__iexact=v)

                matches = Translation.objects.filter(q_obj)
                if matches.exists():
                    result = ", ".join([m.english for m in matches])
                else:
                    result = "Tapylmady."
        except Exception:
            result = "Tapylmady."

    return render(request, 'translator/index.html', {
        'result': result,
        'query': query or "",
        'direction': direction,
    })


def suggest_words(request):
    """Provide live suggestions for autocomplete."""
    query = request.GET.get('q', '').strip().lower()
    direction = request.GET.get('direction', 'en_to_tm')
    suggestions = []

    if query:
        variants = generate_variants(query)
        if direction == 'en_to_tm':
            results = Translation.objects.filter(
                Q(english__icontains=query)
            ).values_list('english', flat=True)[:10]
        else:
            q_obj = Q()
            for v in variants:
                q_obj |= Q(turkmen__icontains=v)
            results = Translation.objects.filter(q_obj).values_list('turkmen', flat=True)[:10]

        suggestions = list(results)

    return JsonResponse({'suggestions': suggestions})
