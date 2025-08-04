# rxconfig.py

import reflex

class REINSConfig(reflex.Config):
    # Turn off the sitemap plugin
    disable_plugins = [
        "reflex.plugins.sitemap.SitemapPlugin",
    ]

config = REINSConfig(app_name="reflex_app")