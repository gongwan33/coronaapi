from flask import jsonify, request, session, app, current_app, make_response, send_file, Response

def setRoutes(app):
    @app.route('/corona/nz/YTExsed193847dkdIEDUCJkdslei394803', methods = ['GET'])
    def getCoronaData():
        try: 
            return jsonify({
                'data': 'hello',
            })
        except Exception as e:
            print(e)
            return jsonify({
                'Info': str(e) 
            }), 404


