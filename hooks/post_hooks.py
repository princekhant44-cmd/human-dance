# CRUD hooks -- register via on_kirak_ready in main.py:
#
# def register_hooks(kirak):
#     @kirak.on("posts").hook("after_create")
#     async def after_post_created(result):
#         print(f"New post: {result['data']['id']}")
#         return result  # must return
#
#     @kirak.auth.hook("after_login")
#     async def after_login(result):
#         return result
