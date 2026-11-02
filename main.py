from dotenv import load_dotenv
load_dotenv()

from kirak import create_kirak_app

app = create_kirak_app(
    models_path="./models/",
)
