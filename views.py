class CategoryItemsSearchView(ListModelMixin, GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryItemsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    # filter_backends = (CustomSearchFilter, )
    # search_fields = ['name', 'dishes__title', ]
    # fiterset_fields = ['dishes__title', 'name']


    # def filter_queryset(self, queryset):
    #     for backend in list(self.filter_backends):
    #         queryset = backend().filter_queryset(self.request,queryset, self)
    #     return  queryset
    
    
    def get_queryset(self):
        return Category.objects.all()
    

    def get(self, request):
        search_term = ''
        el = ''
        if 'search' in request.GET:
            search_term = request.GET['search']
            if search_term is not None:
                categories = None
                if Category.objects.filter(name__icontains=search_term):
                    categories = Category.objects.filter(name__icontains=search_term)
                    serializer = CategoryItemsSerializer(categories, many=True)
                    return Response(serializer.data)

                elif Category.objects.filter(dishes__title__icontains=search_term): 
                    categories = Category.objects.filter(dishes__title__icontains=search_term)
                    dishes = Dish.objects.filter(title__icontains=search_term)
                    category_serializer = CategoryItemsSerializer(categories, many=True)
                    dishes_serializer = DishListSerializer(dishes, many=True)
                    category_serializer_data = category_serializer.data
                    dishes_serializer_data = dishes_serializer.data
                   
                    for category in category_serializer_data:
                        for dishes in range(len(category['dishes'])):
                            count = 0
                            while count < len(category['dishes']):
                                if dishes[count] != search_term and dishes[count] != search_term.capitalize():
                                    print(dishes)
                            # if dishes['title'] != search_term and dishes['title'] != search_term:
                            #     print(dishes)
                                

                             # print(len(category['dishes']) , "\n\n\n")
                            
                        # for dishes in category:
                        #     for dish in dishes: 
                        #         if dish['title'] != search_term:
                        #             del dishes[dish]
                        # el = category.pop('dishes', None)
                        # for dish in range(len(el)-1):
                        #     if el[dish]['title'] == search_term and el[dish]['title'] == search_term.capitalize():
                        #         category['dishes'] = el[dish]
                        #         # print(el[dish])
                        #         # del el[dish]
                        #     elif el[dish]['title'] != search_term and el[dish]['title'] != search_term.capitalize():
                            
                        #         del el[dish]
                    # for category2 in category_serializer_data:
                    #     category2['dishes'] = dishes_serializer_data
                    
                

                return Response(category_serializer_data)  

            elif search_term == None: 
                return Response({
                    'details': "Вы ничего не ввели в поиск.Товаров не найдено"
                })
        
            
        # else: 
        #     categories = Category.objects.all()
        #     serializer = CategoryItemsSerializer(categories, many=True)
            
        #     return Response(serializer.data)
            # for i in categories:
            #     print(i)
            #     print(len(categories))
        
        
    
    # def list(self, request):
    #     queryset = Category.objects.all()

    #     dish_id = self.request.query_params.get('dishes__id', None)
    #     if dish_id is not None:
    #         queryset = queryset.filter(pk=dish_id)
        
    #     serializer = CategoryItemsSerializer(queryset, many=True)
    #     return Response(serializer.data)

        # the_filtered_qs = self.filter_queryset(self.get_queryset())
        
        # categories = the_filtered_qs
        # serializer = CategoryItemsSerializer(categories, many=True)
        # return Response(serializer.data)

    # serializer = CategoryItemsSerializer()

    # def get(self, request,*args, **kwargs):
    #     return self.list(request, *args, **kwargs)
        # categories = Category.objects.all()
        # search_term = ''

        # context = {
        #         "request": request,
        #         "categories": categories
        # }
        # return Response(categories)





 def get(self, request, format=None):
        queryset = self.get_queryset()

        if queryset.exists():
            serializer = CategoryItemsSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"Returned empty queryset"}, status=False)


"categories": [
        {
            "id": 1,
            "name": "Второе",
            "dishes": [
                {
                    "id": 3,
                    "title": "Запеченный судак",
                    "price": 450,