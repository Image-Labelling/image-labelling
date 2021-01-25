from .auth import auth
from .create_polygon import create_polygon
from .home import home
from .howto import howto
from .image import image
from .label import label
from .profile import profile
from .send_files import send_file
from .upload import upload
from .users import users

blueprints = [home, auth, users, upload, label, create_polygon, send_file, howto, profile, image]
