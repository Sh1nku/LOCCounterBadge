from flask import make_response


def construct_exceptions(app):
    @app.errorhandler(405)
    def invalid_method(e):
        return make_response(e.description + ' Allowed methods: ' + ', '.join(e.valid_methods), e.code)