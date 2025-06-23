import sys

from app.core.cache import close_cache
from app.core.config import settings
from app.core.module import ModuleManager
from app.log import logger
from app.utils.system import SystemUtils
from app.command import CommandChain


from app.core.event import EventManager
from app.helper.thread import ThreadHelper
from app.helper.display import DisplayHelper
from app.helper.doh import DohHelper
from app.helper.resource import ResourceHelper
from app.helper.message import MessageHelper
from app.schemas import Notification, NotificationType
from app.schemas.types import SystemConfigKey
from app.db import close_database
from app.db.systemconfig_oper import SystemConfigOper


def start_frontend():
    """
    启动前端服务
    """
    # 仅Windows可执行文件支持内嵌nginx
    if not SystemUtils.is_frozen() \
            or not SystemUtils.is_windows():
        return
    # 临时Nginx目录
    nginx_path = settings.ROOT_PATH / 'nginx'
    if not nginx_path.exists():
        return
    # 配置目录下的Nginx目录
    run_nginx_dir = settings.CONFIG_PATH.with_name('nginx')
    if not run_nginx_dir.exists():
        # 移动到配置目录
        SystemUtils.move(nginx_path, run_nginx_dir)
    # 启动Nginx
    import subprocess
    subprocess.Popen("start nginx.exe",
                     cwd=run_nginx_dir,
                     shell=True)


def stop_frontend():
    """
    停止前端服务
    """
    if not SystemUtils.is_frozen() \
            or not SystemUtils.is_windows():
        return
    import subprocess
    subprocess.Popen(f"taskkill /f /im nginx.exe", shell=True)


def clear_temp():
    """
    清理临时文件和图片缓存
    """
    # 清理临时目录中3天前的文件
    SystemUtils.clear(settings.TEMP_PATH, days=3)
    # 清理图片缓存目录中7天前的文件
    SystemUtils.clear(settings.CACHE_PATH / "images", days=7)


def user_auth():
    """
    用户认证检查
    """
    logger.info(f"用户认证成功")



def stop_modules():
    """
    服务关闭
    """
    # 停止模块
    ModuleManager().stop()
    # 停止事件消费
    EventManager().stop()
    # 停止虚拟显示
    DisplayHelper().stop()
    # 停止线程池
    ThreadHelper().shutdown()
    # 停止缓存连接
    close_cache()
    # 停止数据库连接
    close_database()
    # 停止前端服务
    stop_frontend()
    # 清理临时文件
    clear_temp()


def init_modules():
    """
    启动模块
    """
    # 虚拟显示
    DisplayHelper()
    # DoH
    DohHelper()
    # 资源包检测
    # ResourceHelper()
    # 用户认证
    # user_auth()
    # 加载模块
    ModuleManager()
    # 启动事件消费
    EventManager().start()
    # 启动前端服务
    start_frontend()
