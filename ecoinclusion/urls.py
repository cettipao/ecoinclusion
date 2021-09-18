from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()
router.register(r'intermediarios', IntermediarioViewSet)
router.register(r'centros', CentroReadonlyViewSet)
router.register(r'puntos', PuntoReadonlyViewSet)
router.register(r'depositos', DepositoViewSet)
router.register(r'tipos-de-reciclado', TipoDeRecicladoReadonlyViewSet)

urlpatterns = [
     
     path('',homeView, name="home"),
     path('login/', loginView, name="login"),
     path('somos/', aboutView, name="about"),
     path('register', registerView, name="register"),
     path('logout/', logoutView, name="logout"),
     path('perfil/', perfilView, name="perfil"),
     path('updateperfil/', updatePerfilView, name="updateperfil"),
     path('changepassword/', changePasswordView, name="changepassword"),

     path('dashboard/', dashboardView, name="dashboard"),
     
     path('puntosdeacopio/', puntosView, name="puntosdeacopio"),
     path('puntosdeacopio/delete/<int:id>/', deletePuntoView, name="deletepunto"),
     path('puntosdeacopio/update/<int:id>/', updatePuntoView, name="updatepunto"),

     path('intermediarios/', intermediariosView, name="intermediarios"),
     path('intermediarios/delete/<int:id>/', deleteIntermediarioView, name="deleteintermediario"),
     path('intermediarios/update/<int:id>/', updateIntermediarioView, name="updateintermediario"),

     # Url patterns for django rest framework
     path('api-auth/', include('rest_framework.urls')),
     path('api/', include(router.urls)),
     path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
     path('api/register/', RegisterView.as_view(), name='auth_register'),

]