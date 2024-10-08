"""Google Login Example
"""
import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi_sso.sso.google import GoogleSSO
import json

from resources.student_coupon_resource import StudentCouponResource
from dff_framework.framework.services.config import Config
from services.coupon_service_factory import CouponServiceFactory


from fastapi.staticfiles import StaticFiles
from resources.student_coupon_resource import StudentCouponResource


config = Config()
service_factory = CouponServiceFactory(config)

student_coupon_resource = service_factory.get_service("COUPON_RESOURCE")

# import env

app = FastAPI()


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
CLIENT_ID = config.get_config("CLIENT_ID")
CLIENT_SECRET = config.get_config("CLIENT_SECRET")
OAUTH_URL = config.get_config("OAUTH_URL")

app.mount("/static", StaticFiles(directory="static"), name="static")

sso = GoogleSSO(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=OAUTH_URL + "/auth/callback",
    allow_insecure_http=True,
)


@app.get("/ping", response_class=HTMLResponse)
def ping():
    """

    :return:
    """

    rsp = """
     <!DOCTYPE html>
            <html>
            <head>
                <title>User Info</title>
            </head>
            <body>
               Pong.
            </body>
            </html>
    """
    return rsp


@app.get("/", response_class=HTMLResponse)
async def home_page():
    print("Current directory = " + os.getcwd())
    print("Files = " + str(os.listdir("./")))

    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Google Login</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                margin-top: 100px;
            }
            .container {
                width: 300px;
                margin: 0 auto;
                padding: 20px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #f9f9f9;
            }
            .logo {
                margin-bottom: 20px;
            }
            .button {
                display: inline-block;
                padding: 10px 20px;
                background-color: #4285f4;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <div class="container">
        <p>
        This is the sample web application for <a href="https://donald-f-ferguson.github.io/W4153-Cloud-Computing-Base/">
        W4153 - Cloud Computing.</a>
        </p>
        <p>The application simply demonstrates single sign-on
        via Google for Columbia University students.
        </p>
        <p>
        The application does not capture or maintain any information about users. The application does not
        share any information.
        </p>
        <form action="{OAUTH_URL}/auth/login">
            <div class="logo">
                <img src="{OAUTH_URL}/static/e6156-logo.jpg"
                    height="100px" alt="Google Logo">
            </div>
            <h2>Sign in with your Google Account</h2>
            <button type="submit" class="button">Login with Google</button>
            </form>
        </div>
    </body>
    </html>
    """
    html = html.replace("{OAUTH_URL}", OAUTH_URL)
    result = HTMLResponse(html)
    return result


@app.get("/auth/login")
async def auth_init():
    """Initialize auth and redirect"""
    with sso:
        return await sso.get_login_redirect(params={"prompt": "consent", "access_type": "offline"})


@app.get("/auth/callback", response_class=HTMLResponse)
async def auth_callback(request: Request):
    """Verify login"""
    print("Request = ", request)
    print("URL = ", request.url)

    try:
        with sso:
            user = await sso.verify_and_process(request)
            data = user

            code = request.query_params['code']
            next_url = "./next?code=" + code

            student = user.email
            student = student_coupon_resource.get_info(student)

            print("In auth_callback: Student = \n", json.dumps(student, indent=2, default=str))
            coupon = student.get("coupon_code", None)
            test_coupon = student.get("test_coupon", None)
            coupon_value = student.get("amount", "")

            # if user.email == "dff9@columbia.edu":
            #    raise Exception("Not cool dude.")

            html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>User Info</title>
                </head>
                <body>
                    <h1>User Information</h1>
                    <img src="{user.picture}" alt="User Picture" width="96" height="96"><br>
                    <p><b>ID:</b> {user.id}</p>
                    <p>Email: {user.email}</p>
                    <p>First Name: {user.first_name}</p>
                    <p>Last Name: {user.last_name}</p>
                    <p>Display Name: {user.display_name}</p>
                    <p>Identity Provider: {user.provider}</p>
                    <h1>Google Coupon Information</h1>
                    <p>Google Coupon: {coupon}<br>
                    <p>Coupon Value: {coupon_value}
                </body>
                </html>
                """

            return HTMLResponse(content=html_content)
    except Exception as e:
        print("Exception e = ", e)
        return RedirectResponse("/static/error.html")


@app.get("/next", response_class=HTMLResponse)
async def auth_callback(request: Request):
    """Verify login"""
    print("Request = ", request)
    print("URL = ", request.url)

    try:
        with sso:
            user = await sso.verify_and_process(request)
            data = user

            student = student_coupon_resource.get_info(student)
            print("Student = \n", json.dumps(student, indent=2, default=str))
            coupon = student.get("student_coupon_code", None)
            coupon_value = student.get("Value", None)

            # if user.email == "dff9@columbia.edu":
            #    raise Exception("Not cool dude.")

            html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>User Info</title>
                </head>
                <body>
                    <h1>Still logged in dude.n</h1>
                    <img src="{user.picture}" alt="User Picture" width="96" height="96"><br>
                    <p><b>ID:</b> {user.id}</p>
                    <p>Email: {user.email}</p>
                    <p>First Name: {user.first_name}</p>
                    <p>Last Name: {user.last_name}</p>
                    <p>Display Name: {user.display_name}</p>
                    <p>Identity Provider: {user.provider}</p>
                    <h1>Google Coupon Information</h1>
                    <p>Google Coupon: {coupon}<br>
                    <p>Coupon Value: ${coupon_value}
                </body>
                </html>
                """

            return HTMLResponse(content=html_content)
    except Exception as e:
        print("Exception e = ", e)
        return RedirectResponse("/static/error.html")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
