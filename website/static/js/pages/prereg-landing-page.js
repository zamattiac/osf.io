'use strict';
var $ = require('jquery');
var $osf = require('js/osfHelpers');
var Raven = require('raven-js');
var ko = require('knockout');
require('js/qToggle');
require('js/onboarder.js');
require('js/components/autocomplete');

var xhrconfig = function (xhr) {
    xhr.withCredentials = true;
    xhr.setRequestHeader('Content-Type', 'application/vnd.api+json');
    xhr.setRequestHeader('Accept', 'application/vnd.api+json; ext=bulk');
};


$(function(){
    $('.prereg-button').qToggle();
    $('.prereg-button').click(function(){
        var target = $(this).attr('data-qToggle-target');
        var input = $(target).find('input').first().focus();
    });

    $('#newProject, #newProjectXS').click( function() {
        var title = $(this).parent().find('.new-project-title').val();
        if (!title) {
            return;
        }
        $osf.postJSON('/api/v1/project/new/', {
            title: title,
            campaign: 'prereg'
        }).done(function(response) {
            window.location = response.projectUrl + 'registrations/?campaign=prereg';
        }).fail(function() {
            $osf.growl('Project creation failed. Reload the page and try again.');
        });
    });

    var allNodes = [];
    var allRegistrations = [];

    // Get all projects with multiple calls to get all pages
    function collectProjects (url) {
        var promise = $.ajax({
            method: "GET",
            url: url,
            xhrFields: {
                withCredentials: true
            }
        });
        promise.done(function(result){
            // loop through items and check for admin permission first
            allNodes.concat(result.data);
            if(result.links.next){
                collectProjects(result.links.next);
            }
            else {
                $osf.applyBindings({
                    nodes: allNodes,
                    enableComponents: true
                }, '#existingProject');
                $osf.applyBindings({
                    nodes: allNodes,
                    enableComponents: true
                }, '#existingProjectXS');
            }
        });
        promise.fail(function(xhr, textStatus, error) {
            Raven.captureMessage('Next page load failed for user nodes.', {
                url: url, textStatus: textStatus, error: error
            });
        });
    }


    // Get nodes and apply bindings
    var nodeLink = $osf.apiV2Url('users/me/nodes/', { query : { 'page[size]' : 100}});
    collectProjects(nodeLink);

    // Activate autocomplete for draft registrations
    $.getJSON('/api/v1/prereg/draft_registrations/').then(function(response){
        if (response.draftRegistrations.length) {
            $osf.applyBindings({}, '#existingPrereg');
            $osf.applyBindings({}, '#existingPreregXS');
        }
    });
});
