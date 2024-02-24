from django.shortcuts import render

# class EntitiesApiView(APIView):
#     def get(self, request):
#         lst = Entities.objects.all().values()
#         permission_classes = (IsAuthenticated, )
#         return Response(lst)
    
#     def post(self, request):
#         post_new = Entities.objects.create(
#             name = request.data['name'],
#             entityid = request.data['entityid'],
#         )
#         return Response({'post': model_to_dict(post_new)})

# class EntitiesApiView(generics.ListAPIView):
#     queryset = Entities.objects.all()
#     serializer_class = EntitiesSerializer