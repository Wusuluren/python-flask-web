#蓝本
from flask import Blueprint

main = Blueprint('main', __name__)

#在文件末尾导入，避免循环导入
from . import views, error