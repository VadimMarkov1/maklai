from django.http import JsonResponse
from rest_framework.decorators import api_view
from .utils import find_nouns_positions, generate_nouns_permutations


@api_view(['GET'])
def paraphrase(request):
    try:
        tree_string = request.GET.get('tree', '')
        limit = int(request.GET.get('limit', '20'))
        nouns = find_nouns_positions(tree_string)
        results = generate_nouns_permutations(tree_string, nouns, limit)
        response_data = {'paraphrased_trees': results}
        return JsonResponse(response_data, json_dumps_params={'indent': 4, 'ensure_ascii': False})
    except Exception as e:
        response_data = {'error': str(e).replace('\n', '')}
        return JsonResponse(response_data, json_dumps_params={'indent': 4, 'ensure_ascii': False})

