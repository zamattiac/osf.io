from framework.routing import Rule, json_renderer
from website.routes import OsfWebRenderer

from . import views

api_routes = {
    'rules': [
        Rule(
            '/settings/dataverse/',
            'get',
            views.dataverse_user_config_get,
            json_renderer,
        ),
        Rule(
            '/settings/dataverse/accounts/',
            'post',
            views.dataverse_add_user_account,
            json_renderer,
        ),
        Rule(
            '/settings/dataverse/accounts/',
            'get',
            views.dataverse_account_list,
            json_renderer,
        ),
        Rule(
            [
                '/project/<pid>/dataverse/settings/',
                '/project/<pid>/node/<nid>/dataverse/settings/',
            ],
            'get',
            views.dataverse_get_config,
            json_renderer,
        ),
        Rule(
            [
                '/project/<pid>/dataverse/settings/',
                '/project/<pid>/node/<nid>/dataverse/settings/',
            ],
            'post',
            views.dataverse_set_config,
            json_renderer,
        ),
        Rule(
            [
                '/project/<pid>/dataverse/user-auth/',
                '/project/<pid>/node/<nid>/dataverse/user-auth/',
            ],
            'put',
            views.dataverse_import_auth,
            json_renderer,
        ),
        Rule(
            [
                '/project/<pid>/dataverse/user-auth/',
                '/project/<pid>/node/<nid>/dataverse/user-auth/',
            ],
            'delete',
            views.dataverse_deauthorize_node,
            json_renderer,
        ),
        Rule(
            [
                '/project/<pid>/dataverse/list-datasets/',
                '/project/<pid>/node/<nid>/dataverse/list-datasets/',
            ],
            'post',
            views.dataverse_get_datasets,
            json_renderer,
        ),
        Rule(
            [
                '/project/<pid>/dataverse/hgrid/root/',
                '/project/<pid>/node/<nid>/dataverse/hgrid/root/',
            ],
            'get',
            views.dataverse_root_folder,
            json_renderer,
        ),
        Rule(
            [
                '/project/<pid>/dataverse/publish/',
                '/project/<pid>/node/<nid>/dataverse/publish/',
            ],
            'put',
            views.dataverse_publish_dataset,
            json_renderer,
        ),
        Rule(
            [
                '/project/<pid>/dataverse/widget/',
                '/project/<pid>/node/<nid>/dataverse/widget/',
            ],
            'get',
            views.dataverse_widget,
            OsfWebRenderer('../addons/dataverse/templates/dataverse_widget.mako', trust=False),
        ),
        Rule(
            [
                '/project/<pid>/dataverse/widget/contents/',
                '/project/<pid>/node/<nid>/dataverse/widget/contents/',
            ],
            'get',
            views.dataverse_get_widget_contents,
            json_renderer,
        ),
    ],
    'prefix': '/api/v1'
}
