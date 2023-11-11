import flask
from flask import jsonify, request, Response
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from models import Adverts           
from models import Session        

adverts = flask.Flask('adverts')         


class HttpError(Exception):       # создаем свой класс для описания ошибок
    def __init__(self, status_code: int, description: str):
        self.status_code = status_code
        self.description = description

@adverts.errorhandler(HttpError)
def error_handler(error):
    response = jsonify({'error': error.description})
    response.status_code = error.status_code
    return response

@adverts.before_request
def before_request():             # то, что фласк будет делать перед запросом
    session = Session()           
    request.session = session     

@adverts.after_request                # то, что фласк будет делать после запроса
def after_request(response: Response):
    request.session.close()       # закрываем сессию
    return response

def get_adv(adv_id: int):       # функция проверяет наличие записи с введенным айди 
    adv = request.session.get(Adverts, adv_id)
    if Adverts is None:
        raise HttpError(404, 'advertisement not found')
    
    return adv

def add_adv(adv: Adverts):         # проверяет, нет ли уже такого пользователя
    try:
        request.session.add(adv)
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, 'advertisement already exists')
    return adv




class AdvertsView(MethodView):       # создаем новый класс

    @property
    def session(self) -> Session:
        return request.session



    def get(self, adv_id: int):

        adv = get_adv(adv_id)

        return jsonify({'id': adv.id, 
                        'header': adv.header,
                        'description': adv.description,
                        'creation_time': adv.creation_time.isoformat(),
                        'owner': adv.owner
                        })

    def post(self):
        adv_data = request.json 
        
        if 'header' not in adv_data or 'description' not in adv_data or 'owner'not in adv_data:
            raise HttpError(400, 'header, description and owner are required') 
        
        new_adv = Adverts(**adv_data)
        new_adv = add_adv(new_adv)
        return jsonify({'id': new_adv.id})
   
    def delete(self, adv_id: int):
        adv = get_adv(adv_id)        
        self.session.delete(adv)
        self.session.commit()
        return jsonify({'status': 'ok'})


adv_view = AdvertsView.as_view('adv_view') # преобразуем класс во view-функцию
    
adverts.add_url_rule('/adv', view_func=adv_view, methods=['POST'])
adverts.add_url_rule('/adv/<int:adv_id>', view_func=adv_view, methods=['GET', 'DELETE'])

if __name__ == '__main__':
    adverts.run(debug=True)   