from app.crawlers.adapters.example_adapter import ExampleSiteAdapter
from app.crawlers.adapters.fanqie_adapter import FanqieAdapter
from app.crawlers.adapters.zongheng_adapter import ZonghengAdapter

# 注册所有适配器
ADAPTERS = {
    "example.com": ExampleSiteAdapter,
    "fanqienovel.com": FanqieAdapter,
    "zongheng.com": ZonghengAdapter,
    "www.zongheng.com": ZonghengAdapter,
    "huayu.zongheng.com": ZonghengAdapter,
    "read.zongheng.com": ZonghengAdapter,
}


def get_adapter_for_site(site_name: str):
    """根据网站名称获取适配器"""
    return ADAPTERS.get(site_name)
