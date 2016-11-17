# -*- coding: utf-8 -*-
from app import app, db, session
from flask import request, jsonify
from datetime import timedelta, datetime
from .managers import APIManager, MessageManager, UserSessionManager, MenuManager
from .myLogger import viewLog
from .decorators import processtime


EXPIRE_LIMIT_SECONDS = 20
APIAdmin = APIManager()


@app.route("/api/failtest", methods=["GET"])
def failtest():
    return processFail(), 400


@app.route("/api/session", methods=["GET"])
def sessiontest():
    print(session)
    return str(session), 200


@app.route("/api/session/<value>", methods=["GET"])
def sessioninputtest(value):
    now = datetime.utcnow() + timedelta(hours=9)
    now = int(now.timestamp())
    session[value] = {
        "time": now,
        "act": "test",
    }
    print(session)
    return str(session), 200


@processtime
def sessionCheck():
    now = datetime.utcnow() + timedelta(hours=9)
    now = now.timestamp()

    for key in list(session):
        if now - session[key]["time"] > EXPIRE_LIMIT_SECONDS:
            del session[key]


def processFail():
    message = APIAdmin.process("fail").getMessage()
    viewLog("fail")
    return jsonify(message)


@app.route("/api/keyboard", methods=["GET"])
def yellowKeyboard():
    message = APIAdmin.process("home").getMessage()
    return jsonify(message), 200


@app.route("/api/message", methods=["POST"])
def yellowMessage():
    # TODO : try-except로 에러 캐치하기

    try:
        viewLog("message", request.json)
        message = APIAdmin.process("message", request.json).getMessage()
        raise
        return jsonify(message), 200
    except:
        return processFail(), 400


@app.route("/api/friend", methods=["POST"])
def yellowFriendAdd():
    try:
        viewLog("add", request.json)
        message = APIAdmin.process("add", request.json).getMessage()
        return jsonify(message), 200
    except:
        return processFail(), 400


@app.route("/api/friend/<key>", methods=["DELETE"])
def yellowFriendBlock(key):
    try:
        viewLog("block", key)
        message = APIAdmin.process("block", key).getMessage()
        return jsonify(message), 200
    except:
        return processFail(), 400


@app.route("/api/chat_room/<key>", methods=["DELETE"])
def yellowExit(key):
    # TODO : expire user session

    try:
        viewLog("exit", key)
        message = APIAdmin.process("exit", key).getMessage()
        return jsonify(message), 200
    except:
        return processFail(), 400
