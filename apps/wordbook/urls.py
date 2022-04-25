from django.urls import path
from .views import ViewUserBook, AddWordTerms

urlpatterns = [
    # path('book/', Veiw_Words.as_view()), 
    path('', ViewUserBook.as_view()), 
    path('add_to_dict/', AddWordTerms.as_view()), 
]