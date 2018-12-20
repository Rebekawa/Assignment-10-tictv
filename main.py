import os
from bottle import (get, post, redirect, request, route, run, static_file, template,
                    jinja2_view)
import utils
from functools import partial
from jinja2 import Template

view = partial(jinja2_view, template_lookup=['templates'])

# Static Routes


@route('/browse')
@view('browse.tpl')
def browse_page():
    sectionTemplate = "./templates/browse.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData=utils.my_func())
    show ={
        'id': request.forms.get('id'),
        'rating': request.forms.get('rating'),
        'average': request.forms.get('average'),
        'image': request.forms.get('image'),
        'original': request.forms.get('original'),
        'name': request.forms.get('name'),
    }
    return show


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
