import flask
import re


app = flask.Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)


@app.route("/channel/<name>/")
def channel_name(name):
    messages = flask._app_ctx_stack.channels[name]
    channels = list(flask._app_ctx_stack.channels.keys())
    groups = list(flask._app_ctx_stack.groups.keys())
    dm_users = list(flask._app_ctx_stack.dm_users)
    mpim_users = list(flask._app_ctx_stack.mpim_users)

    return flask.render_template("viewer.html", messages=messages,
                                 name=name.format(name=name),
                                 channels=sorted(channels),
                                 groups=sorted(groups),
                                 dm_users=dm_users,
                                 mpim_users=mpim_users)


@app.route("/group/<name>/")
def group_name(name):
    messages = flask._app_ctx_stack.groups[name]
    channels = list(flask._app_ctx_stack.channels.keys())
    groups = list(flask._app_ctx_stack.groups.keys())
    dm_users = list(flask._app_ctx_stack.dm_users)
    mpim_users = list(flask._app_ctx_stack.mpim_users)

    return flask.render_template("viewer.html", messages=messages,
                                 name=name.format(name=name),
                                 channels=sorted(channels),
                                 groups=sorted(groups),
                                 dm_users=dm_users,
                                 mpim_users=mpim_users)


@app.route("/dm/<id>/")
def dm_id(id):
    messages = flask._app_ctx_stack.dms[id]
    channels = list(flask._app_ctx_stack.channels.keys())
    groups = list(flask._app_ctx_stack.groups.keys())
    dm_users = list(flask._app_ctx_stack.dm_users)
    mpim_users = list(flask._app_ctx_stack.mpim_users)

    return flask.render_template("viewer.html", messages=messages,
                                 id=id.format(id=id),
                                 channels=sorted(channels),
                                 groups=sorted(groups),
                                 dm_users=dm_users,
                                 mpim_users=mpim_users)


@app.route("/mpim/<name>/")
def mpim_name(name):
    messages = flask._app_ctx_stack.mpims[name]
    channels = list(flask._app_ctx_stack.channels.keys())
    groups = list(flask._app_ctx_stack.groups.keys())
    dm_users = list(flask._app_ctx_stack.dm_users)
    mpim_users = list(flask._app_ctx_stack.mpim_users)

    return flask.render_template("viewer.html", messages=messages,
                                 name=name.format(name=name),
                                 channels=sorted(channels),
                                 groups=sorted(groups),
                                 dm_users=dm_users,
                                 mpim_users=mpim_users)


@app.route("/")
def index():
    channels = list(flask._app_ctx_stack.channels.keys())
    if "general" in channels:
        return channel_name("general")
    else:
        return channel_name(channels[0])


@app.route("/", methods=["POST"])
def search_post():
    channels = list(flask._app_ctx_stack.channels.keys())
    groups = list(flask._app_ctx_stack.groups.keys())
    dm_users = list(flask._app_ctx_stack.dm_users)
    mpim_users = list(flask._app_ctx_stack.mpim_users)

    matches = []
    pattern = flask.request.form['pattern']
    if len(pattern) > 0:
      regex = re.compile(pattern)
      for channel in flask._app_ctx_stack.channels.values():
          for message in channel:
              if regex.search(message.raw):
                  matches.append(message)

    return flask.render_template("viewer.html", messages=matches,
                                 channels=sorted(channels),
                                 groups=sorted(groups),
                                 dm_users=dm_users,
                                 mpim_users=mpim_users,
                                 pattern=pattern)
