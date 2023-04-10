from flask import Flask
from application import application
import logging


logging.basicConfig(filename="app.log",
                    format='%(asctime)s - %(message)s',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


 
# Creating an object

 
# Setting the threshold of logger to DEBUG



app = Flask(__name__)







# @app.before_request
# def before_request_func():
#     init()

@app.before_first_request
def before_first_request_func():
    print("This function will run once")


@app.route("/")
def home():
    return "<p>This is the home page</p>"

@app.route("/search/<searchTerm>", methods=['GET'])
def search(searchTerm):
    
    return f"<p>Api to to built in the future: {(searchTerm)}</p>"



def run_flask_app():
    app.run(host='0.0.0.0', port=5000)
    
if __name__ == '__main__':

    obj = application.Application()
    obj.execute_app()
    
    






