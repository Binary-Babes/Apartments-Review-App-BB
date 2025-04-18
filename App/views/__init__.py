# blue prints are imported 
# explicitly instead of using *
from .user import user_views
from .index import index_views
from .auth import auth_views
from .admin import setup_admin

# All views listed here will be registered in add_views()
views = [user_views, index_views, auth_views]
