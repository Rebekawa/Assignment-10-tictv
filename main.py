import os
from bottle import (get, post, redirect, request, route, run, static_file, template,
                    jinja2_view, error)
import utils
from functools import partial
import json
view = partial(jinja2_view, template_lookup=['templates'])

# Static Routes

@error(404)
def error404(error):
    sectionTemplate = "./templates/404.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData={})

@route('/browse')
@view('browse.tpl')
def browse_page():
    sectionTemplate = "./templates/browse.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData=[json.loads(utils.getJsonFromFile(elem)) for elem in utils.AVAILABLE_SHOWS])


@route('/ajax/show/<number>')
@view('show.tpl')
def browse_page(number):
    return template("./templates/show.tpl", version=utils.getVersion(),
                    result=json.loads(utils.getJsonFromFile(number)))

@route('/show/<number>')
@view('show.tpl')
def browse_page(number):
    sectionTemplate = "./templates/show.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData=json.loads(utils.getJsonFromFile(number)))



@route('/search', method='POST')
def search_result():
    research = request.forms.get('q')
    sectionTemplate = "./templates/search.tpl"
    shows = []
    new = []

    for show in utils.AVAILABE_SHOWS:
        json_show = utils.getJsonFromFile(show)
        dict_show = json.loads(json_show)
        shows.append(dict_show)
    for show in shows:
        new.append(show['name'])
    # print(new)
    if research in new:
        print("yay")
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData={})


@route('/show/<number>/episode/<episode_number>')
def show(number, episode_number):
    sectionTemplate = "./templates/episode.tpl"
    json_show = utils.getJsonFromFile(number)
    show = json.loads(json_show)
    episodes = show["_embedded"]["episodes"]
    for episode in episodes:
        if str(episode["id"]) == episode_number:
            result_episode = episode
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData=result_episode)


@route('/ajax/show/<number>/episode/<episode_number>')
def show(number, episode_number):
    json_show = utils.getJsonFromFile(number)
    show = json.loads(json_show)
    episodes = show["_embedded"]["episodes"]
    for episode in episodes:
        if str(episode["id"]) == episode_number:
            result_episode = episode
    return template("./templates/episode.tpl", result=result_episode)



@route('/search')
@view('search.tpl')
def search_page():
    sectionTemplate = "./templates/search.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData={})



@get("/js/<filepath:re:.*\.js>")
def js(filepath):
    return static_file(filepath, root="./js")


@get("/css/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root="./css")


@get("/images/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return static_file(filepath, root="./images")


@route('/')
def index():
    sectionTemplate = "./templates/home.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData={})



if __name__ == "__main__":
    run(host='localhost', port=7000, debug=True)
