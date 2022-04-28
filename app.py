from os import O_TEMPORARY
from flask import Flask, render_template, request, make_response
import operator as op

app = Flask(__name__)
app.debug = True
application = app

operations = ['+', '-', '*', '/']

operations_functions = { '+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv }

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/args')
def args():
    return render_template('args.html')


@app.route('/headers')
def headers():
    return render_template('headers.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    return render_template('form.html')


@app.route('/phoneNumb', methods=['GET', 'POST'])
def phoneNumb():
    err_msg = None
    result = ''
    if (request.form.get('number')):
        result = str(request.form.get('number'))
        result = result.replace('+', '')
        result = result.replace('.', '')
        result = result.replace('(', '')
        result = result.replace(')', '')
        result = result.replace('-', '')
        result = result.replace(' ', '')
        if(result != ''):
            if result.isnumeric():
                if (str(result)[0] == '7' or str(result)[0] == '8'):
                    if (len(result) == 11):
                        result = '8-{}-{}-{}-{}'.format(result[1:4], result[4:7], result[7:9], result[9:11])
                    else: err_msg = 'Введено неправильное кол-во символов'
                else: err_msg= 'Неправильный код страны'
            else: err_msg = 'Введены недопустимые символы'
    return render_template('phoneNumb.html', err_msg = err_msg, result = result)



# @app.route('/calc')
# def calc():
#     try:
#         operation = request.args.get('operation')
#         result = None
#         error_msg = None
#         op1 = float(request.args.get('operand1'))
#         op2 = float(request.args.get('operand2'))
#         if operation == '+':
#             result = op1 + op2
#         elif operation == '-':
#             result = op1 - op2
#         elif operation == '*':
#             result = op1 * op2
#         elif operation == '/':
#             result = op1 / op2
#     except ValueError:
#         error_msg = 'Пожалуйста вводите только числа'
#     except ZeroDivisionError:
#         error_msg = 'На ноль делить нельзя'
#     return render_template('calc.html', operations = operations, result = result, error_msg = error_msg)


@app.route('/calc')
def calc():
    result = None
    error_msg = None
    if (request.args.get('operand1') and request.args.get('operand1')):
        try:
            op1 = float(request.args.get('operand1'))
            op2 = float(request.args.get('operand2'))
            f = operations_functions[request.args.get('operation')]
            result = f(op1, op2)
        except ValueError:
            error_msg = 'Пожалуйста вводите только числа'
        except ZeroDivisionError:
            error_msg = 'На ноль делить нельзя'
        except KeyError:
            error_msg = 'Недопустимая операция'
    return render_template('calc.html', operations = operations, result = result, error_msg = error_msg)



@app.route('/cookies')
def cookies():
    resp = make_response(render_template('cookies.html'))
    if 'username' in request.cookies:
        resp.set_cookie('username', 'some name', expires=0)
    else:
        resp.set_cookie('username', 'some name')
    return resp
