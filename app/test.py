from flask import *
from app import app, socketio
from pathlib import Path
import os
from werkzeug.datastructures import Headers
from werkzeug.wsgi import wrap_file
from time import time
from zlib import adler32

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/test')
def testing():
    return render_template('data_visualization_step.html')

def send_file(
    filename_or_fp,
    mimetype=None,
    as_attachment=False,
    attachment_filename=None,
    add_etags=True,
    cache_timeout=None,
    conditional=False,
    last_modified=None,
):
    mtime = None
    fsize = None

    if hasattr(filename_or_fp, "__fspath__"):
        filename_or_fp = os.fspath(filename_or_fp)

    if isinstance(filename_or_fp, str):
        filename = filename_or_fp
        #filename = '/' + filename
        #if not os.path.isabs(filename):
            #filename = os.path.join(current_app.root_path, filename)
        file = None
        if attachment_filename is None:
            attachment_filename = os.path.basename(filename)
    else:
        file = filename_or_fp
        filename = None

    if mimetype is None:
        if attachment_filename is not None:
            mimetype = (
                mimetypes.guess_type(attachment_filename)[0]
                or "application/octet-stream"
            )

        if mimetype is None:
            raise ValueError(
                "Unable to infer MIME-type because no filename is available. "
                "Please set either `attachment_filename`, pass a filepath to "
                "`filename_or_fp` or set your own MIME-type via `mimetype`."
            )

    headers = Headers()
    if as_attachment:
        if attachment_filename is None:
            raise TypeError("filename unavailable, required for sending as attachment")

        if not isinstance(attachment_filename, str):
            attachment_filename = attachment_filename.decode("utf-8")

        try:
            attachment_filename = attachment_filename.encode("ascii")
        except UnicodeEncodeError:
            quoted = url_quote(attachment_filename, safe="")
            filenames = {
                "filename": unicodedata.normalize("NFKD", attachment_filename).encode(
                    "ascii", "ignore"
                ),
                "filename*": f"UTF-8''{quoted}",
            }
        else:
            filenames = {"filename": attachment_filename}

        headers.add("Content-Disposition", "attachment", **filenames)

    if current_app.use_x_sendfile and filename:
        if file is not None:
            file.close()

        headers["X-Sendfile"] = filename
        fsize = os.path.getsize(filename)
        data = None
    else:
        if file is None:
            file = open(filename, "rb")
            mtime = os.path.getmtime(filename)
            fsize = os.path.getsize(filename)
        elif isinstance(file, io.BytesIO):
            fsize = file.getbuffer().nbytes
        elif isinstance(file, io.TextIOBase):
            raise ValueError("Files must be opened in binary mode or use BytesIO.")

        data = wrap_file(request.environ, file)

    if fsize is not None:
        headers["Content-Length"] = fsize

    rv = current_app.response_class(
        data, mimetype=mimetype, headers=headers, direct_passthrough=True
    )

    if last_modified is not None:
        rv.last_modified = last_modified
    elif mtime is not None:
        rv.last_modified = mtime

    rv.cache_control.public = True
    if cache_timeout is None:
        cache_timeout = current_app.get_send_file_max_age(filename)
    if cache_timeout is not None:
        rv.cache_control.max_age = cache_timeout
        rv.expires = int(time() + cache_timeout)

    if add_etags and filename is not None:
        from warnings import warn

        try:
            check = (
                adler32(
                    filename.encode("utf-8") if isinstance(filename, str) else filename
                )
                & 0xFFFFFFFF
            )
            rv.set_etag(
                f"{os.path.getmtime(filename)}-{os.path.getsize(filename)}-{check}"
            )
        except OSError:
            warn(
                f"Access {filename} failed, maybe it does not exist, so"
                " ignore etags in headers",
                stacklevel=2,
            )

    if conditional:
        try:
            rv = rv.make_conditional(request, accept_ranges=True, complete_length=fsize)
        except RequestedRangeNotSatisfiable:
            if file is not None:
                file.close()
            raise
        # make sure we don't send x-sendfile for servers that
        # ignore the 304 status code for x-sendfile.
        if rv.status_code == 304:
            rv.headers.pop("x-sendfile", None)
    return rv

@app.route('/image')
def image():
    #p = MyPath("/home/ubuntu/FYP-flask/food_.jpg")
    p = "/home/ubuntu/CanteenPreProcessing/result/recording_2019_10_30/bbq/cam_bbq-21240-21360/1-0.jpg"
    #return send_file(p, mimetype="image/jpeg")
    return render_template("test.html")

@app.route('/my_images/<path:filename>')
def get_images(filename):
    #p = MyPath("/home/ubuntu/FYP-flask/food_.jpg")
    t = filename.split(".")[-1]
    p = Path(filename)
    print(p)
    #print(t, p)
    if t == 'jpg':
        return send_file(filename_or_fp=p, mimetype="image/jpeg")
    elif t == 'png':
        return send_file(filename_or_fp=p, mimetype="image/png")

@app.route('/ocr')
def ocr():
    return render_template('input_ocr.html')