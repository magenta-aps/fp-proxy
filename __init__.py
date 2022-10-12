import json
from flask import Flask, send_file, make_response, render_template
from urllib import parse
from wsgiref.handlers import format_date_time
from datetime import datetime
from dateutil.parser import parse as parse_datetime
from requests import get, head


app = Flask(__name__)
INSTANCE = "https://dagsordener.randers.dk/"


@app.template_filter()
def datetimeformat(string):
    return parse_datetime(string).strftime("%d/%m-%Y")


def get_first_path(d, *paths, processor=None):
    for path in paths:
        here = d
        for component in path:
            if component in here:
                here = here[component]
            else:
                here = None
                continue
        if here is not None:
            if processor:
                here = processor(here)
            if here is not None:
                return here
    return None


@app.route("/")
@app.route("/meetings")
def list_meetings():
    committees = get(
        parse.urljoin(INSTANCE, "api/agenda/udvalgsliste")).json()
    return render_template("meeting_list.html", response=committees)


@app.route("/meeting/<uuid:meeting>")
def list_points(meeting):
    points = get(
        parse.urljoin(
            INSTANCE,
            f"api/agenda/dagsorden/{meeting}?"
            "request.select={}")).json()
    response = make_response(
        render_template(
            "meeting_info.html",
            meeting_id=meeting, instance=INSTANCE, response=points))
    timestamp = get_first_path(
        points["Moede"],
        ("ReleasedDate",), ("Dato",),
        processor=lambda ts: parse_datetime(ts).timestamp())
    if timestamp is not None:
        response.headers["Last-Modified"] = format_date_time(timestamp)
    # print(json.dumps(points, indent=True))
    return response


@app.route(
    "/meeting/<uuid:meeting>/attachment/pdf/<uuid:document_id>",
    methods=["HEAD"])
def head_pdf(meeting, document_id):
    # document_id is enough to get the PDF file, but it's not enough to get its
    # metadata (the server doesn't support HEAD requests to objects under
    # /Vis/Pdf/bilag/). We retrieve that from the meeting instead
    points = get(
        parse.urljoin(
            INSTANCE,
            f"api/agenda/dagsorden/{meeting}?"
            "request.select={}")).json()
    response = make_response()
    timestamp = get_first_path(
        points["Moede"],
        ("ReleasedDate",), ("Dato",),
        processor=lambda ts: parse_datetime(ts).timestamp())
    if timestamp is not None:
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Last-Modified"] = format_date_time(timestamp)
    return response


@app.route(
    "/meeting/<uuid:meeting>/attachment/pdf/<uuid:document_id>",
    methods=["GET"])
def get_pdf(meeting, document_id):
    document = get(
        parse.urljoin(
            INSTANCE,
            f"Vis/Pdf/bilag/{document_id}?redirectDirectlyToPdf=true"),
        stream=True)
    response = make_response(document.raw)
    for key in (
            "Content-Disposition", "Content-Length",
            "Content-Type", "Last-Modified",):
        if key in document.headers:
            response.headers[key] = document.headers[key]
    return response
