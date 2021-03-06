import flask
import re
import itertools
import operator


app = flask.Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)


@app.route("/channel/<name>/")
def channel_name(name):
    messages = flask._app_ctx_stack.channels[name]
    if not app.config["NEWEST_FIRST"]:
        messages = sorted(messages, key=operator.attrgetter('datetime'))
    channels = list(flask._app_ctx_stack.channels.keys())
    groups = list(flask._app_ctx_stack.groups.keys())
    dm_users = list(flask._app_ctx_stack.dm_users)
    mpim_users = list(flask._app_ctx_stack.mpim_users)

    return flask.render_template("viewer.html", 
                                 newest_first=app.config["NEWEST_FIRST"],
                                 messages=messages,
                                 name=name.format(name=name),
                                 channels=sorted(channels),
                                 groups=sorted(groups),
                                 dm_users=dm_users,
                                 mpim_users=mpim_users)


@app.route("/group/<name>/")
def group_name(name):
    messages = flask._app_ctx_stack.groups[name]
    if not app.config["NEWEST_FIRST"]:
        messages = sorted(messages, key=operator.attrgetter('datetime'))
    channels = list(flask._app_ctx_stack.channels.keys())
    groups = list(flask._app_ctx_stack.groups.keys())
    dm_users = list(flask._app_ctx_stack.dm_users)
    mpim_users = list(flask._app_ctx_stack.mpim_users)

    return flask.render_template("viewer.html", 
                                 newest_first=app.config["NEWEST_FIRST"],
                                 messages=messages,
                                 name=name.format(name=name),
                                 channels=sorted(channels),
                                 groups=sorted(groups),
                                 dm_users=dm_users,
                                 mpim_users=mpim_users)


@app.route("/dm/<id>/")
def dm_id(id):
    messages = flask._app_ctx_stack.dms[id]
    if not app.config["NEWEST_FIRST"]:
        messages = sorted(messages, key=operator.attrgetter('datetime'))
    channels = list(flask._app_ctx_stack.channels.keys())
    groups = list(flask._app_ctx_stack.groups.keys())
    dm_users = list(flask._app_ctx_stack.dm_users)
    mpim_users = list(flask._app_ctx_stack.mpim_users)

    return flask.render_template("viewer.html", 
                                 newest_first=app.config["NEWEST_FIRST"],
                                 messages=messages,
                                 id=id.format(id=id),
                                 channels=sorted(channels),
                                 groups=sorted(groups),
                                 dm_users=dm_users,
                                 mpim_users=mpim_users)


@app.route("/mpim/<name>/")
def mpim_name(name):
    messages = flask._app_ctx_stack.mpims[name]
    if not app.config["NEWEST_FIRST"]:
        messages = sorted(messages, key=operator.attrgetter('datetime'))
    channels = list(flask._app_ctx_stack.channels.keys())
    groups = list(flask._app_ctx_stack.groups.keys())
    dm_users = list(flask._app_ctx_stack.dm_users)
    mpim_users = list(flask._app_ctx_stack.mpim_users)

    return flask.render_template("viewer.html", 
                                 newest_first=app.config["NEWEST_FIRST"],
                                 messages=messages,
                                 name=name.format(name=name),
                                 channels=sorted(channels),
                                 groups=sorted(groups),
                                 dm_users=dm_users,
                                 mpim_users=mpim_users)


@app.route("/")
def index():
    channels = sorted(list(flask._app_ctx_stack.channels.keys()))
    channel = "general"
    if not channel in channels:
        channel = channels[0]
    if app.config["NEWEST_FIRST"]:
        return channel_name(channel)
    else:
        return flask.render_template("redirect.html", url="/channel/%s#end" % channel)


@app.route("/", methods=["POST"])
def search_post():
    channels = flask._app_ctx_stack.channels
    groups = flask._app_ctx_stack.groups
    dms = flask._app_ctx_stack.dms
    mpims = flask._app_ctx_stack.mpims
    dm_users = list(flask._app_ctx_stack.dm_users)
    mpim_users = list(flask._app_ctx_stack.mpim_users)

    matches = []
    regex = None
    pattern = flask.request.form['pattern']
    if len(pattern) > 0:
      regex = re.compile(pattern, re.IGNORECASE)
      for channel in itertools.chain(channels.values(), groups.values(), dms.values(), mpims.values()):
          for message in channel:
              if regex.search(message.raw):
                  matches.append(message)

    matches = sorted(matches, key=operator.attrgetter('datetime'), reverse=True)

    return flask.render_template("viewer.html", messages=matches,
                                 channels=sorted(list(channels.keys())),
                                 groups=sorted(list(groups.keys())),
                                 dm_users=dm_users,
                                 mpim_users=mpim_users,
                                 pattern=pattern,
                                 regex=regex)
