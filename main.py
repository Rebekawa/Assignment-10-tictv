import os
import bottle
from bottle import (get, request, route, run, static_file, template, jinja2_view, error)
import utils
from functools import partial
import json
from sys import argv


DEBUG = os.environ.get("DEBUG")
bottle.debug(True)

view = partial(jinja2_view, template_lookup=['templates'])


@route('/')
def home_page():
    sectionTemplate = "./templates/home.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData={})


@route('/browse')
@view('browse.tpl')
def browse_page():
    sectionTemplate = "./templates/browse.tpl"
    shows_list = []
    for show in utils.AVAILABLE_SHOWS:
        shows_list.append(json.loads(utils.getJsonFromFile(show)))
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData=shows_list)


@route('/show/<number>')
@view('show.tpl')
def show_page(number):
    sectionTemplate = "./templates/show.tpl"
    show = json.loads(utils.getJsonFromFile(number))
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData=show)


@route('/ajax/show/<number>')
@view('show.tpl')
def show_page(number):
    show = json.loads(utils.getJsonFromFile(number))
    return template("./templates/show.tpl", version=utils.getVersion(), result=show)


@route('/show/<number>/episode/<episode_number>')
@view('episode.tpl')
def episode_page(number, episode_number):
    sectionTemplate = "./templates/episode.tpl"
    show = json.loads(utils.getJsonFromFile(number))
    episodes = show["_embedded"]["episodes"]
    for episode in episodes:
        if episode["id"] == int(episode_number):
            relevant_episode = episode
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData=relevant_episode)


@route('/ajax/show/<number>/episode/<episode_number>')
@view('episode.tpl')
def episode_page(number, episode_number):
    show = utils.getJsonFromFile(number)
    show = json.loads(show)
    episodes = show["_embedded"]["episodes"]
    for episode in episodes:
        if episode["id"] == int(episode_number):
            relevant_episode = episode
    return template("./templates/episode.tpl", result=relevant_episode)


@route('/search')
@view('search.tpl')
def search_page():
    sectionTemplate = "./templates/search.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData={})


@route('/search', method="POST")
@view('search_result.tpl')
def search_page():
    user_input = request.forms.get("q")
    shows_list = []
    for show in utils.AVAILABLE_SHOWS:
        shows_list.append(json.loads(utils.getJsonFromFile(show)))
    relevant_episode = []
    for show in shows_list:
        for episode in show["_embedded"]["episodes"]:
            r = {}
            if type(episode['summary']) == str and user_input in episode['summary'] or type(episode['name']) == str and user_input in episode['name']:
                r["showid"] = show["id"]
                r['episodeid'] = episode["id"]
                r['text'] = show['name'] + " : " + episode["name"]
                relevant_episode.append(r)
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate="./templates/search_result.tpl",
                    sectionData={}, results=relevant_episode, query=user_input)


@error(404)
def error404_page(error):
    sectionTemplate = "./templates/404.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData={})


# Static Routes

@get("/js/<filepath:re:.*\.js>")
def js(filepath):
    return static_file(filepath, root="./js")


@get("/css/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root="./css")


@get("/images/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return static_file(filepath, root="./images")



if DEBUG:
	bottle.run(host='localhost', port=7000)
else:
	bottle.run(host='0.0.0.0', port=argv[1])


#if __name__ == "__main__":
    #run(host='localhost', port=7000, debug=True)
