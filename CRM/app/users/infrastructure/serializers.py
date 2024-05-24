from rest_framework import serializers
from CRM.app.users.domain.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'document', 'document_hash')
        read_only_fields = ('document_hash',)

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        if 'document' in validated_data:
            user.document = validated_data['document']
        user.save()
        return user