
from flask import Flask
from application import application
from multiprocessing import Process


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

@app.route("/hello/<searchTerm>", methods=['GET'])
def bertify(searchTerm):
    
    return f"<p>Api to to built in the future: {(searchTerm)}</p>"

def run_flask_app():
    app.run(host='0.0.0.0', port=5000)
    
if __name__ == '__main__':
    # app.run()
    # windows_process = Process(target=application.execute_app(), args=([1,9,4,5,2,6,8,4],))
    #windows_process = Process(target=application.execute_app)
    #read_process = Process(target=application.read_csv)
    #read_process.start()
    
    obj = application.Application()
    run_flask = Process(target=run_flask_app)
    run_flask.start()
    
    obj.execute_app()
    run_flask.join()
    
    # read_process.join()

    






