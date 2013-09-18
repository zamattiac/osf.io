<%namespace file="_print_logs.mako" import="print_logs"/>
<script src="//code.jquery.com/ui/1.10.3/jquery-ui.js"></script>
<%def name="node_list(nodes, default=None, node_id=None, is_contributor=False, is_registration=False)">
<ul class="list-group ${'sortable' if default=="project_dash" and is_contributor and not is_registration else ''}" node_class="${default}" style="margin-left: 0px;">

%for node in nodes:
    % if node._primary_key is None or node.is_deleted:
        <% continue %>
    % endif
    <li id="projects-widget" node_id="${node._primary_key}" class="project list-group-item" style="display: list-item;">
		<h3 style="line-height:18px;">
			<span style="display:inline-block; width: 400px">
			%if not node.node__parent:
			    <a href="${node.url()}">${node.title}</a>
			%else:
				<a href="${node.url()}">${node.title}</a>
			%endif
			% if node.is_registration:
				| registered: ${node.registered_date.strftime('%Y/%m/%d %I:%M %p')}
			% endif
			</span>
			<i style="float:right;" id="icon-${node._primary_key}" class="icon-plus" onclick="openCloseNode('${node._primary_key}');"></i>
		</h3>
		
		<div class="body hide" id="body-${node._primary_key}" style="overflow:hidden;">
		      Recent Activity
		      %if node.logs:
		      	${print_logs(reversed(node.logs), n=3)}
		      %endif
		</div>
	</li>
%endfor
</ul>

<script>
    $(function(){
        $('.sortable').sortable({
            containment: "#containment",
            tolerance: "pointer",
            items: "> li",
            stop: function(event, ui){
                var sort_list_elm = this;
                var id_list = $(sort_list_elm).sortable("toArray", {
                   attribute: "node_id"
                });
                var page = $(sort_list_elm).attr("node_class");
                checkListChange(id_list, page, sort_list_elm);
            }
        });
    });


    function checkListChange(id_list, page, item){
        if(page=='project_dash'){
            var data_to_send = {}
            data_to_send['new_list'] = JSON.stringify(id_list);
            $.post('/api/v1/project/${node_id}/reorder_components/', data_to_send, function(response){
                if(response['success']=='false'){
                    $(item).sortable("cancel");
                }
            });
          }
    };
</script>
</%def>