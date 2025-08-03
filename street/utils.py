def get_or_create_chat(client, hustler):
    return ChatRoom.objects.get_or_create(client=client, hustler=hustler)