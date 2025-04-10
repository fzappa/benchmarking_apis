from ninja import Router

router = Router()

@router.get("/ping")
async def ping(request):
    return {"message": "pong"}


# from ninja import NinjaAPI
# api = NinjaAPI()

# @api.get("/ping")
# def ping(request):
#     return {"message": "pong"}