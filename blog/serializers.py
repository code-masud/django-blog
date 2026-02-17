# class PostSerializer(serializers.ModelSerializer):

#     def create(self, validated_data):
#         validated_data["created_by"] = self.context["request"].user
#         validated_data["updated_by"] = self.context["request"].user
#         return super().create(validated_data)

#     def update(self, instance, validated_data):
#         validated_data["updated_by"] = self.context["request"].user
#         return super().update(instance, validated_data)
