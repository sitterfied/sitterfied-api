import models

from rest_framework import serializers, viewsets, permissions
from rest_framework import viewsets

# class MyselfSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = models.User
#         fields = ('first_name', 'last_name', 'username', 'email')

user_fields = ('first_name', 'last_name',
               'username', 'last_login',
               'date_joined', 'settings',
               'sitters_in_network',
               'parents_in_network', 'sitter_groups', 'bookings')


class SitterSerializer(serializers.ModelSerializer):

    #todo general availablity
    parent_or_sitter = "Sitter"
    class Meta:
        model = models.Sitter
        fields = user_fields + ('id', 'biography', 'live_zip',
                  'work_zip', 'smoker',
                  'will_transport', 'total_exp',
                  'infant_exp',  'toddler_exp',
                  'preschool_exp', 'school_age_exp',
                  'pre_teen_exp', 'teen_exp',
                  'highest_education', 'last_school',
                  'current_student','certification',
                  'other_services','one_child_min_rate',
                  'one_child_max_rate', 'two_child_min_rate',
                  'two_child_max_rate',  'three_child_min_rate',
                  'three_child_max_rate',  'smokers_ok',
                  'dogs_ok', 'cats_ok',
                  'other_animals_ok',
                  )



class ParentSerializer(serializers.ModelSerializer):

    #contacts
    parent_or_sitter = "Parent"
    class Meta:
        model = models.Parent
        fields = user_fields + ('id', 'emergency_contact', 'physician_contact',
                  'parking_area', 'parking_for_sitter',
                  )


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Settings


class SitterViewSet(viewsets.ModelViewSet):
    queryset = models.Sitter.objects.all()
    serializer_class = SitterSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_fields = ('id', )

class ParentViewSet(viewsets.ModelViewSet):
    queryset = models.Parent.objects.all()
    serializer_class = ParentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_fields = ('id', )


class SettingsViewSet(viewsets.ModelViewSet):
    queryset = models.Settings.objects.all()
    serializer_class = SettingsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


#bookings
#languages
