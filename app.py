from sanic import Sanic
from sanic import response
from sanic.views import HTTPMethodView

import pymysql

db_settings = {
    'DB_HOST': 'localhost',
    'DB_NAME': '',
    'DB_USER': '',
    'DB_PASSWORD': ''
}

app = Sanic('todoApp')
app.config.update(db_settings)


@app.before_server_start
def db_init(app, loop):
    app.ctx.db = pymysql.connect(
        user=app.config.DB_USER,
        password=app.config.DB_PASSWORD,
        host=app.config.DB_HOST,
        db=app.config.DB_NAME
    )
    app.ctx.cursor = app.ctx.db.cursor()


@app.after_server_stop
async def db_close():
    app.ctx.db.close()


class MethodA(HTTPMethodView):
    async def get(self, request):
        sql = "SELECT * from tasks"
        app.ctx.cursor.execute(sql)
        res = app.ctx.cursor.fetchall()

        return response.json(res)

    async def post(self, request):
        if "title" not in request.args:
            return response.text('error', status=400)

        error_message = ''
        status_code = None
        try:
            sql = "Insert Into tasks(title) Values (%s)"
            app.ctx.cursor.execute(sql, (request.args['title']))
            app.ctx.db.commit()
            status_code = 200

        except:
            error_message = 'server error'
            status_code = 500

        finally:
            return response.text(error_message, status=status_code)


class MethodB(HTTPMethodView):
    async def get(self, request, task_id):
        cursor = app.ctx.cursor
        sql = "Select * from tasks where id = %s"
        cursor.execute(sql, task_id)
        res = cursor.fetchone()

        if res is None:
            return response.text('does not exist task id', status=400)

        status_code = 200

        return response.json(res, status=status_code)

    async def delete(self, request, task_id):
        status_code = None
        error_message = ''
        try:
            cursor = app.ctx.cursor
            sql = "Select * from tasks where id = %s"
            cursor.execute(sql, task_id)
            res = cursor.fetchone()

            if res is None:
                status_code = 400
                error_message = 'does not exist task id'
            else:
                sql = "Delete from tasks where id = %s"
                cursor.execute(sql, task_id)
                app.ctx.db.commit()
                status_code = 200
        except:
            error_message = 'server error'
            status_code = 500

        finally:
            return response.text(error_message, status=status_code)

    async def put(self, request, task_id):
        status_code = None
        error_message = ''
        if "title" not in request.args or "status" not in request.args:
            status_code = 400
            error_message = 'title or status was not included in the request.'
            return response.text(error_message, status=status_code)
        try:
            cursor = app.ctx.cursor
            sql = "Select * from tasks where id = %s"
            cursor.execute(sql, task_id)
            res = cursor.fetchone()

            if res is None:
                status_code = 400
                error_message = 'does not exist task id'
            else:
                sql = "Update tasks Set title = %s, status = %s where id = %s"
                title = request.args['title']
                task_status = request.args['status']
                cursor.execute(sql, (title, task_status, task_id))
                app.ctx.db.commit()
                status_code = 200
        except:
            error_message = 'server error'
            status_code = 500

        finally:
            return response.text(error_message, status=status_code)


app.add_route(MethodA.as_view(), '/todo/tasks')
app.add_route(MethodB.as_view(), '/todo/tasks/<task_id:int>')


if __name__ == '__main__':
    app.run(host='localhost', port=5000, auto_reload=True)
