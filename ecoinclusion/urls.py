from ecoinclusion.models import LugarDeReciclado
from ecoinclusion.serializers import IntermediarioSerializer, LugarDeRecicladoSerializer
from django.urls import path
from .views import DepositoViewSet, IntermediarioViewSet,LugarDeRecicladoViewSet, PuntoReadonlyViewSet,  CentroReadonlyViewSet, RegisterView, TipoDeRecicladoReadonlyViewSet, aboutView, changePasswordView, dashboardView, deleteIntermediarioView, deletePuntoView, homeView, loginView, logoutView, perfilView, puntosView, registerView, updateIntermediarioView, updatePuntoView
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()
router.register(r'lugares', LugarDeRecicladoViewSet)
router.register(r'centros', CentroReadonlyViewSet)
router.register(r'puntos', PuntoReadonlyViewSet)
router.register(r'intermediarios', IntermediarioViewSet)
router.register(r'tipos-de-reciclado', TipoDeRecicladoReadonlyViewSet)
router.register(r'depositos', DepositoViewSet)


urlpatterns = [
     
     path('',homeView, name="home"),
     path('login/', loginView, name="login"),
     path('somos/', aboutView, name="about"),
     path('register', registerView, name="register"),
     path('logout/', logoutView, name="logout"),
     path('perfil/', perfilView, name="perfil"),
     path('changepassword/', changePasswordView, name="changepassword"),

     path('dashboard/', dashboardView, name="dashboard"),
     
     path('puntosdeacopio/', puntosView, name="puntosdeacopio"),
     path('puntosdeacopio/delete/<int:id>/', deletePuntoView, name="deletepunto"),
     path('puntosdeacopio/update/<int:id>/', updatePuntoView, name="updatepunto"),

     path('intermediarios/', IntermediarioSerializer, name="intermediarios"),
     path('intermediarios/delete/<int:id>/', deleteIntermediarioView, name="deleteintermediario"),
     path('intermediarios/update/<int:id>/', updateIntermediarioView, name="updateintermediario"),

     # Url patterns for django rest framework
     path('api-auth/', include('rest_framework.urls')),
     path('api/', include(router.urls)),
     path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
     path('api/register/', RegisterView.as_view(), name='auth_register'),

]