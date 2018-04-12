import os

from edurov import WebMethod


def main(video_resolution='1024x768', fps=30, server_port=8000, debug=False):
    web_method = WebMethod(
        video_resolution=video_resolution,
        fps=fps,
        server_port=server_port,
        debug=debug,
        index_file=os.path.join(os.path.dirname(__file__), 'index.html', )
    )
    web_method.serve()


if __name__ == '__main__':
    main()
